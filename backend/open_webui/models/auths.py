import logging
import uuid, os
from typing import Optional

from open_webui.internal.db import Base, get_db
from open_webui.models.users import User
from open_webui.models.users import UserModel, UserProfileImageResponse, Users
from open_webui.env import SRC_LOG_LEVELS
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, String, Text
from jose import jwt, JWTError


from datetime import datetime, timedelta
from fastapi import HTTPException, status, BackgroundTasks
from open_webui.utils.enhanced_email import send_email_smtp

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

# ---------------------------
# SETTINGS (change for prod)
# ---------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_in_prod")
ALGORITHM = "HS256"
ACTIVATION_EXP_HOURS = 24  # token expiry
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "smtp_user")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "smtp_password")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@example.com")
FRONTEND_ACTIVATE_URL = os.getenv("FRONTEND_ACTIVATE_URL", "https://0.0.0.0/activate")  # e.g. where user clicks

BRAND_NAME = os.getenv("BRAND_NAME", "YourApp")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@your-app.com")
TRACKING_PIXEL_URL = os.getenv("TRACKING_PIXEL_URL", "")  # optional
UTM_SOURCE = os.getenv("UTM_SOURCE", "email")
UTM_MEDIUM = os.getenv("UTM_MEDIUM", "activation")
# If you use a transactional provider that expects headers/tags, add here.


####################
# DB MODEL
####################



class Auth(Base):
    __tablename__ = "auth"

    id = Column(String, primary_key=True, unique=True)
    email = Column(String)
    password = Column(Text)
    active = Column(Boolean)


class AuthModel(BaseModel):
    id: str
    email: str
    password: str
    active: bool = True


####################
# Forms
####################


class Token(BaseModel):
    token: str
    token_type: str


class ApiKey(BaseModel):
    api_key: Optional[str] = None


class SigninResponse(Token, UserProfileImageResponse):
    pass


class SigninForm(BaseModel):
    email: str
    password: str


class LdapForm(BaseModel):
    user: str
    password: str


class ProfileImageUrlForm(BaseModel):
    profile_image_url: str


class UpdatePasswordForm(BaseModel):
    password: str
    new_password: str


class SignupForm(BaseModel):
    name: str
    email: str
    password: str
    profile_image_url: Optional[str] = "/user.png"


class AddUserForm(SignupForm):
    role: Optional[str] = "pending"


class AuthsTable:
    
    
    # ---------------------------
    # Utils: token generation & validation
    # ---------------------------
    async def create_activation_token(self, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACTIVATION_EXP_HOURS))
        payload = {"sub": str(user_id), "exp": int(expire.timestamp())}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    
    
    async def verify_activation_token(token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
            return user_id
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired activation token")



    # ---------------------------
    # Utils: send email (async)
    # ---------------------------
    async def send_email(self, subject: str, recipient: str, html_body: str):
        msg = EmailMessage()
        msg["From"] = FROM_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content("Please use an HTML-capable client to view this message.")
        msg.add_alternative(html_body, subtype="html")

        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True,
        )

    async def build_activation_email_html(self, email: str, token: str) -> str:
        link = f"{FRONTEND_ACTIVATE_URL}/{token}"
        return f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>Click the link below to activate your account:</p>
            <p><a href="{link}">Activate account</a></p>
            <p>If you did not create an account, ignore this email.</p>
        </body>
        </html>
        """
        
    def insert_new_auth(
        self,
        email: str,
        password: str,
        name: str,
        profile_image_url: str = "/user.png",
        role: str = "pending",
        oauth: Optional[dict] = None,
    ) -> Optional[UserModel]:
        with get_db() as db:
            log.info("insert_new_auth")

            id = str(uuid.uuid4())

            auth = AuthModel(
                **{"id": id, "email": email, "password": password, "active": True}
            )
            result = Auth(**auth.model_dump())
            db.add(result)

            user = Users.insert_new_user(
                id, name, email, profile_image_url, role, oauth=oauth
            )

            db.commit()
            db.refresh(result)

            if result and user:
                return user
            else:
                return None

    def authenticate_user(
        self, email: str, verify_password: callable
    ) -> Optional[UserModel]:
        log.info(f"authenticate_user: {email}")

        user = Users.get_user_by_email(email)
        if not user:
            return None

        try:
            with get_db() as db:
                auth = db.query(Auth).filter_by(id=user.id, active=True).first()
                if auth:
                    if verify_password(auth.password):
                        return user
                    else:
                        return None
                else:
                    return None
        except Exception:
            return None

    def authenticate_user_by_api_key(self, api_key: str) -> Optional[UserModel]:
        log.info(f"authenticate_user_by_api_key: {api_key}")
        # if no api_key, return None
        if not api_key:
            return None

        try:
            user = Users.get_user_by_api_key(api_key)
            return user if user else None
        except Exception:
            return False

    def authenticate_user_by_email(self, email: str) -> Optional[UserModel]:
        log.info(f"authenticate_user_by_email: {email}")
        try:
            with get_db() as db:
                auth = db.query(Auth).filter_by(email=email, active=True).first()
                if auth:
                    user = Users.get_user_by_id(auth.id)
                    return user
        except Exception:
            return None

    def update_user_password_by_id(self, id: str, new_password: str) -> bool:
        try:
            with get_db() as db:
                result = (
                    db.query(Auth).filter_by(id=id).update({"password": new_password})
                )
                db.commit()
                return True if result == 1 else False
        except Exception:
            return False

    def update_email_by_id(self, id: str, email: str) -> bool:
        try:
            with get_db() as db:
                result = db.query(Auth).filter_by(id=id).update({"email": email})
                db.commit()
                return True if result == 1 else False
        except Exception:
            return False

    def delete_auth_by_id(self, id: str) -> bool:
        try:
            with get_db() as db:
                # Delete User
                result = Users.delete_user_by_id(id)

                if result:
                    db.query(Auth).filter_by(id=id).delete()
                    db.commit()

                    return True
                else:
                    return False
        except Exception:
            return False


    async def send_activation_link(self, user_id: str) -> None:
        log.info(f"send_activation_link to {user_id}")
        # 3. create activation token
        token = await self.create_activation_token(user_id)
        with get_db() as db:
            
            user_obj = db.get(User, user_id)
            user_obj.email_verification_token = token
             
            db.commit()
            db.refresh(user_obj) 
        email_response=await send_email_smtp(user_obj.email, "Activate your account", user_obj.email_verification_token, True)
        
        return None
 


Auths = AuthsTable()

import logging
import uuid, os
import time
from typing import Optional

from open_webui.internal.db import Base, get_db
from open_webui.models.users import User, UserModel, Users, UserProfileImageResponse
from open_webui.env import SRC_LOG_LEVELS
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, String, Text, BigInteger
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
# Password Reset Token Model
####################

class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    id = Column(String, primary_key=True, unique=True)
    user_id = Column(String)
    token = Column(String, unique=True)
    expires_at = Column(BigInteger)
    used = Column(Boolean, default=False)
    created_at = Column(BigInteger)


class PasswordResetTokenModel(BaseModel):
    id: str
    user_id: str
    token: str
    expires_at: int
    used: bool = False
    created_at: int


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


class ResetPasswordForm(BaseModel):
    token: str
    new_password: str


class ForgotPasswordForm(BaseModel):
    email: str


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
 

    # ---------------------------
    # Password Reset Methods
    # ---------------------------
    def create_password_reset_token(self, user_id: str) -> str:
        """Create a password reset token for a user"""
        with get_db() as db:
            # Generate a unique token
            token = str(uuid.uuid4())
            token_id = str(uuid.uuid4())
            
            # Token expires in 1 hour
            expires_at = int(time.time()) + (60 * 60)
            created_at = int(time.time())
            
            # Save token to database
            reset_token = PasswordResetToken(
                id=token_id,
                user_id=user_id,
                token=token,
                expires_at=expires_at,
                used=False,
                created_at=created_at
            )
            
            db.add(reset_token)
            db.commit()
            
            return token

    def verify_password_reset_token(self, token: str) -> Optional[str]:
        """Verify a password reset token and return user_id if valid"""
        try:
            with get_db() as db:
                reset_token = db.query(PasswordResetToken).filter_by(
                    token=token, used=False
                ).first()
                
                if not reset_token:
                    return None
                
                # Check if token has expired
                if int(time.time()) > reset_token.expires_at:
                    return None
                
                return reset_token.user_id
        except Exception as e:
            log.error(f"Error verifying password reset token: {e}")
            return None

    def mark_password_reset_token_used(self, token: str) -> bool:
        """Mark a password reset token as used"""
        try:
            with get_db() as db:
                result = db.query(PasswordResetToken).filter_by(token=token).update(
                    {"used": True}
                )
                db.commit()
                return result > 0
        except Exception as e:
            log.error(f"Error marking token as used: {e}")
            return False

    def delete_expired_reset_tokens(self) -> None:
        """Clean up expired password reset tokens"""
        try:
            with get_db() as db:
                current_time = int(time.time())
                db.query(PasswordResetToken).filter(
                    PasswordResetToken.expires_at < current_time
                ).delete()
                db.commit()
        except Exception as e:
            log.error(f"Error deleting expired tokens: {e}")


Auths = AuthsTable()

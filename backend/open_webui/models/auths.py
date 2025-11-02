import logging
import uuid, os, time
from typing import Optional 
from datetime import datetime, timedelta
from backend.open_webui.utils.enhanced_email import send_activation_email_bg
from open_webui.internal.db import Base, get_db
from open_webui.models.users import User, UserModel, Users
from open_webui.env import SRC_LOG_LEVELS
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, String, Text
from fastapi import BackgroundTasks, Depends, HTTPException, status, Query

from open_webui.utils.auth import verify_password
from jose import jwt, JWTError
from fastapi import HTTPException, status

import aiosmtplib
from email.message import EmailMessage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


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

# HTML template (Jinja2)
HTML_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Activate your {{ brand_name }} account</title>
    <style>
      /* Simple responsive styling that works in most email clients */
      body { margin:0; padding:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color:#f6f9fc; }
      .email-wrap { width:100%; max-width:680px; margin:0 auto; padding:24px; }
      .card { background:#ffffff; border-radius:12px; padding:32px; box-shadow:0 2px 4px rgba(16,24,40,0.05); }
      h1 { margin:0 0 8px 0; font-size:20px; color:#0f172a; }
      p { color:#475569; margin:8px 0 16px 0; line-height:1.4; font-size:15px; }
      .btn { display:inline-block; text-decoration:none; padding:12px 20px; border-radius:10px; font-weight:600; background:linear-gradient(90deg,#4f46e5,#06b6d4); color:white; }
      .muted { color:#94a3b8; font-size:13px; margin-top:16px; }
      .footer { text-align:center; color:#94a3b8; font-size:12px; margin-top:20px; }
      @media (max-width:420px) {
        .card { padding:20px; border-radius:8px; }
        .btn { width:100%; text-align:center; display:block; }
      }
    </style>
  </head>
  <body>
    <div class="email-wrap" role="article" aria-roledescription="email">
      <div class="card">
        <img src="{{ logo_url }}" alt="{{ brand_name }} logo" width="48" style="display:block; margin-bottom:18px;">
        <h1>Activate your {{ brand_name }} account</h1>
        <p>Hi{{ " " + name if name else "" }},</p>
        <p>Thanks for creating an account. Click the button below to activate your account and start using {{ brand_name }}.</p>

        <p style="text-align:center;">
          <a class="btn" href="{{ activation_link }}" target="_blank" rel="noopener noreferrer">Activate account</a>
        </p>

        <p class="muted">If the button doesn't work, copy and paste this link into your browser:</p>
        <p class="muted"><a href="{{ activation_link }}" target="_blank" rel="noopener noreferrer">{{ activation_link }}</a></p>

        <p style="margin-top:18px;">If you didn't create this account, you can ignore this email or contact us at <a href="mailto:{{ support_email }}">{{ support_email }}</a>.</p>

        {% if tracking_pixel %}
        <!-- tracking pixel (optional) -->
        <img src="{{ tracking_pixel }}" alt="" width="1" height="1" style="display:block; margin-top:8px;">
        {% endif %}
      </div>

      <div class="footer">
        <p>&copy; {{ year }} {{ brand_name }}. All rights reserved.</p>
        <p><a href="{{ unsubscribe_link }}">Unsubscribe</a> | <a href="{{ privacy_url }}">Privacy Policy</a></p>
      </div>
    </div>
  </body>
</html>
"""

# Plain text fallback
TEXT_TEMPLATE = """Hi{{ " " + name if name else "" }},

Thanks for creating an account at {{ brand_name }}.

Activate your account by visiting the link below:
{{ activation_link }}

If you did not create this account, ignore this email or contact us at {{ support_email }}.

Thanks,
The {{ brand_name }} Team
"""


# Rate-limit resend: seconds between allowed resends
RESEND_MIN_SECONDS = 60 * 5  # 5 minutes

# ---------------------------
# Database (async SQLAlchemy)
# ---------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Convert postgresql:// to postgresql+asyncpg:// for async operations
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

####################
# DB MODEL
####################


class Auth(Base):
    __tablename__ = "auth"

    id = Column(String, primary_key=True)
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


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    profile_image_url: str


class SigninResponse(Token, UserResponse):
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

# Helper to build activation URL safely
def build_activation_url(token: str) -> str:
    # quote_plus is used to safely encode token for URL param
    token_quoted = quote_plus(token)
    # add UTMs for tracking (optional)
    utm = f"?utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}"
    # If FRONTEND_ACTIVATE_URL already contains query params, adjust accordingly
    sep = "&" if "?" in FRONTEND_ACTIVATE_URL else "?"
    activation_link = f"{FRONTEND_ACTIVATE_URL}{sep}token={token_quoted}&utm_campaign=activation{utm}"
    return activation_link


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
        oauth_sub: Optional[str] = None,
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
                id, name, email, profile_image_url, role, oauth_sub
            )

            db.commit()
            db.refresh(result)

            if result and user:
                return user
            else:
                return None

    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        log.info(f"authenticate_user: {email}")

        user = Users.get_user_by_email(email)
        if not user:
            return None

        try:
            with get_db() as db:
                auth = db.query(Auth).filter_by(id=user.id, active=True).first()
                if auth:
                    if verify_password(password, auth.password):
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

    async def send_activation_link(self, user: UserModel, background_tasks: BackgroundTasks) -> None:
        log.info(f"send_activation_link to {user.email}")
        # 3. create activation token
        token = await self.create_activation_token(user.id)
        with get_db() as db:
            
            user_obj = db.get(User, user.id)
            user_obj.email_verification_token = token
            # chat_item.chat = chat
            # chat_item.title = chat["title"] if "title" in chat else "New Chat"
            # chat_item.updated_at = int(time.time())
            db.commit()
            db.refresh(user_obj)
                
            # user.email_verification_token = token
            # # user.email_verification_sent_at = None
            # db.commit()
            
        background_tasks.add_task(send_activation_email_bg, user.email, token, name=user.name)
        return None


        # # 4. send activation email in background
        # html = await self.build_activation_email_html(user.email, token)
        # background_tasks.add_task(self.send_email_async, "Activate your account", user.email, html)

        # # await self.send_email_async("Activate your account", user.email, html)



Auths = AuthsTable()

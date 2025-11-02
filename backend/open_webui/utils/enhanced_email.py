# enhanced_email.py
import os
import time
from datetime import datetime, timedelta
from typing import Optional
import asyncio
from urllib.parse import quote_plus
from email.message import EmailMessage

import aiosmtplib
from jinja2 import Template

# config (load from env in production)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "smtp_user")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "smtp_password")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@example.com")
FRONTEND_ACTIVATE_URL = os.getenv("FRONTEND_ACTIVATE_URL", "https://your-app.com/activate")
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

# Helper to build activation URL safely
def build_activation_url(token: str) -> str:
    # quote_plus is used to safely encode token for URL param
    token_quoted = quote_plus(token)
    # add UTMs for tracking (optional)
    utm = f"?utm_source={UTM_SOURCE}&utm_medium={UTM_MEDIUM}"
    # If FRONTEND_ACTIVATE_URL already contains query params, adjust accordingly
    sep = "&" if "?" in FRONTEND_ACTIVATE_URL else "?"
    activation_link = f"{FRONTEND_ACTIVATE_URL}/{token_quoted}{sep}token={token_quoted}&utm_campaign=activation{utm}"
    return activation_link

# The enhanced send function
async def send_activation_email(
    recipient: str,
    token: str,
    name: Optional[str] = None,
    *,
    logo_url: str = "https://assets.your-app.com/logo.png",
    unsubscribe_url: str = "https://your-app.com/unsubscribe",
    privacy_url: str = "https://your-app.com/privacy",
    tracking_pixel: Optional[str] = None,
    subject: str = None,
):
    """
    Sends an HTML activation email with a plain-text fallback.
    Use with FastAPI BackgroundTasks: background_tasks.add_task(send_activation_email, user.email, token, name=user.name)
    """
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP configuration not set")

    activation_link = build_activation_url(token)
    subject = subject or f"Activate your {BRAND_NAME} account"
    
    

    # Render templates
    ctx = {
        "brand_name": BRAND_NAME,
        "name": name,
        "activation_link": activation_link,
        "logo_url": logo_url,
        "support_email": SUPPORT_EMAIL,
        "tracking_pixel": tracking_pixel or TRACKING_PIXEL_URL,
        "year": __import__("datetime").datetime.utcnow().year,
        "unsubscribe_link": unsubscribe_url,
        "privacy_url": privacy_url,
    }
    # print(f"Email context: {ctx}")
    print(f"Rendering email templates...{FROM_EMAIL} -> {recipient} {SMTP_HOST} {SMTP_PORT}")
    

    html_content = Template(HTML_TEMPLATE).render(**ctx)
    text_content = Template(TEXT_TEMPLATE).render(**ctx)
    print("Templates rendered.")
    print(f"Sending email to {recipient} via {SMTP_HOST}:{SMTP_PORT}...")
    print(f"Subject: {subject}")
    print(f"text_content: {text_content}")
    print(f"HTML content length: {len(html_content)}")
    print(f"Text content length: {len(text_content)}")
    print(f"From: {FROM_EMAIL}")
    print(f"To: {recipient}")
    print(f"Using SMTP user: {SMTP_USER}")
    print("Preparing email message...")
    # Build email message
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = recipient
    msg["Subject"] = subject
    # recommended headers for deliverability
    msg["List-Unsubscribe"] = f"<mailto:{SUPPORT_EMAIL}>"
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype="html")

    # option: add custom headers recognized by transactional providers
    # msg["X-Entity-Ref-ID"] = "activation-email"

    # send via aiosmtplib
    # await aiosmtplib.send(
    #     msg,
    #     hostname=SMTP_HOST,
    #     port=SMTP_PORT,
    #     username=SMTP_USER,
    #     password=SMTP_PASSWORD,
    #     start_tls=True,
    #     timeout=30,
    # )

# Example sync-friendly wrapper to use with BackgroundTasks
def send_activation_email_bg(recipient: str, token: str, name: Optional[str] = None, **kwargs):
    """
    Helper for FastAPI BackgroundTasks (which accepts callables). This runs the coroutine.
    Usage:
      background_tasks.add_task(send_activation_email_bg, user.email, token, name=user.name)
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # running inside FastAPI event loop -> schedule a task
        asyncio.create_task(send_activation_email(recipient, token, name, **kwargs))
    else:
        # not running inside an event loop (unit tests or script) -> run until complete
        asyncio.run(send_activation_email(recipient, token, name, **kwargs))

# def create_activation_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
#     expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACTIVATION_EXP_HOURS))
#     payload = {"sub": str(user_id), "exp": int(expire.timestamp())}
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return token

# def verify_activation_token(token: str) -> int:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = int(payload.get("sub"))
#         return user_id
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired activation token")

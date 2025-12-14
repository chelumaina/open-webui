# Forgot Password Implementation

This document describes the complete forgot password functionality that has been implemented.

## Overview

A complete password reset flow has been implemented, allowing users to:
1. Request a password reset via email
2. Receive a secure reset link
3. Set a new password using the reset token
4. Sign in with the new password

## Backend Implementation

### Database Model

**Password Reset Token Table** (`password_reset_token`)
- `id`: Unique identifier for the token record
- `user_id`: Reference to the user requesting the reset
- `token`: Unique reset token (UUID)
- `expires_at`: Token expiration timestamp (1 hour from creation)
- `used`: Boolean flag to prevent token reuse
- `created_at`: Token creation timestamp

**Migration File**: `backend/open_webui/migrations/versions/add_password_reset_table.py`

### Models (`backend/open_webui/models/auths.py`)

**New Forms**:
- `ForgotPasswordForm`: Contains email field for password reset request
- `ResetPasswordForm`: Contains token and new_password fields

**New Methods in AuthsTable**:
- `create_password_reset_token(user_id)`: Creates a unique reset token with 1-hour expiration
- `verify_password_reset_token(token)`: Validates token and returns user_id if valid
- `mark_password_reset_token_used(token)`: Marks token as used to prevent reuse
- `delete_expired_reset_tokens()`: Cleanup method for expired tokens

### API Endpoints (`backend/open_webui/routers/auths.py`)

**POST `/api/v1/auths/forgot-password`**
- Request body: `{ "email": "user@example.com" }`
- Creates reset token and sends email
- Returns success message (even if email doesn't exist to prevent enumeration)
- Rate limited to prevent abuse

**POST `/api/v1/auths/reset-password`**
- Request body: `{ "token": "reset-token", "new_password": "newpass123" }`
- Validates token, password requirements
- Updates user password
- Marks token as used
- Returns success message

### Email Service (`backend/open_webui/utils/enhanced_email.py`)

**New Email Templates**:
- `PASSWORD_RESET_HTML_TEMPLATE`: Professional HTML email with reset button
- `PASSWORD_RESET_TEXT_TEMPLATE`: Plain text fallback

**New Functions**:
- `send_password_reset_email()`: Async email sending with aiosmtplib
- `send_password_reset_email_sync()`: Synchronous email sending with smtplib
- `build_reset_password_url(token)`: Constructs the reset URL with token

## Frontend Implementation

### API Client (`src/lib/apis/auths/index.ts`)

**New Functions**:
- `userForgetPassword(email)`: Calls forgot-password endpoint
- `userResetPassword(token, newPassword)`: Calls reset-password endpoint

### Auth Page (`src/routes/auth/+page.svelte`)

**New Features**:
- Added "Forgot Password" link on sign-in page
- New `forgotpassword` mode for password reset request
- Email input form for password reset
- "Back to Sign in" button
- Success toast notification after email sent

### Reset Password Page (`src/routes/auth/reset-password/+page.svelte`)

**Features**:
- Extracts token from URL query parameter
- New password and confirm password fields
- Password validation (minimum 8 characters)
- Password match validation
- Loading state during submission
- Success redirect to sign-in page
- Error handling with toast notifications

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# SMTP Configuration (required)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-smtp-user
SMTP_PASSWORD=your-smtp-password
FROM_EMAIL=noreply@example.com

# Application Settings
WEBUI_URL=https://your-domain.com
WEBUI_NAME="Your App Name"
SUPPORT_EMAIL=support@your-domain.com

# Frontend URLs
FRONTEND_RESET_PASSWORD_URL=https://your-domain.com/auth/reset-password
```

## Security Features

1. **Rate Limiting**: Forgot password endpoint is rate-limited (5 requests per 3 minutes)
2. **Token Expiration**: Reset tokens expire after 1 hour
3. **Single Use**: Tokens can only be used once
4. **Email Enumeration Prevention**: Always returns success, even if email doesn't exist
5. **Password Validation**: Enforces password requirements (minimum 8 characters)
6. **Secure Token Generation**: Uses UUID for unpredictable tokens

## User Flow

1. User clicks "Forgot Password" on sign-in page
2. User enters their email address
3. System generates reset token and sends email (if account exists)
4. User receives email with reset link
5. User clicks link and is taken to reset password page
6. User enters new password twice
7. System validates token and password, then updates account
8. User is redirected to sign-in page
9. User signs in with new password

## Testing the Flow

### Manual Testing Steps

1. **Start the application**:
   ```bash
   make start
   ```

2. **Test Forgot Password Request**:
   - Navigate to `/auth`
   - Click "Forgot Password"
   - Enter a valid user email
   - Check email inbox for reset link

3. **Test Reset Password**:
   - Click the reset link in email
   - Enter new password (min 8 characters)
   - Confirm password matches
   - Submit form
   - Verify redirect to sign-in
   - Sign in with new password

4. **Test Security Features**:
   - Try using the same reset token twice (should fail)
   - Wait for token to expire (1 hour) and try using it (should fail)
   - Try resetting with non-matching passwords (should show error)
   - Try with password < 8 characters (should show error)

## Database Migration

The migration will run automatically when the backend starts. To manually run it:

```bash
cd backend
python -m alembic upgrade head
```

## Troubleshooting

### Emails Not Sending

1. Verify SMTP credentials in environment variables
2. Check SMTP server allows connections from your IP
3. Check application logs for email errors
4. Test SMTP connection separately

### Token Not Working

1. Check token hasn't expired (1 hour limit)
2. Verify token hasn't been used already
3. Check database for token record
4. Ensure URL parameter is correctly formatted

### Frontend Issues

1. Clear browser cache
2. Check browser console for JavaScript errors
3. Verify API endpoints are accessible
4. Check network tab for failed requests

## Future Enhancements

Potential improvements:
- Add cleanup job to regularly delete expired tokens
- Add admin interface to view/manage reset tokens
- Add multi-language support for emails
- Add customizable token expiration time
- Add password reset history tracking
- Add notification when password is changed
- Add two-factor authentication option

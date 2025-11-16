# Security and Password Management

LexLuma places a premium on account security to protect client data and sensitive legal materials. This page covers password best practices, multi-factor authentication (MFA), session controls, and account recovery.

## Core Security Controls

- **Password management:** Set strong, unique passwords. Minimum recommended length: 12 characters with mixed types.  
- **Multi-Factor Authentication (MFA):** Enable TOTP (authenticator app) or SMS-based codes. Use an authenticator app for stronger security.  
- **Single Sign-On (SSO):** Supports SAML/OAuth for enterprise accounts—administrators manage SSO policies.  
- **Active Sessions:** View and terminate active sessions across devices.  
- **Password resets & recovery:** Secure email confirmation required.

## How to Change Password

1. `Settings → Security`  
2. Click **Change Password**, enter current and new passwords, confirm.  
3. Save — a confirmation email is sent.

## MFA Setup

1. Go to `Settings → Security → MFA`.  
2. Choose Authenticator App (recommended) or SMS.  
3. Scan QR code and enter verification token.  
4. Store backup recovery codes securely—these are essential if you lose access.

## Best Practices for Legal Teams

- Enforce MFA for all users handling confidential files.  
- Use SSO with corporate identity providers for central control.  
- Rotate API keys (see API Keys Management) periodically.  
- Keep audit logs to track who accessed or exported sensitive documents.

## Incident Response

- Report suspicious logins immediately.  
- If account is compromised, change password, revoke sessions, and regenerate API keys.

## Related
- [/personal-settings/key-security-best-practices](./key-security-best-practices.md)  
- [/personal-settings/api-keys-management](./api-keys-management.md)
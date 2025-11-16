# Key Security Best Practices

Managing secrets—passwords, API keys, SSO credentials, and recovery codes—requires disciplined processes. This page summarizes best practices to protect client data and maintain compliance.

## Fundamental Rules

- **Least privilege:** Give keys minimal required permissions.  
- **Rotate keys regularly:** Set expirations and rotate keys every 90 days or as policy dictates.  
- **Use workspaces for shared keys:** Avoid sharing personal keys for team integrations.  
- **Secure storage:** Use hardware or cloud-based secret vaults (HashiCorp Vault, cloud KMS) for backups.

## Operational Practices

- **Audit logging:** Track creation, use, and revocation of keys.  
- **Automated alerts:** Notify owners when unusual usage patterns appear.  
- **Emergency rotation:** Have an incident playbook to revoke and re-issue keys quickly.  
- **Least-exposure in emails:** Never transmit keys in plain email or chat.

## For Legal Teams

- Keep integration scopes consistent with data protection obligations.  
- Provide training on secure handling of client-sensitive materials.  
- Include key management in client security audits.

## Related
- [/personal-settings/api-keys-management](./api-keys-management.md)  
- [/personal-settings/security-and-password-management](./security-and-password-management.md)
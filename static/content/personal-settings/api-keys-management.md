# API Keys Management

API keys connect LexLuma to external services (automation scripts, integrations, or third-party tools). This page explains how to create, rotate, revoke, and secure keys.

## Key Concepts

- **Personal vs. Workspace keys:** Personal for individual use; workspace keys for shared integrations.  
- **Scopes & permissions:** Limit what each key can access (read, write, admin).  
- **Rotation & expiry:** Best practice to rotate keys regularly and set expirations.

## How to Create a Key

1. `Settings → Integrations → API Keys`  
2. Click **Create New Key**.  
3. Provide a descriptive name, select scope, and set expiry.  
4. Copy the generated key and store it securely — it will be shown once.

## Revoking & Rotating

- Revoke keys that are no longer needed or suspected to be compromised.  
- Rotate by creating a new key, updating integrations, then revoking the old key.

## Security Tips

- Never embed keys in public repositories.  
- Use environment variables in automation scripts.  
- Audit usage logs periodically for unusual activity.

## Related
- [/personal-settings/adding-and-managing-openai-api-keys](./adding-and-managing-openai-api-keys.md)  
- [/personal-settings/key-security-best-practices](./key-security-best-practices.md)
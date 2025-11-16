# Adding and Managing OpenAI API Keys

LexLuma can integrate with external LLM providers for custom workflows. This page covers adding and managing OpenAI API keys securely within LexLuma.

## Prerequisites

- Valid OpenAI account and API access.  
- Correct billing configuration with OpenAI (if required).  
- Permissions in LexLuma to add workspace-level keys (admins only for shared keys).

## How to Add a Key

1. `Settings → Integrations → OpenAI`  
2. Click **Add Key** and paste your OpenAI API key.  
3. Scope keys as personal or workspace and set any limits.  
4. Test the connection to confirm functionality.

## Management Tips

- Limit usage to necessary endpoints for cost control.  
- Set rate limits or quotas on workspace keys.  
- Monitor spending and request alerts for threshold breaches.

## Security & Compliance

- Treat keys as secrets—store them in secure vaults for backups.  
- Rotate keys periodically and after staff changes.  
- Use workspace keys for reproducible team models with controlled access.

## Related
- [/personal-settings/api-keys-management](./api-keys-management.md)  
- [/personal-settings/key-security-best-practices](./key-security-best-practices.md)
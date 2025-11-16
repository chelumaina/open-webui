# Other Service Integrations

LexLuma supports integrations with various services: document management systems, court filing APIs, billing platforms, and internal data stores. This page gives an overview and governance guidance.

## Typical Integrations

- **DMS / SharePoint / Box:** Sync documents and version control.  
- **E-filing APIs:** Submit court documents directly where supported.  
- **Billing systems:** Map research activity for timekeeping.  
- **Single Sign-On (SSO):** Centralized authentication and user provisioning.

## How to Connect

`Settings → Integrations` — choose a service, provide credentials, and set scopes. For enterprise integrations, admins typically set up global configurations and permissions.

## Governance & Compliance

- Restrict access scopes to principle of least privilege.  
- Use secure connectors rather than storing credentials locally.  
- Review and renew integration tokens periodically.

## Best Practices

- Test integrations in a sandbox environment first.  
- Document data flows to meet client confidentiality obligations.  
- Assign a point person for integration maintenance and security.

## Related
- [/personal-settings/api-keys-management](./api-keys-management.md)
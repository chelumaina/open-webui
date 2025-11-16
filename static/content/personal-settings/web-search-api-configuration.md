# Web Search API Configuration

If your LexLuma instance supports external web search (for current events, gazette updates, or external case law), configure the web search API here to ensure accurate and compliant integrations.

## Common Providers

- Commercial legal databases (subscriptions)  
- General web search APIs (with domain filtering)  
- Custom crawlers or curated sources for specific jurisdictions

## How to Configure

1. `Settings → Integrations → Web Search`  
2. Add API credentials and set allowed domains or source lists.  
3. Configure result caching, refresh intervals, and jurisdiction filters.  
4. Test queries to ensure relevance and quality.

## Governance

- Restrict web search to approved sources to reduce unreliable results.  
- Configure caching to balance freshness vs. query costs.  
- Maintain an audit trail of web search queries for compliance.

## Best Practices

- Use curated legal sources where possible (official gazettes, court portals).  
- Limit wide web searches when working with confidential matters.  
- Set refresh cadence based on the legal area (faster for regulatory updates).

## Related
- [/advanced-features/enabling-and-using-web-search](./enabling-and-using-web-search.md)
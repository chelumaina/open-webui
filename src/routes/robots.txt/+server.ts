export async function GET({ url }) {
  const baseUrl = 'https://lexluma.com';
  const environment = process.env.NODE_ENV;
  
  let disallowedPaths = [];
  
  // Disallow certain paths based on environment or features
  if (environment === 'production') {
    disallowedPaths = ['/admin', '/api/secret'];
  } else {
    // Staging/development - disallow crawling
    disallowedPaths = ['/'];
  }
  
  const robots = `
User-agent: *
${disallowedPaths.map(path => `Disallow: ${path}`).join('\n')}
${disallowedPaths.length === 0 ? 'Allow: /' : ''}

# Sitemaps
Sitemap: ${baseUrl}/sitemap.xml

# Crawl delay
Crawl-delay: 1
`.trim();

  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}
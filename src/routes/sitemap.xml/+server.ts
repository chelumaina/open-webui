import { base } from '$app/paths';

export async function GET({ url }) {
  const baseUrl = 'https://lexluma.com';
  
  // Get all your pages - you might want to fetch this from a CMS or generate dynamically
  const pages = [
    { slug: '', priority: 1.0, changefreq: 'weekly' },
    { slug: 'features/ai-conversational-legal-research', priority: 0.8, changefreq: 'weekly' },
    { slug: 'features/legislation-gazette-navigator', priority: 0.9, changefreq: 'weekly' },
    { slug: 'features/case-law-qa', priority: 0.7, changefreq: 'weekly' },
    { slug: 'features/drafting-assistant', priority: 0.7, changefreq: 'weekly' },
    { slug: 'features/compliance-checklists', priority: 0.7, changefreq: 'weekly' },
    { slug: 'features/knowledge-base-dms-integration', priority: 0.7, changefreq: 'weekly' }, 
  ];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${pages.map(page => `
  <url>
    <loc>${baseUrl}/${page.slug}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'max-age=0, s-maxage=3600'
    }
  });
}
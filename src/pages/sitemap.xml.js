import { getCollection } from 'astro:content';
export async function GET({ site }) {
  const base = site ?? new URL('https://engineering-production-ai.pages.dev');
  const articles = await getCollection('articles');
  const paths = ['/', '/about/', '/projects/', '/articles/', ...articles.map(a => `/articles/${a.id}/`)];
  const escapeXml = (value) => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');
  const body = '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    paths.map(path => `  <url><loc>${escapeXml(new URL(path, base).toString())}</loc></url>`).join('\n') +
    '\n</urlset>';
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}

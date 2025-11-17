// Server-side dummy data (SSR). Replace with DB/API later.
// src/routes/+page.ts
import { error } from '@sveltejs/kit';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url'; // if needed in ESM
import { marked } from 'marked';


export async function load({ fetch }) {
  let content = ''; 
  
  const res = await fetch('/content/json_content.json'); // served from static/
    // content=res;
    if (!res.ok) throw error(500, 'Could not load JSON');
    const mydata = await res.json();

      const contentDir = path.resolve('static/content'); // project-root relative
      const filePath = path.join(contentDir, `index.md`);
      // content=filePath
  
      try {
        const md = await fs.readFile(filePath, 'utf-8');
        const html = marked(md); // Convert MD → HTML
  
        // return { md };
        content = html;
      } catch (e) {
        throw error(404, 'Page not found => '+e);
      }
  return { mydata, content };
}
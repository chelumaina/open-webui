// Server-side dummy data (SSR). Replace with DB/API later.
// src/routes/+page.ts
import { error } from '@sveltejs/kit';
import fs from 'fs/promises';
import path from 'path';
// import { fileURLToPath } from 'url'; // if needed in ESM
import { marked } from 'marked';
	
import {WEBUI_BASE_URL } from '$lib/constants';

  
// const getHelpContent = async () => { 
//   const res = await fetch(`${WEBUI_BASE_URL}/help//`, {
//     method: 'GET',
//     headers: {
//       Accept: 'application/json',
//       // authorization: `Bearer ${token}`
//     }
//   }).then(async (res) => {
//     console.log("Response from verify-email:");
//       if (!res.ok) throw await res.json();
//       return await res.json();
//   })
//   .catch((err) => { 
//     return {error: err.detail || 'Could not fetch help contents from API'};
//   }); 
// };



export async function load({ fetch }) {
  let content = '';
  let mydata={}
  const res = await fetch(`${WEBUI_BASE_URL}/help//`); // served from static/
    // if (!res.ok) throw error(500, 'Could not load JSON');
    mydata = await res.json();

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
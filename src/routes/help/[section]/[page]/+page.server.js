// Server-side dummy data (SSR). Replace with DB/API later.
// src/routes/+page.ts
import { error } from '@sveltejs/kit';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url'; // if needed in ESM
import { marked } from 'marked';
import { WEBUI_BASE_URL } from '$lib/constants';


export async function load({ params, url, fetch }) {
  try {

  const res = await fetch('/content/json_content.json'); // served from static/
    if (!res.ok) throw error(500, 'Could not load JSON');
    const sections_data = await res.json();

    const resp = await fetch(`/content/${params.section}/${params.page}.md`);
    const content = await resp.text();
    const html = marked(content); 

    // // const res = await fetch(`${WEBUI_BASE_URL}/user_guide/`); // served from static/
    // //   // if (!res.ok) throw error(500, 'Could not load JSON');
    // // const sections_data  = await res.json();
  
  


    // // // Import markdown content
    // let content=`/content/${params.section}/${params.page}.md`;
    //  // sanitize params.page to avoid path traversal
    // const name = params.page.replace(/[^a-zA-Z0-9-_]/g, '');
    //   const contentDir = path.resolve('static/content'); // project-root relative
    // const filePath = path.join(contentDir, `${params.section}/${name}.md`);
    //   // content=filePath
  
    //   try {
    //     const md = await fs.readFile(filePath, 'utf-8');
    //     const html = marked(md); // Convert MD → HTML
  
    //     // return { md };
    //     content = html;
    //   } catch (e) {
    //     throw error(404, 'Page not found => '+e);
    //   }
  


    // Define navigation structure
    const sections = sections_data

    // Find current page and calculate next/previous
    let currentSection=[], currentPage={ "title": "Introduction to LexLuma", "slug": "introduction-to-lexluma" }, pageIndex, sectionIndex;
    
    for (let i = 0; i < sections.length; i++) {
      const section = sections[i];
      if (section.slug === params.section) {
        currentSection = section;
        sectionIndex = i;
        for (let j = 0; j < section.pages.length; j++) {
          if (section.pages[j].slug === params.page) {
            currentPage = section.pages[j];
            pageIndex = j;
            break;
          }
        }
        break;
      }
    }

    if (!currentPage) {
      throw error(404, 'Page not found => '+currentPage);
    }

    // Calculate next and previous pages
    let prevPage = null;
    let nextPage = null;

    if (pageIndex > 0) {
      prevPage = {
        title: currentSection.pages[pageIndex - 1].title,
        url: `/help/${params.section}/${currentSection.pages[pageIndex - 1].slug}`
      };
    } else if (sectionIndex > 0) {
      const prevSection = sections[sectionIndex - 1];
      prevPage = {
        title: prevSection.pages[prevSection.pages.length - 1].title,
        url: `/help/${prevSection.slug}/${prevSection.pages[prevSection.pages.length - 1].slug}`
      };
    }

    if (pageIndex < currentSection.pages.length - 1) {
      nextPage = {
        title: currentSection.pages[pageIndex + 1].title,
        url: `/help/${params.section}/${currentSection.pages[pageIndex + 1].slug}`
      };
    } else if (sectionIndex < sections.length - 1) {
      const nextSection = sections[sectionIndex + 1];
      nextPage = {
        title: nextSection.pages[0].title,
        url: `/help/${nextSection.slug}/${nextSection.pages[0].slug}`
      };
    }

    return {
      content:html,
      sections_data:sections,
      currentPage: {
        title: currentPage.title,
        section: currentSection.title,
        slug: currentPage.slug
      },
      seo: {
        metaTitle: currentPage.metaTitle || currentPage.title,
        metaDescription: currentPage.metaDescription || '',
        metaKeywords: currentPage.keywords || '',
        metaStructure: {
        "@context": "https://schema.org",
        "@type": "Use-Gudelines",
        "headline": `${currentPage.metaTitle} - Lex Luma AI`,
        "description": `${currentPage.metaDescription}`,
        "author": {
          "@type": "Organization",
          "name": "Lex Luma"
        }
      }
      },
      prevPage,
      nextPage
    };
  } catch (e) {
    throw error(404, 'Page not found => '+e);
  }
}
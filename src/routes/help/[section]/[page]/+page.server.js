import { error } from '@sveltejs/kit';

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url'; // if needed in ESM
import { marked } from 'marked';


export async function load({ params, url }) {
  try {
    
    // // Import markdown content
    let content=`/content/${params.page}.md`;
     // sanitize params.page to avoid path traversal
    const name = params.page.replace(/[^a-zA-Z0-9-_]/g, '');
    const contentDir = path.resolve('src/lib/content'); // project-root relative
    const filePath = path.join(contentDir, `${name}.md`);

    try {
      const md = await fs.readFile(filePath, 'utf-8');
      const html = marked(md); // Convert MD → HTML

      // return { md };
      content = html;
    } catch (e) {
      throw error(404, 'Page not found');
    }

    

    // Define navigation structure
    const sections = [
      {
        title: 'Getting Started',
        slug: 'getting-started',
        pages: [
          { title: 'Introduction', slug: 'introduction' },
          { title: 'Installation', slug: 'installation' },
          { title: 'Quick Start', slug: 'quick-start' }
        ]
      },
      {
        title: 'Features',
        slug: 'features',
        pages: [
          { title: 'Chat Interface', slug: 'chat-interface' },
          { title: 'Model Management', slug: 'model-management' },
          { title: 'Plugins', slug: 'plugins' }
        ]
      },
      {
        title: 'Advanced',
        slug: 'advanced',
        pages: [
          { title: 'API Reference', slug: 'api-reference' },
          { title: 'Deployment', slug: 'deployment' },
          { title: 'Troubleshooting', slug: 'troubleshooting' }
        ]
      }
    ];

    // Find current page and calculate next/previous
    let currentSection, currentPage, pageIndex, sectionIndex;
    
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
      throw error(404, 'Page not found');
    }

    // Calculate next and previous pages
    let prevPage = null;
    let nextPage = null;

    if (pageIndex > 0) {
      prevPage = {
        title: currentSection.pages[pageIndex - 1].title,
        url: `/docs/${params.section}/${currentSection.pages[pageIndex - 1].slug}`
      };
    } else if (sectionIndex > 0) {
      const prevSection = sections[sectionIndex - 1];
      prevPage = {
        title: prevSection.pages[prevSection.pages.length - 1].title,
        url: `/docs/${prevSection.slug}/${prevSection.pages[prevSection.pages.length - 1].slug}`
      };
    }

    if (pageIndex < currentSection.pages.length - 1) {
      nextPage = {
        title: currentSection.pages[pageIndex + 1].title,
        url: `/docs/${params.section}/${currentSection.pages[pageIndex + 1].slug}`
      };
    } else if (sectionIndex < sections.length - 1) {
      const nextSection = sections[sectionIndex + 1];
      nextPage = {
        title: nextSection.pages[0].title,
        url: `/docs/${nextSection.slug}/${nextSection.pages[0].slug}`
      };
    }

    return {
      content,
      currentPage: {
        title: currentPage.title,
        section: currentSection.title
      },
      prevPage,
      nextPage
    };
  } catch (e) {
    throw error(404, 'Page not found');
  }
}
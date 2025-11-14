import { marked } from 'marked';
import { gfmHeadingId } from 'marked-gfm-heading-id';
import { mangle } from 'marked-mangle';

// Configure marked
marked.use(gfmHeadingId());
marked.use(mangle());

marked.setOptions({
  highlight: function(code, lang) {
    // In a real implementation, you'd use a proper highlighter like Prism
    return `<pre><code class="language-${lang}">${escapeHtml(code)}</code></pre>`;
  },
  breaks: true,
  gfm: true
});

function escapeHtml(html) {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export function renderMarkdown(content) {
  return marked.parse(content);
}
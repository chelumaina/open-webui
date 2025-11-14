<script context="module">
  import { error } from '@sveltejs/kit';
  // We use import.meta.glob to import markdown content as raw text and mdsvex to render
  export async function load({ params }) {
    const modules = import.meta.glob('$lib/content/*.md', { as: 'raw' });
    const entries = Object.entries(modules);
    const map = {};
    for (const [path, loader] of entries) {
      const slug = path.split('/').pop().replace('.md','');
      const content = await loader();
      map[slug] = content;
    }
    const slug = params.slug;
    const md = map[slug];
    if (!md) throw error(404, 'Not found');
    return { raw: md };
  }
</script>

<script>
  export let data;

  console.log(data);
</script>

<article class="prose max-w-none">
  {@html data.raw}
</article>

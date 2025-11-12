<script>
  export let title = 'Default Title';
  export let description = 'Default description';
  export let image = '/default-og.jpg';
  export let canonical = '';
  export let noindex = false;
  export let structuredData = null;
  
  $: fullCanonical = canonical ? canonical : `https://lexluma.com`;
</script>

<svelte:head>
  <!-- Basic Meta -->
  <title>{title}</title>
  <meta name="description" content={description} />
  
  {#if noindex}
    <meta name="robots" content="noindex, nofollow" />
  {/if}
  
  <!-- Open Graph -->
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={image} />
  <meta property="og:url" content={fullCanonical} />
  <meta property="og:type" content="website" />
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={image} />
  
  <!-- Canonical -->
  <link rel="canonical" href={fullCanonical} />
  
  <!-- Structured Data -->
  {#if structuredData}
    <script type="application/ld+json">
      {JSON.stringify(structuredData)}
    </script>
  {/if}
</svelte:head>
<script>
  export let data;
</script>

<svelte:head>
  <meta name="description" content={data.siteDescription} />
  <meta property="og:site_name" content={data.siteTitle} />
</svelte:head>

<slot />
<script>
  export let content = '';
  export let prevPage = null;
  export let nextPage = null;
  export let currentPage = { title: '', section: '' };
</script>

<main class="flex-1 ml-0 lg:ml-64">
  <!-- Content -->
  <div class="px-4 sm:px-8 py-8">
    <div class="max-w-4xl mx-auto">
      {#if content}
        <article class="prose prose-slate dark:prose-invert max-w-none">
          {@html content}
        </article>
        
        <!-- Navigation -->
        <div class="mt-12 pt-8 border-t border-slate-200 dark:border-slate-700 flex justify-between">
          {#if prevPage}
            <a 
              href={prevPage.url} 
              class="flex items-center space-x-2 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              <span>{prevPage.title}</span>
            </a>
          {:else}
            <div></div>
          {/if}
          
          {#if nextPage}
            <a 
              href={nextPage.url} 
              class="flex items-center space-x-2 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300"
            >
              <span>{nextPage.title}</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </a>
          {/if}
        </div>
      {:else}
        <div class="text-center">
          <h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Page Not Found</h1>
          <p class="text-slate-600 dark:text-slate-400 mb-8">The documentation page you're looking for doesn't exist.</p>
          <a href="/" class="inline-flex items-center px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors duration-200">
            Back to Home
          </a>
        </div>
      {/if}
    </div>
  </div>
</main>
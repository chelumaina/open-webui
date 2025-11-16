<script>
  import { page } from '$app/stores';
  
  let { sections, searchQuery, isMobileMenuOpen, closeMobileMenu } = $props();
  
  // Track collapsed state for each section
  let collapsedSections = $state({});
  
  // Initialize all sections as expanded
  $effect(() => {
    sections.forEach(section => {
      if (collapsedSections[section.slug] === undefined) {
        collapsedSections[section.slug] = false;
      }
    });
  });
  
  // Toggle section collapse state
  function toggleSection(slug) {
    collapsedSections[slug] = !collapsedSections[slug];
  }
  
  // Use $derived for computed values at the top level
  const filteredSections = $derived(
    sections.map(section => ({
      ...section,
      pages: section.pages.filter(page => 
        page.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        section.title.toLowerCase().includes(searchQuery.toLowerCase())
      )
    })).filter((section) => section.pages.length > 0)
  );

  
  const currentPath = $derived($page.url.pathname);



</script>

<!-- Desktop Sidebar -->
<aside class="w-85 bg-slate-50 dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 fixed h-screen overflow-y-auto hidden lg:block">
  <div class="p-6">
    <!-- Logo -->
    <div class="flex items-center space-x-3 mb-8">
      <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
        <span class="text-white font-bold text-sm">OW</span>
      </div>
      <span class="text-xl font-bold text-slate-900 dark:text-white">OpenWebUI</span>
    </div>
    
    <!-- Search -->
    <div class="mb-6">
      <div class="relative">
        <input 
          bind:value={searchQuery}
          type="text" 
          placeholder="Search documentation..." 
          class="w-full pl-10 pr-4 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <svg class="w-4 h-4 absolute left-3 top-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>
    
    
    <!-- Navigation -->
    <nav class="space-y-6">
      {#each filteredSections as section}
        <div>
          <button 
            on:click={() => toggleSection(section.slug)}
            class="w-full flex items-center justify-between text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide mb-3 hover:text-primary-600 dark:hover:text-primary-400 transition-colors duration-200"
          >
            <h3>{section.title}</h3>
            <svg 
              class="w-4 h-4 transition-transform duration-200 {collapsedSections[section.slug] ? '-rotate-90' : ''}" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {#if !collapsedSections[section.slug]}
            <ul class="space-y-2">
              {#each section.pages as page}
                <li>
                  <a 
                    href="/help/{section.slug}/{page.slug}" 
                    class="block px-3 py-2 text-sm text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-white dark:hover:bg-slate-700 rounded-lg transition-colors duration-200 {(currentPath === `/help/${section.slug}/${page.slug}` ? 'bg-white dark:bg-slate-700 text-primary-600 dark:text-primary-400 border border-slate-200 dark:border-slate-600' : '')}"
                  >
                    {page.title}
                  </a>
                </li>
              {/each}
            </ul>
          {/if}
        </div>
      {/each}
    </nav>
  </div>
</aside>

<!-- Mobile Sidebar Overlay -->
{#if isMobileMenuOpen}
  <div class="lg:hidden fixed inset-0 z-50">
    <div class="fixed inset-0 bg-black bg-opacity-50" on:click={closeMobileMenu}></div>
    <div class="fixed left-0 top-0 bottom-0 w-64 bg-white dark:bg-slate-800 overflow-y-auto">
      <div class="p-6">
        <!-- Mobile Header -->
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">OW</span>
            </div>
            <span class="text-xl font-bold text-slate-900 dark:text-white">OpenWebUI</span>
          </div>
          <button on:click={closeMobileMenu} class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Mobile Search -->
        <div class="mb-6">
          <div class="relative">
            <input 
              bind:value={searchQuery}
              type="text" 
              placeholder="Search documentation..." 
              class="w-full pl-10 pr-4 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <svg class="w-4 h-4 absolute left-3 top-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        
        <!-- Mobile Navigation -->
        <nav class="space-y-6">
          {#each filteredSections as section}
            <div>
              <button 
                on:click={() => toggleSection(section.slug)}
                class="w-full flex items-center justify-between text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide mb-3 hover:text-primary-600 dark:hover:text-primary-400 transition-colors duration-200"
              >
                <h3>{section.title}</h3>
                <svg 
                  class="w-4 h-4 transition-transform duration-200 {collapsedSections[section.slug] ? '-rotate-90' : ''}" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {#if !collapsedSections[section.slug]}
                <ul class="space-y-2">
                  {#each section.pages as page}
                    <li>
                      <a 
                        href="/help/{section.slug}/{page.slug}" 
                        on:click={closeMobileMenu}
                        class="block px-3 py-2 text-sm text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-white dark:hover:bg-slate-700 rounded-lg transition-colors duration-200 {(currentPath === `/help/${section.slug}/${page.slug}` ? 'bg-white dark:bg-slate-700 text-primary-600 dark:text-primary-400 border border-slate-200 dark:border-slate-600' : '')}"
                      >
                        {page.title}
                      </a>
                    </li>
                  {/each}
                </ul>
              {/if}
            </div>
          {/each}
        </nav>
      </div>
    </div>
  </div>
{/if}
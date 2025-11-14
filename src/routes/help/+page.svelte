<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { Header, Sidebar, HomeContent } from '$lib/components/index.js';
  
  let { data } = $props();

  let sections =  [{
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


  
  let isDark = $state(false);
  let isMobileMenuOpen = $state(false);
  let searchQuery = $state('');
  
  onMount(() => {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    isDark = saved ? saved === 'dark' : prefersDark;
    updateTheme();
  });
  
  function toggleTheme() {
    isDark = !isDark;
    updateTheme();
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }
  
  function updateTheme() {
    document.documentElement.classList.toggle('dark', isDark);
  }
  
  function toggleMobileMenu() {
    isMobileMenuOpen = !isMobileMenuOpen;
  }
  
  function closeMobileMenu() {
    isMobileMenuOpen = false;
  }
</script>

<div class="min-h-screen bg-white dark:bg-slate-900 transition-colors duration-200">
  <div class="flex min-h-screen">
    <!-- {data.sections} -->
    <!-- Sidebar -->
    <Sidebar 
      sections={sections} 
      {searchQuery} 
      {isMobileMenuOpen}
      {closeMobileMenu}
    />
    
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Header -->
      <Header 
        {isDark}
        {toggleTheme}
        {isMobileMenuOpen}
        toggleMobileMenu={toggleMobileMenu}
      />
      
      <!-- Home Content -->
      <HomeContent />
    </div>
  </div>
</div>
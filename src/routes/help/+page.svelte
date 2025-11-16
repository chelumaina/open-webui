<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { Header, Sidebar, HomeContent } from '$lib/components/index.js';
  let { data } = $props();

  
  const { mydata, content } = data;
  // let { data } = $props();

  
  let sections =  mydata || [];
  
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
      <HomeContent content={content} />
    </div>
  </div>
</div>
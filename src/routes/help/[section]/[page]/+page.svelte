<script>
  import { page } from '$app/stores';
	import { onMount, getContext } from 'svelte';
  import Header from '$lib/components/help/TopNav.svelte';
  import Sidebar from '$lib/components/help/Sidebar.svelte';
  import ContentArea from '$lib/components/help/ContentArea.svelte';
  import SEOHead from '$lib/components/seo/SEOHead.svelte';
  const i18n = getContext('i18n');

  let { data } = $props();
  let {sections_data} = data; 
  console.log('Section Page Data:', sections_data); 
  let sections =  sections_data || [];
 
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

<SEOHead
  title="{data.seo.metaTitle} - {$i18n.t('Lex Luma AI')}"
  description={data.seo.metaDescription}
  keywords={data.seo.metaKeywords}
  image="/static/static/apple-touch-icon.png"
  noindex={false}
  structuredData={data.seo.metaStructure}
/>

<div class="min-h-screen bg-white dark:bg-slate-900 transition-colors duration-200">
  <div class="flex min-h-screen">
    <!-- Sidebar -->
     <!-- {sections} -->
    <Sidebar 
      sections={sections} 
      {searchQuery} 
      currentPath={$page.url.pathname}
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
      
      <!-- Documentation Content -->
      <ContentArea 
        content={data.content}
        prevPage={data.prevPage}
        nextPage={data.nextPage}
        currentPage={data.currentPage}
      />
    </div>
  </div>
</div>
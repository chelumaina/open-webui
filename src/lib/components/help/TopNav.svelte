<script>
  import { WEBUI_BASE_URL } from '$lib/constants';

  export let isDark = false;
  export let toggleTheme;
  export let isMobileMenuOpen = false;
  export let toggleMobileMenu;
</script>

<header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-10">
  <div class="flex items-center justify-between px-8 py-4">
    <div class="flex items-center space-x-4">
      {#if isDark}
        <img
                crossorigin="anonymous"
                src="{WEBUI_BASE_URL}/static/favicon-dark.png"
                class="sidebar-new-chat-icon size-12 rounded-full group-hover:hidden"
                alt=""
              />
      {:else}
         <img
                crossorigin="anonymous"
                src="{WEBUI_BASE_URL}/static/favicon.png"
                class="sidebar-new-chat-icon size-12 rounded-full group-hover:hidden"
                alt=""
              />
      {/if}
     
         <!-- <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>  -->
     
      <h1 class="text-2xl font-bold text-slate-900 dark:text-white"><a href="/">Lex Luma AI</a></h1>
    </div>
    
    <div class="flex items-center space-x-4">
      <!-- Theme Toggle -->
      <button 
        on:click={toggleTheme}
        class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
        title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {#if isDark}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        {:else}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        {/if}
      </button>
      
      <!-- GitHub Link -->
      <a 
        href="{WEBUI_BASE_URL}" 
        target="_blank" 
        class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
      >
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 9.75L12 3l9 6.75V21a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1V9.75z"/>
      </svg>
      </a>
    </div>
  </div>
</header>
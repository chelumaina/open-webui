<script>
  import {goto} from '$app/navigation';
 
  import { onMount } from 'svelte';
   
  onMount(() => {
    goto('/help');
  });
  
</script>

<div class="min-h-screen bg-white dark:bg-slate-900 transition-colors duration-200">
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Header -->
      
      <div class="flex-1 flex flex-col min-w-0">
        <div class="px-4 sm:px-8 py-8">
          <div class="max-w-4xl mx-auto text-center">
            <h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Redirecting...</h1>
            <p class="text-slate-600 dark:text-slate-400 mb-8">You are being redirected to the help home page.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
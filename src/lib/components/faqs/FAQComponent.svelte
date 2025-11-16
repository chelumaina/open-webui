<script>
  let { faqs = [] } = $props();
  
  // Track which FAQ items are expanded
  let expandedItems = $state({});
  
  // Toggle FAQ item
  function toggleItem(index) {
    expandedItems[index] = !expandedItems[index];
  }
</script>

<div class="faq-container max-w-4xl mx-auto py-8 px-4">
  <!-- FAQ Header -->
  <!-- <div class="text-center mb-12">
    <h1 class="text-4xl font-bold text-slate-900 dark:text-white mb-4">
      Frequently Asked Questions
    </h1>
    <p class="text-lg text-slate-600 dark:text-slate-400">
      Find answers to common questions about OpenWebUI
    </p>
  </div> -->
  
  <!-- FAQ Items -->
  <div class="space-y-4">
    <!-- {#each faqs as faq, index}
      <div class="faq-item bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden transition-all duration-200 hover:shadow-md">
         <button
          on:click={() => toggleItem(index)}
          class="w-full flex items-center justify-between p-6 text-left focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-inset"
          aria-expanded={expandedItems[index] || false}
        >
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white pr-8">
            {faq.question}
          </h3>
          <svg
            class="w-6 h-6 text-slate-500 dark:text-slate-400 flex-shrink-0 transition-transform duration-200 {expandedItems[index] ? 'rotate-180' : ''}"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        
         {#if expandedItems[index]}
          <div class="px-6 pb-6 text-slate-600 dark:text-slate-300 leading-relaxed">
            {@html faq.answer}
          </div>
        {/if}
      </div>
    {/each} -->
  </div>
  
  <!-- Empty State -->
  <!-- {#if faqs.length === 0}
    <div class="text-center py-12">
      <svg class="w-16 h-16 mx-auto text-slate-300 dark:text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-slate-500 dark:text-slate-400 text-lg">No FAQs available at the moment</p>
    </div>
  {/if} -->
  
  <!-- Contact Section -->
  <div class="mt-12 text-center p-8 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
    <h3 class="text-xl font-semibold text-slate-900 dark:text-white mb-2">
      Still have questions?
    </h3>
    <p class="text-slate-600 dark:text-slate-400 mb-4">
      Can't find the answer you're looking for? Please reach out to our support team.
    </p>
    <a 
      href="#"
      class="inline-flex items-center px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors duration-200"
    >
      Contact Support
      <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
      </svg>
    </a>
  </div>
</div>

<style>
  .faq-item {
    transition: all 0.2s ease-in-out;
  }
  
  .faq-item:hover {
    transform: translateY(-2px);
  }
</style>
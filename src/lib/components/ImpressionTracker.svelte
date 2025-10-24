<script lang="ts">
	import { WEBUI_BASE_URL } from '$lib/constants';
  import { onMount, onDestroy } from 'svelte';

  export let sectionId;
  let sectionEl: HTMLElement;
  let observer: IntersectionObserver | null = null;

  const buildImpressionPayload=(sectionId: string) =>{
    const url = new URL(window.location.href);
    const query = {};
    for (const [key, value] of url.searchParams.entries()) {
      query[key] = value;
    }

    return {
      section_id: sectionId,
      timestamp: new Date().toISOString(),
      path: window.location.pathname,
      full_url: url.toString(),
      query,
      user_agent: navigator.userAgent,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      },
      screen: {
        width: window.screen.width,
        height: window.screen.height
      },
      language: navigator.language,
      referrer: document.referrer
    };
  };

  export const useIntersection=(callback, options = { threshold: 0.5 }) =>{
    return function (node) {
      const observer = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) {
          callback(node);
          observer.unobserve(node); // Only trigger once
        }
      }, options);

      observer.observe(node);

      return {
        destroy() {
          observer.unobserve(node);
        }
      };
    };
  };


  const sendImpression = (sectionId) => {
    // fetch(`${WEBUI_BASE_URL}/api/track-impression`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(buildImpressionPayload(`${sectionId}-section`))

    // });
  };

  onMount(() => {
    console.log("onMount "+sectionId)
    observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        // sendImpression();
        // if (!localStorage.getItem(`seen-${sectionId}`)) {
          sendImpression(sectionId);
          // localStorage.setItem(`seen-${sectionId}`, 'true');
        // }
        
        observer.unobserve(sectionEl);
      }
    }, { threshold: 0.5 });

    observer.observe(sectionEl);
  });

  onDestroy(() => {
    console.log("onDestroy "+sectionId)
    observer?.disconnect();
  });
</script>

<div bind:this={sectionEl}>
  <slot />
</div>

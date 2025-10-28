<script lang="ts">
  export interface Testimonial {
    id: string;
    name: string;
    role: string;
    organization: string;
    jurisdiction: string;
    headline: string;
    quote: string;
    features_used?: string[];
    impact?: Record<string, number | string>;
    rating: number; // 1..5
    date?: string;
    verified?: boolean;
  }

  export let items: Testimonial[] = [];

  // Fixed container & card sizing
  export let containerWidthPx = 1200;   // ⟵ fixed width container
  export let cardWidthPx = 360;         // ⟵ fixed card width
  export let gapPx = 24;                // ⟵ gap between cards
  const cardSpan = () => cardWidthPx + gapPx;

  // Autoplay controls
  export let autoplay = true;
  export let autoplayMs = 3000;
  export let pauseOnHover = true;
  export let wrapToStart = true; // jump back to start when we reach the end

  let scroller: HTMLDivElement | null = null;
  let timer: any;

  const initials = (name: string) =>
    name.trim().split(/\s+/).slice(0,2).map(n => n[0]?.toUpperCase() ?? "").join("");

  function scrollByCards(n = 1) {
    if (!scroller) return;
    const by = n * cardSpan();
    const atEnd = scroller.scrollLeft + scroller.clientWidth >= scroller.scrollWidth - 5;

    if (atEnd && wrapToStart) {
      scroller.scrollTo({ left: 0, behavior: "smooth" });
      return;
    }
    scroller.scrollBy({ left: by, behavior: "smooth" });
  }

  function start() {
    if (!autoplay || timer) return;
    timer = setInterval(() => scrollByCards(1), autoplayMs);
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
  }

  function onPointerDown() {
    // Pause when user drags
    stop();
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === "ArrowRight") { stop(); scrollByCards(1); }
    if (e.key === "ArrowLeft")  { stop(); scrollByCards(-1); }
  }

  // Visibility pause/resume
  const onVis = () => document.hidden ? stop() : start();

  // Lifecycle
  import { onMount, onDestroy } from "svelte";
  onMount(() => {
    if (autoplay) start();
    document.addEventListener("visibilitychange", onVis);
  });
  onDestroy(() => {
    stop();
    document.removeEventListener("visibilitychange", onVis);
  });
</script>

<section class="py-16">
  <div class="mx-auto" style="width: {containerWidthPx}px">
    <div class="mb-6 flex items-end justify-between">
        <div class="mx-auto max-w-3xl text-center">
            <h2 id="testimonials-title" class="text-3xl font-bold tracking-tight sm:text-4xl">
                What Our Users Say
            </h2>
            <p class="mt-3 text-base text-gray-500 dark:text-gray-400">See how we've helped our clients succeed.</p>
        </div>
     </div>

    <div class="relative">
      <!-- edge fades -->
      <div class="pointer-events-none absolute left-0 top-0 h-full w-10 bg-gradient-to-r from-white to-transparent dark:from-gray-950"></div>
      <div class="pointer-events-none absolute right-0 top-0 h-full w-10 bg-gradient-to-l from-white to-transparent dark:from-gray-950"></div>

      <!-- scroller -->
      <div
        bind:this={scroller}
        class="flex snap-x snap-mandatory overflow-x-auto scroll-smooth px-1 gap-0 scrollbar-hide [scrollbar-width:none] [-ms-overflow-style:none]"
        style="scroll-padding-left: 0px;"
        tabindex="0"
        aria-label="Testimonials"
        on:keydown={onKeydown}
        on:pointerdown={onPointerDown}
        on:mouseenter={() => pauseOnHover && stop()}
        on:mouseleave={() => pauseOnHover && start()}>
        {#each items as item (item.id)}
          <figure
            class="snap-start shrink-0 rounded-2xl border border-gray-200 bg-white/70 p-6 shadow-sm hover:shadow-md transition
                   dark:border-gray-800 dark:bg-gray-900/70"
            style="width:{cardWidthPx}px; margin-right:{gapPx}px;">
            <div class="flex items-center gap-4">
              <div class="h-12 w-12 rounded-full bg-gray-200 dark:bg-gray-800 flex items-center justify-center text-sm font-semibold">
                {initials(item.name)}
              </div>
              <figcaption class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold">{item.name}</span>
                  <span class="text-amber-500" aria-label="{item.rating} out of 5 stars">
                    {#each Array(5) as _, i}{i < item.rating ? "★" : "☆"}{/each}
                  </span>
              
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {item.role} · {item.organization} · {item.jurisdiction}
                </p>
              </figcaption>
            </div>

            <p class="mt-3 text-xs font-medium text-gray-900 dark:text-gray-100">{item.headline}</p>
            <blockquote class="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-200">“{item.quote}”</blockquote>

            {#if item.features_used?.length}
              <div class="mt-4 flex flex-wrap gap-2">
                {#each item.features_used.slice(0,3) as f}
                  <span class="inline-flex items-center rounded-full bg-gray-50 px-2.5 py-1 text-[11px] font-medium
                               text-gray-700 dark:bg-gray-800 dark:text-gray-300">{f}</span>
                {/each}
              </div>
            {/if}
          </figure>
        {/each}
      </div>
    </div>
  </div>
</section>

<style>
  .scrollbar-hide::-webkit-scrollbar { display: none; }
</style>

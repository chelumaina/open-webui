<script lang="ts">
  export interface Step {
    title: string;
    description: string;
    /** Tailwind gradient tokens, e.g. "from-indigo-500" */
    gradientFrom: string;
    /** Tailwind gradient tokens, e.g. "to-purple-600" */
    gradientTo: string;
    /** Tailwind color for ping dot, e.g. "bg-yellow-400" */
    pingColor: string;
    /** Optional animation delay for the ping: "delay-500", "delay-1000", etc. */
    pingDelay?: string;
  }

  export let heading = "How It Works";
  export let subheading = "Get started in three simple steps";

  // Defaults tailored to Open WebUI for legal research
  export let steps: Step[] = [
    {
      title: "Sign up and Create Your Workspace",
      description:
        "Sign up, create a secure workspace, upload your documents, and set your sources.",
      gradientFrom: "from-indigo-500",
      gradientTo: "to-purple-600",
      pingColor: "bg-yellow-400",
      pingDelay: "" // no delay
    },
    {
      title: "Connect Law Sources & Configure RAG",
      description:
        "Upload Gazette Notices, Acts & subsidiary legislation, and court decisions. OCR + chunking + metadata. Set Top-K, filters, and citation style.",
      gradientFrom: "from-purple-500",
      gradientTo: "to-pink-600",
      pingColor: "bg-green-400",
      pingDelay: "delay-500"
    },
    {
      title: "Chat, Cite & Export",
      description:
        "Ask in plain language, get paragraph-level citations, draft memos/skeletons, and export to Word/Docs with sources.",
      gradientFrom: "from-pink-500",
      gradientTo: "to-rose-600",
      pingColor: "bg-blue-400",
      pingDelay: "delay-1000"
    }
  ];
</script>

<section class="py-20 bg-white dark:bg-gray-800 s-m2wW3TfO6y5x">
  <div class="container mx-auto px-4 s-m2wW3TfO6y5x">
    <div class="text-center mb-16 s-m2wW3TfO6y5x">
      <h2 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4 s-m2wW3TfO6y5x">
        {heading}
      </h2>
      <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto s-m2wW3TfO6y5x">
        {subheading}
      </p>
    </div>

    <div class="relative s-m2wW3TfO6y5x">
      <!-- Connector line (desktop only) -->
      <div class="hidden md:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200 dark:from-indigo-900 dark:via-purple-900 dark:to-pink-900 transform -translate-y-1/2 z-0 s-m2wW3TfO6y5x"></div>

      <!-- Steps -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10 s-m2wW3TfO6y5x">
        {#each steps as step, i}
          <div class="text-center group s-m2wW3TfO6y5x">
            <div class="relative inline-block mb-6 s-m2wW3TfO6y5x">
              <div class={`w-32 h-32 bg-gradient-to-br ${step.gradientFrom} ${step.gradientTo} rounded-3xl flex items-center justify-center mx-auto shadow-2xl group-hover:scale-110 transition-transform duration-300 s-m2wW3TfO6y5x`}>
                <span class="text-white text-5xl font-extrabold s-m2wW3TfO6y5x">{i + 1}</span>
              </div>

              <!-- ping dot (animated + static) -->
              <div class={`absolute -top-2 -right-2 w-8 h-8 ${step.pingColor} rounded-full animate-ping ${step.pingDelay ?? ''} s-m2wW3TfO6y5x`}></div>
              <div class={`absolute -top-2 -right-2 w-8 h-8 ${step.pingColor} rounded-full s-m2wW3TfO6y5x`}></div>
            </div>

            <h3 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white s-m2wW3TfO6y5x">
              {step.title}
            </h3>
            <p class="text-gray-600 dark:text-gray-400 leading-relaxed s-m2wW3TfO6y5x">
              {step.description}
            </p>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>

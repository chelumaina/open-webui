<script>
	import { goto } from '$app/navigation';
	import ImpressionTracker from '$lib/components/ImpressionTracker.svelte';
	import PaystackCheckout from '$lib/components/payment/PaystackCheckout.svelte';
	import { WEBUI_NAME, config, user } from '$lib/stores';
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

	const i18n = getContext('i18n');

	let loaded = false;
	let selectedPlan = null;
	
	// Paystack configuration - Replace with your actual public key
	const PAYSTACK_PUBLIC_KEY = 'pk_test_your_paystack_public_key_here';

	onMount(async () => {
		loaded = true;
	});

	/**
	 * Handle successful payment
	 */
	function handlePaymentSuccess(event) {
		const { transaction, plan, planData } = event.detail;
		console.log('Payment successful:', { transaction, plan, planData });
		
		toast.success($i18n.t('Subscription activated successfully!'));
	}

	/**
	 * Handle payment cancellation
	 */
	function handlePaymentCancel(event) {
		const { plan } = event.detail;
		console.log('Payment cancelled for plan:', plan);
		toast.info($i18n.t('Payment was cancelled. You can try again anytime.'));
	}
// "7601634e-5d97-4d2f-81dc-4ff609df3530"	"4844b2fe-1df4-4f91-a9cf-83b851b8ca06"	"Basic Plan"
// "eebfa470-8f68-4030-b0ad-f0b345e5f06a"	"4844b2fe-1df4-4f91-a9cf-83b851b8ca06"	"Enterprise Plan"
// "e6a862c6-a6f7-41a1-9614-62a41623f9d8"	"4844b2fe-1df4-4f91-a9cf-83b851b8ca06"	"Enterprise Pro"
let plans = [
  {
    id: 'basic',
    name: 'Basic',
    tagline: 'Perfect for getting started',
    price: '$5',
    period: 'month',
    amount: 5,
    currency: 'USD',
    group_id: '7601634e-5d97-4d2f-81dc-4ff609df3530',
    highlighted: false,
    badge: null,
    features: [
      'Coverage: Basic statutes + case law',
      'Jurisdiction-ready citations',
      'Expanded messaging and uploads',
      'Longer memory and context',
      'Limited deep research',
      // '10K API Calls / month',
      'Up to 8K context tokens / request',
      'Access to custom prompts',
      // '20 requests / minute rate limit',
      // 'Up to 2GB knowledge index storage',
      // 'Upload: 10MB per file, 2GB total',
      // 'Q&A with inline citations',
      // 'Basic semantic search',
      // 'PDF/Word ingestion',
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    tagline: 'Advanced features for professionals',
    price: '$10',
    period: 'month',
    amount: 10,
    currency: 'USD',
    group_id: 'eebfa470-8f68-4030-b0ad-f0b345e5f06a',
    highlighted: true,
    badge: 'Most Popular',
    features: [
      'Everything in Basic',
      'Comprehensive legal coverage',
      'Includes legal sources and gazettes issues',
      'Enhanced research capabilities',
      'Daily content updates',
      'Citations with deep links',
      // 'Unlimited API Calls',
      // 'Up to 200K context tokens',
      // 'Custom rate limits',
      // 'Scalable knowledge index (100GB+)',
      // 'Expanded messaging and uploads',
      // 'Expanded and faster image creation',
      'Expanded memory and context',
    ]
  },
  {
    id: 'enterprise_plus',
    name: 'Enterprise Plus',
    tagline: 'Premium solution for teams',
    price: '$20',
    period: 'month',
    amount: 20,
    currency: 'USD',
    group_id: 'e6a862c6-a6f7-41a1-9614-62a41623f9d8',
    highlighted: false,
    badge: 'Best Value',
    features: [
      'Everything in Enterprise Plan',
      'Enhanced Models trained with Legal datasets',
      'Models trained with court decisions',
      'Priority support 24/7',
      'includes Gazette issues, legal sources and Court Decisions',
      
      // 'Dedicated account manager',
      // 'Custom integrations',
      // 'Advanced analytics',
      // 'Team collaboration tools',
      // 'SSO & SAML support',
      // '99.9% uptime SLA',
      // 'Custom deployment options',
      // 'Quarterly business reviews',
    ]
  }
];

</script>

<!-- Modern Pricing Page -->
<div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-950 dark:to-purple-950">
	<!-- Decorative background elements -->
	<div class="absolute inset-0 overflow-hidden pointer-events-none">
		<div class="absolute top-0 right-0 w-96 h-96 bg-purple-300 dark:bg-purple-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl opacity-20 animate-blob"></div>
		<div class="absolute bottom-0 left-0 w-96 h-96 bg-blue-300 dark:bg-blue-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
		<div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-300 dark:bg-indigo-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
	</div>

	<div class="relative z-10 container mx-auto px-4 py-16">
		<!-- Header Section -->
		<div class="text-center mb-16">
			<div class="inline-flex items-center justify-center px-4 py-2 mb-6 rounded-full bg-purple-100 dark:bg-purple-900/30 border border-purple-200 dark:border-purple-800">
				<svg class="w-5 h-5 mr-2 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
				</svg>
				<span class="text-sm font-semibold text-purple-700 dark:text-purple-300">Flexible Pricing Plans</span>
			</div>
			
			<h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-4">
				Choose Your <span class="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Perfect Plan</span>
			</h1>
			
			<p class="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
				Unlock powerful features and scale your productivity with our comprehensive subscription plans
			</p>
		</div>

		<!-- Pricing Cards -->
		<ImpressionTracker sectionId="subscription-section">
			<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
				{#each plans as plan, index}
					<div 
						class="relative group"
						role="article"
						on:mouseenter={() => selectedPlan = plan.id}
						on:mouseleave={() => selectedPlan = null}
					>
						<!-- Highlighted plan glow effect -->
						{#if plan.highlighted}
							<div class="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
						{/if}
						
						<div 
							class="relative h-full bg-white dark:bg-gray-800 rounded-3xl shadow-xl {plan.highlighted ? 'ring-2 ring-purple-500 dark:ring-purple-400' : 'border border-gray-200 dark:border-gray-700'} transition-all duration-300 hover:shadow-2xl hover:scale-105"
						>
							<!-- Badge for highlighted plans -->
							{#if plan.badge}
								<div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
									<span class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg">
										<svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
											<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
										</svg>
										{plan.badge}
									</span>
								</div>
							{/if}

							<div class="p-8">
								<!-- Plan Header -->
								<div class="mb-8">
									<h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
										{plan.name}
									</h3>
									<p class="text-sm text-gray-600 dark:text-gray-400">
										{plan.tagline}
									</p>
								</div>

								<!-- Price -->
								<div class="mb-8">
									<div class="flex items-baseline">
										<span class="text-5xl font-extrabold text-gray-900 dark:text-white">
											{plan.price}
										</span>
										<span class="text-xl text-gray-600 dark:text-gray-400 ml-2">
											/{plan.period}
										</span>
									</div>
								</div>

								<!-- CTA Button -->
								<div class="mb-8">
									{#if !$user}
										<div class="text-center mb-4">
											<p class="text-sm text-gray-500 dark:text-gray-400 mb-3">
												{$i18n.t('Please log in to subscribe')}
											</p>
											<button
												on:click={() => goto('/auth')}
												class="w-full py-3.5 px-6 rounded-xl font-semibold text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 transform transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 shadow-lg"
											>
												<span class="flex items-center justify-center">
													<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
													</svg>
													Sign In to Subscribe
												</span>
											</button>
										</div>
									{:else}
										<PaystackCheckout
											planId={plan.id}
											paystackPublicKey={PAYSTACK_PUBLIC_KEY}
											disabled={false}
											on:paymentSuccess={handlePaymentSuccess}
											on:paymentCancel={handlePaymentCancel}
										/>
									{/if}
								</div>

								<!-- Features List -->
								<div class="border-t border-gray-200 dark:border-gray-700 pt-8">
									<h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-4 uppercase tracking-wide">
										What's included
									</h4>
									<ul class="space-y-3">
										{#each plan.features.slice(0, 8) as feature}
											<li class="flex items-start">
												<svg class="w-5 h-5 text-purple-600 dark:text-purple-400 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
												</svg>
												<span class="text-sm text-gray-700 dark:text-gray-300">
													{feature}
												</span>
											</li>
										{/each}
										{#if plan.features.length > 8}
											<li class="flex items-start text-sm text-purple-600 dark:text-purple-400 font-medium">
												<svg class="w-5 h-5 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
												</svg>
												And {plan.features.length - 8} more features
											</li>
										{/if}
									</ul>
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</ImpressionTracker>

		<!-- FAQ or Additional Info Section -->
		<div class="mt-20 text-center">
			<div class="max-w-4xl mx-auto bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-3xl shadow-xl p-8 md:p-12 border border-gray-200 dark:border-gray-700">
				<h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
					Need a Custom Solution?
				</h2>
				<p class="text-lg text-gray-600 dark:text-gray-300 mb-8">
					Have unique requirements? Let's discuss a tailored plan that fits your specific needs.
				</p>
				<button
					class="inline-flex items-center px-8 py-4 rounded-xl font-semibold text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/30 hover:bg-purple-200 dark:hover:bg-purple-900/50 border-2 border-purple-200 dark:border-purple-800 transition-all duration-200 hover:scale-105 shadow-lg"
				>
					<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
					</svg>
					Contact Sales
				</button>
			</div>
		</div>

		<!-- Trust Indicators -->
		<div class="mt-16 text-center">
			<div class="flex flex-wrap justify-center items-center gap-8 opacity-60">
				<div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
					<svg class="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
						<path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
					</svg>
					Secure Payments
				</div>
				<div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
					<svg class="w-5 h-5 mr-2 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
						<path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
					</svg>
					Instant Activation
				</div>
				<div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
					<svg class="w-5 h-5 mr-2 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
						<path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
					</svg>
					Cancel Anytime
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	@keyframes blob {
		0% {
			transform: translate(0px, 0px) scale(1);
		}
		33% {
			transform: translate(30px, -50px) scale(1.1);
		}
		66% {
			transform: translate(-20px, 20px) scale(0.9);
		}
		100% {
			transform: translate(0px, 0px) scale(1);
		}
	}

	:global(.animate-blob) {
		animation: blob 7s infinite;
	}

	:global(.animation-delay-2000) {
		animation-delay: 2s;
	}

	:global(.animation-delay-4000) {
		animation-delay: 4s;
	}
</style>
<!-- <script>
	import { goto } from '$app/navigation';
	import { WEBUI_NAME, config } from '$lib/stores';
	import { onMount, getContext } from 'svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	onMount(async () => {
		if ($config) {
			await goto('/');
		}
		loaded = true;
	});
</script> -->

<script>
	import { goto } from '$app/navigation';
	import ImpressionTracker from '$lib/components/ImpressionTracker.svelte';
	import PaystackCheckout from '$lib/components/payment/PaystackCheckout.svelte';
	import { WEBUI_NAME, config, user } from '$lib/stores';
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

	const i18n = getContext('i18n');

	let loaded = false;
	
	// Paystack configuration - Replace with your actual public key
	const PAYSTACK_PUBLIC_KEY = 'pk_test_your_paystack_public_key_here';

	onMount(async () => {
		if ($config) {
			// await goto('/');
		}
		loaded = true;
	});

	/**
	 * Handle successful payment
	 */
	function handlePaymentSuccess(event) {
		const { transaction, plan, planData } = event.detail;
		console.log('Payment successful:', { transaction, plan, planData });
		
		// Here you would typically:
		// 1. Send the transaction details to your backend
		// 2. Update the user's subscription status
		// 3. Redirect to a success page
		
		toast.success($i18n.t('Subscription activated successfully!'));
		
		// Example API call to your backend:
		// updateUserSubscription($user.id, plan, transaction.reference);
		
		// Redirect to dashboard or success page
		// goto('/dashboard');
	}

	/**
	 * Handle payment cancellation
	 */
	function handlePaymentCancel(event) {
		const { plan } = event.detail;
		console.log('Payment cancelled for plan:', plan);
		toast.info($i18n.t('Payment was cancelled. You can try again anytime.'));
	}

let plans = [
  {
    id: 'basic',
    name: 'Basic Plan',
    price: ' $10/mo',
    amount: 10,
    currency: 'USD',
    group_id: '6e475052-cd95-4d8b-8d9e-b0c5b9b3ae98',
    features: [
      // Coverage & content
      'Coverage: Basic statutes + case law',
      'Jurisdiction-ready citations with paragraph anchors',
      'Expanded messaging and uploads',
      'Expanded and faster image creation',
      'Longer memory and context',
      'Limited deep research',

      // Usage & limits
      '10K API Calls / month',
      'Up to 8K context tokens / request',
      '20 requests / minute rate limit',
      'Up to 2GB knowledge index (RAG) storage',
      'Upload: 10MB per file, 2GB total',
      // Capabilities
      'Q&A with inline citations',
      'Basic semantic search over laws & cases',
      'PDF/Word ingestion (OCR optional)',
    //   'Simple chat UI + API (JS/Python SDKs)',
      // Governance & support
    //   'Project roles: Owner, Editor, Viewer',
    //   'Data retention: 14 days (toggleable)',
    //   'Email support (48h SLA)',
      // Analytics
    //   'Basic usage analytics (calls, latency, errors)'
    ]
  },
//   {
//     name: 'Pro',
//     price: '$15/mo',
//     features: [
//       // Coverage & content
//       'Coverage: Statutes + case law + court decisions (trial/appellate/supreme where available)',
//       'Improved precedent mapping & cross-references',
//       // Usage & limits
//       '50K API Calls / month',
//       'Up to 32K context tokens / request',
//       '60 requests / minute rate limit',
//       'Up to 10GB knowledge index (RAG) storage',
//       'Upload: 250MB per file, 10GB total',
//       // Capabilities
//       'Advanced semantic search (filters, facets, date range)',
//       'Batch document analysis & summarization',
//       'Embeddings + RAG API included',
//       'Webhooks for async jobs',
//       'Model routing & fallback (high-availability)',
//       // Governance & support
//       'Audit log (exportable), API keys per project',
//       'Granular RBAC (Org, Project, Key)',
//       'Data retention controls: 30–90 days',
//       'Priority support (24h SLA)',
//       // Analytics
//       'Dashboard: usage by key, endpoint, project',
//       'CSV export & per-key rate limit tuning'
//     ]
//   },
  {
    id: 'enterprise',
    name: 'Enterprise Plan',
    price: '$20/mo',
    amount: 20,
    currency: 'USD',
    group_id: '8ca4c096-2b16-4e19-9586-4a162448fd63',
    features: [
      // Coverage & content
      "Everything in Basic",
      'Coverage: Comprehensive acts, laws, court decisions, gazette notices, and cases',
      'Daily content updates & versioned knowledge base',
      'Citations with source-location deep links',
      // Usage & limits
      'Unlimited API Calls (fair use; custom SLAs)',
      'Up to 200K context tokens / request (long-context endpoints)',
      'Custom per-minute/second rate limits',
      'Scalable knowledge index (100GB+; dedicated vector store)',
      // Capabilities
	  'Expanded messaging and uploads',
      'Expanded and faster image creation',
      'Expanded memory and context',
    //   'Expanded deep research and agent mode',

    //   'Custom connectors (SharePoint, Google Drive, S3)',
    //   'Fine-tuning & domain adapters (by request)',
    //   'On-prem/VPC/hybrid deployment options',
    //   'PII redaction + policy-driven retention',
    //   'Advanced evals & quality gates before deploy',
      // Governance & compliance
    //   'SSO (SAML/OIDC), SCIM user provisioning',
    //   'Granular audit trails & immutable logs',
    //   'DPA & compliance alignment (ISO 27001/GDPR-ready)',
      // Support & reliability
    //   '99.9% uptime SLA, 24/7 incident response',
    //   'Dedicated solutions engineer & quarterly reviews',
      // Analytics
    //   'Organization-wide analytics, cost attribution, and alerts'
    ]
  },
  {
    id: 'enterprise2',
    name: 'Enterprise Plan2',
    price: '$20/mo',
    amount: 20,
    currency: 'USD',
    group_id: '8ca4c096-2b16-4e19-9586-4a162448fd63',
    features: [
      // Coverage & content
      "Everything in Basic",
      'Coverage: Comprehensive acts, laws, court decisions, gazette notices, and cases',
      'Daily content updates & versioned knowledge base',
      'Citations with source-location deep links',
      // Usage & limits
      'Unlimited API Calls (fair use; custom SLAs)',
      'Up to 200K context tokens / request (long-context endpoints)',
      'Custom per-minute/second rate limits',
      'Scalable knowledge index (100GB+; dedicated vector store)',
      // Capabilities
	  'Expanded messaging and uploads',
      'Expanded and faster image creation',
      'Expanded memory and context',
    //   'Expanded deep research and agent mode',

    //   'Custom connectors (SharePoint, Google Drive, S3)',
    //   'Fine-tuning & domain adapters (by request)',
    //   'On-prem/VPC/hybrid deployment options',
    //   'PII redaction + policy-driven retention',
    //   'Advanced evals & quality gates before deploy',
      // Governance & compliance
    //   'SSO (SAML/OIDC), SCIM user provisioning',
    //   'Granular audit trails & immutable logs',
    //   'DPA & compliance alignment (ISO 27001/GDPR-ready)',
      // Support & reliability
    //   '99.9% uptime SLA, 24/7 incident response',
    //   'Dedicated solutions engineer & quarterly reviews',
      // Analytics
    //   'Organization-wide analytics, cost attribution, and alerts'
    ]
  },
  {
    id: 'enterprise3',
    name: 'Enterprise Plan3',
    price: '$20/mo',
    amount: 20,
    currency: 'USD',
    group_id: '8ca4c096-2b16-4e19-9586-4a162448fd63',
    features: [
      // Coverage & content
      "Everything in Basic",
      'Coverage: Comprehensive acts, laws, court decisions, gazette notices, and cases',
      'Daily content updates & versioned knowledge base',
      'Citations with source-location deep links',
      // Usage & limits
      'Unlimited API Calls (fair use; custom SLAs)',
      'Up to 200K context tokens / request (long-context endpoints)',
      'Custom per-minute/second rate limits',
      'Scalable knowledge index (100GB+; dedicated vector store)',
      // Capabilities
	  'Expanded messaging and uploads',
      'Expanded and faster image creation',
      'Expanded memory and context',
    //   'Expanded deep research and agent mode',

    //   'Custom connectors (SharePoint, Google Drive, S3)',
    //   'Fine-tuning & domain adapters (by request)',
    //   'On-prem/VPC/hybrid deployment options',
    //   'PII redaction + policy-driven retention',
    //   'Advanced evals & quality gates before deploy',
      // Governance & compliance
    //   'SSO (SAML/OIDC), SCIM user provisioning',
    //   'Granular audit trails & immutable logs',
    //   'DPA & compliance alignment (ISO 27001/GDPR-ready)',
      // Support & reliability
    //   '99.9% uptime SLA, 24/7 incident response',
    //   'Dedicated solutions engineer & quarterly reviews',
      // Analytics
    //   'Organization-wide analytics, cost attribution, and alerts'
    ]
  }

];


</script>

<div class="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100  min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
	<div class="my-1 flex flex-col items-center justify-center md:mb-0 md:mt-0">
		<div class="text-2xl font-semibold md:text-3xl">Upgrade your plan</div>
	</div>

	<div class="flex-grow overflow-y-scroll">
		<ImpressionTracker sectionId="subscription-section">
			<div class="mt-8 grid gap-6 md:grid-cols-3">
				{#each plans as plan}
					<div class="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 p-6 rounded-lg shadow-md w-100">
						<h2 class="text-xl font-semibold mb-4">{plan.name} <strong>{plan.price}</strong></h2>
						
						<!-- Paystack Checkout Component -->
						<PaystackCheckout
							planId={plan.id}
							paystackPublicKey={PAYSTACK_PUBLIC_KEY}
							disabled={!$user}
							on:paymentSuccess={handlePaymentSuccess}
							on:paymentCancel={handlePaymentCancel}
						/>
						
						{#if !$user}
							<p class="text-sm text-gray-500 dark:text-gray-400 text-center mb-3">
								{$i18n.t('Please log in to subscribe')}
							</p>
						{/if}
						
						<ul class="mb-6">
							{#each plan.features as feature}
								<li class="mb-2">
									<div class="text-l flex cursor-default justify-start gap-3.5">
										<svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" color="primary"><path d="M16.335 10C16.335 9.96334 16.3033 9.90797 16.2314 9.89746C14.3872 9.6308 12.9635 9.10033 11.9385 8.08105C10.9772 7.1251 10.4472 5.81895 10.1621 4.14453L10.1084 3.80469C10.0948 3.71183 10.0216 3.66505 9.96484 3.66504C9.92381 3.66504 9.87863 3.68787 9.85156 3.73047L9.83203 3.7793C9.40877 5.60247 8.88454 7.02131 7.92871 8.04297C7.01515 9.0193 5.78211 9.55662 4.11035 9.84277L3.77051 9.89648C3.69699 9.90725 3.66504 9.96384 3.66504 10C3.66504 10.0362 3.69699 10.0927 3.77051 10.1035L4.11035 10.1572C5.78211 10.4434 7.01515 10.9807 7.92871 11.957C8.88454 12.9787 9.40877 14.3975 9.83203 16.2207C9.8491 16.2942 9.91023 16.335 9.96484 16.335C10.0216 16.335 10.0948 16.2882 10.1084 16.1953C10.3785 14.3567 10.9131 12.9386 11.9385 11.9189C12.9635 10.8997 14.3872 10.3692 16.2314 10.1025L16.2773 10.0879C16.317 10.0662 16.335 10.0277 16.335 10ZM17.665 10C17.665 10.6877 17.1785 11.2454 16.5488 11.3945L16.4219 11.4189C14.7098 11.6665 13.6129 12.1305 12.877 12.8623C12.1414 13.5938 11.6742 14.6843 11.4238 16.3887C11.3197 17.0973 10.7182 17.665 9.96484 17.665C9.27085 17.665 8.68836 17.1772 8.53613 16.5215C8.12392 14.7459 7.6623 13.619 6.95703 12.8652C6.31314 12.1772 5.39414 11.7268 3.88672 11.4688L3.57715 11.4199C2.88869 11.319 2.33496 10.734 2.33496 10C2.33496 9.26603 2.88869 8.681 3.57715 8.58008L3.88672 8.53125C5.39414 8.27321 6.31314 7.82277 6.95703 7.13477C7.6623 6.38104 8.12392 5.25413 8.53613 3.47852L8.56934 3.35742C8.76133 2.76356 9.31424 2.33496 9.96484 2.33496C10.7182 2.33497 11.3197 2.9027 11.4238 3.61133L11.5283 4.22266C11.7954 5.58295 12.2334 6.49773 12.877 7.1377C13.6129 7.86952 14.7098 8.33351 16.4219 8.58105C17.1119 8.68101 17.665 9.26667 17.665 10Z"></path></svg>

										<div class="flex flex-1 items-start gap-2">
											<span class="min-w-0 font-normal text-token-text-primary">{feature}</span>
										</div>
									</div>
								</li>
							{/each}
						</ul>
					</div>
				{/each}
			</div>
		</ImpressionTracker>
		
	</div>
</div>

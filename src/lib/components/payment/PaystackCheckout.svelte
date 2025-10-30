<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { user } from '$lib/stores';
	import {
		createPaystackPayment,
		SUBSCRIPTION_PLANS,
		getUserEmail,
		formatPrice,
		type PaymentData
	} from '$lib/utils/paystack';
	import { initializePayment } from '$lib/apis/payments';

	const dispatch = createEventDispatcher();
	const i18n = getContext('i18n');

	export let planId: 'basic' | 'enterprise';
	export let paystackPublicKey: string = 'pk_test_your_public_key_here'; // Replace with your actual public key
	export let disabled: boolean = false;

	let loading = false;
	let paymentInProgress = false;

	$: plan = SUBSCRIPTION_PLANS[planId];
	$: userEmail = getUserEmail();

	/**
	 * Initialize Paystack payment using our backend
	 */
	async function handlePaystackCheckout() {
		if (!userEmail) {
			toast.error($i18n.t('Please log in to continue with payment'));
			return;
		}

		if (!plan) {
			toast.error($i18n.t('Invalid subscription plan'));
			return;
		}

		if (!localStorage.token) {
			toast.error($i18n.t('Authentication required'));
			return;
		}

		loading = true;
		paymentInProgress = true;

		try {
			// Initialize payment with backend
			const paymentData = {
				amount: plan.amount,
				currency: plan.currency,
				group_id: plan.group_id,
				plan_id: planId,
				plan_name: plan.name,
				callback_url: `${window.location.origin}/subscription/verify`
			};

			const response = await initializePayment(localStorage.token, paymentData);

			if (response.success && response.data?.authorization_url) {
				// Redirect to Paystack checkout
				window.location.href = response.data.authorization_url;
			} else {
				throw new Error(response.message || 'Failed to initialize payment');
			}
		} catch (error) {
			console.error('Payment initialization failed:', error);
			toast.error($i18n.t('Failed to initialize payment. Please try again.'));
			loading = false;
			paymentInProgress = false;
		}
	}

	/**
	 * Handle Paystack popup payment (alternative method)
	 */
	async function handlePopupCheckout() {
		if (!userEmail) {
			toast.error($i18n.t('Please log in to continue with payment'));
			return;
		}

		if (!plan) {
			toast.error($i18n.t('Invalid subscription plan'));
			return;
		}

		loading = true;
		paymentInProgress = true;

		try {
			const paystack = createPaystackPayment(paystackPublicKey, {
				currency: plan.currency,
				environment: 'test' // Change to 'live' for production
			});

			const paymentData: Omit<PaymentData, 'reference'> = {
				amount: plan.amount,
				email: userEmail,
				currency: plan.currency,
				plan: plan.plan_code,
				group_id: plan.group_id,
				metadata: {
					plan_id: planId,
					plan_name: plan.name,
					user_id: $user?.id,
					interval: plan.interval
				},
				channels: ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']
			};

			await paystack.initializePayment(
				paymentData,
				handlePaymentSuccess,
				handlePaymentCancel
			);
		} catch (error) {
			console.error('Payment initialization failed:', error);
			toast.error($i18n.t('Failed to initialize payment. Please try again.'));
			loading = false;
			paymentInProgress = false;
		}
	}

	/**
	 * Handle successful payment
	 */
	function handlePaymentSuccess(transaction: any) {
		loading = false;
		paymentInProgress = false;

		toast.success($i18n.t('Payment successful! Your subscription is now active.'));
		
		// Dispatch event to parent component
		dispatch('paymentSuccess', {
			transaction,
			plan: planId,
			planData: plan
		});

		// You might want to redirect to a success page or update user's subscription status
		// Example: goto('/subscription/success');
	}

	/**
	 * Handle payment cancellation
	 */
	function handlePaymentCancel() {
		loading = false;
		paymentInProgress = false;
		toast.info($i18n.t('Payment cancelled'));
		
		dispatch('paymentCancel', {
			plan: planId
		});
	}
</script>

<!-- Payment button -->
<button
	class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition mt-5 mb-5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
	{disabled}
	on:click={handlePaystackCheckout}
>
	{#if loading || paymentInProgress}
		<svg
			class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
		>
			<circle
				class="opacity-25"
				cx="12"
				cy="12"
				r="10"
				stroke="currentColor"
				stroke-width="4"
			></circle>
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
			></path>
		</svg>
		{paymentInProgress ? $i18n.t('Processing Payment...') : $i18n.t('Loading...')}
	{:else}
		<svg
			class="w-4 h-4 mr-2"
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
			xmlns="http://www.w3.org/2000/svg"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
			></path>
		</svg>
		{#if disabled}
			{$i18n.t('Already Subscribed to')}
		{:else}
			{$i18n.t('Subscribe to')} {plan.name}
		{/if}
	{/if}
</button>


<!-- Alternative: Redirect checkout button -->
<!-- 
<button
	class="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 transition mt-2"
	disabled={loading || disabled}
	on:click={handleRedirectCheckout}
>
	{#if loading}
		<span class="flex items-center justify-center">
			<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
			{$i18n.t('Redirecting...')}
		</span>
	{:else}
		{$i18n.t('Pay with Paystack')}
	{/if}
</button>
-->

<style>
	/* Add custom styles if needed */
</style>
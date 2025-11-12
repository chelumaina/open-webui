<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { toast } from 'svelte-sonner';
	import { user } from '$lib/stores';
	import { verifyPayment } from '$lib/apis/payments';

	const i18n = getContext('i18n');

	let loading = true;
	let verificationStatus: 'verifying' | 'success' | 'failed' | 'cancelled' = 'verifying';
	let transactionData: any = null;
	let errorMessage = '';

	onMount(async () => {
		await verifyPaymentTransaction();
	});

	async function verifyPaymentTransaction() {
		const urlParams = new URLSearchParams(window.location.search);
		const reference = urlParams.get('reference');
		const trxref = urlParams.get('trxref');
		
		// Paystack redirects with either 'reference' or 'trxref'
		const transactionReference = reference || trxref;

		if (!transactionReference) {
			verificationStatus = 'failed';
			errorMessage = $i18n.t('No transaction reference found');
			loading = false;
			return;
		}

		if (!localStorage.token) {
			verificationStatus = 'failed';
			errorMessage = $i18n.t('Authentication required');
			loading = false;
			return;
		}

		try {
			// Verify payment with our backend
			const verification = await verifyPayment(localStorage.token, transactionReference);

			if (verification.success && verification.data?.status === 'success') {
				verificationStatus = 'success';
				transactionData = verification.data;
				
				await handleSuccessfulPayment(verification.data);
				
				toast.success($i18n.t('Payment verified successfully!'));
			} else {
				verificationStatus = 'failed';
				errorMessage = verification.data?.gateway_response || verification.message || $i18n.t('Payment verification failed');
				toast.error($i18n.t('Payment verification failed'));
			}
		} catch (error) {
			console.error('Payment verification error:', error);
			verificationStatus = 'failed';
			errorMessage = typeof error === 'string' ? error : $i18n.t('An error occurred while verifying your payment');
			toast.error($i18n.t('Payment verification failed'));
		} finally {
			loading = false;
		}
	}

	async function handleSuccessfulPayment(data: any) {
		// Extract plan information from metadata
		const planId = data.metadata?.plan_id;
		const planName = data.metadata?.plan_name;
		
		console.log('Successful payment data:', {
			reference: data.reference,
			amount: data.amount / 100, // Convert from kobo
			currency: data.currency,
			plan: planId,
			customer: data.customer
		});

		// Here you would call your backend API to:
		// 1. Activate the user's subscription
		// 2. Store transaction record
		// 3. Update user permissions
		
		// Example API call:
		/*
		try {
			const response = await fetch('/api/subscriptions/activate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${$user?.token}`
				},
				body: JSON.stringify({
					transaction_reference: data.reference,
					plan_id: planId,
					amount: data.amount,
					currency: data.currency,
					paystack_data: data
				})
			});

			if (!response.ok) {
				throw new Error('Failed to activate subscription');
			}

			const result = await response.json();
			console.log('Subscription activated:', result);
		} catch (error) {
			console.error('Failed to activate subscription:', error);
			toast.error($i18n.t('Payment successful but failed to activate subscription. Please contact support.'));
		}
		*/
	}

	function goToDashboard() {
		goto('/');
	}

	function retryPayment() {
		goto('/subscription');
	}
</script>

<svelte:head>
	<title>Payment Verification - {$i18n.t('Lex Luma AI')}</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
	<div class="sm:mx-auto sm:w-full sm:max-w-md">
		<div class="bg-white dark:bg-gray-800 py-8 px-4 shadow sm:rounded-lg sm:px-10">
			{#if loading}
				<!-- Loading State -->
				<div class="text-center">
					<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
					<h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
						{$i18n.t('Verifying Payment')}
					</h2>
					<p class="text-gray-600 dark:text-gray-400">
						{$i18n.t('Please wait while we verify your payment...')}
					</p>
				</div>
			{:else if verificationStatus === 'success'}
				<!-- Success State -->
				<div class="text-center">
					<div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 dark:bg-green-800 mb-4">
						<svg class="h-6 w-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
						</svg>
					</div>
					<h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
						{$i18n.t('Payment Successful!')}
					</h2>
					<p class="text-gray-600 dark:text-gray-400 mb-6">
						{$i18n.t('Your subscription has been activated successfully.')}
					</p>
					
					{#if transactionData}
						<div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6 text-left">
							<h3 class="text-sm font-medium text-gray-900 dark:text-white mb-2">
								{$i18n.t('Transaction Details')}
							</h3>
							<dl class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
								<div class="flex justify-between">
									<dt>{$i18n.t('Reference')}:</dt>
									<dd class="font-mono">{transactionData.reference}</dd>
								</div>
								<div class="flex justify-between">
									<dt>{$i18n.t('Amount')}:</dt>
									<dd>{transactionData.currency} {(transactionData.amount / 100).toFixed(2)}</dd>
								</div>
								{#if transactionData.metadata?.plan_name}
									<div class="flex justify-between">
										<dt>{$i18n.t('Plan')}:</dt>
										<dd>{transactionData.metadata.plan_name}</dd>
									</div>
								{/if}
							</dl>
						</div>
					{/if}
					
					<button
						on:click={goToDashboard}
						class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
					>
						{$i18n.t('Go to Dashboard')}
					</button>
				</div>
			{:else if verificationStatus === 'failed'}
				<!-- Failed State -->
				<div class="text-center">
					<div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 dark:bg-red-800 mb-4">
						<svg class="h-6 w-6 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
						</svg>
					</div>
					<h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
						{$i18n.t('Payment Verification Failed')}
					</h2>
					<p class="text-gray-600 dark:text-gray-400 mb-2">
						{$i18n.t('We were unable to verify your payment.')}
					</p>
					
					{#if errorMessage}
						<p class="text-red-600 dark:text-red-400 text-sm mb-6">
							{errorMessage}
						</p>
					{/if}
					
					<div class="space-y-3">
						<button
							on:click={retryPayment}
							class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
						>
							{$i18n.t('Try Again')}
						</button>
						
						<button
							on:click={goToDashboard}
							class="w-full flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
						>
							{$i18n.t('Go Back')}
						</button>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	/* Add any custom styles if needed */
</style>
<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { getUserSubscription, getUserTransactions } from '$lib/apis/payments';
	import type { UserSubscription, PaymentTransaction } from '$lib/apis/payments';

	const i18n = getContext('i18n');

	let loading = true;
	let subscription: UserSubscription | null = null;
	let transactions: PaymentTransaction[] = [];
	let showTransactions = false;

	onMount(async () => {
		await loadSubscriptionData();
	});

	async function loadSubscriptionData() {
		if (!localStorage.token) {
			toast.error($i18n.t('Authentication required'));
			loading = false;
			return;
		}

		try {
			// Load subscription
			const subResponse = await getUserSubscription(localStorage.token);
			subscription = subResponse.subscription;

			// Load transactions
			const txResponse = await getUserTransactions(localStorage.token, 10, 0);
			transactions = txResponse.transactions;
		} catch (error) {
			console.error('Failed to load subscription data:', error);
			toast.error($i18n.t('Failed to load subscription data'));
		} finally {
			loading = false;
		}
	}

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString();
	}

	function formatAmount(amount: number, currency: string): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: currency
		}).format(amount);
	}

	function getStatusColor(status: string): string {
		switch (status) {
			case 'active':
			case 'success':
				return 'text-green-600 dark:text-green-400';
			case 'pending':
				return 'text-yellow-600 dark:text-yellow-400';
			case 'failed':
			case 'cancelled':
			case 'expired':
				return 'text-red-600 dark:text-red-400';
			default:
				return 'text-gray-600 dark:text-gray-400';
		}
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<h2 class="text-xl font-semibold text-gray-900 dark:text-white">
			{$i18n.t('Subscription Management')}
		</h2>
	</div>

	{#if loading}
		<div class="animate-pulse space-y-4">
			<div class="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
			<div class="h-24 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
		</div>
	{:else}
		<!-- Current Subscription -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
			<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
				{$i18n.t('Current Subscription')}
			</h3>

			{#if subscription}
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div>
						<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
							{$i18n.t('Plan')}
						</label>
						<p class="mt-1 text-sm text-gray-900 dark:text-white">
							{subscription.plan_name}
						</p>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
							{$i18n.t('Status')}
						</label>
						<p class="mt-1 text-sm {getStatusColor(subscription.status)} font-medium">
							{subscription.status.charAt(0).toUpperCase() + subscription.status.slice(1)}
						</p>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
							{$i18n.t('Amount')}
						</label>
						<p class="mt-1 text-sm text-gray-900 dark:text-white">
							{formatAmount(subscription.amount, subscription.currency)}
						</p>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
							{$i18n.t('Billing Cycle')}
						</label>
						<p class="mt-1 text-sm text-gray-900 dark:text-white">
							{subscription.billing_cycle.charAt(0).toUpperCase() + subscription.billing_cycle.slice(1)}
						</p>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
							{$i18n.t('Started')}
						</label>
						<p class="mt-1 text-sm text-gray-900 dark:text-white">
							{formatDate(subscription.started_at)}
						</p>
					</div>

					{#if subscription.expires_at}
						<div>
							<label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
								{$i18n.t('Expires')}
							</label>
							<p class="mt-1 text-sm text-gray-900 dark:text-white">
								{formatDate(subscription.expires_at)}
							</p>
						</div>
					{/if}
				</div>
			{:else}
				<div class="text-center py-6">
					<div class="text-gray-400 dark:text-gray-500 mb-2">
						<svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
						</svg>
					</div>
					<p class="text-gray-500 dark:text-gray-400">
						{$i18n.t('No active subscription found')}
					</p>
					<a
						href="/subscription"
						class="inline-flex items-center px-4 py-2 mt-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
					>
						{$i18n.t('View Plans')}
					</a>
				</div>
			{/if}
		</div>

		<!-- Transaction History -->
		<div class="bg-white dark:bg-gray-800 rounded-lg shadow">
			<div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
				<h3 class="text-lg font-medium text-gray-900 dark:text-white">
					{$i18n.t('Transaction History')}
				</h3>
				<button
					on:click={() => showTransactions = !showTransactions}
					class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 text-sm font-medium"
				>
					{showTransactions ? $i18n.t('Hide') : $i18n.t('Show')}
				</button>
			</div>

			{#if showTransactions}
				<div class="p-6">
					{#if transactions.length > 0}
						<div class="overflow-x-auto">
							<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
								<thead class="bg-gray-50 dark:bg-gray-700">
									<tr>
										<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
											{$i18n.t('Reference')}
										</th>
										<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
											{$i18n.t('Plan')}
										</th>
										<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
											{$i18n.t('Amount')}
										</th>
										<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
											{$i18n.t('Status')}
										</th>
										<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
											{$i18n.t('Date')}
										</th>
									</tr>
								</thead>
								<tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
									{#each transactions as transaction}
										<tr>
											<td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900 dark:text-white">
												{transaction.reference}
											</td>
											<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
												{transaction.plan_name}
											</td>
											<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
												{formatAmount(transaction.amount, transaction.currency)}
											</td>
											<td class="px-6 py-4 whitespace-nowrap">
												<span class="text-sm {getStatusColor(transaction.status)} font-medium">
													{transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
												</span>
											</td>
											<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
												{formatDate(transaction.created_at)}
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					{:else}
						<div class="text-center py-6">
							<div class="text-gray-400 dark:text-gray-500 mb-2">
								<svg class="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
								</svg>
							</div>
							<p class="text-gray-500 dark:text-gray-400">
								{$i18n.t('No transactions found')}
							</p>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	/* Add any custom styles if needed */
</style>
<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { userResetPassword } from '$lib/apis/auths';
	import { WEBUI_BASE_FRONTEND_URL } from '$lib/constants';
	import { WEBUI_NAME } from '$lib/stores';
	import SensitiveInput from '$lib/components/common/SensitiveInput.svelte';

	const i18n = getContext('i18n');

	let token = '';
	let newPassword = '';
	let confirmPassword = '';
	let loading = false;
	let tokenValid = false;

	onMount(() => {
		// Get token from URL query parameter
		token = $page.url.searchParams.get('token') || '';
		
		if (!token) {
			toast.error($i18n.t('Invalid reset link'));
			goto('/auth');
		} else {
			tokenValid = true;
		}
	});

	const resetPasswordHandler = async () => {
		if (!newPassword || !confirmPassword) {
			toast.error($i18n.t('Please fill in all fields'));
			return;
		}

		if (newPassword !== confirmPassword) {
			toast.error($i18n.t('Passwords do not match'));
			return;
		}

		if (newPassword.length < 8) {
			toast.error($i18n.t('Password must be at least 8 characters long'));
			return;
		}

		loading = true;

		try {
			const response = await userResetPassword(token, newPassword);
			
			if (response && response.success) {
				toast.success($i18n.t('Password reset successful! Please sign in with your new password.'));
				// Redirect to signin page after 2 seconds
				setTimeout(() => {
					goto('/auth');
				}, 2000);
			} else {
				toast.error($i18n.t('Failed to reset password. Please try again.'));
			}
		} catch (error) {
			toast.error(`${error}`);
		} finally {
			loading = false;
		}
	};
</script>

<svelte:head>
	<title>
		{$i18n.t('Reset Password')} - {`${$WEBUI_NAME}`}
	</title>
</svelte:head>

<div class="w-full max-h-screen overflow-y-auto h-screen text-white relative" id="reset-password-page">
	<div class="w-full h-full absolute top-0 left-0 bg-white dark:bg-black"></div>

	<div class="w-full absolute top-0 left-0 right-0 h-8 drag-region"></div>

	{#if tokenValid}
		<div
			class="fixed bg-transparent min-h-screen max-h-screen overflow-y-auto w-full flex justify-center font-primary z-50 text-black dark:text-white"
		>
			<div class="w-full px-10 min-h-screen flex flex-col text-center py-4">
				<div class="my-auto flex flex-col justify-center items-center">
					<div class="sm:max-w-md my-auto pb-10 w-full dark:text-gray-100">
						<div class="flex justify-center mb-6">
							<img
								id="logo"
								crossorigin="anonymous"
								src="{WEBUI_BASE_FRONTEND_URL}/static/favicon.png"
								class="size-48 rounded-full"
								alt="logo"
							/>
						</div>

						<form
							class="flex flex-col justify-center"
							on:submit={(e) => {
								e.preventDefault();
								resetPasswordHandler();
							}}
						>
							<div class="mb-1">
								<div class="text-2xl font-medium">
									{$i18n.t('Reset Your Password')}
								</div>
								<div class="mt-2 text-sm text-gray-600 dark:text-gray-400">
									{$i18n.t('Enter your new password below')}
								</div>
							</div>

							<div class="flex flex-col mt-4">
								<div class="mb-3">
									<label for="new-password" class="text-sm font-medium text-left mb-2 block">
										{$i18n.t('New Password')}
									</label>
									<SensitiveInput
										bind:value={newPassword}
										type="password"
										id="new-password"
										class="w-full px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
										placeholder={$i18n.t('Enter your new password')}
										autocomplete="new-password"
										required
										disabled={loading}
									/>
								</div>

								<div class="mb-3">
									<label for="confirm-password" class="text-sm font-medium text-left mb-2 block">
										{$i18n.t('Confirm Password')}
									</label>
									<SensitiveInput
										bind:value={confirmPassword}
										type="password"
										id="confirm-password"
										class="w-full px-4 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
										placeholder={$i18n.t('Confirm your new password')}
										autocomplete="new-password"
										required
										disabled={loading}
									/>
								</div>
							</div>

							<div class="mt-5">
								<button
									class="w-full px-4 py-3 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 border border-blue-600 hover:border-blue-700 rounded-lg shadow-sm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
									type="submit"
									disabled={loading}
								>
									{loading ? $i18n.t('Resetting...') : $i18n.t('Reset Password')}
								</button>
							</div>

							<div class="mt-4 text-sm text-center">
								<button
									class="font-medium underline text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
									type="button"
									on:click={() => goto('/auth')}
									disabled={loading}
								>
									{$i18n.t('Back to Sign in')}
								</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>

		<div class="fixed m-10 z-50">
			<div class="flex space-x-2">
				<div class="self-center">
					<img
						id="logo"
						crossorigin="anonymous"
						src="{WEBUI_BASE_FRONTEND_URL}/static/favicon.png"
						class="w-6 rounded-full"
						alt="logo"
					/>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	:global(#reset-password-page) {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	}
</style>

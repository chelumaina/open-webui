<script lang="ts">
	import DOMPurify from 'dompurify';
	import { marked } from 'marked';

	import { toast } from 'svelte-sonner';

	import { onMount, getContext, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { getBackendConfig } from '$lib/apis';
	import { ldapUserSignIn, getSessionUser, userSignIn, userSignUp } from '$lib/apis/auths';

	import { WEBUI_API_BASE_URL, WEBUI_BASE_URL } from '$lib/constants';
	import { WEBUI_NAME, config, user, socket } from '$lib/stores';
	import SEOHead from '$lib/components/seo/SEOHead.svelte';

	import { generateInitialsImage, canvasPixelTest } from '$lib/utils';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import LandingComponent from '$lib/components/common/LandingComponent.svelte';
	import OnBoarding from '$lib/components/OnBoarding.svelte';
	import SensitiveInput from '$lib/components/common/SensitiveInput.svelte';
	import { redirect } from '@sveltejs/kit';


	import Marquee from '$lib/components/common/Marquee.svelte';
	// import SlideShow from '$lib/common/SlideShow.svelte';
	// import ArrowRightCircle from '$lib/icons/ArrowRightCircle.svelte';

	const i18n = getContext('i18n');

	let loaded = false;
	let isVisible = false;
	let mode = $config?.features.enable_ldap ? 'ldap' : 'signin';

	let form = null;

	let name = '';
	let email = '';
	let password = '';
	let confirmPassword = '';

	let ldapUsername = '';

	const setSessionUser = async (sessionUser, redirectPath: string | null = null) => {
		if (sessionUser) {
			console.log(sessionUser);
			toast.success($i18n.t(`You're now logged in.`));
			if (sessionUser.token) {
				localStorage.token = sessionUser.token;
			}
			$socket.emit('user-join', { auth: { token: sessionUser.token } });
			await user.set(sessionUser);
			await config.set(await getBackendConfig());

			if (!redirectPath) {
				redirectPath = $page.url.searchParams.get('redirect') || '/';
			}

			goto(redirectPath);
			localStorage.removeItem('redirectPath');
		}
	};

	const signInHandler = async () => {
		const sessionUser = await userSignIn(email, password).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		await setSessionUser(sessionUser);
	};

	let getStartedHandler=() => {
		onboarding = false;
		mode = $config?.features.enable_ldap ? 'ldap' : 'signup';
	};

	const signUpHandler = async () => {
		if ($config?.features?.enable_signup_password_confirmation) {
			if (password !== confirmPassword) {
				toast.error($i18n.t('Passwords do not match.'));
				return;
			}
		}

		const sessionUser = await userSignUp(name, email, password, generateInitialsImage(name)).catch(
			(error) => {
				toast.error(`${error}`);
				return null;
			}
		);

		await setSessionUser(sessionUser);
	};

	const ldapSignInHandler = async () => {
		const sessionUser = await ldapUserSignIn(ldapUsername, password).catch((error) => {
			toast.error(`${error}`);
			return null;
		});
		await setSessionUser(sessionUser);
	};

	const submitHandler = async () => {
		if (mode === 'ldap') {
			await ldapSignInHandler();
		} else if (mode === 'signin') {
			await signInHandler();
		} else {
			await signUpHandler();
		}
	};

	const oauthCallbackHandler = async () => {
		// Get the value of the 'token' cookie
		function getCookie(name) {
			const match = document.cookie.match(
				new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)')
			);
			return match ? decodeURIComponent(match[1]) : null;
		}

		const token = getCookie('token');
		if (!token) {
			return;
		}

		const sessionUser = await getSessionUser(token).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		if (!sessionUser) {
			return;
		}

		localStorage.token = token;
		await setSessionUser(sessionUser, localStorage.getItem('redirectPath') || null);
	};

	let onboarding = false;

	async function setLogoImage() {
		await tick();
		const logo = document.getElementById('logo');

		if (logo) {
			const isDarkMode = document.documentElement.classList.contains('dark');

			if (isDarkMode) {
				const darkImage = new Image();
				darkImage.src = `${WEBUI_BASE_URL}/static/favicon-dark.png`;

				darkImage.onload = () => {
					logo.src = `${WEBUI_BASE_URL}/static/favicon-dark.png`;
					logo.style.filter = ''; // Ensure no inversion is applied if favicon-dark.png exists
				};

				darkImage.onerror = () => {
					logo.style.filter = 'invert(1)'; // Invert image if favicon-dark.png is missing
				};
			}
		}
	}

	onMount(async () => {
		isVisible = true;
		const redirectPath = $page.url.searchParams.get('redirect');
		if ($user !== undefined) {
			goto(redirectPath || '/');
		} else {
			if (redirectPath) {
				localStorage.setItem('redirectPath', redirectPath);
			}
		}

		const error = $page.url.searchParams.get('error');
		if (error) {
			toast.error(error);
		}

		await oauthCallbackHandler();
		form = $page.url.searchParams.get('form');

		loaded = true;
		setLogoImage();

		if (($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false) {
			await signInHandler();
		} else {
			onboarding = $config?.onboarding ?? false;
		}
	});
</script>


<SEOHead
  title="Unlock mysteries with AI Legal Research Assistant - {$i18n.t('Lex Luma AI')}"
  description="Unlock mysteries with AI Legal Research Assistant for Lex Luma AI ."
  image="/static/static/apple-touch-icon.png"
  noindex={false}
  structuredData={{
    "@context": "https://schema.org",
    "@type": "Page",
    "headline": "Unlock mysteries with AI Legal Research AssistantAI-powered instant Chat with Gazette Notices, Laws/Legislations & Court. Empower your legal research and decision-making with our AI-driven chat platform. An AI legal research copilot that understands your jurisdiction",
    "description": "Page to allow user to verify their sign up credentials",
    "author": {
      "@type": "Organization",
      "name": "Lex Luma"
    }
  }}
/>
<!-- <svelte:head>
	<title>
		{`${$WEBUI_NAME}`}
	</title>
</svelte:head> -->

<!-- <OnBoarding
	bind:show={onboarding}
	getStartedHandler={() => {
		onboarding = false;
		mode = $config?.features.enable_ldap ? 'ldap' : 'signup';
	}}
/> -->

<div class="w-full max-h-[100dvh] text-white relative overflow-x-hidden" id="auth-page">
	<!-- Animated background gradient -->
	<div class="relative inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-indigo-950 dark:to-purple-950 opacity-70"></div>
	
	{#if loaded}
		<div class="grid lg:grid-cols-3 grid-cols-1 gap-1 h-full relative z-10 overflow-x-hidden">
			<div class="lg:col-span-2 hidden lg:block">
					<!-- Hero Section -->
					<section class="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-800 dark:via-purple-800 dark:to-pink-800">
						<!-- Animated background elements -->
						<div class="absolute inset-0 opacity-20">
							<div class="absolute top-20 left-10 w-72 h-72 bg-white rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
							<div class="absolute top-40 right-10 w-72 h-72 bg-yellow-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-1000"></div>
							<div class="absolute -bottom-8 left-40 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-2000"></div>
						</div>
						
						<div class="relative container mx-auto px-4 py-24 md:py-34 text-center overflow-x-hidden">
							
							
							<div class="transition-all duration-1000 transform {isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}">
								<h1 class="text-4xl sm:text-5xl md:text-7xl font-extrabold mb-6 text-white leading-tight break-words">
									Intelligent Chat.<br/>
									<span class="bg-clip-text text-transparent bg-gradient-to-r from-yellow-200 to-pink-200">
										for Everyone
									</span>
								</h1>

								<Marquee
									duration={5000}
									words={[
										$i18n.t('Explore the cosmos of AI in Legal Research'),
										$i18n.t('Unlock mysteries with AI Legal Research Assistant'),
										$i18n.t('Chat with thousands of legal documents using AI'),
										$i18n.t('Dive into knowledge full of AI into the gazette notices, laws & court decisions'),
										$i18n.t('Discover wonders with AI document chatbot'),
										$i18n.t('Ignite curiosity and creativity with AI'),
										$i18n.t('Forge new paths with AI backed insights'),
										$i18n.t('Unravel secrets using Legal research with AI'),
										$i18n.t('Pioneer insights with AI technology in the field of Legal Research'),
										$i18n.t('Embark on adventures with AI Regulatory Assisted Generation'),
									]}
								/>

								<div class="flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
								
									<a href="/auth" class="group relative bg-white text-indigo-600 px-6 sm:px-10 py-4 rounded-xl font-bold text-base sm:text-lg hover:bg-gray-50 transition-all duration-300 shadow-2xl hover:shadow-xl hover:scale-105 transform">
										<span class="relative z-10">Get Started Free</span>
										<div class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl opacity-0 group-hover:opacity-10 transition-opacity"></div>
									</a>
									<a href="#features" class="group bg-white/10 backdrop-blur-sm border-2 border-white/30 text-white px-6 sm:px-10 py-4 rounded-xl font-bold text-base sm:text-lg hover:bg-white/20 transition-all duration-300 hover:scale-105 transform">
										Learn More
										<span class="inline-block ml-2 transform group-hover:translate-x-1 transition-transform">→</span>
									</a>
								</div>

								<p class="text-xl md:text-2xl mb-10 mt-10 max-w-3xl mx-auto text-gray-100 font-light break-words px-4">
									AI-powered instant Chat with Gazette Notices, Laws/Legislations & Court.
								</p>
								<p class="text-lg md:text-xl mb-10 max-w-3xl mx-auto text-gray-100 font-light break-words px-4">
									Empower your legal research and decision-making with our AI-driven chat platform. An AI legal research copilot that understands your jurisdiction. Ask in plain language, get grounded answers with paragraph-level citations to Gazette Notices, Acts (and subsidiary legislation), and authoritative case law—powered by secure RAG and optional firm-specific fine-tuning.
								</p>
							</div>
						</div>
						
						<!-- Wave separator -->
						<div class="absolute bottom-0 left-0 right-0">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" class="w-full h-auto">
								<path fill="currentColor" class="text-gray-50 dark:text-gray-900" d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,58.7C960,64,1056,64,1152,58.7C1248,53,1344,43,1392,37.3L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"></path>
							</svg>
						</div>
					</section>
				
			</div>
			<div class="lg:col-span-1 relative min-h-screen w-full font-primary z-50 backdrop-blur-sm" id="auth-container">
				<!-- Decorative elements -->
				<div class="absolute top-0 right-0 w-72 h-72 bg-purple-300 dark:bg-purple-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-20 animate-blob"></div>
				<div class="absolute top-0 left-0 w-72 h-72 bg-blue-300 dark:bg-blue-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
				<div class="absolute bottom-0 left-1/2 w-72 h-72 bg-indigo-300 dark:bg-indigo-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
				
				<div class="w-full px-6 sm:px-10 min-h-screen flex flex-col text-center relative z-10">
						{#if ($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false}
							<div class="my-auto pb-10 w-full sm:max-w-md">
								<div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 border border-gray-200 dark:border-gray-700">
									<div class="flex items-center justify-center gap-3 text-xl sm:text-2xl text-center font-semibold text-gray-800 dark:text-gray-200">
										<div>
											{$i18n.t('Signing in to {{WEBUI_NAME}}', { WEBUI_NAME: $WEBUI_NAME })}
										</div>
										<div>
											<Spinner className="size-5" />
										</div>
									</div>
								</div>
							</div>
						{:else}
							<div class="my-auto flex flex-col justify-center items-center">
								<div class="sm:max-w-md my-auto pb-10 w-full">
									<!-- Enhanced auth card with glass morphism effect -->
									<div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-gray-200/50 dark:border-gray-700/50 transform transition-all duration-300 hover:shadow-3xl">
										<div class="flex justify-center mb-8">
											<div class="relative group">
												<div class="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
												<img
													id="logo"
													crossorigin="anonymous"
													src="{WEBUI_BASE_URL}/static/favicon-dark.png"
													class="relative size-20 rounded-full ring-4 ring-white dark:ring-gray-700 shadow-lg transform transition-transform duration-300 group-hover:scale-105"
													alt="Logo"
												/>
											</div>
										</div> 
									<form
										class="flex flex-col justify-center"
										on:submit={(e) => {
											e.preventDefault();
											submitHandler();
										}}
									>
										<div class="mb-6">
											<div class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
												
												{#if $config?.onboarding ?? false}
													{$i18n.t(`Get started with {{WEBUI_NAME}}`, { WEBUI_NAME: $WEBUI_NAME })}
												{:else if mode === 'ldap'}
													{$i18n.t(`Sign in to {{WEBUI_NAME}} with LDAP`, { WEBUI_NAME: $WEBUI_NAME })}
												{:else if mode === 'signin'}
													{$i18n.t(`Sign in to {{WEBUI_NAME}}`, { WEBUI_NAME: $WEBUI_NAME })}
												{:else}
													{$i18n.t(`Sign up to {{WEBUI_NAME}}`, { WEBUI_NAME: $WEBUI_NAME })}
												{/if}
											</div>

											{#if $config?.onboarding ?? false}
												<div class="mt-3 text-xs font-medium text-gray-600 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-800">
													<svg class="inline-block w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
														<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
													</svg>
													{$WEBUI_NAME}
													{$i18n.t(
														'does not make any external connections, and your data stays securely on your locally hosted server.'
													)}
												</div>
											{/if}
										</div>

										{#if $config?.features.enable_login_form || $config?.features.enable_ldap || form}
											<div class="flex flex-col mt-4 space-y-4">
												{#if mode === 'signup'}
													<div class="relative">
														<label for="name" class="text-sm font-semibold text-gray-700 dark:text-gray-300 text-left mb-2 flex items-center">
															<svg class="w-4 h-4 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
															</svg>
															{$i18n.t('Name')}
														</label>
														<div class="relative">
															<input
																bind:value={name}
																type="text"
																id="name"
																class="w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-700/50 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 text-gray-800 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
																autocomplete="name"
																placeholder={$i18n.t('Enter Your Full Name')}
																required
															/>
															<div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
																<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																	<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
																</svg>
															</div>
														</div>
													</div>
												{/if}

												{#if mode === 'ldap'}
													<div class="relative">
														<label for="username" class="text-sm font-semibold text-gray-700 dark:text-gray-300 text-left mb-2 flex items-center">
															<svg class="w-4 h-4 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
															</svg>
															{$i18n.t('Username')}
														</label>
														<div class="relative">
															<input
																bind:value={ldapUsername}
																type="text"
																class="w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-700/50 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-800 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
																autocomplete="username"
																name="username"
																id="username"
																placeholder={$i18n.t('Enter Your Username')}
																required
															/>
															<div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
																<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																	<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
																</svg>
															</div>
														</div>
													</div>
												{:else}
													<div class="relative">
														<label for="email" class="text-sm font-semibold text-gray-700 dark:text-gray-300 text-left mb-2 flex items-center">
															<svg class="w-4 h-4 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
															</svg>
															{$i18n.t('Email')}
														</label>
														<div class="relative">
															<input
																bind:value={email}
																type="email"
																id="email"
																class="w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-700/50 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-800 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
																autocomplete="email"
																name="email"
																placeholder={$i18n.t('Enter Your Email')}
																required
															/>
															<div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
																<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																	<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
																</svg>
															</div>
														</div>
													</div>
												{/if}

												<div class="relative">
													<label for="password" class="text-sm font-semibold text-gray-700 dark:text-gray-300 text-left mb-2 flex items-center">
														<svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
															<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
														</svg>
														{$i18n.t('Password')}
													</label>
													<SensitiveInput
														bind:value={password}
														type="password"
														id="password"
														class="w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-700/50 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 text-gray-800 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
														placeholder={$i18n.t('Enter Your Password')}
														autocomplete={mode === 'signup' ? 'new-password' : 'current-password'}
														name="password"
														required
													/>
												</div>

												{#if mode === 'signup' && $config?.features?.enable_signup_password_confirmation}
													<div class="relative">
														<label for="confirm-password" class="text-sm font-semibold text-gray-700 dark:text-gray-300 text-left mb-2 flex items-center">
															<svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
															</svg>
															{$i18n.t('Confirm Password')}
														</label>
														<SensitiveInput
															bind:value={confirmPassword}
															type="password"
															id="confirm-password"
															class="w-full px-4 py-3 text-sm bg-gray-50 dark:bg-gray-700/50 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 text-gray-800 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500"
															placeholder={$i18n.t('Confirm Your Password')}
															name="confirm-password"
															autocomplete={mode === 'signup' ? 'new-password' : 'current-password'}
															required
														/>
													</div>
												{/if}
											</div>
										{/if}
										<div class="mt-6">
											<!-- {#if onbo$config?.features.enable_login_formarding} -->
											{#if $config?.features.enable_login_form || $config?.features.enable_ldap || form}
												{#if mode === 'ldap'}
													<button
														class="group relative w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-3.5 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-lg hover:shadow-xl"
														type="submit"
													>
														<span class="flex items-center justify-center">
															<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
															</svg>
															{$i18n.t('Authenticate')}
														</span>
													</button>
												{:else}
													<button
														class="group relative w-full bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 text-white font-semibold py-3.5 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 shadow-lg hover:shadow-xl"
														type="submit"
													>
														<span class="flex items-center justify-center">
															<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																{#if mode === 'signin'}
																	<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
																{:else}
																	<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
																{/if}
															</svg>
															{mode === 'signin'
																? $i18n.t('Sign in')
																: ($config?.onboarding ?? false)
																	? $i18n.t('Create Admin Account')
																	: $i18n.t('Create Account')}
														</span>
													</button>

													{#if $config?.features.enable_signup && !($config?.onboarding ?? false)}
														<div class="mt-6 text-sm text-center text-gray-600 dark:text-gray-400">
															{mode === 'signin'
																? $i18n.t("Don't have an account?")
																: $i18n.t('Already have an account?')}

															<button
																class="ml-1 font-semibold text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 underline decoration-2 underline-offset-2 transition-colors duration-200"
																type="button"
																on:click={() => {
																	if (mode === 'signin') {
																		mode = 'signup';
																	} else {
																		mode = 'signin';
																	}
																}}
															>
																{mode === 'signin' ? $i18n.t('Sign up') : $i18n.t('Sign in')}
															</button>
														</div>
													{/if}
												{/if}
											{/if}
										</div>
									</form>

									{#if Object.keys($config?.oauth?.providers ?? {}).length > 0}
										<div class="inline-flex items-center justify-center w-full my-6">
											<hr class="w-full h-px border-0 bg-gray-300 dark:bg-gray-600" />
											{#if $config?.features.enable_login_form || $config?.features.enable_ldap || form}
												<span class="px-4 text-sm font-medium text-gray-500 dark:text-gray-400 bg-white/90 dark:bg-gray-800/90 whitespace-nowrap">
													{$i18n.t('or')}
												</span>
											{/if}
											<hr class="w-full h-px border-0 bg-gray-300 dark:bg-gray-600" />
										</div>
										<div class="flex flex-col space-y-3">
											{#if $config?.oauth?.providers?.google}
												<button
													class="flex justify-center items-center bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 border-2 border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] shadow-md hover:shadow-lg"
													on:click={() => {
														window.location.href = `${WEBUI_BASE_URL}/oauth/google/login`;
													}}
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														viewBox="0 0 48 48"
														class="size-6 mr-3"
													>
														<path
															fill="#EA4335"
															d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
														/><path
															fill="#4285F4"
															d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
														/><path
															fill="#FBBC05"
															d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
														/><path
															fill="#34A853"
															d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
														/><path fill="none" d="M0 0h48v48H0z" />
													</svg>
													<span>{$i18n.t('Continue with {{provider}}', { provider: 'Google' })}</span>
												</button>
											{/if}
											{#if $config?.oauth?.providers?.microsoft}
												<button
													class="flex justify-center items-center bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 border-2 border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] shadow-md hover:shadow-lg"
													on:click={() => {
														window.location.href = `${WEBUI_BASE_URL}/oauth/microsoft/login`;
													}}
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														viewBox="0 0 21 21"
														class="size-6 mr-3"
													>
														<rect x="1" y="1" width="9" height="9" fill="#f25022" /><rect
															x="1"
															y="11"
															width="9"
															height="9"
															fill="#00a4ef"
														/><rect x="11" y="1" width="9" height="9" fill="#7fba00" /><rect
															x="11"
															y="11"
															width="9"
															height="9"
															fill="#ffb900"
														/>
													</svg>
													<span>{$i18n.t('Continue with {{provider}}', { provider: 'Microsoft' })}</span
													>
												</button>
											{/if}
											{#if $config?.oauth?.providers?.github}
												<button
													class="flex justify-center items-center bg-gray-900 dark:bg-gray-700 hover:bg-gray-800 dark:hover:bg-gray-600 text-white font-medium py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] shadow-md hover:shadow-lg"
													on:click={() => {
														window.location.href = `${WEBUI_BASE_URL}/oauth/github/login`;
													}}
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														viewBox="0 0 24 24"
														class="size-6 mr-3"
													>
														<path
															fill="currentColor"
															d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.92 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57C20.565 21.795 24 17.31 24 12c0-6.63-5.37-12-12-12z"
														/>
													</svg>
													<span>{$i18n.t('Continue with {{provider}}', { provider: 'GitHub' })}</span>
												</button>
											{/if}
											{#if $config?.oauth?.providers?.oidc}
												<button
													class="flex justify-center items-center bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 border-2 border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] shadow-md hover:shadow-lg"
													on:click={() => {
														window.location.href = `${WEBUI_BASE_URL}/oauth/oidc/login`;
													}}
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														fill="none"
														viewBox="0 0 24 24"
														stroke-width="1.5"
														stroke="currentColor"
														class="size-6 mr-3"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z"
														/>
													</svg>

													<span
														>{$i18n.t('Continue with {{provider}}', {
															provider: $config?.oauth?.providers?.oidc ?? 'SSO'
														})}</span
													>
												</button>
											{/if}
											{#if $config?.oauth?.providers?.feishu}
												<button
													class="flex justify-center items-center bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 border-2 border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] shadow-md hover:shadow-lg"
													on:click={() => {
														window.location.href = `${WEBUI_BASE_URL}/oauth/feishu/login`;
													}}
												>
													<span>{$i18n.t('Continue with {{provider}}', { provider: 'Feishu' })}</span>
												</button>
											{/if}
										</div>
									{/if}

									{#if $config?.features.enable_ldap && $config?.features.enable_login_form}
										<div class="mt-6">
											<button
												class="flex justify-center items-center text-sm w-full text-center text-gray-600 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 font-medium underline decoration-2 underline-offset-2 transition-colors duration-200"
												type="button"
												on:click={() => {
													if (mode === 'ldap')
														mode = ($config?.onboarding ?? false) ? 'signup' : 'signin';
													else mode = 'ldap';
												}}
											>
												<span
													>{mode === 'ldap'
														? $i18n.t('Continue with Email')
														: $i18n.t('Continue with LDAP')}</span
												>
											</button>
										</div>
									{/if}
								</div>
							</div>
							
							{#if $config?.metadata?.login_footer}
								<div class="mt-6 max-w-md mx-auto">
									<div class="text-xs text-gray-500 dark:text-gray-400 marked text-center p-4 bg-gray-50 dark:bg-gray-700/30 rounded-xl">
										{@html DOMPurify.sanitize(marked($config?.metadata?.login_footer))}
									</div>
								</div>
							{/if}
						</div>
					{/if}
				</div>

				<!-- {#if !$config?.metadata?.auth_logo_position}
					<div class="fixed top-6 left-6 z-50">
						<div class="flex items-center space-x-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md px-4 py-2 rounded-full shadow-lg border border-gray-200 dark:border-gray-700">
							<img
								id="logo"
								crossorigin="anonymous"
								src="{WEBUI_BASE_URL}/static/favicon-dark.png"
								class="w-8 h-8 rounded-full"
								alt="Logo"
							/>
							<span class="text-sm font-semibold text-gray-800 dark:text-gray-200">{$WEBUI_NAME}</span>
						</div>
					</div>
				{/if} -->
			</div>
		</div>
		<div class="w-full p-4 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 shadow-md overflow-x-hidden">
			<main class="container mx-auto px-4 py-0">
				<LandingComponent />
			</main>
		</div>
	{/if}
</div>

<style>
	/* Prevent horizontal overflow */
	#auth-page {
		overflow-x: hidden;
		max-width: 100vw;
	}

	#auth-page * {
		max-width: 100%;
	}

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

	/* Custom scrollbar */
	#auth-page ::-webkit-scrollbar {
		width: 8px;
	}

	#auth-page ::-webkit-scrollbar-track {
		background: transparent;
	}

	#auth-page ::-webkit-scrollbar-thumb {
		background: rgba(156, 163, 175, 0.5);
		border-radius: 4px;
	}

	#auth-page ::-webkit-scrollbar-thumb:hover {
		background: rgba(107, 114, 128, 0.7);
	}

	/* Smooth transitions */
	input,
	button {
		transition: all 0.2s ease-in-out;
	}

	/* Focus visible outline */
	input:focus-visible {
		outline: 2px solid rgb(147, 51, 234);
		outline-offset: 2px;
	}
</style>
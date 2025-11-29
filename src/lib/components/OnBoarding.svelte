<script>
	import { getContext, onMount } from 'svelte';
	const i18n = getContext('i18n');

	import { WEBUI_BASE_URL, WEBUI_BASE_FRONTEND_URL } from '$lib/constants';

	import Marquee from './common/Marquee.svelte';
	import SlideShow from './common/SlideShow.svelte';
	import ArrowRightCircle from './icons/ArrowRightCircle.svelte';
	import Impression from '$lib/components/Impression.svelte';
	import Image from './common/Image.svelte';

	export let show = true;
	export let getStartedHandler = () => {};

	function setLogoImage() {
		const logo = document.getElementById('logo');

		if (logo) {
			const isDarkMode = document.documentElement.classList.contains('dark');

			if (isDarkMode) {
				const darkImage = new Image();
				darkImage.src = `${WEBUI_BASE_FRONTEND_URL}/static/favicon.png`;

				darkImage.onload = () => {
					logo.src = `${WEBUI_BASE_FRONTEND_URL}/static/favicon.png`;
					logo.style.filter = ''; // Ensure no inversion is applied if splash-dark.png exists
				};

				darkImage.onerror = () => {
					logo.style.filter = 'invert(1)'; // Invert image if splash-dark.png is missing
				};
			}
		}
	}

	$: if (show) {
		setLogoImage();
	}
</script>

{#if show}
	<div class="w-full h-screen max-h-screen overflow-y-auto text-white relative">
		<!-- <div class="fixed m-10 z-50">
			<div class="flex space-x-2">
				<div class=" self-center">
					<img
						id="logo"
						crossorigin="anonymous"
						src="{WEBUI_BASE_FRONTEND_URL}/static/logo.png"
						class=" w-6 rounded-full"
						alt="logo"
					/>
				</div>
			</div>
		</div> -->

		<SlideShow duration={5000} />

		<div
			class="w-full h-full absolute top-0 left-0 bg-linear-to-t from-20% from-black to-transparent"
		></div>

		<div class="w-full h-full absolute top-0 left-0 backdrop-blur-xs bg-black/50"></div>

		<div class="relative bg-transparent w-full h-screen max-h-screen overflow-y-auto flex z-10">
			
			<div class="flex flex-col justify-end w-full items-center pb-10 px-4 text-center">
				<Impression sectionId="auth-onboarding-image">
				<div class="flex justify-center mb-6">
					<img
						id="logo"
						crossorigin="anonymous"
						src="{WEBUI_BASE_FRONTEND_URL}/static/favicon.png"
						class="size-48 rounded-full"
						alt="Logo"
					/>
				</div>
				</Impression>
				<Impression sectionId="auth-onboarding-marquee"> 
					<div class="text-5xl lg:text-7xl font-secondary">
						<Marquee
							duration={5000}
							words={[
								$i18n.t('Explore the cosmos'),
								$i18n.t('Unlock mysteries'),
								$i18n.t('Chart new frontiers'),
								$i18n.t('Dive into knowledge'),
								$i18n.t('Discover wonders'),
								$i18n.t('Ignite curiosity'),
								$i18n.t('Forge new paths'),
								$i18n.t('Unravel secrets'),
								$i18n.t('Pioneer insights'),
								$i18n.t('Embark on adventures')
							]}
						/>

						<div class="mt-0.5">{$i18n.t(`wherever you are`)}</div>
					</div>
				</Impression>
				<Impression sectionId="auth-onboarding-start-button"> 
				<div class="flex justify-center mt-8">
					<div class="flex flex-col justify-center items-center">
						<button
							aria-labelledby="get-started"
							class="relative z-20 flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-white/10 hover:bg-white/20 border border-white/20 hover:border-white/30 backdrop-blur-sm transition-all duration-200 font-medium text-base shadow-lg hover:shadow-xl hover:scale-105"
							on:click={() => {
								getStartedHandler();
							}}
						>
							<span id="get-started" class="font-primary font-semibold">
								{$i18n.t(`Get started`)}
							</span>
							<ArrowRightCircle className="size-5" />
						</button>
					</div>
				</div>
				</Impression>
			</div>
		</div>
	</div>
{/if}

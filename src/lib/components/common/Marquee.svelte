<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import { onMount } from 'svelte';

	let idx = 0;

	export let className = '';
	export let words = ['lorem', 'ipsum'];
	export let duration = 4000;

	onMount(() => {
		setInterval(async () => {
			if (idx === words.length - 1) {
				idx = 0;
			} else {
				idx = idx + 1;
			}
		}, duration);
	});
</script>

<div class={className}>
	<div>
		{#key idx}
			<hr />
			<div class=" marquee-item py-5" in:fly={{ y: '30%', duration: 1000 }}>
				<h5 class="text-xl md:text-2xl font-extrabold mb-6 text-white leading-tight s-1epn7BoarYrf">{words.at(idx)}</h5>
			</div>
		{/key}
	</div>
</div>

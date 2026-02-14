<script lang="ts">
	import './layout.css';
	import NavBar from '$lib/components/NavBar.svelte';
	import Header from '$lib/components/Header.svelte';

	let { children } = $props();
</script>

<div class="flex h-screen w-screen overflow-hidden">
	<NavBar />
	<div class="flex flex-1 flex-col">
		<Header />
		<main class="flex-1 overflow-y-auto">
			{@render children()}
		</main>
	</div>
</div>

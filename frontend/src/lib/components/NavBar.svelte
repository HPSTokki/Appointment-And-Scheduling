<script lang="ts">
	import { page } from '$app/state';

	const navLinks = [
		{ href: '/dashboard', label: 'Dashboard' },
		{ href: '/appointments', label: 'Appointments' },
		{ href: '/emr', label: 'Electronic Medical Records (EMR)' },
		{ href: '/inventory', label: 'Inventory' }
	];
</script>

<nav class="flex flex-col items-center justify-evenly border-r-2 border-green-300">
    <h1>
        Placeholder Name
    </h1>
	<div class="flex flex-col items-center justify-center gap-10 px-2 py-2">
		{#each navLinks as links}
			<a
				href={links.href}
				class="w-full rounded-2xl border-2 bg-green-400 px-1 py-4 text-center font-semibold transition-colors {page.url.pathname === links.href
					? 'bg-green-600 text-white'
					: 'text-white hover:bg-slate-700 hover:text-white'} "
			>
				{links.label}
			</a>
		{/each}
	</div>
	<button class="w-46 cursor-pointer rounded-2xl bg-green-400 px-1 py-4 text-white" type="button">
		Logout
	</button>
</nav>

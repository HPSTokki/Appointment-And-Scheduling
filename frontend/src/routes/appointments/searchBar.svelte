<script lang="ts">
	import type { ListResponseAppointment } from '$lib/types';

	interface Props {
		onsearch: (data: ListResponseAppointment) => void;
		onreset: () => void;
	}

	let { onsearch, onreset }: Props = $props()

	let searchMode: 'date' | 'name' = $state('date');
	let searchTerm = $state('');

	async function handleSearch() {
		if (!searchTerm.trim()) return;

		let response;
		if (searchMode === 'date') {
			response = await fetch(
				`http://localhost:8000/appointment/date/${searchTerm}`
			);
		} else {
			response = await fetch(`http://localhost:8000/appointment/search-appointment?search_term=${encodeURIComponent(searchTerm)}`);
		}

		const data: ListResponseAppointment = await response.json();
		onsearch(data);
	}

	function handleReset() {
		searchTerm = '';
		onreset();
	}
</script>

<div class="space-y-3 rounded-lg border border-green-400 bg-white p-4 shadow">
	<!-- Mode toggle -->
	<div class="flex gap-2">
		<button
			onclick={() => (searchMode = 'date')}
			class="rounded-lg px-4 py-1 transition-colors {searchMode === 'date'
				? 'bg-green-500 text-white'
				: 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
		>
			By Date
		</button>
		<button
			onclick={() => (searchMode = 'name')}
			class="rounded-lg px-4 py-1 transition-colors {searchMode === 'name'
				? 'bg-green-500 text-white'
				: 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
		>
			By Client Name
		</button>
	</div>

	<!-- Search input -->
	<div class="flex gap-3">
		<input
			type={searchMode === 'date' ? 'date' : 'text'}
			bind:value={searchTerm}
			onkeydown={(e) => e.key === 'Enter' && handleSearch()}
			placeholder={searchMode === 'date' ? 'Select date' : 'Enter client name'}
			class="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:ring-2 focus:ring-green-500 focus:outline-none"
		/>
		<button
			onclick={handleSearch}
			class="rounded-lg bg-green-500 px-6 py-1 text-white transition-colors hover:bg-green-600"
		>
			Search
		</button>
		<button
			onclick={handleReset}
			class="rounded-lg bg-gray-200 px-6 py-1 text-gray-700 transition-colors hover:bg-gray-300"
		>
			Reset
		</button>
	</div>
</div>

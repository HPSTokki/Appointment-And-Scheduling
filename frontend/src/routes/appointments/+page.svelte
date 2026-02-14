<script lang="ts">
	import searchBar from '$lib/components/searchBar.svelte';
	import { onMount } from 'svelte';
    import type { ResponseAppointment, ListResponseAppointment } from '$lib/types';

	let appointments: ResponseAppointment[] = [];
	let totalCount = $state(0);

	onMount(async() => {
        await loadTodaysAppointment();
    })

    async function loadTodaysAppointment() {
        const today = new Date().toISOString().split('T')[0];
        const response = await fetch(`http://localhost:8000/appointment/date/${today}`)
        const data: ListResponseAppointment = await response.json()
        appointments = data.appointments 
        totalCount = appointments.length
    }

</script>

<div>
	<h1 class="text-4xl font-bold tracking-wide">Appointment</h1>
	<h2 class="text-1xl font-semibold tracking-wide">Manage and Schedule Appointment</h2>
	<p>
		{#if totalCount > 0}
			<span class="font-bold">{totalCount} Appointments</span>
		{:else}
			No Appointment
		{/if}
	</p>
</div>
<div>Search bar</div>
<div>Main Data Drop Point</div>

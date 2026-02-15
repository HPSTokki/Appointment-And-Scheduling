<script lang="ts">
	import SearchBar from './searchBar.svelte';
	import { onDestroy, onMount } from 'svelte';
	import type { ResponseAppointment, ListResponseAppointment } from '$lib/types';
	import { refreshAll } from '$app/navigation';

	let { data } = $props<{
		data: {
			appointments: ListResponseAppointment;
		};
	}>();

	let appointments = $derived(data.appointments);
	let totalCount = $derived(appointments.length);
	let currentDate = $state(new Date());
	let intervalId: ReturnType<typeof setInterval>;
	let selectedStatus: string = $state('All');

	onMount(async () => {
		intervalId = setInterval(() => {
			currentDate = new Date();
		}, 1000);
	});

	onDestroy(() => {
		if (intervalId) clearInterval(intervalId);
	});

	function handleSearch(data: ListResponseAppointment) {
		appointments = data.appointments;
		totalCount = appointments.length;
	}

	function handleReset() {
		refreshAll()
	}
</script>

<div class="space-y-6">
	<!-- This is greeter section -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold tracking-wide text-slate-700">Today's Appointment</h1>
			<p class="mt-1 text-slate-600">
				{currentDate.toLocaleDateString('en-US', {
					weekday: 'long',
					year: 'numeric',
					month: 'long',
					day: 'numeric',
					hour: 'numeric',
					minute: 'numeric',
					second: 'numeric'
				})}
			</p>
		</div>
		<div class="rounded-lg bg-green-500 px-6 py-4">
			{#if totalCount === 0}
				<p class="text-lg font-medium text-slate-900">No Appointments for Today!</p>
			{:else}
				<p class="text-lg font-medium text-slate-900">Total Appointments:</p>
				<p class="text-lg font-medium text-slate-900">{totalCount} Appointments</p>
			{/if}
		</div>
	</div>
	<SearchBar onsearch={handleSearch} onreset={handleReset} />
	<div class="space-y-3">
		{#if appointments.length === 0}
			<p>No Appointments!</p>
			<a href="/appointments/add-appointment">Add Appointment</a>
		{:else}
			{#each appointments as appointment}
				<div class="rounded-lg border border-green-400 bg-white p-4 shadow">
					<div class="flex items-start justify-between">
						<div>
							<h3 class="text-lg">
								<span class="text-lg font-bold">Client Name:</span>
								{appointment.client_name}
							</h3>
							<p>Pet Name: {appointment.pet_name}</p>
							<p>Complain: {appointment.chief_complaint}</p>
						</div>
						<div class="text-right">
							<p>
								{new Date(appointment.appointment_date).toLocaleTimeString('en-US', {
									weekday: 'long',
									year: 'numeric',
									month: 'long',
									day: 'numeric',
									hour: 'numeric'
								})}
							</p>
							<span>
								{appointment.status}
							</span>
						</div>
					</div>
				</div>
			{/each}
		{/if}
	</div>
</div>

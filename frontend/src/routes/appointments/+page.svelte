<script lang="ts">
	import SearchBar from './searchBar.svelte';
	import { onDestroy, onMount } from 'svelte';
	import type { ResponseAppointment, ListResponseAppointment } from '$lib/types';
	import { refreshAll } from '$app/navigation';

	let { data } = $props<{
		data: {
			appointments: ResponseAppointment[];
		};
	}>();

	let appointments: ResponseAppointment[] = $derived(data.appointments);
	let totalCount = $derived(appointments.length);
	let currentDate = $state(new Date());
	let intervalId: ReturnType<typeof setInterval>;
	let selectedStatus: string = $state('All');

	const statusFilters = ['All', 'Waitlist', 'Completed'];

	onMount(async () => {
		intervalId = setInterval(() => {
			currentDate = new Date();
		}, 1000);
	});

	onDestroy(() => {
		if (intervalId) clearInterval(intervalId);
	});

	async function loadTodaysAppointment() {
		const today = new Date().toISOString().split('T')[0];
		const response = await fetch(`http://localhost:8000/appointment/date/${today}`);
		const data: ListResponseAppointment = await response.json();
		appointments = data.appointments;
		selectedStatus = 'All';
	}

	async function handleStatusFilter(status: string) {
		selectedStatus = status;

		if (status === 'All') {
			await loadTodaysAppointment();
		} else {
			const response = await fetch(
				`http://localhost:8000/appointment/status?filter_term=${status}`
			);
			const data: ListResponseAppointment = await response.json();
			appointments = data.appointments;
		}
	}

	function handleSearch(data: ListResponseAppointment) {
		appointments = data.appointments;
		totalCount = appointments.length;
	}

	function handleReset() {
		loadTodaysAppointment();
	}
</script>

<div class="space-y-4">
	<!-- This is greeter section -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold tracking-wide text-slate-700">Today's Appointment</h1>
			<p class=" text-slate-600">
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
		<div class="rounded-lg bg-green-500 px-6 py-2">
			{#if totalCount === 0}
				<p class="text-lg font-medium text-slate-900">No Appointments for Today!</p>
			{:else}
				<p class="text-lg font-medium text-slate-900">Total Appointments:</p>
				<p class="text-lg font-medium text-slate-900">{totalCount} Appointments</p>
			{/if}
		</div>
	</div>

	<SearchBar onsearch={handleSearch} onreset={handleReset} />

	<!-- Status Filter Below -->
	<div class="rounded-lg border border-green-500 bg-white p-4 shadow">
		<p class="mb-3 text-sm font-medium text-gray-700">Filter By Status:</p>
		<div class="flex gap-2">
			{#each statusFilters as status}
				<button
					onclick={() => handleStatusFilter(status)}
					class="rounded-lg px-4 py-2 transition-colors {selectedStatus === status
						? 'bg-green-600 text-white'
						: 'bg-green-800 text-white hover:bg-green-800'}"
				>
					{status}
				</button>
			{/each}
		</div>
	</div>
	<!-- End of Status Filter Section -->

	<!-- Tables Part -->
	<div class="space-y-2 overflow-hidden rounded-lg border border-green-400 bg-white shadow">
		<table class="w-full">
			<thead class="border-b border-gray-200 bg-gray-50">
				<tr>
					<th class="px-4 py-3 text-left text-sm font-medium tracking-wider text-gray-700">
						Time
					</th>
					<th class="px-4 py-3 text-left text-sm font-medium tracking-wider text-gray-700">
						Client
					</th>
					<th class="px-4 py-3 text-left text-sm font-medium tracking-wider text-gray-700">
						Pet
					</th>
					<th class="px-4 py-3 text-left text-sm font-medium tracking-wider text-gray-700">
						Reason
					</th>
					<th class="px-4 py-3 text-left text-sm font-medium tracking-wider text-gray-700">
						Status
					</th>
					<th class="px-4 py-3 text-left text-sm font-medium tracking-wider text-gray-700">
						Actions
					</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-green-800">
				{#if appointments.length === 0}
					<tr>
						<td colspan="6" class="px-4 py-8 text-center text-gray-700"> No Appointments Found </td>
					</tr>
				{:else}
					{#each appointments as appointment}
						<tr class="transition-colors hover:bg-gray-50">
							<td class="px-4 py-4 whitespace-nowrap">
								<div class="text-sm font-medium text-gray-900">
									{new Date(appointment.appointment_date).toLocaleDateString('en-US', {
										hour: 'numeric',
										minute: '2-digit'
									})}
								</div>
								<div class="text-xs text-gray-900">
									{new Date(appointment.appointment_date).toLocaleDateString('en-US', {
										month: 'short',
										day: 'numeric'
									})}
								</div>
							</td>
							<td class="px-4 py-4 whitespace-nowrap">
								<div class="text-sm font-medium text-gray-900">
									{appointment.client_name}
								</div>
							</td>
							<td class="px-4 py-4 whitespace-nowrap">
								<div class="text-sm font-medium text-gray-900">
									{appointment.pet_name}
								</div>
							</td>
							<td class="px-4 py-4">
								<div
									class="max-w-xs truncate text-sm font-medium text-gray-700"
									title={appointment.chief_complaint}
								>
									{appointment.chief_complaint}
								</div>
							</td>
							<td class="px-4 py-4 whitespace-nowrap">
								<span
									class="full inline-flex rounded px-3 py-1 text-xs leading-5 font-semibold {appointment.status ===
									'Completed'
										? 'bg-green-100 text-green-50'
										: appointment.status === 'Waitlist'
											? 'bg-yellow-500 text-yellow-50'
											: 'bg-gray-800 text-white'}"
								>
									{appointment.status}
								</span>
							</td>
							<td class="px-4 py-4 whitespace-nowrap text-sm">
								<div class="flex gap-2">
									<button class="text-white px-2 py-1 rounded hover:text-white font-medium bg-green-600">
										View
									</button>
									<button class="text-white px-2 py-1 rounded hover:text-white font-medium bg-blue-600">
										Edit
									</button>
								</div>
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
</div>

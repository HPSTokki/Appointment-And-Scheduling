<script lang="ts">

    import type { ResponsePet, ResponseClient, InsertAppointment, ListResponseClient, ListResponsePet } from "$lib/types";
    import { goto } from "$app/navigation";

    let currentStep = $state<'client' | 'pet' | 'appointment'>('client')

    let selectedClient: ResponseClient | null = $state(null);
    let selectedPet: ResponsePet | null = $state(null);
    
    let clientSearchTerm = $state('')
    let clientResults: ResponseClient[] = $state([]);
    let petResults: ResponsePet[] = $state([])

    let appointmentDate = $state('')
    let appointmentTime = $state('')
    let visitType = $state('')
    let chiefComplaint = $state('')
    let bookingSource = $state('Walkin')

    const visitTypes = [
        'Wellness', 'Checkup', 'Vaccination', 'Diagnostic', 'Emergency'
    ];

    async function searchClients() {
        if (!clientSearchTerm.trim()) return;

        const response = await fetch(`http://localhost:8000/client/search-client?search_term=${encodeURIComponent(clientSearchTerm)}`)
        const data: ListResponseClient = await response.json()
        clientResults = data.clients;

    }

    async function selectClient(client: ResponseClient) {
        selectedClient = client

        const response = await fetch(`http://localhost:8000/pet/client/${encodeURIComponent(client.client_id)}`)
        const data: ListResponsePet = await response.json()
        petResults = data.pets

        currentStep = 'pet'

    }

    function selectPet(pet: ResponsePet){
        selectedPet = pet;
        currentStep = 'appointment'
    }

    async function submitAppointment() {
        if (!selectedClient || !selectedPet) return;

        const appointmentDateAndTime = `${appointmentDate}T${appointmentTime}:00`;

        const appointmentData = {
            client_id: selectedClient.client_id,
            pet_id: selectedPet.pet_id,
            appointment_date: appointmentDateAndTime,
            visit_type_code: visitType,
            chief_complaint: chiefComplaint,
            booking_source: bookingSource,
            status: 'Waitlist'
        }

        const response = await fetch(`http://localhost:8000/appointment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appointmentData)
        })

        if (response.ok) {
            goto('/appointments')
        }

    };

    function goBack() {
        if (currentStep === 'pet') {
            currentStep = 'client';
            selectedClient = null;
            petResults = []
        } else if (currentStep === 'appointment') {
            currentStep = 'pet',
            selectedPet = null
        }
    }

</script>

<div class="max-w-4xl mx-auto space-y-6">
  <!-- Header -->
  <div class="flex items-center justify-between">
    <h1 class="text-3xl font-bold text-slate-700">Book Appointment</h1>
    <a href="/appointments" class="text-blue-600 hover:text-blue-800">← Back to List</a>
  </div>

  <!-- Step Indicator -->
  <div class="flex items-center justify-between bg-white p-4 rounded-lg shadow">
    <div class="flex items-center gap-2">
      <div class="w-8 h-8 rounded-full flex items-center justify-center {currentStep === 'client' ? 'bg-green-500 text-white' : 'bg-gray-200'}">
        1
      </div>
      <span class="font-medium">Select Client</span>
    </div>
    <div class="flex-1 h-1 bg-gray-200 mx-4"></div>
    <div class="flex items-center gap-2">
      <div class="w-8 h-8 rounded-full flex items-center justify-center {currentStep === 'pet' ? 'bg-green-500 text-white' : 'bg-gray-200'}">
        2
      </div>
      <span class="font-medium">Select Pet</span>
    </div>
    <div class="flex-1 h-1 bg-gray-200 mx-4"></div>
    <div class="flex items-center gap-2">
      <div class="w-8 h-8 rounded-full flex items-center justify-center {currentStep === 'appointment' ? 'bg-green-500 text-white' : 'bg-gray-200'}">
        3
      </div>
      <span class="font-medium">Appointment Details</span>
    </div>
  </div>

  <!-- Step Content -->
  <div class="bg-white p-6 rounded-lg shadow">
    {#if currentStep === 'client'}
      <!-- Step 1: Search Client -->
      <h2 class="text-xl font-semibold mb-4">Search for Client</h2>
      
      <div class="flex gap-3 mb-6">
        <input
          type="text"
          bind:value={clientSearchTerm}
          onkeydown={(e) => e.key === 'Enter' && searchClients()}
          placeholder="Enter client name..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
        />
        <button
          onclick={searchClients}
          class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          Search
        </button>
      </div>

      {#if clientResults.length > 0}
        <div class="space-y-2">
          {#each clientResults as client}
            <button
              onclick={() => selectClient(client)}
              class="w-full p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left"
            >
              <div class="font-semibold">{client.full_name}</div>
              <div class="text-sm text-gray-600">{client.email} • {client.mobile_no}</div>
            </button>
          {/each}
        </div>
      {/if}

    {:else if currentStep === 'pet'}
      <!-- Step 2: Select Pet -->
      <div class="mb-4">
        <button onclick={goBack} class="text-blue-600 hover:text-blue-800">← Back</button>
      </div>
      
      <h2 class="text-xl font-semibold mb-2">Select Pet for {selectedClient?.full_name}</h2>
      <p class="text-gray-600 mb-6">Choose which pet this appointment is for</p>

      {#if petResults.length > 0}
        <div class="space-y-2">
          {#each petResults as pet}
            <button
              onclick={() => selectPet(pet)}
              class="w-full p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left"
            >
              <div class="font-semibold">{pet.name}</div>
              <div class="text-sm text-gray-600">{pet.species_type} • {pet.breed}</div>
            </button>
          {/each}
        </div>
      {:else}
        <p class="text-gray-500">No pets found for this client.</p>
      {/if}

    {:else if currentStep === 'appointment'}
      <!-- Step 3: Appointment Details -->
      <div class="mb-4">
        <button onclick={goBack} class="text-blue-600 hover:text-blue-800">← Back</button>
      </div>
      
      <h2 class="text-xl font-semibold mb-2">Appointment Details</h2>
      <p class="text-gray-600 mb-6">
        Client: {selectedClient?.full_name} • Pet: {selectedPet?.name}
      </p>

      <form onsubmit={(e) => { e.preventDefault(); submitAppointment(); }} class="space-y-4">
        <!-- Date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input
            type="date"
            bind:value={appointmentDate}
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
          />
        </div>

        <!-- Time -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Time</label>
          <input
            type="time"
            bind:value={appointmentTime}
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
          />
        </div>

        <!-- Visit Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Visit Type</label>
          <select
            bind:value={visitType}
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
          >
            <option value="">Select type...</option>
            {#each visitTypes as type}
              <option value={type}>{type}</option>
            {/each}
          </select>
        </div>

        <!-- Chief Complaint -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Reason for Visit</label>
          <textarea
            bind:value={chiefComplaint}
            required
            rows="3"
            placeholder="Describe the reason for the appointment..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
          ></textarea>
        </div>

        <!-- Booking Source -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Booking Source</label>
          <select
            bind:value={bookingSource}
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
          >
            <option value="Walkin">Walk-in</option>
            <option value="Phone">Phone</option>
            <option value="Message">Message</option>
          </select>
        </div>

        <!-- Submit -->
        <div class="flex gap-3 pt-4">
          <button
            type="submit"
            class="flex-1 px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 font-medium"
          >
            Book Appointment
          </button>
          <button
            type="button"
            onclick={() => goto('/appointments')}
            class="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Cancel
          </button>
        </div>
      </form>
    {/if}
  </div>
</div>
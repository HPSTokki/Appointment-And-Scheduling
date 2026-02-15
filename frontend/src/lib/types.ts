export type ResponseAppointment = {
    pet_id: number
    client_id: number
    appointment_id: number
    appointment_date: Date
    visit_type_code: string
    chief_complaint: string
    booking_source: string
    status: string
    created_at: Date

    pet_name: string | null
    client_name: string | null
}

export type InsertAppointment = {
    pet_id: number
    client_id: number
    appointment_date: Date
    visit_type_code: string
    chief_complaint: string
    booking_source: string
    status: string
}

export type ListResponseAppointment = {
    appointments: ResponseAppointment[];
}

export type ResponseClient = {
    client_id: number
    full_name: string
    mobile_no: string | null
    tel_no: string | null
    preferred_contact_method: string
    email: string
    address: string
    is_new_client: boolean
    created_at: Date
}

export type ListResponseClient = {
    clients: ResponseClient[]
}

export type ResponsePet = {
    pet_id: number;
    client_id: number;
    name: string;
    species_type: string;
    breed: string;
    date_of_birth: string;
    sex: string;
    is_spayed_neutered: boolean;
    weight_kg: number | null;
    created_at: string;
}

export type ListResponsePet = {
    pets: ResponsePet[]
}
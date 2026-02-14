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

export type ListResponseAppointment = {
    appointments: ResponseAppointment[];
}
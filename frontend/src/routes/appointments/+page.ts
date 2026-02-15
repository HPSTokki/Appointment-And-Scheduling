import type { ListResponseAppointment } from "$lib/types";
import type { PageLoad } from "./$types";

export const load: PageLoad = async({fetch}) => {
    const today = new Date().toISOString().split('T')[0];
    const response = await fetch(`http://localhost:8000/appointment/date/${today}`)
    if (!response.ok) {
        throw new Error('Failed to Load Appointments')
    }
    const data: ListResponseAppointment = await response.json()
    return {
        appointments: data.appointments       
    }
}
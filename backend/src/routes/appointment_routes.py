from src.dto.appointment_dto import ListResponseAppointment, ResponseAppointment, InsertAppointment, UpdateAppointment
from src.services.appointment_service import AppointmentService
from fastapi import HTTPException, APIRouter
from src.engine import SessionDep
from datetime import date

router = APIRouter(prefix="/appointment", tags=["Appointments"])

@router.post("/", response_model=ResponseAppointment)
def create_appointment(session: SessionDep, appointment_data: InsertAppointment):
    service = AppointmentService(session)
    appointment = service.create_appointment(appointment_data)
    return appointment

@router.get("/", response_model=ListResponseAppointment)
def get_all_appointment(session: SessionDep):
    service = AppointmentService(session)
    appointments = service.get_all_appointment()
    return {
        "appointments": appointments
    }

@router.get("/search-appointment", response_model=ListResponseAppointment)
def get_appointments_by_name(session: SessionDep, search_term: str):
    service = AppointmentService(session)
    appointments = service.get_appointments_by_name(search_term)
    return {
        "appointments": appointments
    }

@router.get("/date/{target_date}", response_model=ListResponseAppointment)
def get_appointments_by_date(session: SessionDep, target_date: date):
    service = AppointmentService(session)
    appointments = service.get_appointments_by_date(target_date)
    return {
        "appointments": appointments
    }

@router.get("/{appointment_id}", response_model=ResponseAppointment)
def get_one_appointment(session: SessionDep, appointment_id: int):
    service = AppointmentService(session)
    appointment = service.get_one_appointment(appointment_id)
    return appointment

@router.put("/update/{appointment_id}", response_model=ResponseAppointment)
def update_appointment(session: SessionDep, appointment_id: int, update_appointment_data: UpdateAppointment):
    service = AppointmentService(session)
    appointment = service.update_appointment(appointment_id, update_appointment_data)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment Not Found")

    return appointment
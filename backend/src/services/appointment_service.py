from src.dto.appointment_dto import InsertAppointment, UpdateAppointment
from src.models.appointment_model import Appointment, Pet, Client
from sqlmodel import select, Session
from datetime import datetime, date

class AppointmentService():
    def __init__(self, session: Session):
        self.session = session

    def create_appointment(self, appointment_data: InsertAppointment) -> Appointment:
        appointment = Appointment.model_validate(appointment_data)
        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return appointment
    
    def get_one_appointment(self, appointment_id: int) -> dict:

        stmt = select(Appointment, Pet.name, Client.full_name).join(
            Pet, Appointment.pet_id == Pet.pet_id
        ).join(
            Client, Appointment.client_id == Client.client_id
        ).where(
            Appointment.appointment_id == appointment_id
        )

        result = self.session.exec(stmt).first()

        if not result:
            return None

        appointment, pet_name, client_name = result
        
        appointment_dict = appointment.model_dump()
        appointment_dict["pet_name"] = pet_name
        appointment_dict["client_name"] = client_name

        return appointment_dict
    
    def get_all_appointment(self) -> list[dict]:
        stmt = select(Appointment, Pet.name, Client.full_name).join(
            Pet, Appointment.pet_id == Pet.pet_id
        ).join(
            Client, Appointment.client_id == Client.client_id
        )

        results = self.session.exec(stmt).all()

        appointments = []

        for appointment, pet_name, client_name in results:
            appointment_dict = appointment.model_dump()
            appointment_dict["pet_name"] = pet_name
            appointment_dict["client_name"] = client_name
            appointments.append(appointment_dict)

        return appointments
    
    def get_appointments_by_date(self, target_date: date) -> list[dict]:
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

        stmt = select(Appointment, Pet.name, Client.full_name).join(
            Pet, Appointment.pet_id == Pet.pet_id
        ).join(
            Client, Appointment.client_id == Client.client_id
        ).where(
            Appointment.appointment_date >= start_of_day,
            Appointment.appointment_date <= end_of_day
        )

        results = self.session.exec(stmt).all()

        appointments = []
        for appointment, pet_name, client_name in results:
            appointment_dict = appointment.model_dump()
            appointment_dict["pet_name"] = pet_name
            appointment_dict["client_name"] = client_name
            appointments.append(appointment_dict) 

        return appointments

    def update_appointment(self, appointment_id: int, update_appointment_data: UpdateAppointment) -> dict | None:
        appointment = self.session.get(Appointment, appointment_id)

        if not appointment:
            return None

        updated_appointment = update_appointment_data.model_dump(exclude_unset=True)

        for key, value in updated_appointment.items():
            setattr(appointment, key, value)

        self.session.commit()
        self.session.refresh(appointment)

        pet = self.session.get(Pet, appointment.pet_id)
        client = self.session.get(Client, appointment.client_id)

        appointment_dict = appointment.model_dump()
        appointment_dict["pet_name"] = pet.name if pet else None
        appointment_dict["client_name"] = client.full_name if client else None

        return appointment_dict

    def get_appointments_by_name(self, search_term: str) -> list[dict]:
        stmt = select(Appointment, Client.full_name).join(
            Client, Appointment.client_id == Client.client_id
        ).where(
            Client.full_name.ilike(f"%{search_term}%")
        )

        results = self.session.exec(stmt).all()

        appointments = []
        for appointment, client_name in results:
            appointment_dict = appointment.model_dump()
            appointment_dict["client_name"] = client_name
            appointments.append(appointment_dict)

        return appointments
    
    def filter_appointments_by_status(self, filter_term: str) -> list[dict]:
        stmt = select(Appointment, Pet.name, Client.full_name).join(
            Pet, Appointment.pet_id == Pet.pet_id
        ).join(
            Client, Appointment.client_id == Client.client_id
        ).where(
            Appointment.status.ilike(f"%{filter_term}%")
        )

        results = self.session.exec(stmt).all()

        appointments = []
        for appointment, client_name, pet_name in results:
            appointment_dict = appointment.model_dump()
            appointment_dict["pet_name"] = pet_name
            appointment_dict["client_name"] = client_name
            appointments.append(appointment_dict)

        return appointments
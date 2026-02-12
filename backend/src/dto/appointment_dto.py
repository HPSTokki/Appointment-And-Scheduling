from pydantic import BaseModel
from datetime import datetime

class InsertClient(BaseModel):
    full_name: str
    mobile_no: str | None = None
    tel_no: str | None = None
    preferred_contact_method: str = "Mobile Number"
    email: str
    address: str

class ResponseClient(BaseModel):
    client_id: int
    full_name: str
    mobile_no: str | None = None
    tel_no: str | None = None
    preferred_contact_method: str = "Mobile Number"
    email: str
    address: str
    is_new_client: bool
    created_at: datetime

class InsertPet(BaseModel):
    client_id: int
    name: str
    breed: str
    species_type: str
    is_spayed_neutered: bool
    weight_kg: float | None = None
    date_of_birth: datetime
    sex: str

class ResponsePet(BaseModel):
    pet_id: int
    client_id: int
    name: str
    breed: str
    species_type: str
    is_spayed_neutered: bool
    weight_kg: float | None = None
    date_of_birth: datetime
    sex: str
    created_at: datetime

class InsertAppointment(BaseModel):
    pet_id: int
    client_id: int
    appointment_date: datetime
    visit_type_code: str
    chief_complaint: str
    booking_source: str

class ResponseAppointment(BaseModel):
    pet_id: int
    client_id: int
    appointment_id: int
    appointment_date: datetime
    visit_type_code: str
    chief_complaint: str
    booking_source: str
    status: str
    created_at: datetime

    pet_name: str | None = None
    client_name: str | None = None

class UpdateAppointment(BaseModel):
    appointment_date: datetime | None = None
    visit_type_code: str | None = None
    chief_complaint: str | None = None
    status: str | None = None

class NewClientBooking(BaseModel):
    client: InsertClient
    pet: InsertPet
    appointment: InsertAppointment



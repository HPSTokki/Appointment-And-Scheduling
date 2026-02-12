from sqlmodel import SQLModel, Field
from sqlalchemy import String
from datetime import datetime

class Client(SQLModel, table=True):
    __tablename__ = "clients"

    client_id: int = Field(default=None, primary_key=True)
    full_name: str = Field(sa_type=String)
    mobile_no: str | None = Field(sa_type=String, default=None) 
    tel_no: str | None = Field(sa_type=String, default=None)
    preferred_contact_method: str = Field(sa_type=String, default="Mobile Number")
    email: str = Field(sa_type=String)
    address: str = Field(sa_type=String)
    is_new_client: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Pet(SQLModel, table=True):
    __tablename__ = "pets"

    pet_id: int = Field(default=None, primary_key=True)
    client_id: int = Field(default=None, foreign_key="clients.client_id")
    name: str = Field(sa_type=String)
    breed: str = Field(sa_type=String)
    species_type: str = Field(sa_type=String)
    is_spayed_neutered: bool = Field(default=False)
    weight_kg: float | None = None
    date_of_birth: datetime
    sex: str = Field(sa_type=String)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Appointment(SQLModel, table=True):
    __tablename__ = "appointments"

    appointment_id: int = Field(default=None, primary_key=True)
    pet_id: int = Field(default=None, foreign_key="pets.pet_id")
    client_id: int = Field(default=None, foreign_key="clients.client_id")
    appointment_date: datetime
    visit_type_code: str = Field(sa_type=String)
    chief_complaint: str = Field(sa_type=String)
    booking_source: str = Field(sa_type=String)
    status: str = Field(sa_type=String)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)



    
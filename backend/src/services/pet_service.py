from sqlmodel import select, Session
from src.models.appointment_model import Pet
from src.dto.appointment_dto import InsertPet, UpdatePet

class PetService():
    def __init__(self, session: Session):
        self.session = session

    def create_pet(self, pet_data: InsertPet) -> Pet:
        pet = Pet.model_validate(pet_data)
        self.session.add(pet)
        self.session.commit()
        self.session.refresh(pet)
        return pet
    
    def get_one_pet(self, pet_id: int) -> Pet:
        pet = self.session.get(Pet, pet_id)
        return pet
    
    def get_all_pet(self) -> list[Pet]:
        stmt = select(Pet)
        return self.session.exec(stmt).all()

    def update_pet(self, pet_id: int, update_pet_data: UpdatePet) -> Pet:
        pet = self.session.get(Pet, pet_id)
        
        if not pet:
            return None

        updated_pet_data = update_pet_data.model_dump(exclude_unset=True)

        for key, value in updated_pet_data.items():
            setattr(pet, key, value)

        self.session.commit()
        self.session.refresh(pet)

        return pet
    
    def get_pets_by_name(self, search_term: str) -> list[Pet]:
        stmt = select(Pet).where(
            Pet.name.ilike(f"%{search_term}%")
        )

        return self.session.exec(stmt).all()



from src.dto.appointment_dto import InsertPet, ResponsePet, ListResponsePet, UpdatePet
from src.services.pet_service import PetService
from fastapi import APIRouter, HTTPException
from src.engine import SessionDep

router = APIRouter(prefix="/pet", tags=["Pets"])

@router.post("/", response_model=ResponsePet)
def create_pet(session: SessionDep, pet_data: InsertPet):
    service = PetService(session)
    pet = service.create_pet(pet_data)
    return pet

@router.get("/", response_model=ListResponsePet)
def get_all_pet(session: SessionDep):
    service = PetService(session)
    pets = service.get_all_pet()
    return {
        "pets": pets
    }

@router.get("/search-pet", response_model=ListResponsePet)
def get_pets_by_name(session: SessionDep, search_term: str):
    service = PetService(session)
    pets = service.get_pets_by_name(search_term)
    if not pets:
        raise HTTPException(status=404, detail=f"Pets with name: {search_term}, doesn't exists")
    return {
        "pets": pets
    }

@router.get("/client/{client_id}", response_model=ListResponsePet)
def get_pets_by_client_id(session: SessionDep, client_id: int):
    service = PetService(session)
    pets = service.get_pets_by_client_id(client_id)
    return {
        "pets": pets
    }

@router.get("/{pet_id}", response_model=ResponsePet)
def get_one_pet(session: SessionDep, pet_id: int):
    service = PetService(session)
    pet = service.get_one_pet(pet_id)
    if not pet:
        raise HTTPException(status=404, detail="Pet Not Found")
    return pet

@router.put("/{pet_id}", response_model=ResponsePet)
def update_pet(session: SessionDep, pet_id: int, update_pet_data: UpdatePet):
    service = PetService(session)
    pet = service.update_pet(pet_id, update_pet_data)
    if not pet:
        raise HTTPException(status=404, detail="Failed to update pet data")
    return pet
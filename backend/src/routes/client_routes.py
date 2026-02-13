from src.dto.appointment_dto import ListResponseClient, ResponseClient, InsertClient, UpdateClient
from src.services.client_service import ClientService
from fastapi import HTTPException, APIRouter
from src.engine import SessionDep

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/", response_model=ResponseClient)
def create_client(session: SessionDep, client_data: InsertClient):
    service = ClientService(session)
    client = service.create_client(client_data)
    return client

@router.get("/", response_model=ListResponseClient)
def get_all_client(session: SessionDep):
    service = ClientService(session)
    clients = service.get_all_client()
    return {
        "clients": clients
    }

@router.get("/{client_id}", response_model=ResponseClient)
def get_one_client(session: SessionDep, client_id: int):
    service = ClientService(session)
    client = service.get_one_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found!")
    return client

@router.put("/{client_id}", response_model=ResponseClient)
def update_client(session: SessionDep, client_id: int, update_client_data: UpdateClient):
    service = ClientService(session)
    client = service.update_client(client_id, update_client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Update Failed")
    return client

@router.get("/search-client/", response_model=ListResponseClient)
def get_clients_by_name(session: SessionDep, search_term: str):
    service = ClientService(session)
    clients = service.get_clients_by_name(search_term)
    if not clients:
        raise HTTPException(status_code=404, detail=f"No Clients Found with name: {search_term}")
    return {
        "clients": clients
    }

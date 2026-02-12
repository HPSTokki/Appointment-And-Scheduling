from src.dto.appointment_dto import ListResponseClient, ResponseClient, InsertClient
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

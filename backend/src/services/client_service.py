from sqlmodel import select, Session
from src.models.appointment_model import Client
from src.dto.appointment_dto import InsertClient, ResponseClient

class ClientService():
    def __init__(self, session: Session):
        self.session = session

    def create_client(self, client_data: InsertClient) -> Client:
        client = Client.model_validate(client_data)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client
    
    def get_one_client(self, client_id: int) -> Client:
        client = self.session.get(Client, client_id)
        return client
    
    def get_all_client(self) -> list[Client]:
        stmt = select(Client)
        return self.session.exec(stmt).all()

    
    
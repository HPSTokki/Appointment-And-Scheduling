from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated, Generator
from pathlib import Path
from dotenv import load_dotenv

import os

load_dotenv()

BASE_PATH = Path(__file__).resolve()
LOCAL_DB_PATH = BASE_PATH / "local.db" # This is local sqlite path directed to be placed beside engine

sqlite_url = f"sqlite:///{LOCAL_DB_PATH}"
supabase_url = os.getenv("SUPABASE_URL")

# Option only for if using sqlite/local db
connect_args = {
    "check_same_thread": False
}

engine = create_engine(supabase_url, echo=True)

def get_session() -> Generator[SQLModel, None, None]:
    with Session(engine) as session:
        yield session

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import client_routes, pet_routes, appointment_routes

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(client_routes.router)
app.include_router(pet_routes.router)
app.include_router(appointment_routes.router)

@app.get("/")
def get_root():
    return {
        "ok": True
    }
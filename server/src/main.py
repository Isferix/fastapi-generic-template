from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .ports.api import api
from .settings import get_settings

settings = get_settings()

server = FastAPI()

origins = [
    "https://localhost:8000",
    "https://0.0.0.0:8000",
]

# Configurar el middleware CORS
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

server.include_router(api)

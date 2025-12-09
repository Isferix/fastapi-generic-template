import asyncio

from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from fastapi import Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from .src.db.repositories.cliente_repo import SqliteRepositorioCliente
from settings import get_settings



# from .db.scripts.db import get_enum_repo, get_basic_repo, get_cliente_repo, get_clientes_folder_repo, get_medio_pago_repo

# from src.domain.models.basic import *
# from src.domain.models.master import *
# from src.domain.models.cliente import *

# from src.application.queries.report_cliente import DashBoardCliente

# from .api.events import event_bus

settings = get_settings()

# env = Environment(loader=FileSystemLoader('./web/dynamic'))
app = FastAPI(lifespan=lifespan)

origins = [
    f"https://{settings.HOST_IP}:{settings.HOST_PORT}",
    f"https://localhost:8000",
    f"https://0.0.0.0:8000",
]

# Configurar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
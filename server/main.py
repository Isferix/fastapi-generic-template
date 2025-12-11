from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import get_settings

settings = get_settings()

app = FastAPI()

origins = [
    f"https://{settings.HOST_IP}:{settings.HOST_PORT}",
    "https://localhost:8000",
    "https://0.0.0.0:8000",
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

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, SecretStr, ValidationError

# --- Helper para secretos ---
BASE_SECRET_PATH = "/run/secrets"


# --- Configuración tipada ---
class AppSettings(BaseModel):
    # Variables de control
    ENV: str = Field("dev", description="Modo de ejecución: dev o prod")
    SECRET_PREFIX: str = Field(
        "", description="Prefijo opcional para secretos de Docker"
    )

    # Variables tipadas del servicio
    DB_ADAPTER: str = Field("in-memory", description="Adaptador de base de datos")
    DB_URI: Optional[str | SecretStr] = Field(
        None, description="URI de conexión a la base de datos"
    )


def get_secret(secret_name: str) -> Optional[str | SecretStr]:
    """Lee un secreto desde /run/secrets/{secret_name} si existe."""
    secret_path = Path(f"{BASE_SECRET_PATH}/{secret_name}")
    if secret_path.exists():
        return secret_path.read_text().strip()
    return None


# --- Funciones para pipeline modular ---
def set_secret_config(values: dict, prefix: str = ""):
    for key in values.keys():
        secret_name = f"{prefix}{key.lower()}"
        val = get_secret(secret_name)
        if val:
            values[key] = val


def set_env_vars(values: dict):
    for key in values.keys():
        if key in os.environ:
            values[key] = os.environ[key]


def set_dotenv_config(values: dict, env_mode: str = "dev"):
    env_path = (
        Path(f".env.{env_mode}") if Path(f".env.{env_mode}").exists() else Path(".env")
    )
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() in values and not values[k.strip()]:
                    values[k.strip()] = v.strip()


SETTINGS: AppSettings | None = None

# --- Pipeline definido ---
PIPELINES = {
    "dev": ("env_file", "env_vars", "secrets"),
    "default": ("secrets", "env_vars", "env_file"),
}

FUNCTIONS = {
    "secrets": set_secret_config,
    "env_vars": set_env_vars,
    "env_file": set_dotenv_config,
}


# --- Loader ---
def load_settings() -> None:
    """Ejecuta el pipeline para construir un dict con todas las variables."""
    # Valores iniciales (vacíos)
    values: dict[str, str | SecretStr] = {
        field: "" for field in AppSettings.model_fields.keys()
    }

    env_mode = os.getenv("ENV", "dev").lower()
    prefix = os.getenv("SECRET_PREFIX", "")

    for source in PIPELINES.get(env_mode, PIPELINES["default"]):
        if source == "secrets":
            FUNCTIONS[source](values, prefix)
        elif source == "env_file":
            FUNCTIONS[source](values, env_mode)
        else:
            FUNCTIONS[source](values)

    global SETTINGS
    valid = AppSettings.model_validate(values)
    if not valid:
        raise ValidationError("Error en configuración tipada")
    SETTINGS = valid


# --- Singleton cacheado ---
@lru_cache()
def get_settings() -> AppSettings:
    try:
        global SETTINGS
        if not SETTINGS:
            load_settings()
        return SETTINGS
    except ValidationError as e:
        raise RuntimeError(f"Error en configuración tipada: {e}")


# --- Ejemplo ---
if __name__ == "__main__":
    get_settings()
    print(SETTINGS)  # type: ignore

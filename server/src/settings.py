from functools import lru_cache

from pydantic import BaseModel, SecretStr
from pydantic_settings import (
    BaseSettings,
    NestedSecretsSettingsSource,
    SettingsConfigDict,
)


class AppSettings(BaseModel):
    pass


class DbSettings(BaseModel):
    adapter: str
    db_uri: SecretStr


class Settings(BaseSettings):
    app: AppSettings
    db: DbSettings

    model_config = SettingsConfigDict(
        env_prefix="MY_",
        env_nested_delimiter="__",
        secrets_dir="secrets",
        secrets_nested_delimiter="_",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            NestedSecretsSettingsSource(file_secret_settings),
        )


@lru_cache
def get_settings():
    return Settings()

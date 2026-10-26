from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# Proje ana dizinini (Root) dinamik olarak bulur (Windows/Linux fark etmeksizin çalışır)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT_DIR / "configs" / "config.yaml"


class DataConfig(BaseModel):
    raw_path: str
    processed_train_path: str
    processed_test_path: str
    test_size: float
    random_state: int


class ModelConfig(BaseModel):
    target_column: str
    experiment_name: str
    xgb_params: Dict[str, Any]


class AppConfig(BaseModel):
    project_name: str
    version: str
    data: DataConfig
    model: ModelConfig


class EnvSettings(BaseSettings):
    ENVIRONMENT: str = "development"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    MLFLOW_TRACKING_URI: str

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """SQLAlchemy için PostgreSQL bağlantı cümlesini dinamik üretir."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


def load_yaml_config(path: Path = CONFIG_PATH) -> AppConfig:
    """YAML dosyasını okur ve Pydantic şemasıyla doğrular."""
    if not path.exists():
        raise FileNotFoundError(f"Konfigürasyon dosyası bulunamadı: {path}")
    with open(path, "r", encoding="utf-8") as file:
        raw_config = yaml.safe_load(file)
    return AppConfig(**raw_config)


# Projenin her yerinden doğrudan import edip kullanacağımız tekil (Singleton) nesneler
env_settings = EnvSettings()
app_config = load_yaml_config()
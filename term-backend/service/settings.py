from datetime import timedelta
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseSettings):
    S3_URI: str
    S3_USER: str
    S3_PASSWORD: str

    BIM_BUCKET: str = "bim-forge"
    DOCUMENTS_BUCKET: str = "doc-forge"


class InfluxDBSettings(BaseSettings):
    INFLUXDB_URL: str
    INFLUXDB_TOKEN: str
    INFLUXDB_ORG: str

    INFLUXDB_SENSORS_BUCKET: str = "sensor-bucket"


class Settings(S3Settings, InfluxDBSettings):
    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = True

    ENVIRONMENT: str = "dev"

    SERVICE_VERSION: str = "0.1.0"

    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str
    JWT_SECRET: str
    USER_SESSION_LIFETIME_SECONDS: int = timedelta(hours=1).seconds

    POSTGRES_SERVERS: PostgresDsn

    XML_SCHEMA_PATH: Path = Path("artifacts/explanatorynote-01-03.xsd")
    UNITS_MAP_PATH: Path = Path("artifacts/units.json")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

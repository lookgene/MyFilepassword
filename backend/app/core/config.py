"""Core configuration module."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "FilePassword"
    app_env: Literal["development", "staging", "production"] = "development"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = Field(..., min_length=32)

    # API
    api_v1_prefix: str = "/api/v1"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # Database
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/filepassword"
    )
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_pool_recycle: int = 3600

    @property
    def async_database_url(self) -> str:
        """Convert database URL to async version."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_decode_responses: bool = True

    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    # Storage
    storage_provider: Literal["minio", "oss", "s3"] = "minio"
    storage_endpoint: str = "localhost:9000"
    storage_access_key: str = "minioadmin"
    storage_secret_key: str = "minioadmin"
    storage_bucket: str = "filepassword"
    storage_use_ssl: bool = False
    storage_region: str = "us-east-1"

    # JWT
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""
    smtp_from_name: str = "FilePassword"

    # SMS
    sms_access_key: str = ""
    sms_secret_key: str = ""
    sms_sign_name: str = ""
    sms_template_code: str = ""

    # WeChat Pay
    wechat_pay_mchid: str = ""
    wechat_pay_api_v3_key: str = ""
    wechat_pay_serial_no: str = ""
    wechat_pay_private_key_path: str = ""
    wechat_pay_certificate_path: str = ""
    wechat_pay_notify_url: str = ""

    # Alipay
    alipay_appid: str = ""
    alipay_private_key: str = ""
    alipay_public_key: str = ""
    alipay_notify_url: str = ""

    # Celery
    celery_broker_url: str = "amqp://guest:guest@localhost:5672/"
    celery_result_backend: str = "redis://localhost:6379/1"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 100

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # File Upload
    upload_max_file_size: int = 2 * 1024 * 1024 * 1024  # 2GB
    upload_allowed_extensions: list[str] = [
        "zip",
        "rar",
        "7z",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
    ]
    upload_chunk_size: int = 8 * 1024 * 1024  # 8MB

    # Virus Scan
    virus_scan_enabled: bool = True
    virus_scan_host: str = "localhost"
    virus_scan_port: int = 3310

    # Crack Engine
    crack_worker_dir: str = "/tmp/crack"
    crack_max_concurrent_tasks: int = 10
    crack_task_timeout: int = 7 * 24 * 60 * 60  # 7 days

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["json", "text"] = "json"

    # Sentry
    sentry_dsn: str = ""
    sentry_environment: str = "development"
    sentry_traces_sample_rate: float = 1.0

    # Prometheus
    prometheus_enabled: bool = True

    # Frontend
    frontend_url: str = "http://localhost:3000"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

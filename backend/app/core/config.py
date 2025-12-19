from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 应用基本配置
    APP_NAME: str = "在线加密文件解密服务"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/file_decryption"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # RabbitMQ配置
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # 文件存储配置
    FILE_STORAGE_PATH: str = "./uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # 破解引擎配置
    HASHCAT_PATH: str = "/usr/bin/hashcat"
    MAX_CRACK_TIME: int = 7 * 24 * 60 * 60  # 7天
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

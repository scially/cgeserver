from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    PROJECT_NAME: str  = "CGEServer"
    PROJECT_PORT: int  = 9000
    DATABASE_NAME: str = "cgeserver.db"
    DATABASE_URL: str  = f"sqlite:///{DATABASE_NAME}"

    PRODUCTION: bool = True

    SECRET_KEY: str = "09d25e094aaa6ca2556d818166b7a9563b93f7199f6f0f4caa6cf63b88e8d3f2"
    SECRET_ALGORITHM: str = "HS256"
    SECRET_TOKEN_EXPIRE_MINUTES: int = 10

settings = Settings()
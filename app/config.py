from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    PROJECT_NAME: str  = "CGEServer"
    PROJECT_PORT: int  = 9000
    DATABASE_NAME: str = "cgeserver.db"
    DATABASE_URL: str  = f"sqlite:///{DATABASE_NAME}"

    PRODUCTION: bool = False


settings = Settings()
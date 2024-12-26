from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_TOKEN: str = "your-jwt-secret-key"
    JWT_REFRESH_TOKEN: str = "your-jwt-refresh-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://postgres:MDJiJRpYPofUEWBSkCRMRBSgPGugqSrT@autorack.proxy.rlwy.net:42994/railway"

    class Config:
        env_file = ".env"

settings = Settings()

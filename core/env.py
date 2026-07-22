from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ML_SERVICE_URL: str
    AUTH_SERVICE_URL: str
    CRYPTO_SERVICE_URL: str
    API_KEY: str
    FIREBASE_CREDENTIALS_PATH: str = ""

    # Cargar explícitamente desde el .env del backend
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()

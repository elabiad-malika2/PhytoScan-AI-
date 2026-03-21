from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Ajouter pour Postgres
    POSTGRES_USER: str =None
    POSTGRES_PASSWORD: str=None
    POSTGRES_DB: str=None
    POSTGRES_HOST: str=None
    POSTGRES_PORT: int=None

    GEMINI_API_KEY:str
    GROQ_API_KEY: str

    MLFLOW_TRACKING_URI:str
    OPENAI_API_KEY:str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
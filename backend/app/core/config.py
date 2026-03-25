from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Optionnel si DATABASE_URL pointe ailleurs (ex. SQLite en tests / CI)
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None

    GEMINI_API_KEY:str
    GROQ_API_KEY: str

    MLFLOW_TRACKING_URI:str
    OPENAI_API_KEY:str

    # Racine des données (uploads, rapports, modèles). Docker : /app/data ; CI : chemin sous le workspace.
    DATA_ROOT: str = "/app/data"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
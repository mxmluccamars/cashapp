from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "CashApp API"
    API_V1_STR: str = "/api/v1"
    
    # URL de conexão com o banco. Por padrão, usa SQLite local.
    # Se mudar para PostgreSQL no futuro, basta alterar essa variável no .env!
    DATABASE_URL: str = "sqlite:///./cashapp.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
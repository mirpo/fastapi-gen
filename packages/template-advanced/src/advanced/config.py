from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    secret_key: str
    # TODO: Point at PostgreSQL for production, e.g.
    # DATABASE_URL="postgresql://user:password@localhost/dbname"
    database_url: str = "sqlite:///./app.db"
    # Origins allowed to call this API from a browser.
    # Set as a JSON list, e.g. CORS_ORIGINS='["https://app.example.com"]'
    cors_origins: list[str] = ["http://localhost:3000"]
    # Where uploaded files are stored; TODO: replace with cloud storage (S3, GCS)
    upload_dir: str = "uploads"


settings = Settings()

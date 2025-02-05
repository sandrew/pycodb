from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration for interacting with NocoDB.

    Loads environment variables from the .env file
    or system environment variables. Uses Pydantic for data validation.
    """

    NOCO_URL: str
    NOCO_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

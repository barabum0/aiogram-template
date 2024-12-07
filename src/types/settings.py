from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )
    mongodb_url: str
    mongodb_name: str
    bot_token: str


settings = Settings()

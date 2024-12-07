from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )
    bot_token: str


settings = Settings()  # type: ignore[call-arg]

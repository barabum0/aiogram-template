from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from src.types.settings import settings


async def initialize_database() -> None:
    logger.info("Initialising database...")

    await init_beanie(
        database=AsyncIOMotorClient(settings.mongodb_url).get_database(settings.mongodb_name), document_models=[]
    )

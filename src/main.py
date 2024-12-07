from aiogram import Bot as AiogramBot
from aiogram import Dispatcher
from aiogram.types import Update
from loguru import logger

from src.router import router
from src.services.logging import configure_logger
from src.services.middlewares.logging import logger_middleware
from src.types.settings import settings

dispatcher = Dispatcher()


async def on_startup(bot: AiogramBot) -> None:
    me = await bot.get_me()

    logger.info("Starting bot {bot_name}", bot_name=me.full_name)


@dispatcher.update()
async def on_update(event: Update) -> None:
    """Test-handler for logs"""


def main() -> None:
    configure_logger()
    main_bot = AiogramBot(token=settings.bot_token)

    dispatcher.update.middleware(logger_middleware)
    dispatcher.startup.register(on_startup)

    dispatcher.include_router(router)

    dispatcher.run_polling(
        main_bot,
        # all for testing purposes
        allowed_updates=[
            "message",
            "edited_message",
            "channel_post",
            "edited_channel_post",
            "inline_query",
            "chosen_inline_result",
            "callback_query",
            "shipping_query",
            "pre_checkout_query",
            "poll",
            "poll_answer",
            "my_chat_member",
            "chat_member",
            "chat_join_request",
            "message_reaction",
            "message_reaction_count",
            "chat_boost",
            "removed_chat_boost",
            "deleted_business_messages",
            "business_connection",
            "edited_business_message",
            "business_message",
            "purchased_paid_media",
        ],
    )


if __name__ == "__main__":
    main()

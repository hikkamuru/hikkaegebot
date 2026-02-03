"""
Telegram-бот для подготовки к ЕГЭ по профильной математике
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start_router, practice_router, profile_router, top_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Set BOT_TOKEN environment variable or edit .env file")
        sys.exit(1)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(start_router)
    dp.include_router(practice_router)
    dp.include_router(profile_router)
    dp.include_router(top_router)

    logger.info("Starting EGE Math Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

"""
Telegram-бот для подготовки к ЕГЭ по профильной математике
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start_router, practice_router, profile_router, top_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Запуск бота"""
    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.error("Не указан токен бота! Укажите BOT_TOKEN в файле .env")
        return
    
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(practice_router)
    dp.include_router(profile_router)
    dp.include_router(top_router)
    
    # Запуск бота
    logger.info("Бот запущен!")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

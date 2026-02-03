"""
Обработчик команды /start
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import START_MESSAGE
from database import db
from keyboards import get_main_keyboard

router = Router()

# Хранилище для отслеживания состояния пользователей
user_sessions = {}


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Создаем пользователя в базе данных, если его нет
    if not db.user_exists(user_id):
        db.create_user(user_id, username, first_name)
    
    # Инициализируем сессию пользователя
    user_sessions[user_id] = {
        "is_training": False,
        "tasks": [],
        "current_task_index": 0,
        "score": 0,
        "correct": 0,
        "wrong": 0
    }
    
    await message.answer(
        START_MESSAGE,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏠 Главное меню")
@router.message(F.text == "/menu")
async def cmd_menu(message: Message):
    """Показать главное меню"""
    user_id = message.from_user.id
    
    # Сбрасываем сессию пользователя
    if user_id in user_sessions:
        user_sessions[user_id]["is_training"] = False
    
    await message.answer(
        "📚 <b>Главное меню</b>\n\nВыберите действие:",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

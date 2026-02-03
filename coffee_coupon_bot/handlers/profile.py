"""
Обработчик профиля пользователя
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from config import PROFILE_MESSAGE
from database import db
from keyboards import get_main_keyboard

router = Router()


@router.message(Command("profile"))
@router.message(F.text == "📊 Моя статистика")
async def cmd_profile(message: Message):
    """Показать профиль пользователя"""
    user_id = message.from_user.id
    
    # Получаем информацию о пользователе из базы данных
    user = db.get_user(user_id)
    
    if user is None:
        await message.answer(
            "Вы еще не начали тренировку. Нажмите /start для начала работы с ботом.",
            reply_markup=get_main_keyboard()
        )
        return
    
    # user = (user_id, username, first_name, points, correct_answers, wrong_answers, total_questions, created_at, updated_at)
    points = user[3]
    correct = user[4]
    wrong = user[5]
    total = user[6]
    
    # Вычисляем процент успеха
    if total > 0:
        percentage = round(correct / total * 100, 1)
    else:
        percentage = 0
    
    # Формируем имя пользователя
    username = user[2] if user[2] else "Пользователь"
    if user[1]:
        username = f"@{user[1]}"
    
    text = PROFILE_MESSAGE.format(
        points=points,
        correct=correct,
        wrong=wrong,
        percentage=percentage,
        total=total
    )
    
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

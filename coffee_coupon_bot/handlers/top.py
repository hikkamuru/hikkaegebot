"""
Обработчик топа пользователей
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from config import TOP_MESSAGE
from database import db
from keyboards import get_main_keyboard

router = Router()


@router.message(Command("top"))
@router.message(F.text == "🏆 Топ пользователей")
async def cmd_top(message: Message):
    """Показать топ пользователей"""
    user_id = message.from_user.id
    
    # Получаем топ пользователей
    top_users = db.get_top_users(10)
    
    # Получаем место текущего пользователя
    user_place = db.get_user_place(user_id)
    user = db.get_user(user_id)
    
    if not top_users:
        await message.answer(
            "Пока нет пользователей в топе. Будьте первым! 🎯",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Формируем список топа
    top_list = ""
    for i, user_data in enumerate(top_users, 1):
        # user_data = (user_id, username, first_name, points, correct_answers)
        username = user_data[1] if user_data[1] else user_data[2]
        points = user_data[3]
        
        medal = ""
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = f"{i}."
        
        top_list += f"{medal} {username} — {points} очков\n"
    
    # Получаем очки текущего пользователя
    user_points = user[3] if user else 0
    
    text = TOP_MESSAGE.format(
        top_list=top_list,
        user_place=user_place,
        user_points=user_points
    )
    
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

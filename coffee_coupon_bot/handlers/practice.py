"""
Обработчик тренировок
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import (
    CORRECT_ANSWER_MESSAGE,
    INCORRECT_ANSWER_MESSAGE,
    TRAINING_STARTED_MESSAGE,
    TRAINING_STOPPED_MESSAGE,
    NO_MORE_QUESTIONS_MESSAGE,
    POINTS_FOR_CORRECT_ANSWER
)
from database import db
from keyboards import get_main_keyboard, get_answer_keyboard, get_practice_keyboard, get_restart_keyboard
from fipi_data.tasks import math_tasks

router = Router()

# Хранилище сессий пользователей (глобально из start.py)
user_sessions = {}


async def send_next_question(user_id: int, callback: CallbackQuery = None, message: Message = None):
    """Отправить следующий вопрос пользователю"""
    if user_id not in user_sessions:
        return
    
    session = user_sessions[user_id]
    
    if session["current_task_index"] >= len(session["tasks"]):
        # Все вопросы отвечены
        await show_final_results(user_id, callback or message)
        return
    
    current_task = session["tasks"][session["current_task_index"]]
    
    text = f"📝 <b>Задание {session['current_task_index'] + 1} из {len(session['tasks'])}</b>\n\n"
    text += f"📌 <b>{current_task['topic']}</b>\n\n"
    text += f"{current_task['question']}\n\n"
    text += f"🏆 Счёт: {session['score']} очков"
    
    if callback:
        await callback.message.edit_text(
            text,
            reply_markup=get_answer_keyboard(current_task["answers"]),
            parse_mode="HTML"
        )
    elif message:
        await message.answer(
            text,
            reply_markup=get_answer_keyboard(current_task["answers"]),
            parse_mode="HTML"
        )


async def show_final_results(user_id: int, target):
    """Показать финальные результаты"""
    session = user_sessions[user_id]
    
    # Обновляем статистику пользователя в базе
    user = db.get_user(user_id)
    
    if session["correct"] + session["wrong"] > 0:
        percentage = round(session["correct"] / (session["correct"] + session["wrong"]) * 100, 1)
    else:
        percentage = 0
    
    text = NO_MORE_QUESTIONS_MESSAGE.format(
        correct=session["correct"],
        wrong=session["wrong"],
        percentage=percentage,
        total_points=session["score"]
    )
    
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=get_restart_keyboard(), parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=get_restart_keyboard(), parse_mode="HTML")
    
    session["is_training"] = False


@router.message(Command("practice"))
@router.message(F.text == "🎯 Начать тренировку")
async def cmd_practice(message: Message):
    """Начать тренировку"""
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "is_training": False,
            "tasks": [],
            "current_task_index": 0,
            "score": 0,
            "correct": 0,
            "wrong": 0
        }
    
    session = user_sessions[user_id]
    
    # Получаем случайные задания
    session["tasks"] = math_tasks.get_random_tasks(10)
    session["current_task_index"] = 0
    session["score"] = 0
    session["correct"] = 0
    session["wrong"] = 0
    session["is_training"] = True
    
    text = TRAINING_STARTED_MESSAGE.format(
        total=len(session["tasks"]),
        score=session["score"]
    )
    
    await message.answer(text, parse_mode="HTML")
    
    # Отправляем первый вопрос
    await send_next_question(user_id, message=message)


@router.message(Command("stop"))
@router.message(F.text == "🛑 Остановить")
async def cmd_stop(message: Message):
    """Остановить тренировку"""
    user_id = message.from_user.id
    
    if user_id in user_sessions:
        session = user_sessions[user_id]
        
        if session["correct"] + session["wrong"] > 0:
            percentage = round(session["correct"] / (session["correct"] + session["wrong"]) * 100, 1)
        else:
            percentage = 0
        
        text = TRAINING_STOPPED_MESSAGE.format(
            correct=session["correct"],
            wrong=session["wrong"],
            percentage=percentage,
            total_points=session["score"]
        )
        
        session["is_training"] = False
        
        await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")


@router.callback_query(F.data.startswith("answer_"))
async def callback_answer(callback: CallbackQuery):
    """Обработка ответа на задание"""
    user_id = callback.from_user.id
    
    if user_id not in user_sessions:
        await callback.message.edit_text("Начните тренировку заново /practice")
        return
    
    session = user_sessions[user_id]
    
    if not session["is_training"]:
        await callback.message.edit_text("Тренировка завершена. Начните заново /practice")
        return
    
    if session["current_task_index"] >= len(session["tasks"]):
        await callback.message.edit_text("Все задания решены!")
        return
    
    # Получаем индекс ответа
    answer_index = int(callback.data.split("_")[1])
    current_task = session["tasks"][session["current_task_index"]]
    
    # Проверяем правильность ответа
    is_correct = answer_index == current_task["correct_index"]
    
    # Обновляем сессию
    if is_correct:
        session["score"] += POINTS_FOR_CORRECT_ANSWER
        session["correct"] += 1
        
        # Обновляем базу данных
        db.update_user_stats(user_id, True)
        
        text = CORRECT_ANSWER_MESSAGE.format(
            explanation=current_task["explanation"]
        )
    else:
        session["wrong"] += 1
        
        # Обновляем базу данных
        db.update_user_stats(user_id, False)
        
        text = INCORRECT_ANSWER_MESSAGE.format(
            correct_answer=current_task["answers"][current_task["correct_index"]],
            explanation=current_task["explanation"]
        )
    
    # Добавляем в историю
    db.add_answer_to_history(user_id, current_task["id"], is_correct)
    
    # Переходим к следующему вопросу
    session["current_task_index"] += 1
    
    # Показываем результат ответа
    await callback.message.edit_text(
        text,
        parse_mode="HTML"
    )
    
    # Отправляем следующий вопрос через небольшую задержку
    import asyncio
    await asyncio.sleep(1)
    
    if session["current_task_index"] < len(session["tasks"]):
        await send_next_question(user_id, callback=callback)
    else:
        await show_final_results(user_id, callback)


@router.callback_query(F.data == "restart")
async def callback_restart(callback: CallbackQuery):
    """Перезапуск тренировки"""
    await cmd_practice(callback.message)


@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    user_id = callback.from_user.id
    
    if user_id in user_sessions:
        user_sessions[user_id]["is_training"] = False
    
    await callback.message.edit_text(
        "📚 <b>Главное меню</b>\n\nВыберите действие:",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

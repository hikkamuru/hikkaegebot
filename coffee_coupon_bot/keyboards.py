"""
Клавиатуры для Telegram-бота
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню бота"""
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="🎯 Начать тренировку"),
        KeyboardButton(text="📊 Моя статистика"),
        KeyboardButton(text="🏆 Топ пользователей"),
        KeyboardButton(text="🛑 Остановить")
    )
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


def get_answer_keyboard(answers: list) -> InlineKeyboardMarkup:
    """Клавиатура с вариантами ответов"""
    builder = InlineKeyboardBuilder()
    
    for i, answer in enumerate(answers):
        builder.add(
            InlineKeyboardButton(
                text=answer,
                callback_data=f"answer_{i}"
            )
        )
    
    builder.adjust(2)
    return builder.as_markup()


def get_practice_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора режима тренировки"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📚 Все задания", callback_data="practice_all"),
        InlineKeyboardButton(text="🎯 Задания 1-11", callback_data="practice_1_11"),
        InlineKeyboardButton(text="🔢 Задания 12-18", callback_data="practice_12_18"),
        InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")
    )
    builder.adjust(2, 2)
    return builder.as_markup()


def get_restart_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для перезапуска тренировки"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🔄 Заново", callback_data="restart"),
        InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")
    )
    builder.adjust(2)
    return builder.as_markup()

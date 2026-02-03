"""
Инициализация обработчиков
"""

from handlers.start import router as start_router
from handlers.practice import router as practice_router
from handlers.profile import router as profile_router
from handlers.top import router as top_router

__all__ = ['start_router', 'practice_router', 'profile_router', 'top_router']

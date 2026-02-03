"""
Работа с базой данных для хранения статистики пользователей
"""

import sqlite3
import os
from config import DB_PATH


class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self):
        """Инициализация подключения к базе данных"""
        self.db_path = DB_PATH
        self.conn = None
        self.cursor = None
        self.create_tables()
    
    def connect(self):
        """Установить соединение с базой данных"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Закрыть соединение с базой данных"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Создать необходимые таблицы"""
        self.connect()
        
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                points INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                wrong_answers INTEGER DEFAULT 0,
                total_questions INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица истории ответов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS answer_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_id INTEGER,
                is_correct BOOLEAN,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        self.conn.commit()
        self.close()
    
    def get_user(self, user_id):
        """Получить информацию о пользователе"""
        self.connect()
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = self.cursor.fetchone()
        self.close()
        return user
    
    def create_user(self, user_id, username, first_name):
        """Создать нового пользователя"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        self.conn.commit()
        self.close()
    
    def update_user_stats(self, user_id, correct):
        """Обновить статистику пользователя"""
        self.connect()
        if correct:
            self.cursor.execute('''
                UPDATE users SET
                    points = points + 1,
                    correct_answers = correct_answers + 1,
                    total_questions = total_questions + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
        else:
            self.cursor.execute('''
                UPDATE users SET
                    wrong_answers = wrong_answers + 1,
                    total_questions = total_questions + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
        self.conn.commit()
        self.close()
    
    def add_answer_to_history(self, user_id, task_id, is_correct):
        """Добавить запись в историю ответов"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO answer_history (user_id, task_id, is_correct)
            VALUES (?, ?, ?)
        ''', (user_id, task_id, is_correct))
        self.conn.commit()
        self.close()
    
    def get_top_users(self, limit=10):
        """Получить топ пользователей по очкам"""
        self.connect()
        self.cursor.execute('''
            SELECT user_id, username, first_name, points, correct_answers
            FROM users
            ORDER BY points DESC
            LIMIT ?
        ''', (limit,))
        top_users = self.cursor.fetchall()
        self.close()
        return top_users
    
    def get_user_place(self, user_id):
        """Получить место пользователя в топе"""
        self.connect()
        self.cursor.execute('''
            SELECT COUNT(*) + 1 FROM users WHERE points > (
                SELECT points FROM users WHERE user_id = ?
            )
        ''', (user_id,))
        place = self.cursor.fetchone()[0]
        self.close()
        return place
    
    def user_exists(self, user_id):
        """Проверить, существует ли пользователь"""
        self.connect()
        self.cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
        exists = self.cursor.fetchone() is not None
        self.close()
        return exists


# Глобальный экземпляр базы данных
db = Database()

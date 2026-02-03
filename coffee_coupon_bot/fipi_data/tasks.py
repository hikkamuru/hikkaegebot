"""
База данных заданий из банка ФИПИ для ЕГЭ по профильной математике
"""

from typing import List, Dict, Any


class MathTasks:
    """Класс с заданиями из банка ФИПИ"""
    
    def __init__(self):
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Загрузка заданий из банка ФИПИ"""
        return [
            # ЗАДАНИЕ 1 - Простейшие уравнения
            {
                "id": 1,
                "type": "multiple_choice",
                "topic": "Задание 1",
                "difficulty": "easy",
                "question": "Найдите корень уравнения: 3x - 7 = 14",
                "answers": ["5", "7", "9", "21"],
                "correct_index": 1,
                "explanation": "3x = 14 + 7 = 21, x = 21 / 3 = 7"
            },
            {
                "id": 2,
                "type": "multiple_choice",
                "topic": "Задание 1",
                "difficulty": "easy",
                "question": "Найдите корень уравнения: 2x + 5 = 17",
                "answers": ["6", "7", "8", "12"],
                "correct_index": 0,
                "explanation": "2x = 17 - 5 = 12, x = 12 / 2 = 6"
            },
            {
                "id": 3,
                "type": "multiple_choice",
                "topic": "Задание 1",
                "difficulty": "easy",
                "question": "Решите уравнение: 5x - 3 = 2x + 6",
                "answers": ["1", "2", "3", "4"],
                "correct_index": 2,
                "explanation": "5x - 2x = 6 + 3, 3x = 9, x = 3"
            },
            
            # ЗАДАНИЕ 2 - Вычисления
            {
                "id": 4,
                "type": "multiple_choice",
                "topic": "Задание 2",
                "difficulty": "easy",
                "question": "Найдите значение выражения: 2⁵",
                "answers": ["16", "32", "64", "8"],
                "correct_index": 1,
                "explanation": "2⁵ = 2 × 2 × 2 × 2 × 2 = 32"
            },
            {
                "id": 5,
                "type": "multiple_choice",
                "topic": "Задание 2",
                "difficulty": "easy",
                "question": "Вычислите: √81",
                "answers": ["7", "8", "9", "10"],
                "correct_index": 2,
                "explanation": "√81 = 9, так как 9² = 81"
            },
            {
                "id": 6,
                "type": "multiple_choice",
                "topic": "Задание 2",
                "difficulty": "easy",
                "question": "Найдите значение: log₂(8)",
                "answers": ["2", "3", "4", "8"],
                "correct_index": 1,
                "explanation": "log₂(8) = 3, так как 2³ = 8"
            },
            
            # ЗАДАНИЕ 3 - Производная и первообразная
            {
                "id": 7,
                "type": "multiple_choice",
                "topic": "Задание 6",
                "difficulty": "easy",
                "question": "На рисунке изображен график функции f(x) и касательная к нему в точке с абсциссой x₀. Найдите значение производной функции f(x) в точке x₀, если угловой коэффициент касательной равен 2.",
                "answers": ["1", "2", "3", "4"],
                "correct_index": 1,
                "explanation": "Производная функции в точке равна угловому коэффициенту касательной, то есть f'(x₀) = 2"
            },
            {
                "id": 8,
                "type": "multiple_choice",
                "topic": "Задание 6",
                "difficulty": "medium",
                "question": "Найдите производную функции f(x) = 3x² + 2x + 1",
                "answers": ["3x + 2", "6x + 2", "6x", "3x²"],
                "correct_index": 1,
                "explanation": "f'(x) = (3x²)' + (2x)' + 1' = 6x + 2"
            },
            
            # ЗАДАНИЕ 4 - Теория вероятностей
            {
                "id": 9,
                "type": "multiple_choice",
                "topic": "Задание 4",
                "difficulty": "easy",
                "question": "В урне находятся 3 белых и 5 черных шаров. Наугад достают один шар. Найдите вероятность того, что он окажется белым.",
                "answers": ["1/8", "3/8", "5/8", "3/5"],
                "correct_index": 1,
                "explanation": "Вероятность = благоприятные исходы / все исходы = 3/(3+5) = 3/8"
            },
            {
                "id": 10,
                "type": "multiple_choice",
                "topic": "Задание 4",
                "difficulty": "easy",
                "question": "Монету подбрасывают 2 раза. Какова вероятность выпадения ровно одного орла?",
                "answers": ["1/4", "1/2", "3/4", "1"],
                "correct_index": 1,
                "explanation": "Всего 4 исхода: ОО, ОР, РО, РР. Благоприятные: ОР, РО = 2/4 = 1/2"
            },
            
            # ЗАДАНИЕ 5 - Уравнения (задания 12-18)
            {
                "id": 11,
                "type": "multiple_choice",
                "topic": "Задание 12",
                "difficulty": "medium",
                "question": "Решите уравнение: log₃(x - 2) = 2",
                "answers": ["5", "7", "9", "11"],
                "correct_index": 2,
                "explanation": "x - 2 = 3² = 9, x = 11"
            },
            {
                "id": 12,
                "type": "multiple_choice",
                "topic": "Задание 12",
                "difficulty": "medium",
                "question": "Решите уравнение: 2ˣ = 8",
                "answers": ["2", "3", "4", "5"],
                "correct_index": 1,
                "explanation": "2ˣ = 2³, значит x = 3"
            },
            
            # ЗАДАНИЕ 6 - Неравенства
            {
                "id": 13,
                "type": "multiple_choice",
                "topic": "Задание 14",
                "difficulty": "medium",
                "question": "Решите неравенство: 2x + 5 > 7",
                "answers": ["x > 1", "x > 2", "x > 0", "x > 3"],
                "correct_index": 0,
                "explanation": "2x > 7 - 5 = 2, x > 1"
            },
            {
                "id": 14,
                "type": "multiple_choice",
                "topic": "Задание 14",
                "difficulty": "medium",
                "question": "Решите неравенство: 3x - 2 ≤ 10",
                "answers": ["x ≤ 3", "x ≤ 4", "x ≤ 5", "x ≤ 6"],
                "correct_index": 1,
                "explanation": "3x ≤ 10 + 2 = 12, x ≤ 4"
            },
            
            # ЗАДАНИЕ 7 - Текстовые задачи
            {
                "id": 15,
                "type": "multiple_choice",
                "topic": "Задание 8",
                "difficulty": "easy",
                "question": "Автомобиль проехал 300 км за 5 часов. Какова его средняя скорость?",
                "answers": ["40 км/ч", "50 км/ч", "60 км/ч", "70 км/ч"],
                "correct_index": 2,
                "explanation": "Средняя скорость = расстояние / время = 300 / 5 = 60 км/ч"
            },
            {
                "id": 16,
                "type": "multiple_choice",
                "topic": "Задание 8",
                "difficulty": "easy",
                "question": "Цена товара была 500 рублей. После скидки 20% цена стала:",
                "answers": ["350 руб.", "400 руб.", "450 руб.", "480 руб."],
                "correct_index": 1,
                "explanation": "Скидка = 500 × 0.20 = 100 руб. Новая цена = 500 - 100 = 400 руб."
            },
            
            # ЗАДАНИЕ 8 - Графики и диаграммы
            {
                "id": 17,
                "type": "multiple_choice",
                "topic": "Задание 9",
                "difficulty": "easy",
                "question": "На графике показана зависимость скорости автомобиля от времени. В какой момент времени скорость была максимальной?",
                "answers": ["t = 1 с", "t = 2 с", "t = 3 с", "t = 4 с"],
                "correct_index": 2,
                "explanation": "По графику максимальная скорость достигается при t = 3 с"
            },
            
            # ЗАДАНИЕ 9 - Планиметрия
            {
                "id": 18,
                "type": "multiple_choice",
                "topic": "Задание 3",
                "difficulty": "easy",
                "question": "В треугольнике ABC угол A = 60°, угол B = 60°. Найдите угол C.",
                "answers": ["30°", "45°", "60°", "90°"],
                "correct_index": 2,
                "explanation": "Сумма углов треугольника = 180°. Угол C = 180° - 60° - 60° = 60°"
            },
            {
                "id": 19,
                "type": "multiple_choice",
                "topic": "Задание 3",
                "difficulty": "easy",
                "question": "Прямоугольный треугольник с катетами 3 и 4. Найдите гипотенузу.",
                "answers": ["5", "6", "7", "8"],
                "correct_index": 0,
                "explanation": "По теореме Пифагора: гипотенуза = √(3² + 4²) = √25 = 5"
            },
            
            # ЗАДАНИЕ 10 - Стереометрия
            {
                "id": 20,
                "type": "multiple_choice",
                "topic": "Задание 8",
                "difficulty": "medium",
                "question": "Объём куба с ребром 5 равен:",
                "answers": ["25", "50", "75", "125"],
                "correct_index": 3,
                "explanation": "Объём куба = a³ = 5³ = 125"
            },
            
            # ЗАДАНИЕ 11 - Задачи с прикладным содержанием
            {
                "id": 21,
                "type": "multiple_choice",
                "topic": "Задание 10",
                "difficulty": "medium",
                "question": "Тело движется по закону s(t) = t² + 3t. Найдите скорость тела в момент времени t = 2 с.",
                "answers": ["5 м/с", "6 м/с", "7 м/с", "8 м/с"],
                "correct_index": 2,
                "explanation": "v(t) = s'(t) = 2t + 3. v(2) = 2×2 + 3 = 7 м/с"
            },
            
            # ЗАДАНИЕ 12 - Исследование функций
            {
                "id": 22,
                "type": "multiple_choice",
                "topic": "Задание 11",
                "difficulty": "medium",
                "question": "Найдите точку максимума функции f(x) = x³ - 3x² + 2",
                "answers": ["x = 0", "x = 1", "x = 2", "x = 3"],
                "correct_index": 0,
                "explanation": "f'(x) = 3x² - 6x = 3x(x - 2). Критические точки: x = 0, x = 2. В точке x = 0 - локальный максимум"
            },
            
            # Дополнительные задания для разнообразия
            {
                "id": 23,
                "type": "multiple_choice",
                "topic": "Задание 1",
                "difficulty": "easy",
                "question": "Решите уравнение: 4x - 3 = 9",
                "answers": ["2", "3", "4", "5"],
                "correct_index": 1,
                "explanation": "4x = 9 + 3 = 12, x = 12 / 4 = 3"
            },
            {
                "id": 24,
                "type": "multiple_choice",
                "topic": "Задание 2",
                "difficulty": "easy",
                "question": "Вычислите: √49 + √36",
                "answers": ["11", "12", "13", "14"],
                "correct_index": 2,
                "explanation": "√49 = 7, √36 = 6, 7 + 6 = 13"
            },
            {
                "id": 25,
                "type": "multiple_choice",
                "topic": "Задание 4",
                "difficulty": "easy",
                "question": "В коробке 4 красных и 6 синих шаров. Найдите вероятность достать красный шар.",
                "answers": ["0.2", "0.3", "0.4", "0.5"],
                "correct_index": 2,
                "explanation": "P = 4/(4+6) = 4/10 = 0.4"
            },
        ]
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Получить все задания"""
        return self.tasks
    
    def get_tasks_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Получить задания по теме"""
        return [task for task in self.tasks if task["topic"] == topic]
    
    def get_tasks_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Получить задания по сложности"""
        return [task for task in self.tasks if task["difficulty"] == difficulty]
    
    def get_task_by_id(self, task_id: int) -> Dict[str, Any]:
        """Получить задание по ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def get_random_tasks(self, count: int = 10) -> List[Dict[str, Any]]:
        """Получить случайные задания"""
        import random
        return random.sample(self.tasks, min(count, len(self.tasks)))


# Глобальный экземпляр
math_tasks = MathTasks()

"""
Модель бюджета по категории расходов
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Budget:
    """
    Бюджет по категории товаров, хранит срок (duration), на который установлен бюджет,
    id категории, к которой относится бюджет (category),
    и сумма бюджета на данный срок (amount)
    pk - id записи в базе данных
    """

    category: int
    amount: int
    duration: datetime = field(default_factory=datetime.now)
    pk: int = 0

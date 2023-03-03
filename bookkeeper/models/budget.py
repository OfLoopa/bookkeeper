"""
Модель бюджета по категории расходов
"""
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterator

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Budget:
    """
    Бюджет по категории товаров, хранит срок (duration), на который установлен бюджет,
    id категории, к которой относится бюджет (category),
    и сумма бюджета на данный срок (amount)
    """
    # TODO: подумать о возможности добавления бюджета по всем категориям (выставить All или None у категории)

    category: int
    amount: int
    duration: datetime = field(default_factory=datetime.now)

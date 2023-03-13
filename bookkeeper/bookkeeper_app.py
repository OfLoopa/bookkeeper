"""
Presenter в MVP-модели.
Класс Bookkeeper описывает полностью приложение с БД и View
"""
from datetime import datetime, timedelta
from typing import Protocol, Callable, Optional
from dateutil import relativedelta

from bookkeeper.view.app import View
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.utils import build_dict_tree_from_list
from bookkeeper.repository.abstract_repository import AbstractRepository


class AbstractView(Protocol):
    """
    interface of an abstract view class (GUI)
    """
    window: type

    def start_app(self) -> None:
        pass

    def register_handlers(
            self, handlers: dict[str, list[Optional[Callable]]] | None = None
    ):
        pass


class Bookkeeper:
    """
    Класс Presenter
    """

    def __init__(self,
                 view: AbstractView,
                 repository_factory: dict[type, AbstractRepository]):
        """
        При создании экземпляра запускает приложение.
        В качестве параметров передается класс с GUI и
        функция, создающая репозитории (фабрика)
        """
        self.view = view
        self.view.register_handlers(self.get_handlers())
        self.repository_factory = repository_factory

        self.cat_repo = repository_factory[Category]
        self.budget_repo = repository_factory[Budget]
        self.expenses_repo = repository_factory[Expense]

        self.view.start_app()

    def get_handlers(self) -> dict[str, list[Optional[Callable]]]:
        """
        Метод возвращает словарь обработчиков,
        разбитых по страницам в GUI, на которых эти функции запускаются
        """
        handlers_dist = {
            "category": [
                self.get_category_tree,
                self.add_new_category,
                self.edit_existing_category,
                self.delete_category
            ],
            "expenses": [
                self.get_expenses,
                self.get_categories_list,
                self.add_expense,
                self.edit_expenses,
                self.update_budgets,
                self.get_expense_from_repo
            ],
            "budget": [
                self.get_budget,
                self.set_budget
            ]
        }
        return handlers_dist

    def get_category_tree(self) -> dict:
        """
        Строит и возвращает дерево существующих категорий
        """
        categories_list = self.cat_repo.get_all()
        categories_tree = build_dict_tree_from_list(categories_list)
        return categories_tree

    def add_new_category(
            self, category_name: str, parent_id: int | None = None
    ) -> None:
        """Добавление новой категории в репозиторий"""
        self.cat_repo.add(Category(name=category_name.capitalize(), parent=parent_id))
        self.view.window.categories_page.categories_list.set_tree(
            category_tree_getter=self.get_category_tree
        )
        self.view.window.expenses_page.add_expense.choose_category.category_box.update_categories(
            category_list_getter=self.get_categories_list
        )

    def edit_existing_category(
            self, category_id: int,
            new_name: str | None = None,
            new_parent_id: int | None = None
    ) -> None:
        """
        Редактирование существующей категории
        """
        if new_name is None:
            new_name = self.cat_repo.get(category_id).name
        self.cat_repo.update(
            Category(name=new_name.capitalize(), parent=new_parent_id, pk=category_id)
        )
        self.view.window.categories_page.categories_list.set_tree(
            category_tree_getter=self.get_category_tree
        )
        self.view.window.expenses_page.add_expense.choose_category.category_box.update_categories(
            category_list_getter=self.get_categories_list
        )

    def delete_category(self, category_id: int) -> None:
        """Удаление категории"""
        self.cat_repo.delete(category_id)
        self.view.window.categories_page.categories_list.set_tree(
            category_tree_getter=self.get_category_tree
        )
        self.view.window.expenses_page.add_expense.choose_category.category_box.update_categories(
            category_list_getter=self.get_categories_list
        )

    def get_expenses(self) -> list[Expense]:
        """Возвращает список расходов"""
        expenses = self.expenses_repo.get_all()
        return expenses

    def edit_expenses(
            self, pk: int, amount: float, category: str,
            expense_date: datetime, comment: str
    ) -> None:
        """
        Редактирование существующего расхода
        Если категория не входит в список существующих категорий,
        то создается новая
        """
        edit_expense = Expense(
            pk=pk, amount=amount, category=category,
            expense_date=expense_date, comment=comment
        )
        existing_categories = self.get_categories_list()
        if category not in existing_categories:
            self.add_new_category(category)
        self.expenses_repo.update(edit_expense)

    def add_expense(
            self, amount: float, date: datetime, category: str, comment: str
    ) -> None:
        """Добавление записи о расходе"""
        self.expenses_repo.add(
            Expense(amount=amount, category=category, expense_date=date, comment=comment)
        )
        self.view.window.expenses_page.expenses_list.set_expenses(
            expenses_getter=self.get_expenses
        )

    def get_categories_list(self) -> list[str]:
        """Получение списка существующих категорий"""
        categories_list = self.cat_repo.get_all()
        categories = []
        for category in categories_list:
            categories.append(category.name)
        return categories

    def get_budget(self) -> list[Budget]:
        """Получение бюджетов на день, неделю и месяц"""
        day_budgets = self.budget_repo.get_all(
            subquery="WHERE expiration_date="
                     "(SELECT MAX(expiration_date) FROM budget WHERE duration='День')")
        week_budgets = self.budget_repo.get_all(
            subquery="WHERE expiration_date="
                     "(SELECT MAX(expiration_date) FROM budget WHERE duration='Неделя')")
        month_budgets = self.budget_repo.get_all(
            subquery="WHERE expiration_date="
                     "(SELECT MAX(expiration_date) FROM budget WHERE duration='Месяц')")
        return day_budgets + week_budgets + month_budgets

    def get_expenses_from_data_range(
            self, end_date: datetime, start_date: datetime = datetime.now()
    ) -> list[Expense]:
        """Получение расходов за определенный промежуток времени"""
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
        expenses = self.expenses_repo.get_all(
            subquery=f"WHERE expense_date <= '{end_date_str}'"
                     f" AND expense_date > '{start_date_str}'"
        )
        return expenses

    def set_budget(self, amount: float, duration: str) -> None:
        """Функция, задающая бюджет на период
        duration: "День", "Неделя", "Месяц"
        """
        if duration == "День":
            expiration_date = datetime.now() + timedelta(days=1)
        elif duration == "Неделя":
            expiration_date = datetime.now() + timedelta(weeks=1)
        elif duration == "Месяц":
            expiration_date = datetime.now() + relativedelta.relativedelta(months=1)
        else:
            raise ValueError("Wrong duration, set День/Неделя/Месяц")
        possible_expenses = self.get_expenses_from_data_range(
            end_date=expiration_date
        )
        start_amount = 0.0
        for expense in possible_expenses:
            start_amount += expense.amount
        budget = Budget(
            amount=start_amount, limits=amount,
            duration=duration, expiration_date=expiration_date
        )
        self.budget_repo.add(budget)
        self.view.window.budget_page.budget_window.set_budgets(
            budgets_getter=self.get_budget
        )

    def get_budgets_with_appropriate_period(self, date: datetime) -> list[Budget]:
        """Получение бюджета, в период которого попадает дата"""
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        budgets = self.budget_repo.get_all(
            subquery=f"WHERE start_date < '{date_str}'"
                     f" AND expiration_date >= '{date_str}'"
        )
        return budgets

    def update_budgets(self, value: float, date: datetime) -> None:
        """Обновление бюджета"""
        budgets = self.get_budgets_with_appropriate_period(date=date)
        for budget in budgets:
            budget.amount += value
            self.budget_repo.update(budget)

        self.view.window.budget_page.budget_window.set_budgets(
            budgets_getter=self.get_budget
        )

    def get_expense_from_repo(self, pk: int) -> Expense:
        """Получение расхода по его уникальному номеру"""
        return self.expenses_repo.get(pk)


if __name__ == "__main__":
    app = Bookkeeper(
        view=View(), repository_factory=SQLiteRepository.repository_factory(
            models=[Category, Expense, Budget],
            db_file='bookkeeper/databases/client.sqlite.db'
        )
    )

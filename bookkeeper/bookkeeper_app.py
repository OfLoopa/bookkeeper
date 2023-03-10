import datetime
from typing import Protocol, Callable, Optional

from bookkeeper.view.app import View
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.utils import build_dict_tree_from_list

categories_example = [
    ["продукты", None, 1],
    ["мясо", 1, 2],
    ["сырое мясо", 2, 3],
    ["мясные продукты", 2, 4],
    ["сладости", 1, 5],
    ["книги", None, 6],
    ["одежда", None, 7],
]


class AbstractView(Protocol):
    window: type

    def start_app(self) -> None:
        pass

    def register_handlers(self, handlers: dict[str, list[Optional[Callable]]] | None = None):
        pass

    def set_category_list(self, categories: dict | None = None) -> None:
        pass

    def add_category(self):
        pass

    def rename_category(self):
        pass

    def delete_category(self):
        pass


class Bookkeeper:

    def __init__(self,
                 view: AbstractView,
                 repository_factory: type):
        self.view = view
        self.view.register_handlers(self.get_handlers())
        self.repository_factory = repository_factory

        self.cat_repo = repository_factory[Category]
        self.budget_repo = repository_factory[Budget]
        self.expenses_repo = repository_factory[Expense]

        self.view.start_app()

    def get_handlers(self) -> dict[str, list[Optional[Callable]]]:
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
                self.edit_expenses
            ]
        }
        return handlers_dist

    def get_category_tree(self) -> dict:
        categories_list = self.cat_repo.get_all()
        categories_tree = build_dict_tree_from_list(categories_list)
        return categories_tree

    def add_new_category(self, category_name: str, parent_id: int | None = None) -> None:
        self.cat_repo.add(Category(name=category_name, parent=parent_id))
        self.view.window.categories_page.categories_list.set_tree(category_tree_getter=self.get_category_tree)
        self.view.window.expenses_page.add_expense.choose_category.update_categories(
            category_list_getter=self.get_categories_list)

    def edit_existing_category(self, category_id: int, new_name: str | None = None, new_parent_id: int | None = None) -> None:
        if new_name is None:
            new_name = self.cat_repo.get(category_id).name
        self.cat_repo.update(Category(name=new_name, parent=new_parent_id, pk=category_id))
        self.view.window.categories_page.categories_list.set_tree(category_tree_getter=self.get_category_tree)
        self.view.window.expenses_page.add_expense.choose_category.update_categories(
            category_list_getter=self.get_categories_list)

    def delete_category(self, category_id: int) -> None:
        self.cat_repo.delete(category_id)
        self.view.window.categories_page.categories_list.set_tree(category_tree_getter=self.get_category_tree)
        self.view.window.expenses_page.add_expense.choose_category.update_categories(
            category_list_getter=self.get_categories_list)

    def get_expenses(self) -> list[Expense]:
        expenses = self.expenses_repo.get_all()
        return expenses

    def edit_expenses(self, pk: int, amount: float, category: str, expense_date: datetime.datetime, comment: str) -> None:
        edit_expense = Expense(
            pk=pk, amount=amount, category=category, expense_date=expense_date, comment=comment)
        self.expenses_repo.update(edit_expense)

    def add_expense(self, amount: float, date: datetime.datetime, category: str, comment: str) -> None:
        self.expenses_repo.add(Expense(amount=amount, category=category, expense_date=date, comment=comment))
        self.view.window.expenses_page.expenses_list.set_expenses(expenses_getter=self.get_expenses)

    def get_categories_list(self) -> list[str]:
        categories_list = self.cat_repo.get_all()
        categories = []
        for category in categories_list:
            categories.append(category.name)
        return categories


if __name__ == "__main__":
    app = Bookkeeper(
        view=View(), repository_factory=SQLiteRepository.repository_factory(
            models=[Category, Expense, Budget],
            db_file='bookkeeper/databases/client.sqlite.db'
        )
    )

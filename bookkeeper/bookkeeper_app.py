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
            ]
        }
        return handlers_dist

    def get_category_tree(self) -> dict:
        categories_list = self.cat_repo.get_all()
        categories_tree = build_dict_tree_from_list(categories_list)
        return categories_tree

    def add_new_category(self, category_name, parent_id) -> None:
        if parent_id == "":
            self.cat_repo.add(Category(name=category_name))
        else:
            self.cat_repo.add(Category(name=category_name, parent=int(parent_id)))
        self.view.window.categories_page.categories_list.set_tree(category_tree_getter=self.get_category_tree)

    def edit_existing_category(self, category_id, new_name, new_parent_id) -> None:
        if new_parent_id == "":
            self.cat_repo.update(Category(name=new_name, parent=None, pk=int(category_id)))
        else:
            self.cat_repo.update(Category(name=new_name, parent=int(new_parent_id), pk=int(category_id)))
        self.view.window.categories_page.categories_list.set_tree(category_tree_getter=self.get_category_tree)

    def delete_category(self, category_id) -> None:
        self.cat_repo.delete(int(category_id))
        self.view.window.categories_page.categories_list.set_tree(category_tree_getter=self.get_category_tree)


if __name__ == "__main__":
    app = Bookkeeper(
        view=View(), repository_factory=SQLiteRepository.repository_factory(
            models=[Category, Expense, Budget],
            db_file='bookkeeper/databases/client.sqlite.db'
        )
    )

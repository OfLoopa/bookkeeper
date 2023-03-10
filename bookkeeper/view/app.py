"""
Класс приложения на PyQT (view)
"""
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from functools import partial
from typing import Optional, Callable

from bookkeeper.view.expenses_page import expensesPage
from bookkeeper.view.categories_page import categoriesPage
from bookkeeper.view.budget_page import BudgetPage
from bookkeeper.utils import set_elem_in_tree, delete_elem_from_tree, get_elem_in_tree, get_elem_parent

categories_example = {
    1: {
        "name": "продукты",
        2: {
            "name": "мясо",
            3: {
                "name": "сырое мясо"
            },
            4: {
                "name": "мясные продукты"
            }
        },
        5: {
            "name": "сладости"
        }
    },
    6: {
        "name": "книги"
    },
    7: {
        "name": "одежда"
    },
    8: {
        "name": "почта"
    }
}


def get_example():
    return categories_example


def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except Exception as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))

    return inner


class pageManagerToolbar(QtWidgets.QWidget):
    def __init__(self, *args, parent: type | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.parent = parent

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.expensesBtn = QtWidgets.QPushButton(text="Расходы")
        self.expensesBtn.clicked.connect(partial(self.set_page, 0))
        self.layout.addWidget(self.expensesBtn)

        self.budgetBtn = QtWidgets.QPushButton(text="Бюджет")
        self.budgetBtn.clicked.connect(partial(self.set_page, 1))
        self.layout.addWidget(self.budgetBtn)

        self.categoriesBtn = QtWidgets.QPushButton(text="Категории расходов")
        self.categoriesBtn.clicked.connect(partial(self.set_page, 2))
        self.layout.addWidget(self.categoriesBtn)

    def set_page(self, page_index=0) -> None:
        self.parent.page_layout.setCurrentIndex(page_index)
        # print("button was clicked: ", str(self.parent.page_layout.currentIndex()))


class MainWindow(QtWidgets.QWidget):
    get_category_handler: Optional[Callable]
    add_category_handler: Optional[Callable]
    edit_category_handler: Optional[Callable]
    delete_category_handler: Optional[Callable]

    get_expenses_handler: Optional[Callable]
    get_categories_handler: Optional[Callable]
    add_expense_handler: Optional[Callable]
    edit_expense_handler: Optional[Callable]

    def __init__(self, *args,
                 category_handlers: list[Optional[Callable]],
                 expenses_handlers: list[Optional[Callable]],
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.register_category_handlers(category_handlers)
        self.register_expenses_handlers(expenses_handlers)

        self.setWindowTitle("The BookKeeper App")
        self.setGeometry(50, 50, 800, 900)

        self.budget_page = BudgetPage()
        self.expenses_page = expensesPage(
            get_handler=self.get_expenses_handler,
            get_categories_handler=self.get_categories_handler,
            add_handler=self.add_expense_handler,
            edit_handler=self.edit_category_handler
        )
        self.categories_page = categoriesPage(
            get_handler=self.get_category_handler,
            add_handler=self.add_category_handler,
            edit_handler=self.edit_category_handler,
            delete_handler=self.delete_category_handler
        )
        self.menuBarWidget = pageManagerToolbar(parent=self)

        self.layout = QtWidgets.QVBoxLayout()

        self.page_layout = QtWidgets.QStackedLayout()
        self.page_layout.addWidget(self.expenses_page)
        self.page_layout.addWidget(self.budget_page)
        self.page_layout.addWidget(self.categories_page)

        self.layout.addWidget(self.menuBarWidget)
        self.layout.addLayout(self.page_layout)
        self.setLayout(self.layout)

    def register_category_handlers(self, handlers: list[Optional[Callable]]) -> None:
        self.get_category_handler = handlers[0]
        self.add_category_handler = handlers[1]
        self.edit_category_handler = handlers[2]
        self.delete_category_handler = handlers[3]

    def register_expenses_handlers(self, handlers: list[Optional[Callable]]) -> None:
        self.get_expenses_handler = handlers[0]
        self.get_categories_handler = handlers[1]
        self.add_expense_handler = handlers[2]
        self.edit_category_handler = handlers[3]


class View:
    app: QtWidgets.QApplication
    window: MainWindow
    category_handlers: list[Optional[Callable]]
    expenses_handlers: list[Optional[Callable]]

    def __init__(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)

    def start_app(self) -> None:
        self.window = MainWindow(
            category_handlers=self.category_handlers,
            expenses_handlers=self.expenses_handlers
        )
        self.window.show()
        sys.exit(self.app.exec())

    def register_handlers(self, handlers_obj: dict[str, list[Optional[Callable]]] | None = None):
        if handlers_obj is None:
            handlers_obj = self.register_example_handlers()
        self.category_handlers = handlers_obj["category"]
        self.expenses_handlers = handlers_obj["expenses"]

    # Test View handlers
    def setter_example(self, category_name, parent_id):
        if parent_id == "":
            categories_example[8] = {"name": category_name}
        else:
            set_elem_in_tree(categories_example, [category_name, int(parent_id), 8])
        self.window.categories_page.categories_list.set_tree(category_tree_getter=get_example)

    def editor_example(self, category_id, new_name, new_parent_id):
        parent_id = get_elem_parent(categories_example, category_id)
        if new_parent_id == "":
            set_elem_in_tree(categories_example, [new_name, parent_id, int(category_id)])
        else:
            delete_elem_from_tree(categories_example, int(category_id))
            set_elem_in_tree(categories_example, [new_name, int(new_parent_id), int(category_id)])
        self.window.categories_page.categories_list.set_tree(category_tree_getter=get_example)

    def deleter_example(self, category_id):
        if category_id != "":
            delete_elem_from_tree(categories_example, int(category_id))
        self.window.categories_page.categories_list.set_tree(category_tree_getter=get_example)

    def register_example_handlers(self):
        return {
            "category": [get_example, self.setter_example, self.editor_example, self.deleter_example]
        }


if __name__ == "__main__":
    view = View()
    view.register_handlers()
    view.start_app()

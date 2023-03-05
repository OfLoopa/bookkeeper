import sys
from PySide6 import QtCore, QtGui, QtWidgets
from functools import partial

from expenses_page import expensesPage
from categories_page import categoriesPage
from budget_page import BudgetPage


class pageManagerToolbar(QtWidgets.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
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

    def set_page(self, page_index=0):
        self.parent.page_layout.setCurrentIndex(page_index)
        print("button was clicked: ", str(self.parent.page_layout.currentIndex()))


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("The BookKeeper App")

        self.budget_page = BudgetPage()
        self.expenses_page = expensesPage()
        self.categories_page = categoriesPage()
        self.menuBarWidget = pageManagerToolbar(parent=self)

        self.layout = QtWidgets.QVBoxLayout()

        self.page_layout = QtWidgets.QStackedLayout()
        self.page_layout.addWidget(self.expenses_page)
        self.page_layout.addWidget(self.budget_page)
        self.page_layout.addWidget(self.categories_page)

        self.layout.addWidget(self.menuBarWidget)
        self.layout.addLayout(self.page_layout)
        self.setLayout(self.layout)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

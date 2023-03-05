from PySide6 import QtCore, QtGui, QtWidgets
from dataclasses import dataclass, field
from datetime import datetime


expenses_example = [
    ('2023-01-09 15:09:00', 7.49, 'Хозтовары', 'Пакет на кассе'),
    ('2023-01-09 15:09:00', 139.99, 'Сыр', ''),
    ('2023-01-06 20:32:02', 5546.0, 'Книги', 'Книги по Python и pyqt'),
]

categories_example = "Продукты Сладости Книги Одежда".split()


@dataclass
class ExpenseItem:
    data: str
    amount: float
    category: str
    comment: str = ''
    # data: datetime = field(default_factory=datetime.now)


class expensesList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.expenses_title = QtWidgets.QLabel("Последние расходы")

        self.expenses_table = QtWidgets.QTableWidget(4, 20)
        self.expenses_table.setColumnCount(4)
        self.expenses_table.setRowCount(len(expenses_example))
        self.expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split()
        )
        self.header = self.expenses_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

        self.set_data(expenses_example)

        self.layout.addWidget(self.expenses_title)
        self.layout.addWidget(self.expenses_table)

    def set_data(self, data: list[tuple]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(str(x).capitalize())
                )


class addAmountElement(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.add_amount_label = QtWidgets.QLabel("Сумма")
        self.add_amount_input = QtWidgets.QLineEdit()
        self.add_amount_input.setPlaceholderText('Введите сумму, которую вы потратили')
        self.layout.addWidget(self.add_amount_label)
        self.layout.addWidget(self.add_amount_input)


class chooseCategoryElement(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.choose_category_label = QtWidgets.QLabel("Категория")
        self.layout.addWidget(self.choose_category_label)

        self.category_box = QtWidgets.QComboBox()
        for category in categories_example:
            self.category_box.addItem(category)

        self.layout.addWidget(self.category_box)


class elementAddExpense(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_expense_title = QtWidgets.QLabel("Добавить новую запись:")
        self.add_btn = QtWidgets.QPushButton(text="Добавить")

        self.layout.addWidget(self.add_expense_title)
        self.layout.addWidget(addAmountElement())
        self.layout.addWidget(chooseCategoryElement())
        self.layout.addWidget(self.add_btn)


class expensesPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.expenses_list = expensesList()
        self.layout.addWidget(self.expenses_list)

        self.add_expense = elementAddExpense()
        self.layout.addWidget(self.add_expense)


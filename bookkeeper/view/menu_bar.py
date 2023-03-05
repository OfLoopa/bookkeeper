from PySide6 import QtCore, QtGui, QtWidgets


class pageManagerToolbar(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.expensesBtn = QtWidgets.QPushButton(text="Расходы")
        self.layout.addWidget(self.expensesBtn)

        self.budgetBtn = QtWidgets.QPushButton(text="Бюджет")
        self.layout.addWidget(self.budgetBtn)

        self.categoriesBtn = QtWidgets.QPushButton(text="Категории расходов")
        self.layout.addWidget(self.categoriesBtn)

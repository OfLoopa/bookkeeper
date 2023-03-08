"""
Виджет для отображения страницы просмотра и задания бюджета в окне приложения
"""
from PySide6 import QtWidgets


budget_example = [
    ('День', 705.43, 1000),
    ('Неделя', 6719.2, 7000),
    ('Месяц', 10592.96, 30000),
]


class setBudgetInput(QtWidgets.QWidget):
    def __init__(self, name, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.period = QtWidgets.QLabel(name)
        self.input = QtWidgets.QLineEdit()
        self.save_btn = QtWidgets.QPushButton("Сохранить")

        self.layout.addWidget(self.period)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.save_btn)


class BudgetWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.budget_window_title = QtWidgets.QLabel("Бюджет")

        self.expenses_table = QtWidgets.QTableWidget(3, 3)
        self.expenses_table.setColumnCount(3)
        self.expenses_table.setRowCount(3)
        self.expenses_table.setHorizontalHeaderLabels(
            ["", "Сумма", "Бюджет"]
        )
        self.header = self.expenses_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)

        self.set_data(budget_example)

        self.layout.addWidget(self.budget_window_title)
        self.layout.addWidget(self.expenses_table)

    def set_data(self, data: list[tuple]) -> None:
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(str(x).capitalize())
                )


class ChangeBudgetWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.change_budget_window_title = QtWidgets.QLabel("Задать Бюджет")

        self.layout.addWidget(self.change_budget_window_title)
        self.layout.addWidget(setBudgetInput("День"))
        self.layout.addWidget(setBudgetInput("Неделя"))
        self.layout.addWidget(setBudgetInput("Месяц"))


class BudgetInfoWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.budget_info_window_title = QtWidgets.QLabel("Подсказка")
        self.budget_info = QtWidgets.QLabel(
            """
            Бюджет задается на следующие сроки:
            
                День - на календарный день с 0:00 до 23:59
                
                Неделя - на календарную неделю с понедельника 0:00 до воскресенья 23:59
                
                Месяц - на календарный месяц с первого дня месяца до последнего
            """
        )

        self.layout.addWidget(self.budget_info_window_title)
        self.layout.addWidget(self.budget_info)


class BudgetPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.budget_window = BudgetWindow()
        self.layout.addWidget(self.budget_window)

        self.change_budget_window = ChangeBudgetWindow()
        self.layout.addWidget(self.change_budget_window)

        self.budget_info = BudgetInfoWindow()
        self.layout.addWidget(self.budget_info)

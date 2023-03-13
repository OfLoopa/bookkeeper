"""
Виджет для отображения страницы просмотра и задания бюджета в окне приложения
"""
from typing import Optional, Callable
from PySide6 import QtWidgets, QtCore

from bookkeeper.models.budget import Budget


class setBudgetInput(QtWidgets.QWidget):
    """
    Класс виджета ввода бюджета на опреленный срок
    """
    def __init__(self, name, *args,
                 budget_setter: Optional[Callable],
                 **kwargs) -> None:
        """name - название периода,
        на который задается бюджет
        (например "День")"""
        super().__init__(*args, **kwargs)
        self.duration = name
        self.setter = budget_setter

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.period = QtWidgets.QLabel(name)
        self.input = QtWidgets.QLineEdit()
        self.save_btn = QtWidgets.QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_btn_clicked)

        self.layout.addWidget(self.period)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.save_btn)

    @QtCore.Slot()
    def save_btn_clicked(self) -> None:
        """Функия-слот,
        обрабатывающая нажатие на кнопку сохранения"""
        try:
            limit = float(self.input.text())
            self.setter(limit, self.duration)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', str(e))


class BudgetWindow(QtWidgets.QWidget):
    """Класс виджета с окном, отображающим бюджеты"""
    def __init__(self, *args,
                 budgets_getter: Optional[Callable],
                 **kwargs) -> None:
        """budgets_getter: обработчик, возвращающий список бюджетов"""
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.budget_window_title = QtWidgets.QLabel("Бюджет")
        self.layout.addWidget(self.budget_window_title)

        self.budgets_table = QtWidgets.QTableWidget(3, 3)
        self.budgets_table.setColumnCount(3)
        self.budgets_table.setRowCount(3)
        self.budgets_table.setHorizontalHeaderLabels(
            ["", "Сумма", "Бюджет"]
        )
        self.header = self.budgets_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)

        self.set_budgets(budgets_getter)

    def build_budgets(self, data: list[Budget]) -> None:
        """Функция создает ячейки таблицы
        по входящему списку бюджетов"""
        for i, row in enumerate(data):
            self.budgets_table.setItem(
                i, 0,
                QtWidgets.QTableWidgetItem(row.duration)
            )
            self.budgets_table.setItem(
                i, 1,
                QtWidgets.QTableWidgetItem(str(row.amount))
            )
            self.budgets_table.setItem(
                i, 2,
                QtWidgets.QTableWidgetItem(str(row.limits))
            )

    def set_budgets(self, budgets_getter: Callable) -> None:
        """Функция перестраивает таблицу с бюджетами"""
        if self.budgets_table.itemAt(0, 0) is not None:
            self.layout.removeWidget(self.budgets_table)

        budgets_data = budgets_getter()

        self.budgets_table = QtWidgets.QTableWidget(3, 3)
        self.budgets_table.setColumnCount(3)
        self.budgets_table.setRowCount(3)
        self.budgets_table.setHorizontalHeaderLabels(
            ["", "Сумма", "Бюджет"]
        )
        self.header = self.budgets_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)

        self.build_budgets(budgets_data)
        self.layout.addWidget(self.budgets_table)


class ChangeBudgetWindow(QtWidgets.QWidget):
    """
    Класс виджета изменения бюджетов
    """
    def __init__(self, *args,
                 budgets_setter: Optional[Callable],
                 **kwargs) -> None:
        """budgets_setter: обработчик, изменяющий бюджет"""
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.change_budget_window_title = QtWidgets.QLabel("Задать Бюджет")

        self.layout.addWidget(self.change_budget_window_title)
        self.layout.addWidget(setBudgetInput(name="День", budget_setter=budgets_setter))
        self.layout.addWidget(setBudgetInput(name="Неделя", budget_setter=budgets_setter))
        self.layout.addWidget(setBudgetInput(name="Месяц", budget_setter=budgets_setter))


class BudgetInfoWindow(QtWidgets.QWidget):
    """
    Класс виджета информационного окна
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.budget_info_window_title = QtWidgets.QLabel("Подсказка")
        self.budget_info = QtWidgets.QLabel(
            """
            Бюджет задается на следующие сроки:            
                День - на следующий календарный день с 0:00 до 23:59
                Неделя - на календарную неделю, начиная с следующего дня с 0:00
                Месяц - на календарный месяц, начиная с следующего дня 0:00
            """
        )

        self.layout.addWidget(self.budget_info_window_title)
        self.layout.addWidget(self.budget_info)


class BudgetPage(QtWidgets.QWidget):
    """Класс виджета страницы бюджетов"""
    def __init__(self, *args,
                 get_handler: Optional[Callable],
                 set_handler: Optional[Callable],
                 **kwargs) -> None:
        """
        :param get_handler: обработчик для получения списка бюджетов
        :param set_handler: обработчик для задания бюджета
        """
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.budget_window = BudgetWindow(budgets_getter=get_handler)
        self.layout.addWidget(self.budget_window)

        self.change_budget_window = ChangeBudgetWindow(budgets_setter=set_handler)
        self.layout.addWidget(self.change_budget_window)

        self.budget_info = BudgetInfoWindow()
        self.layout.addWidget(self.budget_info)

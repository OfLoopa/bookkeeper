from PySide6 import QtCore, QtGui, QtWidgets
from dataclasses import dataclass, field
from datetime import datetime


categories_example = "Продукты Сладости Книги Одежда".split()


class categoryItem(QtWidgets.QWidget):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.category_name = QtWidgets.QLabel(name)
        self.edit_btn = QtWidgets.QPushButton("Редактировать")

        self.layout.addWidget(self.category_name)
        self.layout.addWidget(self.edit_btn)


class categoriesList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.categories_title = QtWidgets.QLabel("Список категорий")

        self.layout.addWidget(self.categories_title)
        for cat in categories_example:
            self.layout.addWidget(categoryItem(cat))


class addCategoryInput(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.input_name = QtWidgets.QLabel("Название категории")
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Введите название новой категории")
        self.save_btn = QtWidgets.QPushButton("Сохранить")

        self.layout.addWidget(self.input_name)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.save_btn)


class elementAddCategory(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Добавление новой категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(addCategoryInput())


class categoriesPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.categories_list = categoriesList()
        self.layout.addWidget(self.categories_list)

        self.add_category = elementAddCategory()
        self.layout.addWidget(self.add_category)

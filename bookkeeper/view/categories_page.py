"""
Виджет для отображения страницы списка категорий в окне приложения
"""
from PySide6 import QtWidgets


categories_example = {
    "продукты": {
        "мясо": {
            "сырое мясо": {},
            "мясные продукты": {}
        },
        "сладости": {}
    },
    "книги": {},
    "одежда": {}
}


class categoriesList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.category_tree = QtWidgets.QTreeWidget()
        self.category_tree.setHeaderLabels(["Список категорий"])
        self.category_tree.setColumnCount(1)
        self.build_category_tree(data=categories_example, parent=self.category_tree)

        self.layout.addWidget(self.category_tree)

    def build_category_tree(self,
                            data: dict | None = None,
                            parent: QtWidgets.QTreeWidgetItem | QtWidgets.QTreeWidget | None = None
                            ) -> None:
        for key, value in data.items():
            item = QtWidgets.QTreeWidgetItem(parent)
            item.setText(0, key)
            if isinstance(value, dict):
                self.build_category_tree(data=value, parent=item)


class addCategoryInput(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
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
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Добавление новой категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(addCategoryInput())


class categoriesPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.categories_list = categoriesList()
        self.layout.addWidget(self.categories_list)

        self.add_category = elementAddCategory()
        self.layout.addWidget(self.add_category)

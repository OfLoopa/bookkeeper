"""
Виджет для отображения страницы списка категорий в окне приложения
"""
from PySide6 import QtWidgets, QtCore
from typing import Callable, Optional

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
    }
}


def get_example():
    return categories_example


class categoriesList(QtWidgets.QWidget):
    """
    Элемент отображения дерева категорий

    Для отображения необходимо указать функцию,
    которая будет возвращать дерево для отображения
    (json-like объект)
    """
    def __init__(self, *args, category_getter: Optional[Callable] = get_example, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.getter = category_getter

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.category_tree = QtWidgets.QTreeWidget()
        self.category_tree.setHeaderLabels(["Список категорий"])
        self.category_tree.setColumnCount(1)

        self.set_tree(category_tree_getter=category_getter)

    def build_category_tree(self,
                            data: dict[str, dict] | None = None,
                            parent: QtWidgets.QTreeWidgetItem | QtWidgets.QTreeWidget | None = None
                            ) -> None:
        for key, value in data.items():
            if not isinstance(key, str):
                item = QtWidgets.QTreeWidgetItem(parent)
                item.setText(0, value["name"])
                item.setText(1, str(key))
                if isinstance(value, dict):
                    self.build_category_tree(data=value, parent=item)

    def set_tree(self, category_tree_getter: Callable) -> None:
        if self.category_tree.itemAt(0, 0) is not None:
            self.category_tree.setParent(None)

        self.category_tree = QtWidgets.QTreeWidget()
        self.category_tree.setHeaderLabels(["Список категорий", "Id категории"])
        self.category_tree.setColumnCount(2)
        tree_data = category_tree_getter()
        self.build_category_tree(data=tree_data, parent=self.category_tree)
        self.layout.addWidget(self.category_tree)


class addCategoryInput(QtWidgets.QWidget):
    """
    Элемент добавления новой категории в дерево
    """
    def __init__(self, *args, category_adder: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.adder = category_adder

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.input_category_name = QtWidgets.QLineEdit()
        self.input_category_name.setPlaceholderText("Введите название новой категории")

        self.input_parent_id = QtWidgets.QLineEdit()
        self.input_parent_id.setPlaceholderText("Введите id родительской категории")

        self.save_btn = QtWidgets.QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_btn_clicked)

        self.layout.addWidget(self.input_category_name)
        self.layout.addWidget(self.input_parent_id)
        self.layout.addWidget(self.save_btn)

    @QtCore.Slot()
    def save_btn_clicked(self):
        print("add")
        new_category_name = self.input_category_name.text()
        parent_id = self.input_parent_id.text()
        self.adder(new_category_name, parent_id)


class editCategoryInput(QtWidgets.QWidget):
    """
    Элемент редактирования категории в дереве
    """
    def __init__(self, *args, category_editor: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.editor = category_editor

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.input_id_category = QtWidgets.QLineEdit()
        self.input_id_category.setPlaceholderText("Введите id изменяемой категории")

        self.input_category_name = QtWidgets.QLineEdit()
        self.input_category_name.setPlaceholderText("Введите новое название категории")

        self.input_parent_id = QtWidgets.QLineEdit()
        self.input_parent_id.setPlaceholderText("Введите новый id родительской категории")

        self.save_btn = QtWidgets.QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_btn_clicked)

        self.layout.addWidget(self.input_id_category)
        self.layout.addWidget(self.input_category_name)
        self.layout.addWidget(self.input_parent_id)
        self.layout.addWidget(self.save_btn)

    @QtCore.Slot()
    def save_btn_clicked(self):
        print("edit")
        category_id = self.input_id_category.text()
        new_category_name = self.input_category_name.text()
        new_parent_id = self.input_parent_id.text()
        self.editor(category_id, new_category_name, new_parent_id)


class deleteCategoryInput(QtWidgets.QWidget):
    """
    Элемент удаления категории из дерева
    """
    def __init__(self, *args, category_deleter: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.deleter = category_deleter

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.input_id_category = QtWidgets.QLineEdit()
        self.input_id_category.setPlaceholderText("Введите id удаляемой категории")

        self.delete_btn = QtWidgets.QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_btn_clicked)

        self.layout.addWidget(self.input_id_category)
        self.layout.addWidget(self.delete_btn)

    @QtCore.Slot()
    def delete_btn_clicked(self):
        print("delete")
        category_id = self.input_id_category.text()
        self.deleter(category_id)


class elementAddCategory(QtWidgets.QWidget):
    def __init__(self, *args, adder: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Добавление новой категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(addCategoryInput(category_adder=adder))


class elementEditCategory(QtWidgets.QWidget):
    def __init__(self, *args, editor: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Редактирование существующей категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(editCategoryInput(category_editor=editor))


class elementDeleteCategory(QtWidgets.QWidget):
    def __init__(self, *args, deleter: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Удаление существующей категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(deleteCategoryInput(category_deleter=deleter))


class categoriesPage(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.categories_list = categoriesList()
        self.layout.addWidget(self.categories_list)

        self.add_category = elementAddCategory(adder=self.setter_example)
        self.layout.addWidget(self.add_category)

        self.edit_category = elementEditCategory(editor=self.editor_example)
        self.layout.addWidget(self.edit_category)

        self.delete_category = elementDeleteCategory(deleter=self.deleter_example)
        self.layout.addWidget(self.delete_category)

    def setter_example(self, category_name, parent_id):
        if parent_id == "":
            categories_example[8] = {"name": category_name}
        else:
            set_elem_in_tree(categories_example, [category_name, int(parent_id), 8])
        self.categories_list.set_tree(category_tree_getter=get_example)

    def editor_example(self, category_id, new_name, new_parent_id):
        parent_id = get_elem_parent(categories_example, category_id)
        if new_parent_id == "":
            set_elem_in_tree(categories_example, [new_name, parent_id, int(category_id)])
        else:
            delete_elem_from_tree(categories_example, int(category_id))
            set_elem_in_tree(categories_example, [new_name, int(new_parent_id), int(category_id)])
        self.categories_list.set_tree(category_tree_getter=get_example)

    def deleter_example(self, category_id):
        if category_id != "":
            delete_elem_from_tree(categories_example, int(category_id))
        self.categories_list.set_tree(category_tree_getter=get_example)

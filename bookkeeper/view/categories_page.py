"""
Виджет для отображения страницы списка категорий в окне приложения
"""
from PySide6 import QtWidgets, QtCore
from typing import Callable, Optional


class categoriesList(QtWidgets.QWidget):
    """
    Элемент отображения дерева категорий

    Для отображения необходимо указать функцию,
    которая будет возвращать дерево для отображения
    (json-like объект)
    """
    def __init__(self, *args, category_getter: Optional[Callable], **kwargs) -> None:
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
        """Функия строит дерево в виджете,
         на вход подается дерево категорий и родительский элемент в дереве"""
        for key, value in data.items():
            if not isinstance(key, str):
                item = QtWidgets.QTreeWidgetItem(parent)
                item.setText(0, value["name"])
                item.setText(1, str(key))
                if isinstance(value, dict):
                    self.build_category_tree(data=value, parent=item)

    def set_tree(self, category_tree_getter: Callable) -> None:
        """Функция перерисовки дерева категорий"""
        if self.category_tree.itemAt(0, 0) is not None:
            self.layout.removeWidget(self.category_tree)

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
        """Функция-слот, обрабатывающая нажатие на кнопку сохранения"""
        try:
            new_category_name = self.input_category_name.text()
            if new_category_name == "":
                raise ValueError("Введите название категории")
            parent_text = self.input_parent_id.text()
            parent_id = int(parent_text) if parent_text != "" else None
            print("add new category: ", new_category_name, " with parent ", parent_id)
            self.adder(new_category_name, parent_id)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, 'Warning', str(e))


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
        """Функция-слот, обрабатывающая нажатие на кнопку сохранения"""
        try:
            try:
                category_id = int(self.input_id_category.text())
            except ValueError:
                raise ValueError("Введите целое число - номер категории")
            new_category_name = self.input_category_name.text()
            new_id = self.input_parent_id.text()
            new_parent_id = int(new_id) if new_id != "" else None
            print("edit category: ", category_id,
                  " with new name ", new_category_name,
                  " and parent_id ", new_parent_id)
            self.editor(category_id, new_category_name, new_parent_id)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', str(e))


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
        """Функция-слот, обрабатывающая нажатие на кнопку удаления"""
        try:
            try:
                category_id = int(self.input_id_category.text())
            except ValueError:
                raise ValueError("Введите число - номер удаляемой категории")
            print("delete category: ", category_id)
            self.deleter(category_id)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', str(e))


class elementAddCategory(QtWidgets.QWidget):
    """
    Класс виджета добавления элемента в дерево категорий
    """
    def __init__(self, *args, adder: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Добавление новой категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(addCategoryInput(category_adder=adder))


class elementEditCategory(QtWidgets.QWidget):
    """
    Класс виджета изменения элемента в дереве категорий
    """
    def __init__(self, *args, editor: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel(
            "Редактирование существующей категории"
        )

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(editCategoryInput(category_editor=editor))


class elementDeleteCategory(QtWidgets.QWidget):
    """
    Класс виджета удаления элемента из дерева категорий
    """
    def __init__(self, *args, deleter: Optional[Callable], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_category_title = QtWidgets.QLabel("Удаление существующей категории")

        self.layout.addWidget(self.add_category_title)
        self.layout.addWidget(deleteCategoryInput(category_deleter=deleter))


class categoriesPage(QtWidgets.QWidget):
    """
    Класс виджета страницы категорий
    """
    def __init__(self, *args,
                 get_handler: Optional[Callable],
                 add_handler: Optional[Callable],
                 edit_handler: Optional[Callable],
                 delete_handler: Optional[Callable],
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.categories_list = categoriesList(category_getter=get_handler)
        self.layout.addWidget(self.categories_list)

        self.add_category = elementAddCategory(adder=add_handler)
        self.layout.addWidget(self.add_category)

        self.edit_category = elementEditCategory(editor=edit_handler)
        self.layout.addWidget(self.edit_category)

        self.delete_category = elementDeleteCategory(deleter=delete_handler)
        self.layout.addWidget(self.delete_category)

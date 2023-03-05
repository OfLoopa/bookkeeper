import sys
from PySide6 import QtCore, QtGui, QtWidgets

from menu_bar import pageManagerToolbar
from expenses_page import expensesPage
from categories_page import categoriesPage


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("The BookKeeper App")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.menuBarWidget = pageManagerToolbar()
        self.layout.addWidget(self.menuBarWidget)

        self.currentPage = categoriesPage()
        self.layout.addWidget(self.currentPage)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

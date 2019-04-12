from PyQt5.QtWidgets import (QDockWidget, QHBoxLayout, QPushButton, QLineEdit, QWidget)
from PyQt5.QtCore import (Qt, pyqtSignal)


class SearchBar(QDockWidget):
    search = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        mainWidget = QWidget()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search")

        searchBtn = QPushButton("Search")
        searchBtn.clicked.connect(self.searchClicked)

        layout.addWidget(self.searchBar)
        layout.addWidget(searchBtn)

        mainWidget.setLayout(layout)

        self.setWidget(mainWidget)

        self.setMaximumHeight(50)
        self.setTitleBarWidget(QWidget(None))
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)

    def searchClicked(self):
        if self.searchBar.text() == "":
            self.search.emit("123")
        else:
            self.search.emit(self.searchBar.text())
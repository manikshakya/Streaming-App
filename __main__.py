import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer)
from PyQt5.QtMultimediaWidgets import (QVideoWidget)

from mainWindow import MainWindow
from mainVideo import MainVideo

app = QApplication([])
mainWindow = MainWindow()
sys.exit(app.exec_())
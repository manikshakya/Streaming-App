from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QHBoxLayout, QPushButton, QSlider,
                             QLabel, QSizePolicy, QVBoxLayout, QStyle, QDesktopWidget)
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer)
from PyQt5.QtMultimediaWidgets import (QVideoWidget)

from PyQt5.QtCore import (QUrl, Qt, QSize)
from PyQt5.QtGui import (QCloseEvent, QPixmap, QIcon)

class MainVideo(QMainWindow):

    def __init__(self, videoUrl):
        super().__init__()
        self.video = videoUrl

        self.init_ui()

    def init_ui(self):
        url = self.video

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()
        self.videoWidget.setFullScreen(False)
        self.videoWidget.keyPressEvent = self.exitFullScreen

        # self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url))) # For Local files Only
        self.mediaPlayer.setMedia(QMediaContent(QUrl(url))) # For URLs
        self.mediaPlayer.play()
        self.playState = True

        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.playButton.clicked.connect(self.play)


        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setTracking(False)
        print("Tracking: ", self.positionSlider.hasTracking())
        # self.positionSlider.sliderPressed.connect(self.pause)
        self.positionSlider.sliderReleased.connect(self.sliderReleased)
        # self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.valueChanged.connect(self.setPosition)

        self.length = QLabel()

        image = QPixmap("./images/fullscreen.png")
        image = image.scaled(30, 30)

        # fullScreen = QLabel()
        # fullScreen.setFixedHeight(image.height())
        # fullScreen.setFixedWidth(image.width())
        # fullScreen.setPixmap(image)
        # # fullScreen.setStyleSheet("border: 1px solid black")
        # fullScreen.mousePressEvent = self.fullscreen

        fullScreen = QPushButton()
        fullScreen.setIcon(QIcon(image))
        fullScreen.setIconSize(QSize(30, 30))
        fullScreen.setFixedWidth(image.width())
        fullScreen.setFixedHeight(image.height())
        fullScreen.setStyleSheet("border: none")
        fullScreen.clicked.connect(self.fullscreen)

        '''
            Error Label not used yet.
        '''
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Maximum)



        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.length)
        controlLayout.addWidget(fullScreen)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        wid.setLayout(layout)

        self.setWindowTitle("Video Display from URL")
        self.resize(400, 400)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        # self.mediaPlayer.durationChanged.connect(self.durationChanged)
        # self.mediaPlayer.error.connect(self.handleError)
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)

        self.show()
        self.center()

    def mediaStatusChanged(self, status):
        print("Status: ", status)
        print("Duration: ", self.mediaPlayer.duration()/1000)
        self.positionSlider.setMinimum(0)
        self.positionSlider.setMaximum(self.mediaPlayer.duration()/1000)
        self.length.setText(str(int((self.mediaPlayer.position() / 1000) / 60)).zfill(2) + ":"
                            + str(round((self.mediaPlayer.position() / 1000) % 60)).zfill(2)
                            + "/" + str(int((self.mediaPlayer.duration() / 1000) / 60)) + ":"
                            + str(round((self.mediaPlayer.duration() / 1000) % 60)).zfill(2))

    def setPosition(self, position):
        if not self.positionSlider.isSliderDown():
            print("Track Position: ", position)
        else:
            print("Slider Down Position: ", position)

    def play(self):
        if not self.playState:
            self.mediaPlayer.play()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.playState = True
            self.resize(401, 400)
            self.resize(400, 400)
            self.center()
        else:
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.playState = False

    def pause(self):
        self.mediaPlayer.pause()

    def sliderReleased(self):
        print("Value: ", type(self.positionSlider.value()))
        self.mediaPlayer.setPosition(self.positionSlider.value() * 1000)

    # def play(self):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.mediaPlayer.pause()
    #     else:
    #         self.mediaPlayer.play()
    #
    # def mediaStateChanged(self, state):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.playButton.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPause))
    #     else:
    #         self.playButton.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPlay))
    #
    def positionChanged(self, position):
        print("Media Player Position: ", str(int(position / 1000)))
        self.positionSlider.setValue(position/1000)
        duration = str(int((self.mediaPlayer.duration() / 1000) / 60)) + ":" \
                   + str(round((self.mediaPlayer.duration() / 1000) % 60)).zfill(2)

        self.length.setText(str(int((self.mediaPlayer.position() / 1000) / 60)).zfill(2) + ":"
                            + str(round((self.mediaPlayer.position() / 1000) % 60)).zfill(2)
                            + "/" + duration)
    #
    # def durationChanged(self, duration):
    #     print("Duration Change Called")
    #     self.positionSlider.setRange(0, duration)
    #
    # def setPosition(self, position):
    #     # print("Slider: ", int(self.positionSlider.value() / 1000))
    #     print("Slider Pos: ", position)
    #     self.mediaPlayer.setPosition(position)
    #
    # def handleError(self):
    #     self.playButton.setEnabled(False)
    #     self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
    #
    # def sliderPressed(self):
    #     self.mediaPlayer.pause()
    #
    # def sliderReleased(self):
    #     self.mediaPlayer.play()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def closeEvent(self, a0: QCloseEvent):
        self.mediaPlayer.stop()

    # ====================================================== Try here
    def fullscreen(self, event):
        if self.videoWidget.isFullScreen():
            self.videoWidget.setFullScreen(False)
            self.show()
            # self.showNormal()
            print("Fullscreen: True")
        else:
            self.hide()

            self.videoWidget.setFullScreen(True)

            # widget = QWidget()
            # widget.setLayout(self.controlLayout)
            # widget.move(0, 0)
            # self.show()

            # self.showFullScreen()
            print("Fullscreen: False")

    def exitFullScreen(self, event):
        # print("Keypressevent", self.videoWidget.isFullScreen())
        # self.videoWidget.setFullScreen(False)
        # self.show()
        if event.key() == Qt.Key_Right:
            self.mediaPlayer.setPosition(self.mediaPlayer.position() + 5000)
            print(self.mediaPlayer.position())
        elif event.key() == Qt.Key_Left:
            self.mediaPlayer.setPosition(self.mediaPlayer.position() - 5000)
            print(self.mediaPlayer.position())
        elif event.key() == Qt.Key_Escape:
            self.videoWidget.setFullScreen(False)
            self.show()

        # if event.key() == Qt.Key_Escape:
        #     self.videoWidget.setFullScreen(False)
        #     # event.accept()
        #     # self.showNormal()
        #     print("Key Press")
        #     # self.fullscreen

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            duration = str(int((self.mediaPlayer.duration() / 1000) / 60)) + ":" \
                       + str(round((self.mediaPlayer.duration() / 1000) % 60)).zfill(2)

            min = str(int((self.mediaPlayer.duration() / 1000) / 60))
            sec = str(round((self.mediaPlayer.duration() / 1000) % 60)).zfill(2)

            # self.mediaPlayer.setPosition(self.mediaPlayer.position() + 5000)
            self.mediaPlayer.setPosition((self.positionSlider.value() * 1000) + 5000)
            if self.playState:
                self.mediaPlayer.pause()
                self.mediaPlayer.play()
                self.resize(401, 400)
                self.resize(400, 400)
                self.center()

            # self.length.setText(str(int((self.mediaPlayer.position() / 1000) / 60)).zfill(2) + ":"
            #                     + str(round((self.mediaPlayer.position() / 1000) % 60)).zfill(2)
            #                     + "/" + duration)
            print(self.mediaPlayer.position())
        elif event.key() == Qt.Key_Left:
            self.mediaPlayer.setPosition(self.mediaPlayer.position() - 5000)
            print(self.mediaPlayer.position())
        elif event.key() == Qt.Key_Space:
            self.play()
            # if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            #     self.mediaPlayer.pause()
            # else:
            #     self.mediaPlayer.play()
            #     self.resize(401, 401)
            #     self.resize(400, 400)



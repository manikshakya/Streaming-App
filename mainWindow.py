from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel,
                             QScrollArea)
from PyQt5.QtGui import (QPixmap, QImage)
from PyQt5.QtCore import Qt

from bs4 import BeautifulSoup
import requests

import urllib.request
from urllib.request import Request
import functools

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from mainVideo import MainVideo
from getVideo import GetVideo
from searchBar import SearchBar

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.base_url = ""

        self.init_ui()

    def init_ui(self):

        searchBar = SearchBar()
        self.addDockWidget(Qt.TopDockWidgetArea, searchBar)
        searchBar.search.connect(self.searchText)

        self.gridLayout = self.gridResult()

    '''
        VideoWindow: This function takes in video url and image index to get the video.
        Note:
            source_object = label ==> is not used by the function right now.
    '''
    def videoWindow(self, event, source_object=None, video=None, index=None):
        print("Clicked, from", source_object, video, "Index: ", index)

        # # self.getVideo(video)

        if self.cacheLinks[index] == "":
            videoUrl = GetVideo()
            url = videoUrl.getVideoLink(video)
            self.cacheLinks[index] = url
            # print(url)
        else:
            url = self.cacheLinks[index]

        print(url)
        self.mainVideo = MainVideo(self.base_url + url)

    def getVideo(self, url):
        # All Working in here ----------------------
        options = Options()
        options.add_argument("headless")

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"

        chrome_path = r"./driver/chromedriver"
        driver = webdriver.Chrome(chrome_path, chrome_options=options)
        driver.get(url)
        html = driver.page_source # driver.find_element_by_tag_name("html")
        # html = driver.find_element_by_id("player_el")
        driver.close()
        print(type(html))
        # print((html))
        # print(html.get_attribute("innerHTML"))
        # print(html.get_attribute("outerHTML"))

        self.getVideoLink(html)

        # print(self.base_url + videoLink["src"])
        # self.mainVideo = MainVideo(self.base_url + videoLink["src"])
        # print(driver.current_url)

    def getVideoLink(self, html):
        source = BeautifulSoup(html, "lxml")
        # source = BeautifulSoup(html, "html.parser")
        videoLink = source.find(id="player_el")
        print(type(videoLink))
        print(videoLink["src"])

    def searchText(self, text):
        if text != "":
            self.gridResult(self.base_url + "/" + "-".join(text.split()) + ".html")

        # self.update()

    def gridResult(self, url=None):
        if url is None:
            url = self.base_url

        source = requests.get(url).text

        html = BeautifulSoup(source, "lxml")

        # print("Source type: ", type(source))
        # print("HTML type: ", type(html))
        # print(html.prettify())

        links = html.select("div.post_text + a")
        titles = html.select("div.post_text")

        videoLinks = []
        imageLinks = []

        ''' Index to keep track of which image was clicked on. '''
        index = 0

        '''
            Create an empty array to store the links of the visited video.
        '''
        self.cacheLinks = []
        '''
            Initialize 36 empty string to the cachelinks array.
            To check if the link is present in that particular index. 
        '''
        for i in range(36):
            self.cacheLinks.append("")

        '''
            Iterate over the links to get the image source and the page source of the video.
        '''
        for link in links:
            if link.img is not None:
                img = "http:" + link.img['src']  # Get the image source

                url = Request(img)
                data = urllib.request.urlopen(url).read()

                image = QImage()
                image.loadFromData(data)

                container = QVBoxLayout()

                label1 = QLabel()
                label2 = QLabel(titles[index].text)
                # label1.setText("Hello")
                label1.setPixmap(QPixmap(image).scaled(200, 150, Qt.KeepAspectRatio))
                label1.setScaledContents(True)
                label1.setStyleSheet("border: 1px solid black")
                label1.mousePressEvent = functools.partial(self.videoWindow, source_object=label1,
                                                           video=self.base_url + link['href'], index=index)

                print(label2.text())

                label1.setMaximumWidth(320)
                label1.setMaximumHeight(200)

                label2.setMaximumWidth(230)
                label2.setMaximumHeight(15)

                container.addWidget(label2)
                container.addWidget(label1)

                videoLinks.append(self.base_url + link['href'])

                '''
                    Append all the data to attach to the GridLayout.
                '''
                imageLinks.append(container)
                # imageLinks.append(label1)
            index += 1

        '''
            Put all the images in the Grid Layout.
            Click the image to pop up the video playing window.
        '''
        a = 1
        r = 0
        c = 0
        gridLayout = QGridLayout()
        for x in imageLinks:
            if a < 3:
                a += 1
            else:
                a = 1

            gridLayout.addLayout(x, r, c)
            # gridLayout.addWidget(x, r, c)
            c += 1
            if c == 3:
                c = 0
                r += 1

        scrollArea = QScrollArea()

        scrollChildArea = QWidget()
        scrollChildArea.setLayout(gridLayout)

        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setMinimumHeight(600)
        scrollArea.setMaximumHeight(600)
        scrollArea.setWidget(scrollChildArea)
        # scrollArea.setFrameShape(QFrame().NoFrame)
        scrollArea.setStatusTip("Preview")

        # """ Get the image from the given URL  """
        # # Set argument headers={"User-Agent": "Mozilla/5.0"} to cheat the spider/bot agent
        # url = Request('http://s17.trafficdeposit.com/blog/img/5aeb0d1c0a832/5c77e2cdecca0/0.jpg')
        # data = urllib.request.urlopen(url).read()
        #
        # image = QImage()
        # image.loadFromData(data)

        self.setCentralWidget(scrollArea)

        self.setWindowTitle("Testing")
        self.resize(800, 600)
        self.show()

        return gridLayout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup

class GetVideo():

    def __init__(self):
        super().__init__()

        # self.init_ui(url)

    def getVideoLink(self, url):
        options = Options()
        options.add_argument("headless")

        chrome_path = r"./driver/chromedriver"
        driver = webdriver.Chrome(chrome_path, chrome_options=options)
        driver.get(url)

        html = driver.page_source  # driver.find_element_by_tag_name("html")
        # html = driver.find_element_by_id("player_el")
        driver.close()
        # print(type(html))

        source = BeautifulSoup(html, "lxml")
        # source = BeautifulSoup(html, "html.parser")
        videoLink = source.find(id="player_el")
        # print(type(videoLink))
        # print(videoLink["src"])

        return videoLink["src"]
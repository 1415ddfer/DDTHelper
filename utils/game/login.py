import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from utils.game.default import *


class PostLogin(requests.Session):
    def __init__(self, acc):
        super().__init__()
        self.acc = acc

    def post_login(self):
        self.post(url=POST_URL_43, data=POST_4399(self.acc[3], self.acc[4]), headers=POST_HEADER)

    def post_login_7k(self):
        self.post(url=POST_URL_7k, data=POST_7K7K(self.acc[3], self.acc[4]), headers=POST_HEADER)

    def get_url_7k(self):
        res2 = self.get(url=SERVER_7K7K(self.acc[1]), headers=POST_HEADER)  # 成功登陆以后，查看我们的用户数据
        soup = BeautifulSoup(res2.text, 'lxml')
        iframe_value = soup.select_one("#url").attrs["value"]

        SId = iframe_value.split('&')[2].split('=')[1]

        res3 = self.get(url=iframe_value, headers=POST_HEADER)
        soup = BeautifulSoup(res3.text, 'lxml')
        return GAME_7K7K(SId, soup.select_one("#\\37 road-ddt-game > embed").attrs["src"])

    def get_url(self):
        res2 = self.get(url=SERVER_4399(self.acc[1]), headers=POST_HEADER)  # 成功登陆以后，查看我们的用户数据

        soup = BeautifulSoup(res2.text, 'lxml')
        iframe_src = soup.select_one("#game_box").attrs["src"]

        SId = iframe_src.split('&')[4].split('=')[1]

        res3 = self.get(iframe_src, headers=POST_HEADER)
        soup = BeautifulSoup(res3.content, 'lxml')
        return GAME_4399(SId, soup.select_one("#\\37 road-ddt-game > embed").attrs["src"])


# 模拟登陆方案
class Browser(webdriver.Chrome):
    def __init__(self, account):
        self.has_true = False
        self.account = account
        super().__init__(executable_path='./plugin/chromedriver')

    def do7k7k(self):
        self.get(SERVER_7K7K(self.account[1]))
        try:
            self.find_element_by_id('username').send_keys(self.account[3])
        except:
            time.sleep(10)
            return
        self.find_element_by_id('password').send_keys(self.account[4])
        print(self.find_element_by_id('password').submit())
        for i in range(0, 100):
            time.sleep(0.5)
            if self.isElementExist('iframepage'):
                self.has_true = True
                break
        if self.has_true:
            iframe = self.find_element_by_id('iframepage')
            # //*[@id="iframepage"]
            # 切换嵌套的页面
            print(iframe.get_attribute("src"))
            self.switch_to.frame(iframe)
            self.flash = self.find_element_by_xpath('//*[@id="7road-ddt-game"]/embed')
            self.url = self.flash.get_attribute('src')
            print(self.url)
        self.quit()
        if self.has_true:
            return self.url

    def do4933(self):
        self.get(SERVER_4399(self.account[1]))
        try:
            self.find_element_by_id('s_user').send_keys(self.account[3])
        except:
            time.sleep(10)
            return
        self.find_element_by_id('s_password').send_keys(self.account[4])
        print(self.find_element_by_id('s_password').submit())
        for i in range(0, 100):
            time.sleep(0.5)
            if self.isElementExist('game_box'):
                self.has_true = True
                break
        if self.has_true:
            iframe = self.find_element_by_id('game_box')
            # //*[@id="game_box"]
            # //*[@id="iframepage"]
            # 切换嵌套的页面
            print(iframe.get_attribute("src"))
            self.switch_to.frame(iframe)
            self.flash = self.find_element_by_xpath('//*[@id="7road-ddt-game"]/embed')
            self.url = self.flash.get_attribute('src')
            print(self.url)
        self.quit()
        if self.has_true:
            return self.url

    def isElementExist(self, element):
        flag = True
        try:
            self.find_element_by_id(element)
            return flag
        except:
            flag = False
            return flag

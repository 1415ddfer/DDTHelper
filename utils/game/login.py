import time

from bs4 import BeautifulSoup
from requests import Session

from utils.game.default import *


class PostLogin(Session):
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

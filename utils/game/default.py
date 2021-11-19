RES_PATH = './res/'

TITLE_ICON_GAME = RES_PATH + "title.png"

TITLE_PLUGIN_RUNNING = RES_PATH + "run.jpge"
TITLE_PLUGIN_STOPPED = RES_PATH + "end.jpge"


# login mode
POST_URL_43 = 'http://ptlogin.4399.com/ptlogin/login.do?v=1'
POST_URL_7k = 'http://zc.7k7k.com/post_login'
POST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36 '}


def POST_4399(user, password):
    return {
        'loginFrom': 'uframe',
        'postLoginHandler': 'default',
        'layoutSelfAdapting': 'true',
        'externalLogin': 'qq',
        'displayMode': 'popup',
        'layout': 'vertical',
        'appId': 'www_home',
        'mainDivId': 'popup_login_div',
        'includeFcmInfo': 'false',
        'userNameLabel': '4399用户名',
        'userNameTip': '请输入4399用户名',
        'welcomeTip': '欢迎回到4399',
        'username': user,
        'password': password
    }


def POST_7K7K(user, password):
    return {
        'username': user,
        'password': password,
        'rf': 'http://www.7k7k.com/#bottom'
    }


# url
def SERVER_4399(s_id):
    return "http://web.4399.com/stat/togame.php?target=ddt&server_id=S" + str(s_id)


def SERVER_7K7K(s_id):
    return "http://web.7k7k.com/games/togame.php?target=ddt_7&server_id=" + str(s_id)


def GAME_4399(s_id, data):
    return 'http://' + str(s_id) + '.ddt.qq933.com/' + data


def GAME_7K7K(s_id, data):
    return 'http://s' + str(s_id) + '.ddt.youxi567.com/' + data
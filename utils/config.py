import json
import sqlite3


class SQLHelper:
    file_db = './userDate/acc.db'

    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect(self.file_db)
        self.c = self.con.cursor()

    def get_all_table(self):
        try:
            self.c.execute("select name from sqlite_master where type='table'")
            tab_name = self.c.fetchall()
            tab_name = [line[0] for line in tab_name]
            return tab_name
        except sqlite3.Error as e:
            print(e)
            return []

    def get_all_row(self, table):
        str_command = "SELECT * FROM " + table
        self.c.execute(str_command)
        return self.c.fetchall()

    def get_max_row(self, table):
        str_command = "SELECT max(rowid) from " + str(table)
        self.c.execute(str_command)
        print(self.c.fetchone()[0])  # .fetchone()[0]

    def create_table(self, table):
        str_command = '''
        CREATE TABLE ''' + table + '''
        (
        SERVER_NAME          INT     NOT NULL,
        SERVER_ID            INT     NOT NULL,
        DIY_NAME             TEXT    NOT NULL,
        USER                 TEXT    NOT NULL,
        PASS_WORLD           TEXT    NOT NULL)
        '''
        self.c.execute(str_command)

    def is_have_user_in_team(self, table, user):
        str_command = "SELECT * FROM " + table + " WHERE user= '" + user + "'"
        try:
            self.c.execute(str_command)
        except sqlite3.Error as e:
            print(e)
            return False
        if not self.c.fetchall():
            return True
        return False

    def add_user(self, table, acc):
        str_command = "INSERT INTO " \
                      + table + \
                      " (SERVER_NAME,SERVER_ID,DIY_NAME,USER,PASS_WORLD) VALUES (?,?,?,?,?)"
        self.c.execute(str_command, (acc[0], acc[1], acc[2], acc[3], acc[4]))

    def del_user(self, group, user):
        str_command = '''
        DELETE FROM ''' + group + ''' 
        WHERE USER = "''' + user + '''"'''
        try:
            self.c.execute(str_command)
        except Exception as e:
            print(e)

    def update_user(self, table, acc, old_user):
        str_command = "UPDATE " + table + " "\
                      "SET SERVER_NAME = ?," \
                      "SERVER_ID = ?," \
                      "DIY_NAME = ?," \
                      "USER = ?," \
                      "PASS_WORLD = ? " \
                      "WHERE USER = ?"
        try:
            self.c.execute(str_command, (acc[0], acc[1], acc[2], acc[3], acc[4], old_user))
        except Exception as e:
            print(e)

    def del_table(self, table):
        str_command = 'drop table ' + table
        self.c.execute(str_command)

    def close(self):
        self.con.commit()
        self.con.close()


def set_defaults():
    def_str = {
        'flash': {
            'mode': 1
        },
        'login': {
            'mode': 'null',
            'group_state': 0,
            'driver': False
        },
        'group': {
            '第一队': 'TEAM0'
        }}
    def_js = json.dumps(def_str)
    def_file = open("config.json", 'w')
    def_file.write(def_js)
    def_file.close()


class GetConfig:
    acc = []  # [[服务商,区服,显示名字,账号,密码], ]
    default_config = []
    group = []
    group_db = []
    flash_status = -1
    flash_obj = None
    config_file = "config.json"
    acc_file = './userdata/acc.bin'
    flash_sa = './plugin/flashplayer_sa.exe'
    flash_ocx = './plugin/Flash64_34_0_0_92.ocx'
    web_driver = './plugin/chromedriver'
    flash_com = "{D27CDB6E-AE6D-11CF-96B8-444553540000}"

    dbHelper = None

    def __init__(self):
        super(GetConfig, self).__init__()
        # 读取配置文件
        try:
            with open(self.config_file, 'r') as f:
                self.data = json.load(f)
        except Exception as e:
            print(e)
            set_defaults()
            with open(self.config_file, 'r') as f:
                self.data = json.load(f)
        self.init_data()

    def get_group(self):
        # self.group = list(map(str, sorted(self.data['group'].keys())))
        # self.group.reverse()
        for key in self.data['group']:
            self.group.append(key)

    def init_data(self):
        self.get_group()
        self.dbHelper = SQLHelper()
        self.group_db = self.dbHelper.get_all_table()
        print(self.group_db)
        self.check_db()
        if self.get_group_state() == 'null':
            print('初始化...')
            self.set_group_state(self.group[0])
        self.init_team(self.get_group_state())

    def init_team(self, key):
        if self.dbHelper is None:
            self.dbHelper = SQLHelper()
        try:
            self.acc = self.dbHelper.get_all_row(self.data['group'][key])
            self.set_group_state(key)
        except KeyError:
            print('key错误')
            print(key)
            if self.group:
                print(self.group[0])
                self.set_group_state(self.group[0])
                key = self.get_group_state()
                self.acc = self.dbHelper.get_all_row(self.data['group'][key])
                self.set_group_state(key)
            else:
                print('no team')

        self.dbHelper.close()
        self.dbHelper = None

    def get_group_state(self):
        return self.data['login']['group_state']

    def set_group_state(self, key):
        self.data['login']['group_state'] = key

    def change_cf(self, key_0, key_1, value_):
        print(key_0, key_1, value_)
        self.data[key_0][key_1] = value_
        self.save_cf()

    def save_cf(self):
        def_js = json.dumps(self.data)
        print('配置已保存')
        def_file = open("config.json", 'w')
        def_file.write(def_js)
        def_file.close()

    def create_new_team(self, name):
        if self.dbHelper is None:
            self.dbHelper = SQLHelper()
        num = int(list(self.data['group'].values())[-1][4]) + 1
        self.data['group'][name] = 'TEAM' + str(num)
        self.dbHelper.create_table('TEAM' + str(num))
        self.change_cf('login', 'group_state', name)
        self.group = []
        self.get_group()

    def check_db(self):
        if not self.dbHelper.get_all_table():
            self.dbHelper.create_table('TEAM0')
        if self.dbHelper.get_all_table() != self.data['group']:
            if len(self.dbHelper.get_all_table()) > len(self.group):
                for i in range(len(self.dbHelper.get_all_table()) - len(self.group)):
                    self.data['group']['第' + str(len(self.group) + 1) + '队'] = 'TEAM' + str(len(self.group))
                    print('导入没被标注的表')
                    self.save_cf()
            else:
                for i in range(len(self.group) - len(self.dbHelper.get_all_table())):
                    self.dbHelper.create_table('TEAM' + str(len(self.group) - 1))
                    print('创建没导入的表')

    def rename_team(self, o, n):
        self.data['group'][n] = self.data['group'].pop(o)
        self.save_cf()

    def del_team(self, o):
        if self.dbHelper is None:
            self.dbHelper = SQLHelper()
        self.dbHelper.del_table(self.data['group'].pop(o))
        self.save_cf()
        self.dbHelper.close()
        self.dbHelper = None

    def add_data(self, list0, team):
        if self.dbHelper is None:
            self.dbHelper = SQLHelper()
        if team is None:
            team = self.data['group'][str(self.get_group_state())]
        if self.dbHelper.is_have_user_in_team(team, list0[3]):
            self.dbHelper.add_user(team, list0)

    def del_user(self, user):
        if self.dbHelper is None:
            self.dbHelper = SQLHelper()
        self.dbHelper.del_user(self.data['group'][str(self.get_group_state())], user[3])

    def rewrite_data(self, res, user):
        if self.dbHelper is None:
            self.dbHelper = SQLHelper()
        self.dbHelper.update_user(self.data['group'][str(self.get_group_state())], res, user)

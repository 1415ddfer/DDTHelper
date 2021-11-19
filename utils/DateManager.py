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
        print('aaa')

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
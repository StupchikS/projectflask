import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = "SELECT * FROM mainmenu"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения базы данных " + str(e))
        return []

    def get_menu2(self):
        sql = "SELECT * FROM mainmenu2"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения базы данных " + str(e))
        return []

    def get_now_auto(self):
        sql = "SELECT * FROM autonow"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения базы данных " + str(e))
        return []

    def get_past_auto(self):
        sql = "SELECT * FROM autopast"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения базы данных " + str(e))
        return []

    def add_auto(self, marka, model, information, year, price):
        try:
            self.__cur.execute("INSERT INTO autobase VALUES(NULL, ?, ?, ?, ?, ?)", (marka, model, information, year, price))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка записи базы данных" + str(e))
            return False
        return True

    def get_auto(self):
        try:
            self.__cur.execute(f"SELECT * FROM autobase")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("ошибка чтения базы данных" + str(e))
        return False

    def get_auto_id(self, select_id):

        try:
            self.__cur.execute(f"SELECT * FROM autobase WHERE id LIKE '{select_id}'")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("ошибка чтения базы данных" + str(e))

        return False

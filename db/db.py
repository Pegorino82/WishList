import json
import mysql.connector
from mysql.connector import errorcode

with open('db/settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)


class MySQLDB:
    USER = settings.get('USER')
    PASSWORD = settings.get('PASSWORD')
    HOST = settings.get('HOST')

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        '''
        Подключется к базе self.db_name, если такой не существует, то создает ее
        :return: None
        '''
        self.conn = mysql.connector.connect(
            host=self.HOST,
            user=self.USER,
            password=self.PASSWORD,
        )
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                '''CREATE SCHEMA IF NOT EXISTS {} CHARACTER SET `UTF8`'''.format(self.db_name)
            )
            self.conn.connect(database=self.db_name)
        except mysql.connector.Error as err:
            print(err)

    def create_table(self):
        '''
        Создает таблицу wishes
        :return: None
        '''
        sql = """CREATE TABLE IF NOT EXISTS `wishes` (
                `id` INT(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `title` VARCHAR(25) NOT NULL,
                `price` FLOAT NOT NULL,
                `link` VARCHAR(128) NOT NULL,
                `snippet` VARCHAR(512) )"""
        self.cursor.execute(sql)

    def add_wish(self, title: str, price: (float, int), link: str, snippet: str):
        '''
        Создает новую запись в таблице wishes
        :param title: название желания
        :param price: цена
        :param link: ссылка
        :param snippet: описание
        :return: id or None
        '''
        sql = """INSERT INTO `wishes` 
        (`title`, `price`, `link`, `snippet`)
         VALUES 
         (%s, %s, %s, %s)"""
        try:
            self.cursor.execute(sql, (title, price, link, snippet))
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(err)

    def fetch_all(self):
        '''
        Возвращает все записи
        :return: generator object
        '''
        sql = """SELECT * FROM `wishes`"""
        self.cursor.execute(sql)
        return (x for x in self.cursor.fetchall())

    def fetch_one(self, **kwargs):
        '''
        Возвращает одну запись, удовлетворяющую условиям в **kwargs
        :param kwargs: аргуманты для извлечения записи поле: значение
        :return: найденная запись в tuple
        '''
        sql = """SELECT * FROM `wishes` WHERE {}""".format(
            ' AND '.join([f'{item[0]} = \'{item[1]}\'' for item in kwargs.items()]))
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def update_wish(self, wish_id: int, **kwargs):
        '''
        Обновляет запись по id значениями из **kwargs
        :param wish_id: id записи
        :param kwargs: аргуманты для обновления поле: значение
        :return:
        '''
        sql = """UPDATE `wishes` SET {} WHERE id = %s""".format(
            ', '.join([f'{item[0]} = \'{item[1]}\'' for item in kwargs.items()]))
        try:
            self.cursor.execute(sql, (wish_id,))
            self.conn.commit()
            self.cursor.execute("""SELECT * FROM `wishes` WHERE id=%s""", (wish_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

    def delete_wish(self, wish_id: int):
        '''
        Удаляет запись по id
        :param wish_id: id записи
        :return: None
        '''
        sql = """DELETE FROM `wishes` WHERE id = %s"""
        self.cursor.execute(sql, (wish_id,))
        self.conn.commit()


if __name__ == '__main__':
    pass

import webbrowser
from PyQt5 import QtWidgets, uic
from templates.main_form import Ui_MainWindow as ui_class
from db.db import MySQLDB


class WishListForm(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__get_db()
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.createButton.clicked.connect(self.create_wish_item)
        self.ui.browser.cellClicked.connect(self.row_action)

        self.show_wishes()

    def __get_db(self):
        self.db = MySQLDB('wish_list_db')
        self.db.connect()
        self.db.create_table()

    def row_action(self):
        '''
        Действия с выбранной записью (редактировать, удалить, перейти по ссылке)
        :return:None
        '''
        row = self.ui.browser.currentRow()
        self.ui.browser.selectRow(row)
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setWindowTitle('Action')
        msg.setText('Выберите действие')

        edit_button = msg.addButton('Редактировать', QtWidgets.QMessageBox.AcceptRole)
        del_button = msg.addButton('Удалить', QtWidgets.QMessageBox.AcceptRole)
        link_button = msg.addButton('Перейти по ссылке', QtWidgets.QMessageBox.AcceptRole)
        msg.addButton('Отмена', QtWidgets.QMessageBox.RejectRole)

        msg.exec()

        # edit row
        if msg.clickedButton() == edit_button:
            wish_id = self.ui.browser.item(row, 0).text()
            title = self.ui.browser.item(row, 1).text()
            price = self.ui.browser.item(row, 2).text()
            link = self.ui.browser.item(row, 3).text()
            snippet = self.ui.browser.item(row, 4).text()
            self.edit_wish(row, wish_id, title, price, link, snippet)

        # delete row
        elif msg.clickedButton() == del_button:
            result = QtWidgets.QMessageBox.question(self,
                                                    "Потверждение",
                                                    f"Удалить запись {self.ui.browser.item(row, 1).text()}?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                wish_id = self.ui.browser.item(row, 0).text()
                self.db.delete_wish(wish_id)
                self.ui.browser.removeRow(row)

        # forward link
        elif msg.clickedButton() == link_button:
            link = self.ui.browser.item(row, 3).text()
            try:
                webbrowser.open_new_tab(link)
            except Exception as err:
                print(err)

    def show_wishes(self):
        '''
        Заполняет таблицу записями из бд
        :return:None
        '''
        for row, wish in enumerate(self.db.fetch_all()):
            self.ui.browser.insertRow(row)
            self.ui.browser.setItem(row, 0, QtWidgets.QTableWidgetItem(str(wish[0])))  # id
            self.ui.browser.setItem(row, 1, QtWidgets.QTableWidgetItem(wish[1]))  # title
            self.ui.browser.setItem(row, 2, QtWidgets.QTableWidgetItem(str(wish[2])))  # price
            self.ui.browser.setItem(row, 3, QtWidgets.QTableWidgetItem(wish[3]))  # link
            self.ui.browser.setItem(row, 4, QtWidgets.QTableWidgetItem(wish[4]))  # snippet

    def add_wish(self, wish_id: int):
        '''
        Добавляет (новую) запись в конец
        :param wish_id: Id (созданной) записи
        :return:None
        '''
        wish = self.db.fetch_one(id=wish_id)
        row = self.ui.browser.rowCount()
        self.ui.browser.insertRow(row)
        self.ui.browser.setItem(row, 0, QtWidgets.QTableWidgetItem(str(wish[0])))  # id
        self.ui.browser.setItem(row, 1, QtWidgets.QTableWidgetItem(wish[1]))  # title
        self.ui.browser.setItem(row, 2, QtWidgets.QTableWidgetItem(str(wish[2])))  # price
        self.ui.browser.setItem(row, 3, QtWidgets.QTableWidgetItem(wish[3]))  # link
        self.ui.browser.setItem(row, 4, QtWidgets.QTableWidgetItem(wish[4]))  # snippet

    def create_wish_item(self):
        '''
        Активирует окно для создания записи
        :return:None
        '''
        dialog = uic.loadUi('templates/create_form.ui')

        def save_wish():
            '''
            Сохраняет запись из данных формы в бд
            :return:None
            '''
            title = dialog.titleField.text()
            price = dialog.priceField.text()
            link = dialog.linkField.text()
            snippet = dialog.snippetField.toPlainText()

            wish_id = self.db.add_wish(title, float(price.replace(',', '.')), link, snippet)

            dialog.titleField.clear()
            dialog.priceField.clear()
            dialog.linkField.clear()
            dialog.snippetField.clear()

            dialog.close()
            self.add_wish(wish_id)

        dialog.acceptButton.clicked.connect(save_wish)
        dialog.cancelButton.clicked.connect(lambda: dialog.close())
        dialog.exec()

    def update_wish(self, row: int, wish: tuple):
        '''
        Обновляет строку таблицы данными из wish
        :param row: номер строки
        :param wish: кортеж с данными записи из бд (id: int, title: str, price: float, link: str, snippet: str)
        :return:None
        '''
        self.ui.browser.setItem(row, 0, QtWidgets.QTableWidgetItem(str(wish[0])))  # id
        self.ui.browser.setItem(row, 1, QtWidgets.QTableWidgetItem(wish[1]))  # title
        self.ui.browser.setItem(row, 2, QtWidgets.QTableWidgetItem(str(wish[2])))  # price
        self.ui.browser.setItem(row, 3, QtWidgets.QTableWidgetItem(wish[3]))  # link
        self.ui.browser.setItem(row, 4, QtWidgets.QTableWidgetItem(wish[4]))  # snippet

    def edit_wish(self, row: int, wish_id: int, title: str, price: float, link: str, snippet: str):
        '''
        Открывает окно для редактирования записи и заполняет его данными
        :param row: номер строки таблицы
        :param wish_id: id записи
        :param title: текущее название
        :param price: текущая цена
        :param link: текущая ссылка
        :param snippet: текущее описание
        :return:None
        '''
        dialog = uic.loadUi('templates/create_form.ui')

        dialog.titleField.setText(title)
        dialog.priceField.setValue(float(price.replace(',', '.')))
        dialog.linkField.setText(link)
        dialog.snippetField.setText(snippet)

        def update_wish(row: int, wish_id: int):
            '''
            Обновляет запись в бд и вызывает функцию обновления строки в таблице
            :param row: номер строки таблицы
            :param wish_id: id записи
            :return:None
            '''
            title = dialog.titleField.text()
            price = dialog.priceField.text()
            link = dialog.linkField.text()
            snippet = dialog.snippetField.toPlainText()

            updated_wish = self.db.update_wish(
                wish_id,
                title=title,
                price=float(price.replace(',', '.')),
                link=link,
                snippet=snippet
            )

            dialog.close()
            self.update_wish(row, updated_wish)

        dialog.acceptButton.clicked.connect(lambda: update_wish(row, wish_id))
        dialog.cancelButton.clicked.connect(lambda: dialog.close())
        dialog.exec()


if __name__ == '__main__':
    pass

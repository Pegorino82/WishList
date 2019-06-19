import sys
from PyQt5 import QtWidgets
from wish_gui import WishListForm


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WishListForm()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

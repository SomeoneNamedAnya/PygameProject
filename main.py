import sys

class HomePage(QMainWindow):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    ex.show()
    sys.exit(app.exec_())

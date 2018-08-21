from MainAction import MainWindow
from PyQt5 import QtWidgets
from PyQt5 import Qt


if __name__ == "__main__":
    import sys
    print("QT VERSION: ", Qt.PYQT_VERSION_STR)
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

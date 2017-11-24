# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""



from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from libs import myImageScene

from Ui_Form import Ui_MainWindow
from libs import myItemType

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.image = None
        self.image_scene = myImageScene(self.statusBar)
        self.graphicsView.setScene(self.image_scene)


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Slot documentation goes here.
        """
        self.image_path_list, img_type = QtWidgets.QFileDialog.getOpenFileNames(caption='choice image..', filter='*.jpg;;*.png')
        self.statusBar.showMessage('add image list..')
        self.img_idx = 0
        self.all_img_num = len(self.image_path_list)
        self.listWidget_image_list.addItems(self.image_path_list)
        self.display_image()

    def cursor_next(self):
        if self.img_idx >= self.all_img_num - 1:
            return False
        else:
            self.img_idx += 1
            return True

    def cursor_prev(self):
        if self.img_idx <= 0:
            return False
        else:
            self.img_idx -= 1
            return True

    def display_image(self):
        # cv_image = cv2.imread(image_path)
        # h, w, c = cv_image.shape
        # bytes_per_line = w * c
        # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        # qt_image = QtGui.QImage(cv_image, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        if self.all_img_num == 0:
            return

        image_path = self.image_path_list[self.img_idx]
        pixmap = QtGui.QPixmap()
        pixmap.load(image_path)
        self.image = QtWidgets.QGraphicsPixmapItem(pixmap)

        self.image_scene.clear()
        # rect = QtCore.QRectF(0, 0, 0, 0)
        # self.graphicsView.setSceneRect(rect)
        self.image_scene.addItem(self.image)


    @pyqtSlot()
    def on_actionNext_Image_triggered(self):
        if self.image:
            self.image_scene.removeItem(self.image)
        if self.cursor_next():
            self.display_image()


    @pyqtSlot()
    def on_actionPrev_Image_triggered(self):
        if self.image:
            self.image_scene.removeItem(self.image)
        if self.cursor_prev():
            self.display_image()


    @pyqtSlot()
    def on_actionCreate_RectBox_triggered(self):
        self.image_scene.setInsertType(myItemType.RECT)

    @pyqtSlot()
    def on_actionZoom_in_triggered(self):
        self.image_scene.setInsertType(myItemType.CIRCLE)

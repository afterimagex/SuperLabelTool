# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""



from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from libs import myImageScene

# from Ui_Form import Ui_MainWindow
from Form_ui import Ui_MainWindow
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

        # self.treeWidget_file.topLevelItem(0).setText(0, _translate("MainWindow", "23123.jpg"))


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Slot documentation goes here.
        """
        self.image_list, img_type = \
            QtWidgets.QFileDialog.getOpenFileNames(caption='choice image..',
                                                   filter='JPEG(*.jpg);;PNG(*.png);;ALL(*.*)')
        self.img_idx = 0
        self.all_num_img = len(self.image_list)

        # for i in range(len(image_list)):
        #     QtWidgets.QTreeWidgetItem(self.treeWidget_file)
        #     _dir, _file = os.path.split(image_list[i])
        #     self.dockFilelist.setWindowTitle(_dir)
        #     self.treeWidget_file.topLevelItem(i).setText(0, _file)
        self.display_image()

    @pyqtSlot()
    def on_actionOpen_Dir_triggered(self):
        pass

    @pyqtSlot()
    def on_actionOpen_Annotation_Dir_triggered(self):
        pass

    @pyqtSlot()
    def on_pushButton_editer_clicked(self):
        name_str = self.lineEdit_editer.text()
        title_str = 'Editer---[{}]'.format(name_str)
        if len(name_str) > 0:
            self.groupBox_editer.setTitle(title_str)


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
        if self.all_num_img <= 0:
            pass

        # image_path = self.listWidget_image_list.item(self.img_idx).text()
        image_path = self.image_list[self.img_idx]
        pixmap = QtGui.QPixmap()
        pixmap.load(image_path)
        self.image = QtWidgets.QGraphicsPixmapItem(pixmap)

        # self.image_scene.clear()
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
    def on_actionZoomIn_triggered(self):
        self.image_scene.setInsertType(myItemType.CIRCLE)

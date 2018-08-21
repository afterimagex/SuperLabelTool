# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThread, pyqtBoundSignal
from PyQt5.QtGui import QImage
from libs import myImageScene
from PIL import Image
from PIL import ImageFile
from PIL.ImageQt import ImageQt
import configparser
import time

# from Ui_Form import Ui_MainWindow
from Form_ui import Ui_MainWindow
from modules.PascalVoc import PascalVocEngine
import pytesseract
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

os.environ['TESSDATA_PREFIX'] = os.path.join('./tesseract', 'tessdata')
pytesseract.pytesseract.tesseract_cmd = os.path.join('./tesseract', 'tesseract.exe')

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

        self.image_scene = myImageScene(self)
        self.graphicsView.setScene(self.image_scene)
        # self.graphicsView.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        # self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.graphicsView.setRenderHint(QtGui.QPainter.TextAntialiasing)

        # self.graphicsView.wheelEvent.connect(self.gview_event)

        self.img_idx = 0
        self.all_img_num = 0
        self.editor = 'unkonw'
        self.editor_lock = False
        self.pascal_voc = PascalVocEngine('test')
        self.change_flag = False
        self.resize_flag = False
        self.text_change_flag = False
        self.has_tesseract = True
        self.load_label_word()
        self.treeWidget_file.itemDoubleClicked.connect(self.on_treeWidget_file_dclicked)
        # self.treeWidget_file.topLevelItem(0).setText(0, _translate("MainWindow", "23123.jpg"))
        self.graphicsView.installEventFilter(self)
        self.image_scene.wheel_scroll.connect(self.scene_wheel)
        self.image_scene.mouse_position.connect(self.scene_mouse_pos_update)
        self.image_scene.rectInserted.connect(self.rect_inserted)


    def rect_inserted(self, item):
        pass


    def scene_wheel(self, p_int):
        factor = 1.41 ** (p_int / 240.0)
        self.graphicsView.scale(factor, factor)

    def scene_mouse_pos_update(self, x, y):
        self.statusBar.showMessage('X:{} Y:{}'.format(x, y))

    def mkr(self, fx):
        if not os.path.exists(fx):
            os.makedirs(fx)
        return fx

    def get_config(self, section, key):
        config = configparser.ConfigParser()
        cfg_file = os.path.split(os.path.realpath(__file__))[0] + '/db.conf'
        try:
            config.read(cfg_file)
            return config.get(section, key)
        except FileNotFoundError:
            print("db.conf is not found.")

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Slot documentation goes here.
        """
        self.image_list, img_type = \
            QtWidgets.QFileDialog.getOpenFileNames(caption='choice image..',
                                                   filter='JPEG(*.jpg);;PNG(*.png);;ALL(*.*)')
        self.img_idx = 0
        self.all_img_num = len(self.image_list)
        self.update()

    def on_treeWidget_file_dclicked(self, tree_item, p_int):
        index = self.treeWidget_file.indexFromItem(tree_item, 0)
        self.im_index_at(index.row())

    @pyqtSlot()
    def on_actionOpen_Dir_triggered(self):
        try:
            default_dir = self.get_config('image_dir', 'path')
        except:
            default_dir = './'
        try:
            dir_name = QtWidgets.QFileDialog.getExistingDirectory(caption='choice image directory..',
                                                                  directory=default_dir)
        except:
            return

        self.img_idx = 0
        self.image_list = [os.path.join(dir_name, d) for d in os.listdir(dir_name) if
                           d.endswith('jpg') | d.endswith('PNG') and d[0] != '.']
        print(self.image_list)

        if len(self.image_list) <= 0:
            return
        self.all_img_num = len(self.image_list)

        for i in range(len(self.image_list)):
            tree_item = QtWidgets.QTreeWidgetItem(self.treeWidget_file)
            _dir, _file = os.path.split(self.image_list[i])
            self.dockFilelist.setWindowTitle(_dir)
            tree_item.setText(0, _file)
            # self.treeWidget_file.topLevelItem(i).setText(0, _file)
        self.update_image()

    @pyqtSlot()
    def on_actionOpen_Annotation_Dir_triggered(self):
        try:
            default_dir = self.get_config('anno_dir', 'path')
        except:
            default_dir = './'
        try:
            self.anno_save_dir = QtWidgets.QFileDialog.getExistingDirectory(caption='choice anno save directory..',
                                                                            directory=default_dir)
        except:
            return

    def update_image(self):

        if self.all_img_num <= 0:
            return

        self.image_scene.clear()

        image_path = self.image_list[self.img_idx]
        image = Image.open(image_path)

        if self.resize_flag:
            old_size = image.size
            width = self.doubleSpinBox_rw.value()
            height = self.doubleSpinBox_rh.value()
            if self.radioButton_refixed.isChecked():
                width = int(round(float(width)))
                height = int(round(float(height)))
                self.label_3.setText("Pixel")
                if width > 0 and height > 0:
                    image = image.resize((width, height))
            if self.radioButton_rescale.isChecked():
                self.label_3.setText("Ratio")
                if width > 0 and height > 0 and width and 100 and height < 100:
                    nw = int(round(1.0 * old_size[0] * width))
                    nh = int(round(1.0 * old_size[1] * height))
                    image = image.resize((nw, nh))

        self.bak_image = image
        if self.checkBox.isChecked():
            self.ocr_detect()

        if self.radioButton_word.isChecked():
            im_base_name = os.path.split(self.image_list[self.img_idx])[-1]
            im_loc = im_base_name.rfind('_')
            base_key = im_base_name[:im_loc]
            try:
                text_word = '\n'.join(self.words_map[base_key])
                self.textEdit.setText(text_word)
            except:
                pass

        im_data = image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QtGui.QImage(im_data, image.size[0], image.size[1], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)
        ###############
        # qim = ImageQt(image)
        # pixmap = QtGui.QPixmap.fromImage(qim)
        ###############
        self.image_scene.addPixmap(pixmap)
        self.image_scene.setSceneRect(self.image_scene.itemsBoundingRect())

        self.statusBar.showMessage(image_path)

    @pyqtSlot()
    def on_actionNext_triggered(self):
        self.next_index()
        self.read_text_anno()

    @pyqtSlot()
    def on_actionPrev_triggered(self):
        self.prev_index()
        self.read_text_anno()

    def im_index_at(self, p_int):
        try:
            assert 0 <= p_int < self.all_img_num
            self.img_idx = p_int
            self.image_scene.clear()
            self.update_image()
        except:
            pass

    def next_index(self):
        if self.img_idx >= self.all_img_num - 1:
            pass
        else:
            self.img_idx += 1
            self.image_scene.clear()
            self.update_image()

    def prev_index(self):
        if self.img_idx <= 0:
            pass
        else:
            self.img_idx -= 1
            self.image_scene.clear()
            self.update_image()

    @pyqtSlot()
    def on_actionCreate_RectBox_triggered(self):
        pass
        # self.image_scene.setInsertType(myItemType.RECT)

    @pyqtSlot()
    def on_actionZoomIn_triggered(self):
        factor = 1.41 ** (120 / 240.0)
        self.graphicsView.scale(factor, factor)
        # self.image_scene.setInsertType(myItemType.CIRCLE)

    @pyqtSlot()
    def on_actionZoomOut_triggered(self):
        factor = 1.41 ** (-120 / 240.0)
        self.graphicsView.scale(factor, factor)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        if self.editor_lock:
            self.lineEdit_3.setDisabled(False)
            self.pushButton_2.setText('OK')
            self.editor_lock = False
        else:
            self.editor = self.lineEdit_3.text()
            self.lineEdit_3.setDisabled(True)
            self.pushButton_2.setText('unlock')
            self.editor_lock = True

    def save_anno(self):
        if self.text_change_flag:
            try:
                bs_idx = os.path.split(self.image_list[self.img_idx])[-1]
                bs_idx = os.path.splitext(bs_idx)[0]
                orc_text = self.lineEdit_2.text()
                # orc_text = QtCore.QTextCodec.canEncode(orc_text)
                if orc_text == '' or orc_text is None:
                    return
                voc_wt = self.pascal_voc.writer()
                voc_wt.filename.text = bs_idx
                voc_wt.editor.text = self.editor
                textbox = voc_wt.add_object('text')
                textbox.set_textbox(orc_text)
                voc_wt.save(os.path.join(self.anno_save_dir, bs_idx + '.xml'))
            except:
                pass

    def read_text_anno(self):
        try:
            bs_idx = os.path.split(self.image_list[self.img_idx])[-1]
            bs_idx = os.path.splitext(bs_idx)[0]
            xml_path = os.path.join(self.anno_save_dir, bs_idx + '.xml')
            voc_rd = self.pascal_voc.reader(xml_path)
            for txt in voc_rd.get_items('textbox'):
                itxt = dict(txt.find('string').text)['string']
                self.lineEdit_2.setText(itxt)
                self.text_change_flag = False
        except:
            pass

    def read_editor(self):
        try:
            bs_idx = os.path.split(self.image_list[self.img_idx])[-1]
            bs_idx = os.path.splitext(bs_idx)[0]
            xml_path = os.path.join(self.anno_save_dir, bs_idx + '.xml')
            voc_rd = self.pascal_voc.reader(xml_path)
            return voc_rd.editor.text
        except:
            return ''

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        self.save_anno()
        self.text_change_flag = False

    @pyqtSlot()
    def on_lineEdit_2_returnPressed(self):
        self.save_anno()
        self.lineEdit_2.clear()
        self.on_actionNext_triggered()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.lineEdit_2.clear()
        self.next_index()
        self.read_text_anno()
        return 0

    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        self.lineEdit_2.clear()
        self.prev_index()
        self.read_text_anno()
        return 0

    def on_checkBox_resize_toggled(self, stat):
        if stat:
            self.doubleSpinBox_rw.setEnabled(True)
            self.doubleSpinBox_rh.setEnabled(True)
            self.radioButton_refixed.setEnabled(True)
            self.radioButton_rescale.setEnabled(True)
        else:
            self.doubleSpinBox_rw.setDisabled(True)
            self.doubleSpinBox_rh.setDisabled(True)
            self.radioButton_refixed.setDisabled(True)
            self.radioButton_rescale.setDisabled(True)
        self.resize_flag = stat

    def ocr_detect(self):
        try:
            if self.has_tesseract:
                text = pytesseract.image_to_string(self.bak_image, lang='eng')
                if self.radioButton_det.isChecked():
                    self.textEdit.setText(text)
                self.lineEdit_2.setText(text)
                return text
            else:
                pass
        except:
            pass

    def load_label_word(self):
        try:
            words_file = self.get_config('words', 'path')
            self.words_map = {}
            with open(words_file, 'r', encoding='UTF-8') as wf:
                for _line in wf.readlines():
                    line = _line.strip().split('|')
                    key = line[1]
                    value = line[2:]
                    self.words_map[key] = value
        except:
            pass

    @pyqtSlot()
    def on_pushButton_detect_clicked(self):
        if hasattr(self, 'bak_image'):
            self.ocr_detect()

    def on_lineEdit_2_textChanged(self, qstr):
        self.text_change_flag = True
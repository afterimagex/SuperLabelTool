# encoding: utf-8
from enum import Enum
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QRectF, QSizeF, QLineF, QPointF, qrand, QMimeData
from PyQt5.QtGui import QPen, QPolygonF, QBrush, QColor, QDrag
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsEllipseItem, QTreeWidget


from PyQt5.QtCore import (qAbs, QLineF, QPointF, qrand, QRectF, QSizeF, qsrand,
        Qt, QTime)
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter,
        QPainterPath, QPen, QPolygonF, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene,
        QGraphicsView, QStyle)

class myItemType(Enum):
    NONE = 0
    LINE = 1
    CIRCLE = 2
    POINT = 3
    RECT = 4
    POLYGON = 5



class myRectItem(QGraphicsRectItem):
    def __init__(self, rect, scene):
        super(myRectItem, self).__init__(rect)

        color = QColor(qrand() % 256, qrand() % 256, qrand() % 256)

        self.setToolTip(
            "QColor(%d, %d, %d)\nClick and drag this color onto the robot!" %
            (color.red(), color.green(), color.blue())
        )

        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        # self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        # self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        # self.setZValue(0)
        self.setAcceptDrops(True)
        self.setSelected(True)
        scene.addItem(self)
        self.setPen(QPen(color, 2))
        # self.setBrush(QBrush(Qt.DiagCrossPattern))

    def mouseMoveEvent(self, event):
        pass


    def hoverEnterEvent(self, *args, **kwargs):
        self.setCursor(Qt.ClosedHandCursor)

    # def acceptHoverEvents(self):
    #     print(123123)

    def mousePressEvent(self, event):
        # self.setCursor(Qt.ClosedHandCursor)
        # self.focusItem()
        print(1)

    def dragMoveEvent(self, *args, **kwargs):
        pass

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print(e.mimeData().text())

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        print(1)


class myLineItem(QGraphicsLineItem):
    def __init__(self, line, parent=None):
        super(myLineItem, self).__init__(line, parent)
        self.setPen(QPen(Qt.black, 2))


class myCircleItem(QGraphicsEllipseItem):
    def __init__(self, circle, parent=None):
        super(myCircleItem, self).__init__(circle, parent)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                      QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setPen(QPen(Qt.red, 2))
        self.setBrush(QBrush(Qt.Dense7Pattern))


class myImageScene(QGraphicsScene):
    wheel_scroll = pyqtSignal(int)
    mouse_position = pyqtSignal(int, int)
    rectInserted = pyqtSignal(myRectItem)
    def __init__(self, parent=None):
        super(myImageScene, self).__init__(parent)
        self.line = None
        self.rect = None
        self.circle = None
        self.point = None
        self.item_type = myItemType.NONE


    def setInsertType(self, itype):
        self.item_type = itype

    def myRectF(self, pt1, pt2):
        x = pt1.x()
        y = pt1.y()
        w = pt2.x() - pt1.x()
        h = pt2.y() - pt1.y()
        return QRectF(x, y, w, h)

    def mouseMoveEvent(self, mouseEvent):
        pt = mouseEvent.scenePos()
        self.mouse_position.emit(pt.x(), pt.y())
        if self.item_type != myItemType.LINE and self.line:
            p1 = self.line.line().p1()
            p2 = mouseEvent.scenePos()
            if self.item_type == myItemType.RECT and self.rect:
                newRect = self.myRectF(p1, p2)
                self.rect.setRect(newRect)
                newLine = QLineF(p1, p2)
                self.line.setLine(newLine)
                self.update()
            elif self.item_type == myItemType.CIRCLE and self.circle:
                newRect = self.myRectF(p1, p2)
                self.circle.setRect(newRect)



    def mousePressEvent(self, MouseEvent):
        if MouseEvent.button() == Qt.LeftButton and self.item_type != myItemType.NONE:
            pt = MouseEvent.scenePos()
            self.line = myLineItem(QLineF(pt, pt))
            if self.item_type == myItemType.RECT:
                self.rect = myRectItem(self.myRectF(pt, pt), self)
                self.addItem(self.line)
            elif self.item_type == myItemType.CIRCLE:
                self.circle = myCircleItem(self.myRectF(pt, pt))
            elif self.item_type == myItemType.POINT:
                self.point = myCircleItem(QRectF(pt.x(), pt.y(), 4, 4))
                self.point.setPen(QPen(Qt.cyan, 4))
                self.addItem(self.point)
        elif MouseEvent.button() == Qt.LeftButton and self.item_type == myItemType.NONE:
            try:
                currect_item = self.selectedItems()[0]
                # currect_item.setPen(QPen((255, 255, 0), 2))
                print(currect_item)
            except:
                pass



    def mouseReleaseEvent(self, MouseEvent):
        if self.item_type != myItemType.LINE and self.line:
            if self.item_type == myItemType.RECT and self.rect:
                self.rectInserted.emit(self.rect)
                self.rect = None
            elif self.item_type == myItemType.CIRCLE and self.circle:
                self.circle = None
            self.removeItem(self.line)
            self.line = None
            self.item_type = myItemType.NONE
        self.update()


    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.text() == 'r':
            self.item_type = myItemType.RECT
        if QKeyEvent.text() == 'p':
            self.item_type = myItemType.POINT
        if QKeyEvent.text() == 'c':
            self.item_type = myItemType.CIRCLE
        if QKeyEvent.text() == 'q':
            try:
                self.removeItem(self.selectedItems()[-1])
                self.update()
            except:
                pass


    def keyReleaseEvent(self, QKeyEvent):
        pass

    def wheelEvent(self, event):
        scroll = event.delta()
        self.wheel_scroll.emit(scroll)



class myQTreeWidget(QTreeWidget):
    # item_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super(myQTreeWidget, self).__init__(parent)

    # def itemClicked(self, QTreeWidgetItem, p_int):
    #     self.item_clicked.emit(p_int)

'''
============================================================
                       .::::.  
                     .::::::::.  
                    :::::::::::  
                 ..:::::::::::'  
              '::::::::::::'  
                .::::::::::  
           '::::::::::::::..  
                ..::::::::::::.  
              ``::::::::::::::::  
               ::::``:::::::::'        .:::.  
              ::::'   ':::::'       .::::::::.  
            .::::'      ::::     .:::::::'::::.  
           .:::'       :::::  .:::::::::' ':::::.  
          .::'        :::::.:::::::::'      ':::::.  
         .::'         ::::::::::::::'         ``::::.  
     ...:::           ::::::::::::'              ``::.  
    ```` ':.          ':::::::::'                  ::::..  
                       '.:::::'                    ':'````..  
=============================================================
'''

'''
//                      d*##$.
// zP"""""$e.           $"    $o
//4$       '$          $"      $
//'$        '$        J$       $F
// 'b        $k       $>       $
//  $k        $r     J$       d$
//  '$         $     $"       $~
//   '$        "$   '$E       $
//    $         $L   $"      $F ...
//     $.       4B   $      $$$*"""*b
//     '$        $.  $$     $$      $F
//      "$       R$  $F     $"      $
//       $k      ?$ u*     dF      .$
//       ^$.      $$"     z$      u$$$$e
//        #$b             $E.dW@e$"    ?$
//         #$           .o$$# d$$$$c    ?F
//          $      .d$$#" . zo$>   #$r .uF
//          $L .u$*"      $&$$$k   .$$d$$F
//           $$"            ""^"$$$P"$P9$
//          JP              .o$$$$u:$P $$
//          $          ..ue$"      ""  $"
//         d$          $F              $
//         $$     ....udE             4B
//          #$    """"` $r            @$
//           ^$L        '$            $F
//             RN        4N           $
//              *$b                  d$
//               $$k                 $F
//               $$b                $F
//                 $""               $F
//                 '$                $
//                  $L               $
//                  '$               $
//                   $               $
'''
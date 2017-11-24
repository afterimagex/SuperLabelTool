# encoding: utf-8
from enum import Enum
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QRectF, QSizeF, QLineF, QPointF
from PyQt5.QtGui import QPen, QPolygonF, QBrush
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsEllipseItem


class myItemType(Enum):
    NONE = 0
    LINE = 1
    CIRCLE = 2
    POINT = 3
    RECT = 4
    POLYGON = 5


class myRectItem(QGraphicsRectItem):
    def __init__(self, rect, parent=None):
        super(myRectItem, self).__init__(rect, parent)
        self.setPen(QPen(Qt.green, 2))
        self.setBrush(QBrush(Qt.DiagCrossPattern))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)


class myLineItem(QGraphicsLineItem):
    def __init__(self, line, parent=None):
        super(myLineItem, self).__init__(line, parent)
        self.setPen(QPen(Qt.black, 2))

class myCircleItem(QGraphicsEllipseItem):
    def __init__(self, circle, parent=None):
        super(myCircleItem, self).__init__(circle, parent)
        self.setPen(QPen(Qt.red, 2))
        self.setBrush(QBrush(Qt.Dense7Pattern))

class myImageScene(QGraphicsScene):
    def __init__(self, statusBar, parent=None):
        super(myImageScene, self).__init__(parent)
        self.line = None
        self.rect = None
        self.circle = None
        self.point = None
        self.item_type = myItemType.NONE
        self.statusBar =statusBar

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
        self.statusBar.showMessage('X:{} Y:{}'.format(pt.x(), pt.y()))
        if self.item_type != myItemType.LINE and self.line:
            p1 = self.line.line().p1()
            p2 = mouseEvent.scenePos()
            if self.item_type == myItemType.RECT and self.rect:
                newRect = self.myRectF(p1, p2)
                self.rect.setRect(newRect)
                newLine = QLineF(p1, p2)
                self.line.setLine(newLine)
            elif self.item_type == myItemType.CIRCLE and self.circle:
                newRect = self.myRectF(p1, p2)
                self.circle.setRect(newRect)

    def mousePressEvent(self, MouseEvent):
        if MouseEvent.button() == Qt.LeftButton and self.item_type != myItemType.NONE:
            pt = MouseEvent.scenePos()
            self.line = myLineItem(QLineF(pt, pt))
            if self.item_type == myItemType.RECT:
                self.rect = myRectItem(self.myRectF(pt, pt))
                self.addItem(self.rect)
                self.addItem(self.line)
            elif self.item_type == myItemType.CIRCLE:
                self.circle = myCircleItem(self.myRectF(pt, pt))
                self.addItem(self.circle)
            elif self.item_type == myItemType.POINT:
                self.point = myCircleItem(QRectF(pt.x(), pt.y(), 4, 4))
                self.point.setPen(QPen(Qt.cyan, 4))
                self.addItem(self.point)

    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        if self.item_type != myItemType.LINE and self.line:
            if self.item_type == myItemType.RECT and self.rect:
                self.rect = None
            elif self.item_type == myItemType.CIRCLE and self.circle:
                self.circle = None
            self.removeItem(self.line)
            self.line = None
            self.item_type = myItemType.NONE

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.text() == 'r':
            self.item_type = myItemType.RECT
        if QKeyEvent.text() == 'p':
            self.item_type = myItemType.POINT
        if QKeyEvent.text() == 'c':
            self.item_type = myItemType.CIRCLE
        if QKeyEvent.text() == 'q':
            self.removeItem(self.focusItem())
        # self.ctrlPressed =

    def keyReleaseEvent(self, QKeyEvent):
        pass




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
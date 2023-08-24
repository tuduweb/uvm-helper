#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
"""
ZetCode PyQt5 tutorial 
In this example, we create a simple
window in PyQt5.
author: Jan Bodnar
website: zetcode.com 
Last edited: August 2017
"""
 
import sys, math
from PyQt5.QtWidgets import QApplication, QWidget, QListView, QListWidget, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QGridLayout
from PyQt5.QtCore import QEvent



class pkt_flow(object):
    lack_sop = 0
    lack_eop = 0
    has_err = 0
    
    def __init__(self) -> None:
        print(self.lack_sop, self.lack_eop, self.has_err)
        pass

class vlan_tag(object):
    def __init__(self) -> None:
        pass

import random
class bin_eth_pkt(object):
    flow = pkt_flow()
    eth_pkt_data = []

    def __init__(self) -> None:
        for i in range(0, 10):
            self.eth_pkt_data.append(i)
            self.flow.lack_sop = 0
            self.flow.lack_eop = random.randint(0, 1)
            pass
        
        print(self.eth_pkt_data)
        pass



class EthPktItemWidget(QWidget):
    _pkt = None
    _id = 0

    def __init__(self, id, name, pkt, parent = None) -> None:
        super().__init__(parent)

        self._pkt = pkt
        self._id = id

        iconLabel = QLabel("%d" % id)
        iconLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken);
        left = QLabel(name)

        if (self._pkt is not None and isinstance(self._pkt, bin_eth_pkt)):

            if(self._pkt.flow.lack_sop == 0 and self._pkt.flow.lack_eop == 0):
                left.setText("P")
                left.setStyleSheet("QLabel{background-color:rgb(152,251,152);}")
            elif(self._pkt.flow.lack_sop == 0 and self._pkt.flow.lack_eop == 1):
                left.setText("E")
                left.setStyleSheet("QLabel{background-color:rgb(240,128,128);}")
            else:
                left.setText("H")

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(iconLabel)
        layout.addWidget(left)
        self.setLayout(layout)

class EthPktDisplayWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        items = []

        for index in range(1, 10):
            pkt = bin_eth_pkt()
            item = EthPktItemWidget(index, "item_%d" % index, pkt)
            items.append(item)
            layout.addWidget(item)

class EthPktDetailCeil(QLabel):
    _id = 0

    def __init__(self, __id, value, parent = None) -> None:
        super().__init__("h%x" % value, parent)
        self._id = __id
        self.setStyleSheet("QLabel{background-color:rgb(173,216,230);}")

    def enterEvent(self, event):
        self.setStyleSheet("QLabel{background-color:rgb(244,164,96);}")

    def leaveEvent(self, event):
        self.setStyleSheet("QLabel{background-color:rgb(173,216,230);}")

class EthPktDetailWidget(QWidget):
    pkt = None
    groupSplitValues = [4, 10, 20]

    martixLayout = None

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        text = QLabel("display")
        layout.addWidget(text)

        martixFrame = QFrame()
        self.martixLayout = QGridLayout()
        martixFrame.setLayout(self.martixLayout)

        layout.addWidget(martixFrame)

        pkt = bin_eth_pkt()

        for index in range(0, len(pkt.eth_pkt_data)):
            tmpLabel = EthPktDetailCeil(index, index + 2)
            self.martixLayout.addWidget(tmpLabel, math.floor(index / 8), index % 8)


        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        # print(obj, event.type())
        if event.type() == QEvent.MouseButtonPress:  # Catch the TouchBegin event.
            print('We have a MouseButtonPress', obj)

            if (isinstance(obj, EthPktDetailWidget)):
                # obj.setStyleSheet("QLabel{background-color:rgb(244,164,96);}")

                print("martix count %d" % self.martixLayout.count())
                for itemIndex in range(0, self.martixLayout.count()):
                    item = self.martixLayout.itemAt(itemIndex)
                    
                    if (item and item.widget()):
                        print("%d/%d _id=%d" % (itemIndex, self.martixLayout.count(), item.widget()._id), item)
                        print(item.widget()._id)
                        if (item.widget()._id < 10):
                            item.widget().setStyleSheet("QLabel{background-color:rgb(244,164,96);}")

            return True
        elif event.type() == QEvent.HoverLeave:  # Catch the TouchEnd event.
            print('We have a HoverLeave')
            return True

        return super(EthPktDetailWidget, self).eventFilter(obj, event)



if __name__ == '__main__':
    
    onePkt = bin_eth_pkt()
    app = QApplication(sys.argv)
    w = QWidget()

    layout = QHBoxLayout()
    w.setLayout(layout)


    mainWidget = EthPktDisplayWidget(w)
    detailWidget = EthPktDetailWidget(w)


    layout.addWidget(mainWidget)
    layout.addWidget(detailWidget)

    #listWidget = QListWidget(w)
    #w.layout().addWidget(mainWidget)
    #listWidget.addItem("123")

    w.resize(640, 480)
    # w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    sys.exit(app.exec_()) 
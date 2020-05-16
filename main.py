from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QLineEdit,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
import sys
import textwrap
from bs4 import BeautifulSoup as bs
import requests
import time
from urllib.request import Request, urlopen
import ctypes
import functools
from PyQt5.QtCore import pyqtSlot

start = time.time()



           
class Window(QMainWindow):

    def slut_start(self):
      self.user = ctypes.windll.user32

      self.title = []
      self.site = []
      self.img = []
      self.chaps = []
      url = "https://m.mangairo.com/manga-list/type-latest/ctg-all/state-all/page-1"
      content = requests.get(url)
      soup = bs(content.content,'html.parser')

      for cnt in soup.find_all("a",{"class": "tooltip"}):
        if cnt.img != None:
            self.img.append(cnt.img["src"])
            if len(cnt.img["alt"]) < 18:
                self.title.append(cnt.img["alt"])
                continue
            elif " " in cnt.img["alt"][17:len(cnt.img["alt"])]:
                index = cnt.img["alt"][17:len(cnt.img["alt"])].index(" ")
                #print("index {} on {}".format(index,cnt.img["alt"][17:len(cnt.img["alt"])]))
            newTitle = cnt.img["alt"][0:17+index] + "\n" + cnt.img["alt"][17+index:len(cnt.img["alt"])]
            self.title.append(newTitle)


    def __init__(self):
        super().__init__()
        self.slut_start()
        self.user = ctypes.windll.user32
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Manga Reader")
        self.setStyleSheet("background-color: grey;")
        
        self.resize(self.user.GetSystemMetrics(0), self.user.GetSystemMetrics(1))
        self.main_label1 = QtWidgets.QLabel(self.centralwidget)
        self.main_label2 = QtWidgets.QLabel(self.centralwidget)
        self.summary_button = QtWidgets.QLabel(self.centralwidget)
        self.chapList_button = QtWidgets.QLabel(self.centralwidget)

        
        layout = QtWidgets.QHBoxLayout(self)
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(scrollAreaWidgetContents)
        
        scrollArea.setWidget(scrollAreaWidgetContents)
        layout.addWidget(scrollArea)
        layout.setGeometry(QtCore.QRect(0,0,int(self.frameGeometry().width()),self.frameGeometry().height()))
        imgList, titleList = [], []
        photo_hCounter, title_hCounter = 0,0,
        title_vCounter = 2
        photo_vCounter = 3
        
        gridLayout.setHorizontalSpacing(20)
        
        searchBox = QLineEdit(self)
        searchBox.resize(280,40)
        searchBox.setStyleSheet("background-color: white;")
        gridLayout.addWidget(searchBox,0,0)
        for i in  range(20):
            F = QtWidgets.QLabel(self.centralwidget)
            img = self.loadImage(self.img[i])
            F.setPixmap(QPixmap(img))

            label_title = QPushButton(self)
            label_title.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0); color : white; }");
            label_title.setFixedSize(100,50)
            titleList.append(label_title)
            imgList.append(F)

            gridLayout.setRowStretch(i,100)
            gridLayout.setColumnStretch(i,100)

            if title_hCounter >= 10:
                title_vCounter += 2
                photo_vCounter += 2
                title_hCounter , photo_hCounter = 0,0

            gridLayout.addWidget(titleList[i],title_vCounter,title_hCounter)

            gridLayout.addWidget(imgList[i], photo_vCounter, photo_hCounter)

            title_hCounter += 1
            photo_hCounter += 1

            titleList[i].setText(self.title[i])
            #titleList[i].mousePressEvent = functools.partial(self.label_event2, F=imgList[i])

        self.setCentralWidget(self.centralwidget)
        self.showMaximized()
        self.show()
        
    def loadImage(self,image_url):
            img = QImage()
            req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            img.loadFromData(data)  
            img = img.scaled(100,150)
            return img
    def localImage(self,source,label,scaleW,scaleH):
        pixmap = QPixmap(source)
        label.setFixedSize(scaleW,scaleH)
        label.setPixmap(pixmap)
        return label
        
    def popup_message(self,event,message):
        msg = QMessageBox()
        msg.setWindowTitle("Manga Summary")

        msg.setText(' '.join(message.split()))
        x = msg.exec_()  # this will show our messagebox




App = QApplication(sys.argv)
window = Window()
end = time.time()
print(end-start)
sys.exit(App.exec())

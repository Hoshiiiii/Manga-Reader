from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
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
            if len(cnt.img["alt"]) < 10:
                self.title.append(cnt.img["alt"])
                continue
            #newTitle = cnt.img["alt"][0:10] + "\n" + cnt.img["alt"][10:len(cnt.img["alt"])]
            newTitle = cnt.img["alt"][0:10]
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
        imgList = []
        titleList = []
        title_vCounter = 0
        title_hCounter = 0
        photo_vCounter = 1
        photo_hCounter = 0
        gridLayout.adjustSize()
        for i in  range(10):
            F = QtWidgets.QLabel(self.centralwidget)
            img = QImage()
            req = Request(self.img[i], headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            img.loadFromData(data)
            img = img.scaled(100,150)
            F.setPixmap(QPixmap(img))

            label_title = QPushButton(self)
            label_title.setStyleSheet("QLabel { color : white; }");
            label_title.adjustSize()
            titleList.append(label_title)
            imgList.append(F)

            gridLayout.setRowStretch(i,200)
            
            if title_hCounter >= 8:
                title_vCounter += 2
                photo_vCounter += 2
                title_hCounter , photo_hCounter = 0,0

            gridLayout.addWidget(titleList[i],title_vCounter,title_hCounter)

            gridLayout.addWidget(imgList[i], photo_vCounter, photo_hCounter)

            title_hCounter +=1
            photo_hCounter += 1

            titleList[i].setText(self.title[i])
            titleList[i].mousePressEvent = functools.partial(self.label_event2, F=imgList[i])

        self.setCentralWidget(self.centralwidget)
        self.showMaximized()
        self.show()
    def label_event2(self, event, F=None):
        F.setPixmap(QPixmap(""))

    def label_events(self, event, site=None):
        url = site
        content = requests.get(url)
        soup = bs(content.content,'html.parser')
        title = soup.find("meta",  property="og:title")
        desc = soup.find("meta",  property="og:description")
        image = soup.find("img",{"class":"rounded"})

        '''
        img = QImage()
        data = urlopen(image["src"]).read()
        img.loadFromData(data)
        img = img.scaled(600,400)
        self.main_label2.setPixmap(QPixmap(img))
        self.main_label2.setGeometry(QtCore.QRect(int(self.width()/4),0,600,400))
        '''
        pixmap = QPixmap('sum.png')
        self.summary_button.setPixmap(pixmap)
        self.summary_button.setGeometry(QtCore.QRect(int(self.width()/4)+10,0,pixmap.height(),pixmap.width()+10))
        self.summary_button.mousePressEvent = functools.partial(self.popup_message, message=desc["content"])

        self.buttonMaker(pixmap,self.chapList)
    def buttonMaker(self,image_name,button_name,):
        pixmap = QPixmap(image_name)
        button_name.setPixmap(pixmap)
        button_name.setGeometry(QtCore.QRect(int(self.width()/4),400,pixmap.width(),pixmap.height()))
        #button_name.mousePressEvent = functools.partial(self.popup_message, message=desc["content"])


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

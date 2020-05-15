from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QMessageBox
import sys
import textwrap
from bs4 import BeautifulSoup as bs
import requests
import time
from urllib.request import urlopen
import ctypes
import functools

start = time.time()

class Window(QMainWindow):

    def slut_start(self):
      self.user = ctypes.windll.user32
      self.url = "https://mangadex.org/updates"
      self.content = requests.get(self.url)
      self.soup = bs(self.content.content,'html.parser')
      self.title = []
      self.site = []
      self.img = []
      self.chaps = []
      soupConc = ["a",{"class":"manga_title text-truncate"},'img',]
      for cnt in self.soup.find_all(soupConc):
          if cnt.has_attr('class') and "text-truncate" in cnt['class']:
              if len(cnt['class']) > 1 and cnt['class'][0] == 'manga_title':
                  self.site.append("https://mangadex.org" + cnt["href"])
                  '''if len(cnt["title"]) > 20:
                      cnt["title"] = cnt["title"][0:20] + "\n" + cnt["title"][21:len(cnt["title"])]
                      print(cnt["title"])
                      continue'''
                  self.title.append(cnt["title"] + "\n")
          elif cnt.has_attr('alt') and cnt["src"][:13] == "/images/manga":
              self.img.append("https://mangadex.org" + cnt["src"])





    def __init__(self):
        super().__init__()
        self.slut_start()

        self.user = ctypes.windll.user32
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Manga Reader")
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
        self.gridLayout2 = QtWidgets.QGridLayout(scrollAreaWidgetContents)
        layout.addWidget(scrollArea)
        layout.setGeometry(QtCore.QRect(0,0,int(self.frameGeometry().width()),self.frameGeometry().height()))
        imgList = []
        titleList = []
        title_vCounter = 0
        title_hCounter = 0
        photo_vCounter = 1
        photo_hCounter = 0
        for i in  range(20):
            F = QtWidgets.QLabel(self.centralwidget)

            img = QImage()
            data = urlopen(self.img[i]).read()
            img.loadFromData(data)
            img = img.scaled(100,150)
            F.setPixmap(QPixmap(img))

            titleList.append(QLabel(self.title[i]))
            imgList.append(F)

            if title_hCounter >= 4:
                title_vCounter += 2
                photo_vCounter += 2
                title_hCounter , photo_hCounter = 0,0
                
            gridLayout.addWidget(titleList[i],title_vCounter,title_hCounter)

            gridLayout.addWidget(F, photo_vCounter, photo_hCounter)

            title_hCounter +=1
            photo_hCounter += 1

            #titleList[i].mousePressEvent = functools.partial(self.label_events, site=self.site[i])

        self.setCentralWidget(self.centralwidget)
        self.showMaximized()
        self.show()
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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout
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
      self.main_label1 = QLabel()
      self.main_label2 = QLabel()
      soupConc = ["a",{"class":"manga_title text-truncate"},'img',]
      for cnt in self.soup.find_all(soupConc):
          if cnt.has_attr('class') and "text-truncate" in cnt['class']:
              if len(cnt['class']) > 1 and cnt['class'][0] == 'manga_title':
                  self.title.append(cnt["title"] + "\n")
                  self.site.append("https://mangadex.org" + cnt["href"])
              else:
                  self.chaps.append(cnt.text)
          elif cnt.has_attr('alt') and cnt["src"][:13] == "/images/manga":  
              self.img.append("https://mangadex.org" + cnt["src"])
      

      for x in range(len(self.title)):
          self.title[x]+= self.chaps[x]


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

        layout = QtWidgets.QHBoxLayout(self)
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(scrollAreaWidgetContents)
        scrollArea.setWidget(scrollAreaWidgetContents)
        layout.addWidget(scrollArea)
        layout.setGeometry(QtCore.QRect(0,0,int(self.frameGeometry().width() /4),self.frameGeometry().height()))
        
        x_pos = 0
        y_pos = 0
        imgList = []
        titleList = []

        for i in  range(len(self.img)):
            F = QtWidgets.QLabel(self.centralwidget)

            img = QImage()
            data = urlopen(self.img[i]).read()
            img.loadFromData(data)
            img = img.scaled(100,150)
            F.setPixmap(QPixmap(img))
        
            titleList.append(QLabel(self.title[i]))
            imgList.append(F)
            gridLayout.addWidget(titleList[i], i, 1)
            gridLayout.addWidget(F, i, 0)
            titleList[i].mousePressEvent = functools.partial(self.print_some, site=self.site[i])

        self.setCentralWidget(self.centralwidget)
        self.showMaximized()
        self.show()
    def print_some(self, event, site=None):
        url = site
        content = requests.get(url)
        soup = bs(content.content,'html.parser')
        title = soup.find("meta",  property="og:title")
        desc = soup.find("meta",  property="og:description")
        image = soup.find("img",{"class":"rounded"})

        self.main_label2.setGeometry(QtCore.QRect(int(self.frameGeometry().width() /4),0,600,400))
        img = QImage()
        data = urlopen(image["src"]).read()
        img.loadFromData(data)
        self.main_label2.setPixmap(QPixmap(img))

        
        self.main_label1.setText(textwrap.fill(desc["content"], 100))
        self.main_label1.setGeometry(QtCore.QRect(int(self.frameGeometry().width() /4),100,300,200))

App = QApplication(sys.argv)
window = Window()
end = time.time()
print(end-start)
sys.exit(App.exec())

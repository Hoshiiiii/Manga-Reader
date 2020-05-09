from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
import sys

from bs4 import BeautifulSoup as bs
import requests
import time
from urllib.request import urlopen
import ctypes

start = time.time()

class Window(QWidget):

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

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Manga Reader")
        self.resize(self.user.GetSystemMetrics(0), self.user.GetSystemMetrics(1))
        #self.setStyleSheet("background-image: url(sample.jpg)")


        x_pos = 0
        y_pos = 0
        imgList = []
        titleList = []
        formLayout =QFormLayout()
        groupBox = QGroupBox("")
        F = QtWidgets.QLabel(self.centralwidget)

        for i in  range(len(self.img)):
            F = QtWidgets.QLabel(self.centralwidget)

            img = QImage()
            data = urlopen(self.img[i]).read()
            img.loadFromData(data)
            img = img.scaled(100,150)

            F.setPixmap(QPixmap(img))

            titleList.append(QLabel(self.title[i]))
            imgList.append(F)

            formLayout.addRow(imgList[i],titleList[i])

        titleList[0].mousePressEvent = self.do_smthing
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(self.frameGeometry().height())
        scroll.setFixedWidth(self.frameGeometry().width() /4)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.showMaximized()

        self.show()
    def do_smthing(self,event):
        print("YO")
App = QApplication(sys.argv)
window = Window()
end = time.time()
print(end-start)
sys.exit(App.exec())

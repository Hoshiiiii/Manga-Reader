from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage

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


      for cnt in self.soup.find_all("a",attrs={"class":"manga_title text-truncate"}):
          self.title.append(cnt["title"])
          self.site.append("https://mangadex.org" + cnt["href"])

      for cnt in self.soup.find_all("img"):
          if cnt["src"][:13] == "/images/manga":
              self.img.append("https://mangadex.org" + cnt["src"])

              
    def __init__(self):
        super().__init__()
        self.slut_start()
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Manga Reader")
        self.resize(self.user.GetSystemMetrics(0), self.user.GetSystemMetrics(1))
        self.setStyleSheet("background-color: rgb(255, 255, 255)\n")
        
        formLayout =QFormLayout()
        groupBox = QGroupBox("")
        
        self.imageDict = {}
        self.titleDict = {}

        x_pos = 0
        y_pos = 0
        imgList = []
        titleList = []
        F = QtWidgets.QLabel(self.centralwidget)

        for i in  range(len(self.img)):
            F = QtWidgets.QLabel(self.centralwidget)
                
            F.setGeometry(QtCore.QRect(x_pos,y_pos , 100, 150))
            img = QImage()
            data = urlopen(self.img[i]).read()
            img.loadFromData(data)
            img = img.scaled(100,150)
            
            F.setPixmap(QPixmap(img))
                
            titleList.append(QLabel(self.title[i]))
            imgList.append(F)
            formLayout.addRow(imgList[i],titleList[i])
            y_pos+=100
        

            
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(self.frameGeometry().height())
        scroll.setFixedWidth(self.frameGeometry().width() - 20)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        self.show()
        
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
end = time.time()
print(end-start)


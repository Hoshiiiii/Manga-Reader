from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage


from bs4 import BeautifulSoup as bs
import requests
import time
from urllib.request import urlopen
import sys



class Ui_MainWindow(object):
   def __init__(self):
      self.start = time.time()


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




   def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 860)
        MainWindow.setStyleSheet("background-color: rgb(66, 70, 88)\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.imageDict = {}
        self.titleDict = {}

        x_pos = 0
        y_pos = 0
        x_pos2 = 400
        y_pos2 = 0
        for x in range(8):
            if x >= 4:
                self.imageDict["self_label" + str(x)] = QtWidgets.QLabel(self.centralwidget)

                self.imageDict["self_label" + str(x)].setGeometry(QtCore.QRect(x_pos2,y_pos2 , 100, 150))
                self.imageDict["self_label" + str(x)].setText("")
                img = QImage()
                data = urlopen(self.img[x]).read()
                img.loadFromData(data)
                img = img.scaled(100,150)
                self.imageDict["self_label" + str(x)].setPixmap(QPixmap(img))

                #Title Dictionary
                self.titleDict["self_label" + str(x)] = QtWidgets.QLabel(self.centralwidget)
                self.titleDict["self_label" + str(x)].setGeometry(QtCore.QRect(x_pos2+100, y_pos2, 101, 31))
                font = QtGui.QFont()
                font.setFamily("Miriam Fixed")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.titleDict["self_label" + str(x)].setFont(font)
                self.titleDict["self_label" + str(x)].setObjectName("label_2")
                y_pos2 += 150
            else:
                #Image Dictionary
                self.imageDict["self_label" + str(x)] = QtWidgets.QLabel(self.centralwidget)

                self.imageDict["self_label" + str(x)].setGeometry(QtCore.QRect(x_pos,y_pos , 100, 150))
                self.imageDict["self_label" + str(x)].setText("")
                img = QImage()
                data = urlopen(self.img[x]).read()
                img.loadFromData(data)
                img = img.scaled(100,150)
                self.imageDict["self_label" + str(x)].setPixmap(QPixmap(img))

                #Title Dictionary
                self.titleDict["self_label" + str(x)] = QtWidgets.QLabel(self.centralwidget)
                self.titleDict["self_label" + str(x)].setGeometry(QtCore.QRect(x_pos+100, y_pos, 101, 31))
                font = QtGui.QFont()
                font.setFamily("Miriam Fixed")
                font.setPointSize(16)
                font.setBold(False)
                font.setWeight(50)
                self.titleDict["self_label" + str(x)].setFont(font)
                self.titleDict["self_label" + str(x)].setObjectName("label_2")

                y_pos += 150



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 748, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.end = time.time()
        print(self.end-self.start)

   def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        for x in range(8):
            self.titleDict["self_label" + str(x)].setText(_translate("MainWindow", self.title[x]))

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

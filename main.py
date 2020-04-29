from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage


from bs4 import BeautifulSoup as bs
import requests
import time
from urllib.request import urlopen



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
          self.title.append("https://mangadex.org" + cnt["title"])
          self.site.append("https://mangadex.org" + cnt["href"])

      for cnt in self.soup.find_all("img"):
          if cnt["src"][:13] == "/images/manga":
              self.img.append("https://mangadex.org" + cnt["src"])




   def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(748, 510)
        MainWindow.setStyleSheet("background-color: rgb(66, 70, 88)\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.variable_maker = {}
        x_pos = -50

        for x in range(6):
            x_pos += 110
            self.variable_maker["self_label" + str(x)] = QtWidgets.QLabel(self.centralwidget)

            self.variable_maker["self_label" + str(x)].setGeometry(QtCore.QRect(x_pos,MainWindow.frameGeometry().height() - 200 , 100, 150))
            self.variable_maker["self_label" + str(x)].setText("")
            img = QImage()
            data = urlopen(self.img[x]).read()
            img.loadFromData(data)
            img = img.scaled(100,150)
            self.variable_maker["self_label" + str(x)].setPixmap(QPixmap(img))


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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


'''
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 310, 100, 150))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 310, 100, 150))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(350, 310, 100, 150))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(240, 310, 100, 150))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(460, 310, 100, 150))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(570, 310, 100, 150))
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(140, 80, 100, 150))
        self.label_4.setText("")
        '''

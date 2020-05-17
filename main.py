from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QLineEdit,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from get_mangainfo import get_latest,get_popular
import ctypes, functools,requests, time,sys
start = time.time()



           
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        latest_images, latest_titles = get_latest()
        popular_images, popular_titles = get_popular()

        self.user = ctypes.windll.user32
        

        #Setting up Main Window Properties
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Manga Reader")
        self.setStyleSheet("background-color: grey;")
        self.resize(self.user.GetSystemMetrics(0), self.user.GetSystemMetrics(1))
        
        #Setting up Layout and Scroll area properties
        layout = QtWidgets.QHBoxLayout(self)
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(scrollAreaWidgetContents)
        scrollArea.setWidget(scrollAreaWidgetContents)

        layout.addWidget(scrollArea)
        layout.setGeometry(QtCore.QRect(0,0,int(self.frameGeometry().width()),self.frameGeometry().height()))
        
        #Variable declartion for properties
        horizontal_space = 100
        searchbox_size = [100,20]
        gridLayout.setHorizontalSpacing(horizontal_space)
        #Main Widgets
        searchBox = QLineEdit(self)
        searchBox.setStyleSheet("background-color: white;")
        searchBox.setGeometry(self.user.GetSystemMetrics(0) - 200,10,searchbox_size[0],searchbox_size[1])

        search_button = QPushButton(self)
        search_button.setStyleSheet("background-color:white;");
        search_button.setFixedSize(50,20)
        search_button.setGeometry(self.user.GetSystemMetrics(0) - 80,10,0,0)

        popular,latest = self.buttons_init()
        #Main
        latest_titleList, latest_imageList = self.load_resources(20,latest_images,latest_titles)
        popular_titleList, popular_imageList = self.load_resources(20,popular_images,popular_titles)

        #self.apply_resources(20,latest_titleList,latest_imageList,gridLayout)
        popular.clicked.connect(functools.partial(self.apply_resources,20,popular_titleList,popular_imageList,gridLayout))
        latest.clicked.connect(functools.partial(self.apply_resources,20,latest_titleList,latest_imageList,gridLayout))

        self.setCentralWidget(self.centralwidget)
        self.showMaximized()
        self.show()
    def buttons_init(self):
        popular = QPushButton(self)
        popular.setStyleSheet("background-color:white;");
        popular.setFixedSize(50,20)
        popular.setGeometry(0,10,0,0)
        popular.setText("Popular Button")        

        latest = QPushButton(self)
        latest.setStyleSheet("background-color:white;");
        latest.setFixedSize(50,20)
        latest.setGeometry(100,10,0,0)
        latest.setText("Latest Button")

        return popular,latest
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

    def on_click(self,num_loops,images,imgList):
        for x in range(num_loops):
            imgList[x].setPixmap(QPixmap(self.loadImage(images[x])))
            
        
    def load_resources(self,num_loops,images,titles):
        titleList,imgList = [],[]
        title_size = [100,50]

        for i in  range(num_loops):
            #Loading image
            image_label = QtWidgets.QLabel(self.centralwidget)
            img = self.loadImage(images[i])
            img = img.scaled(100,150)
            #Setting button properties
            label_title = QPushButton()
            label_title.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0); color : white; }");
            label_title.setFixedSize(title_size[0],title_size[1])
            #Adding widgets to a list
            titleList.append(label_title)
            imgList.append(image_label)
            #Applying image and text
            titleList[i].setText(titles[i])
            image_label.setPixmap(QPixmap(img))
        return titleList, imgList

        #popular.clicked.connect(functools.partial(self.on_click,20,popular_images,imgList))
    def apply_resources(self,num_loops,titleList,imgList,gridLayout):
        #Declaring variables for layout properties
        photo_horizontal, title_horizontal = 0,0,
        title_vertical = 10
        photo_vertical = 11
        rowcol_stretch = 100

        for i in  range(num_loops):

            gridLayout.setRowStretch(i,150)
            gridLayout.setColumnStretch(i,100)
            if title_horizontal >= 5:
                title_vertical += 2
                photo_vertical += 2
                title_horizontal , photo_horizontal = 0,0

            gridLayout.addWidget(titleList[i],title_vertical,title_horizontal)

            gridLayout.addWidget(imgList[i], photo_vertical, photo_horizontal)

            title_horizontal += 1
            photo_horizontal += 1


App = QApplication(sys.argv)
window = Window()
end = time.time()
print(end-start)
sys.exit(App.exec())

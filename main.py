from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QLineEdit,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from get_mangainfo import get_latest,get_popular, get_search,get_manga
import ctypes, functools,requests, time,sys
start = time.time()



           
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        latest_images, latest_titles,latest_sites = get_latest()
        popular_images, popular_titles,popular_sites = get_popular()
        self.user = ctypes.windll.user32
        self.rows,self.columns = 0,0

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
        gridLayout.setHorizontalSpacing(horizontal_space)
        self.search_titleList,self.search_imageList = [],[]
        
        #Setting the main widgets through functions
        popular,latest,search_box,search_button = self.buttons_init()
        
        #Main - Load resources
        self.latest_titleList, self.latest_imageList,latest_siteList = self.load_resources(20,latest_images,latest_titles,latest_sites,gridLayout)
        self.popular_titleList, self.popular_imageList,popular_siteList = self.load_resources(20,popular_images,popular_titles,popular_sites,gridLayout)
        
        #Setting up for button clicks
        search_button.clicked.connect(functools.partial(self.apply_searchResources,search_box,gridLayout))
        popular.clicked.connect(functools.partial(self.apply_resources,20,self.popular_titleList,self.popular_imageList,gridLayout,"popular"))
        latest.clicked.connect(functools.partial(self.apply_resources,20,self.latest_titleList,self.latest_imageList,gridLayout,"latest"))
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
            
        
    def load_resources(self,num_loops,images,titles,sites,gridLayout):
        titleList,imgList,siteList = [],[],[]
        title_size = [100,20]

        for i in  range(num_loops):
            #Appending urls
            siteList.append(sites[i])
            #Loading image
            image_label = QtWidgets.QLabel(self.centralwidget)
            img = self.loadImage(images[i])
            img = img.scaled(100,150)
            #Setting button properties
            label_title = QPushButton()
            label_title.setStyleSheet("""QPushButton {
    background-color: red;
    border-color: beige;
    font: bold 14px;
}""")
            label_title.setFixedSize(title_size[0],title_size[1])
            #Adding widgets to a list
            titleList.append(label_title)
            imgList.append(image_label)
            #Applying image and text
            titleList[i].setText(titles[i])
            image_label.setPixmap(QPixmap(img))
            titleList[i].clicked.connect(functools.partial(self.load_manga,sites[i],titles[i],gridLayout))
        return titleList, imgList,siteList
   
    def apply_resources(self,num_loops,titleList,imgList,gridLayout,condition):
        if condition == "popular":
            for x in range(len(self.latest_imageList)):
                self.latest_imageList[x].hide()
                self.latest_titleList[x].hide() 
        else:
            for x in range(len(self.latest_imageList)):
                self.popular_imageList[x].hide()
                self.popular_titleList[x].hide() 

        for x in range(len(self.search_imageList)):
         self.search_imageList[x].setParent(None)
         self.search_titleList[x].setParent(None)
        #Declaring variables for layout properties
        photo_horizontal, title_horizontal = 0,0,
        title_vertical,photo_vertical = 0,1
        rowcol_stretch = 100

        self.adjust_grid(num_loops,gridLayout,titleList,imgList,photo_horizontal,title_horizontal,title_vertical,photo_vertical,rowcol_stretch)


    def load_manga(self,site,title,gridLayout):
        #Clear widgets in the layout
        self.clear_layout()

        #Add new widgets
        chap_url,img,description = get_manga(site)
        title_label = QtWidgets.QLabel(self.centralwidget)
        title_label.setText(title)
        image_label = QtWidgets.QLabel(self.centralwidget)
        image = self.loadImage(img)
        image_label.setPixmap(QPixmap(image))

        #Adjust widgets 
        rowcol_stretch = 100
        rows,columns = 0,0

        gridLayout.setRowStretch(rows,150)
        gridLayout.setColumnStretch(columns,100)

        gridLayout.addWidget(title_label,rows,columns)
        
        gridLayout.addWidget(image_label, rows+1,columns)
        title_label.show()
        image_label.show()
    def apply_searchResources(self,search_input,gridLayout):
        for x in range(len(self.search_titleList)):
         self.search_imageList[x].setParent(None)
         self.search_titleList[x].setParent(None)
        for x in range(len(self.popular_titleList)):
            self.popular_titleList[x].hide()
            self.popular_imageList[x].hide()  
            self.latest_titleList[x].hide()
            self.latest_imageList[x].hide()   
        search_images, search_titles,search_sites,search_details = get_search(search_input.text())

        self.search_titleList, self.search_imageList,search_sites = self.load_resources(len(search_titles),search_images,search_titles,search_sites,gridLayout)
        photo_horizontal, title_horizontal = 0,0,
        title_vertical = 0
        photo_vertical = 1
        rowcol_stretch = 100

     
        self.adjust_grid(len(self.search_titleList),gridLayout,self.search_titleList,self.search_imageList,photo_horizontal,title_horizontal,title_vertical,photo_vertical,rowcol_stretch)  
    def buttons_init(self):
        searchbox_size = [100,20]

        popular = QPushButton(self)
        popular.setStyleSheet("background-color:white;");
        popular.setFixedSize(50,20)
        popular.setGeometry(self.user.GetSystemMetrics(0) - 80,50,0,0)
        popular.setText("Popular Button")        

        latest = QPushButton(self)
        latest.setStyleSheet("background-color:white;");
        latest.setFixedSize(50,20)
        latest.setGeometry(self.user.GetSystemMetrics(0) - 80,100,0,0)
        latest.setText("Latest Button")

        searchBox = QLineEdit(self)
        searchBox.setStyleSheet("background-color: green;")
        searchBox.setGeometry(self.user.GetSystemMetrics(0) - 200,10,searchbox_size[0],searchbox_size[1])

        search_button = QPushButton(self)
        search_button.setStyleSheet("background-color:white;");
        search_button.setFixedSize(50,20)
        search_button.setGeometry(self.user.GetSystemMetrics(0) - 80,10,0,0)
        return popular,latest,searchBox,search_button
    def adjust_grid(self,loops,gridLayout,titleList,imgList,photo_horizontal,title_horizontal,title_vertical,photo_vertical,rowcol_stretch):
        for i in  range(loops):
            gridLayout.setRowStretch(i,150)
            gridLayout.setColumnStretch(i,100)
            if title_horizontal >= 5:
                title_vertical += 2
                photo_vertical += 2
                title_horizontal , photo_horizontal = 0,0

            gridLayout.addWidget(titleList[i],title_vertical,title_horizontal)

            gridLayout.addWidget(imgList[i], photo_vertical, photo_horizontal)

            titleList[i].show()
            imgList[i].show()

            title_horizontal += 1
            photo_horizontal += 1  
    def clear_layout(self):
        for x in range(len(self.search_imageList)):
         self.search_imageList[x].setParent(None)
         self.search_titleList[x].setParent(None) 
        for x in range(len(self.latest_imageList)):
            self.latest_imageList[x].hide()
            self.latest_titleList[x].hide() 
        for x in range(len(self.popular_imageList)):
            self.popular_imageList[x].hide()
            self.popular_titleList[x].hide() 
App = QApplication(sys.argv)
window = Window()
end = time.time()
print(end-start)
sys.exit(App.exec())

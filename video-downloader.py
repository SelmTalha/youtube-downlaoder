#!/usr/bin/env python3 
import threading
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets , uic
from PyQt5.QtWidgets import *
from pytube import *
import sys,os,os.path,time
import urllib.request
from pathlib import Path
from threading import *


root_dir = Path("~").expanduser()

class MainApp(QMainWindow ,Thread):
    def __init__(self):
        global root_dir
        super(MainApp,self).__init__()
        uic.loadUi('main.ui',self)
        self.UiDesigner()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.name=""
        self.youtube=""
        self.location="{}/Downloads/".format(root_dir)
        self.offset=None
        self.kisayol = QShortcut(QKeySequence("ESC"), self)
        self.kisayol.activated.connect(self.anamenu)
        self.stackedWidget.setCurrentWidget(self.ana_menu)
        self.pushButton.clicked.connect(self.single_dw_page)
        self.pushButton_2.clicked.connect(self.playlist_dw_page)
        self.pushButton_10.clicked.connect(self.showMinimized)
        self.pushButton_7.clicked.connect(self.close_Application)
        self.lineEdit_2.setText("{}/Downloads".format(root_dir))


    def close_Application(self):
        choice=QMessageBox.question(self,'Output Control',"Are you sure you want to log out? \n(Ongoing downloads may be terminated !)" , QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    #############################################################################################
    # Mouse Event and Title Bar Move
    #############################################################################################

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    #############################################################################################
    # Sayfalara Yönlendirmeler
    #############################################################################################
        
    def save_file_path(self):
        fname=QFileDialog.getSaveFileName(self,'Save File',self.name,'Video Files (*.mp4 *.avi *.ts)')
        dosya_yolu=fname[0]
        a=dosya_yolu.split("/")
        a.pop()
        print(a)
        self.location="/".join(a)
        self.lineEdit_2.setText(dosya_yolu)

    def download_video(self):
        url = self.lineEdit.text()
        self.youtube=YouTube(url)
        reso=self.comboBox.currentText()
        yt = self.youtube.streams.filter(resolution=reso,progressive="True").first()
        yt.download(self.location)
        QApplication.processEvents()
        self.label_6.setText("Successfully downloaded !")

    def content_get(self):
        try:
            url = self.lineEdit.text()
            self.youtube=YouTube(url)
            content=f"""Video Title : {self.youtube.title}\nVideo Description : {self.youtube.description[:45]}...\nVideo Owner : {self.youtube.author}\nVideo Length : {self.youtube.length} second\nViews : {self.youtube.views}"""
            self.label_7.setText("Video Content")
            self.lineEdit_2.setText("{}/Downloads/{}".format(root_dir,self.youtube.title))
            self.video_content.setText(content)
            self.name=self.youtube.title
            for i in self.youtube.streams.filter(progressive="True"):
                self.comboBox.addItem(i.resolution)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(True)
            self.lineEdit.setEnabled(False)
            
            print()
                
        except Exception as ex:
            print(ex)
            self.video_content.setText("<p style='color:red'>The video is not available. Please make sure the Url/Link is correct</p>")

    def save_file_path_pwd(self):
        fname=QFileDialog.getSaveFileName(self,'Save File',self.playlist.title,'Video Files (*.mp4 *.avi *.ts)')
        self.lineEdit_4.setText(fname[0])

    def content_get_pdw(self):
        try:
            self.playlist = Playlist(self.lineEdit_3.text())
            self.label_13.setText(str(len(self.playlist.video_urls)))
            self.lineEdit_4.setText("{}/Downloads/Playlist/{}".format(root_dir,self.playlist.title))
            self.pushButton_9.setEnabled(True)
            self.pushButton_16.setEnabled(False)
                
        except Exception as ex:
            self.console.append("Error Message: {}".format(ex))
            self.console.append("<span style='color:red'>The playlist is not available or incorrect! Please make sure the URL / Link is correct !</span>")

    def anamenu(self):
        self.stackedWidget.setCurrentWidget(self.ana_menu)
        self.clear()

    def single_dw_page(self):
        self.stackedWidget.setCurrentWidget(self.single_download_page)
        self.pushButton_5.clicked.connect(self.content_get)
        self.pushButton_8.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.close_Application)
        self.dw_button.clicked.connect(self.download_video)
        self.pushButton_6.clicked.connect(self.save_file_path)
        self.pushButton_11.clicked.connect(self.showMinimized)
        self.pushButton_12.clicked.connect(self.close_Application)

    def playlist_dw_page(self):
        global root_dir
        self.stackedWidget.setCurrentWidget(self.playlist_download_page)
        self.pushButton_9.clicked.connect(self.save_file_path_pwd)
        self.lineEdit_4.setText("{}/Downloads/Playlist/".format(root_dir))
        self.pushButton_16.clicked.connect(self.content_get_pdw)
        self.pushButton_15.clicked.connect(self.clear)
        self.pushButton_14.clicked.connect(self.showMinimized)
        self.pushButton_13.clicked.connect(self.close_Application)
        self.pvd_button.clicked.connect(self.download_pwd_video)

    def download_pwd_video(self):
        if self.lineEdit_3.text()!="":
            try:
                start_video=0
                self.console.append("----------------------------------------------------------------------------------")
                self.console.append("<span style='color:rgb(78, 154, 6)'>Download Started!</span>")
                for video in self.playlist.videos:
                    vid_title=video.title
                    self.console.append("----------------------------------------------------------------------------------")
                    self.console.append("({}/{})".format(start_video,len(self.playlist.video_urls))+vid_title)
                    video.streams.filter(resolution="720p",progressive="True").first().download(self.lineEdit_4.text())
                    start_video+=1
                self.console.append("<span style='color:rgb(78, 154, 6)'>Succesfully Complete!</span>")
                self.console.append("----------------------------------------------------------------------------------")
            except:
                self.console.append("<span style='color:red'>Something went wrong !</span>")
        else:
            self.console.append("<span style='color:red'>Fill in the blank fields !</span>")

    def exit(self):
        sys.exit()

    def clear(self):
        self.label_6.setText("")
        self.lineEdit.setText("")
        self.label_7.setText("")
        self.video_content.setText("")
        self.pushButton_6.setEnabled(False)
        self.pushButton_5.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.pushButton_9.setEnabled(False)
        self.pushButton_16.setEnabled(True)
        self.lineEdit_3.setText("")
        self.label_13.setText("")
        self.comboBox.clear()
        self.console.clear()


    def UiDesigner(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/tekli_video.png"), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(32, 32))
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("icons/oynatma_listesi.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QSize(32, 32))
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("icons/cikis.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QSize(32, 32))
        icon3 = QIcon()
        icon3.addPixmap(QPixmap("icons/s_location.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon3)
        self.pushButton_6.setIconSize(QSize(18, 18))
        self.pushButton_9.setIcon(icon3)
        self.pushButton_9.setIconSize(QSize(18, 18))
        icon4 = QIcon()
        icon4.addPixmap(QPixmap("icons/search.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QSize(18, 18))
        self.pushButton_16.setIcon(icon4)
        self.pushButton_16.setIconSize(QSize(18, 18))
        icon5 = QIcon()
        icon5.addPixmap(QPixmap("icons/trash.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_8.setIcon(icon5)
        self.pushButton_8.setIconSize(QSize(18, 18))
        self.pushButton_15.setIcon(icon5)
        self.pushButton_15.setIconSize(QSize(18,18))
        icon6 = QIcon()
        icon6.addPixmap(QPixmap("icons/icon.ico"), QIcon.Normal, QIcon.Off)
        self.iconButton.setIcon(icon6)
        self.iconButton.setIconSize(QSize(32, 32))
        self.iconButton_3.setIcon(icon6)
        self.iconButton_3.setIconSize(QSize(32, 32))
        self.iconButton_4.setIcon(icon6)
        self.iconButton_4.setIconSize(QSize(32, 32))

        #Label icon
        #self.resim_etiketi.setPixmap(QtGui.QPixmap("indir.jpg"))

def main():
    app = QApplication(sys.argv) 
    be=MainApp()
    be.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
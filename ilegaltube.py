import os
import subprocess
import pytube
import sys
import PyQt5
import time
import webbrowser
from pytube import *

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox

global url, yt, pl
Ui_MainWindow, QtBaseClass = uic.loadUiType('diseno.ui')


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Descargador de videos y audios de YouTube")  
        self.boton_descargar.clicked.connect(self.moreskia)
        self.boton_cancelar.clicked.connect(self.cancelar)
        url = self.lineedit_url.text()
        #self.commandLinkButton.clicked.connect(lambda: webbrowser.open('https://ilegaltube.blogspot.com/2021/05/ilegaltube-music.html'))
       
    def moreskia(self):
     url = self.lineedit_url.text()
     print(url)
        
     if url:
       
        if (self.radiobutton_video.isChecked() == True and self.checkBox.isChecked() == False and url):
            print("condicional video")
            
            if "playlist" in url:
                QMessageBox.warning(self, 'ILegalTUBES', " URL corresponde a una Playlist. Seleccione: \"Incluir en descarga todos los elementos de la playlist\"")
                self.moreskia                              
            else:
                print("*** estoy en else de condicional video")
                yt=YouTube(url)
                print(yt.title)
                self.label_progreso.setText("Descargando...  " + yt.title)
                self.dir_path = QFileDialog.getExistingDirectory(self, "Elige una ruta de descarga", "E:\\")
                yt.streams.first().download(self.dir_path)
                self.label_progreso.setText("Descarga finalizada")
           
       
        if (self.radiobutton_audio.isChecked() == True and self.checkBox.isChecked() == False):
            print("condicional audio")
            if "playlist" in url:
                QMessageBox.warning(self, 'ILegalTUBES', " URL corresponde a una Playlist. Seleccione: \"Incluir en descarga todos los elementos de la playlist\"")
                self.moreskia                              
            else:
                yt=YouTube(url)
                print(yt.title)
                self.label_progreso.setText("Descargando...  " + yt.title)
                self.dir_path = QFileDialog.getExistingDirectory(self, "Elige una ruta de descarga", "E:\\")
                yt.streams.filter(only_audio=True).first().download(self.dir_path)
                self.label_progreso.setText("Descarga finalizada")
                yt_title=yt.title.replace("'","")
                yt_title=yt_title.replace(".","")
                yt_title=yt_title.replace(",","")
                yt_title=yt_title.replace('"',"")
                yt_title=yt_title.replace('´',"")
                print(yt_title)
                print(f"""******* ffmpeg -i "{self.dir_path}/{yt_title}.mp4" "{self.dir_path}/{yt_title}.mp3" ****** """)
                subprocess.call(f""" ffmpeg -i "{self.dir_path}/{yt_title}.mp4" "{self.dir_path}/{yt_title}.mp3" """, shell=True)
                os.remove(self.dir_path+"/"+yt_title+".mp4")
            
        if (self.radiobutton_video.isChecked() == True and self.checkBox.isChecked() == True):
            print("condicional video y checkbox")
            pl=Playlist(url)
            self.label_progreso.setText("Descargando... "+pl.title)
            if not "playlist" in url:
                QMessageBox.warning(self, 'ILegalTUBES', " Dirección URL no corresponde a una Playlist ")
                self.moreskia                              
            else:
                self.dir_path = QFileDialog.getExistingDirectory(self, "Elige una ruta de descarga", "E:\\")
                for vid in pl.videos:
                    print("tiempo")
                    vid.streams.first().download(self.dir_path)
                    self.label_progreso.setText("Descargando...  "+vid.title)
            self.label_progreso.setText("Descarga finalizada")      

        if (self.radiobutton_audio.isChecked() == True and self.checkBox.isChecked() == True):
            print("condicional audio y checkbox")
            pl=Playlist(url)
            self.label_progreso.setText("Descargando...  "+pl.title)
            if not "playlist" in url:
                QMessageBox.warning(self, 'ILegalTUBES', " Dirección URL no corresponde a una playlist ")
                self.moreskia
            else:
                self.dir_path = QFileDialog.getExistingDirectory(self, "Elige una ruta de descarga", "E:\\")
                for aud in pl.videos:
                    self.label_progreso.setText("Descargando...  "+aud.title)
                    aud.streams.filter(only_audio=True).first().download(self.dir_path)
                    aud_title=aud.title.replace("'","")
                    aud_title=aud_title.replace(".","")
                    aud_title=aud_title.replace(",","")
                    aud_title=aud_title.replace('"',"")
                                               
                    print(" *** archivo filtrado:  "+aud_title)

                    
                    print(f""" ffmpeg -i "{self.dir_path}/{aud_title}.mp4" "{self.dir_path}/{aud_title}.mp3" """)
                    subprocess.call(f""" ffmpeg -i "{self.dir_path}/{aud_title}.mp4" "{self.dir_path}/{aud_title}.mp3" """, shell=True)
                    os.remove(self.dir_path+"/"+aud_title+".mp4")     

                    self.label_progreso.setText("Descarga finalizada")

        elif self.radiobutton_audio.isChecked() == False and self.radiobutton_video.isChecked() == False:
                    QMessageBox.warning(self, 'iLegalTUBES', "Debes seleccionar el tipo de multimedia (Video o Audio) ")
       
     else :
        QMessageBox.warning(self, 'ILegalTUBES', " Debes indicar una direccion URL")
        self.moreskia
       
    
    def cancelar(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()

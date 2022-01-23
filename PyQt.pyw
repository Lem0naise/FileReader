from math import trunc
from optparse import check_choice
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6 import QtGui


import sys
from striprtf.striprtf import rtf_to_text
import mimetypes


# Setting up application
app = QApplication(sys.argv)


accepted_types = [
    'text/html', 
    'text/plain', 
    'application/rtf',
    'application/xml', 
    'application/cfg',
    'application/javascript',
    'application/python',
    'text/x-python',
    'application/vbs'

]

type = None

def check_file_ext(ext):

    global type
    # File checker (if not recognizing)
    if ext[-3:] == "cfg":
        type  = 'application/cfg'

    if ext[-3:] == "pyw":
        type = 'application/python'

    if ext[-2:] == "py":
        type = 'application/python'

    if ext[-3:] == "vbs":
        type = 'application/vbs'

#Actual reading file


def read_file(url):
    
    global type

    #Guessing file type
    type = mimetypes.guess_type(url)
    type = type[0]

    if type == None:
        check_file_ext(url)

    #If still cannot read file type, ensure to say right thing
    if type == None:
        return (f"No current support for .{url.split('.')[-1]} files.")
    
    if type not in accepted_types:
        return f"No current support for {type} files."


    with open(url, 'r') as file:
        
        text= file.read()

    if url[-3:] == 'rtf':
        # If Mac Rich text File, do some weird stripping
        text = rtf_to_text(text)

    return text






# When file dialog called

def b_pressed(self):
    x = QFileDialog.getOpenFileName(window, "Open file", "~/", 'All files (*)')
    

    text = read_file(x[0])
    window.label.setText(text)
    window.adjustSize()
    window.label.adjustSize()
    window.label.setText(text)
    
    window.adjustSize()
    window.label.adjustSize()



# Setting up windows
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True) # Accepting drag drops




        self.setWindowTitle("File Compressor")

        self.label = QLabel("Click to browse or drag files here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.mousePressEvent = b_pressed
        self.label.setFont(QFont('.AppleSystemUIFont', 20))

        


        # Drag and Drop widget


        layout = QVBoxLayout()
        self.label.resize(self.width(), self.height())
        layout.addWidget(self.label)
    

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        

    # Drag and Drop functioning


    

    
    def dragEnterEvent(self, event):

        self.temp_text = self.label.text()

        app.setStyleSheet("QMainWindow { background-color: grey }")


        if event.mimeData().hasUrls():
            self.label.setText("Release to read file!")
            event.accept()
            print("event")
        else:
            self.label.setText("Double check what you're dropping.")
            event.ignore()


    def dragLeaveEvent(self, event):

        app.setStyleSheet("")
        self.label.setText(self.temp_text)



    def dropEvent(self, event):
        app.setStyleSheet("")

        url = event.mimeData().urls()[0].toLocalFile()
            

        
        text = read_file(url)
        self.label.setText(text)
        self.adjustSize()
        self.label.adjustSize()
        self.label.setText(text)
        
        self.adjustSize()
        self.label.adjustSize()
        


        

        


window = MainWindow()

window.show()

# App exec loop
app.exec()
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Notepad(QMainWindow):
    
    def __init__(self):
        super(Notepad, self).__init__()
        
        self.initUI()
        
    def initUI(self):    
        
        self.fh = ' '
        self.filename = 'untitled.txt'
        
        openAct = QAction("Open...", self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip("Open an existing file")
        openAct.triggered.connect(self.openFile)
        
        newAct = QAction( "New", self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip("Create new file")
        newAct.triggered.connect(self.newFile)
        
        saveAct = QAction(  "Save", self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip("Save file")
        saveAct.triggered.connect(self.saveFile)
        
        saveasAct = QAction(  "Save as...", self)
        saveasAct.setStatusTip("Save as new file")
        saveasAct.triggered.connect(self.saveasFile)
        
        exitAct = QAction("Exit", self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip("Exit Notes")
        exitAct.triggered.connect(self.closeFile)
        
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.setStyleSheet("""
                              QMenuBar {
                                    background-color: rgb(40,40,40);
                                }

                                QMenuBar::item {
                                    spacing: 3px;
                                    color: white;
                                    padding: 1px 4px;
                                    background: transparent;
                                }

                                QMenuBar::item:selected { 
                                    background: rgb(70,70,70);
                                }

                                QMenuBar::item:pressed {
                                    background: #646464;
                                }
                              
                              """)
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openAct)
        fileMenu.setStyleSheet("""
                                QMenu{
                                    border:1px solid black; 
                                    margin:2px; 
                                    background-color: rgb(40,40,40); 
                                    color: white
                                } 
                                QMenu::item {
                                    padding:5px;
                                }
                                QMenu::item:selected{
                                    background-color:rgb(70,70,70)
                                }
                               """)
        fileMenu.addAction(newAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(saveasAct)
        fileMenu.addAction(exitAct)
        
        
        
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet("""
                                        border:1px solid rgb(40,40,40);
                                        background-color: rgb(44,44,44);
                                        color:rgb(211,215,207); 
                                        font: 16px "Ubuntu Mono"
                                    """)
        self.textEdit.setFocus()
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("background-color:rgb(40,40,40);color: white")
        
        self.show()
        self.setCentralWidget(self.textEdit)
        self.setGeometry(300,200,600,400)
        tmp = ('%s' % self.filename)
        self.setWindowTitle(tmp)
        self.setWindowIcon( QIcon('icon.png'))
        
    def openFile(self):
        
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File')
        
        
        if QFile.exists(self.filename):
            self.fh = QFile(self.filename)
                
            self.fh.open(QFile.ReadWrite)
            data = self.fh.readAll()
            codec = QTextCodec.codecForUtfText(data)
            unistr = codec.toUnicode(data)

            self.textEdit.setText(unistr)
            self.fh.close()
            tmp = ('%s' % self.filename)
            self.setWindowTitle(tmp)
        
    def saveFile(self):
        
        if self.fh == ' ':
            self.filename, _ = QFileDialog.getSaveFileName(self, \
                                     "Save file", 'untitled.txt')
        elif not QFile.exists(self.filename):
            self.filename, _ = QFileDialog.getSaveFileName(self, \
                                     "Save file", 'untitled.txt')
        self.fh = QFile(self.filename)
        self.fh.open(QFile.ReadWrite)
        data = self.textEdit.toPlainText()
        self.fh.write(str(data))
        self.fh.close()
        
        tmp = ('%s' % self.filename)
        self.setWindowTitle(tmp)    
        
    def saveasFile(self):
    
        self.filename, _ = QFileDialog.getSaveFileName(self, "Save file", 'untitled.txt')
        self.fh = QFile(self.filename)
        self.fh.open(QFile.ReadWrite)
        data = self.textEdit.toPlainText()
        self.fh.write(str(data))
        self.fh.close()
        
        tmp = ('%s' % self.filename)
        self.setWindowTitle(tmp)
        
    def newFile(self):
        
        self.fh = ' '
        self.filename = "untitled.txt"
        tmp = ('%s' % self.filename)
        self.setWindowTitle(tmp)
        self.textEdit.clear()
    
    def closeFile(self):
        self.close()
        
        
app = QApplication(sys.argv)
app.setApplicationName("Notes")

window = Notepad()
window.show()

app.exec_()

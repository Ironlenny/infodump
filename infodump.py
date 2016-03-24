# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from OpenGL import GL # Workaround for
                      # https://bugs.launchpad.net/ubuntu/+source/python-qt4/+bug/941826

def exit():
    sys.exit

def saveRecord():
    print('handler called')
    print((textArea.property('text')))
    print((textField.property('text')))

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine(QUrl('gui.qml'))
    window = engine.rootObjects()[0]
    textArea = window.findChild(QObject, "noteArea")
    textField = window.findChild(QObject, "tagField")
    button = window.findChild(QObject, "contextButton")
#    menuExit = window.findChild(QObject, 'exit')
    button.clicked.connect(saveRecord)
#    menuExit.clicked.connect(exit)
    window.show()
    app.exec_()

main()
import sys

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtQml


class Gui():

    def __init__(self):
        super(Gui, self).__init__()
        self.app = PyQt5.QtGui.QGuiApplication(sys.argv)
        self.engine = PyQt5.QtQml.QQmlApplicationEngine(PyQt5.QtCore.QUrl('gui.qml'))
        self.window = self.engine.rootObjects()[0]

    def run(self):
        self.window.show()
        self.app.exec_()

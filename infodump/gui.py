import sys

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtQml

class _Model(PyQt5.QtCore.QObject):

    def __init__(self, parent=None):
        super(self).__init__(parent)
        self._noteField = ''
        self._tagField = 'Tags...'

    @PyQt5.QtCore.pyqtProperty('QString')
    def noteField(self):
      return self._noteField
    
    @noteField.setter
    def noteField(self, noteField):
      self._noteField = noteField
      
    @PyQt5.QtCore.pyqtProperty('QString')
    def tagField(self):
      return self._tagField
    
    @tagField.setter
    def tagField(self, tagField):
      self._tagField = tagField
    
    @PyQt5.QtCore.pyqtSlot()
    def save(self):
      guicontrol.save_note(self._noteField, self._tagField)
      
    @PyQt5.QtCore.pyqtSlot()
    def search(self):
      guicontrol.search(self._tagField)
     
class Gui():

    def __init__(self, controlObj):
        super(Gui, self).__init__()
        PyQt5.QtQml.qmlRegisterType(_Model, 'infodump.gui.controller', 1, 0, 'controller')
        self.app = PyQt5.QtGui.QGuiApplication(sys.argv)
        self.engine = PyQt5.QtQml.QQmlApplicationEngine(PyQt5.QtCore.QUrl('gui.qml'))
        self.window = self.engine.rootObjects()[0]
        # self.component = PyQt5.QtQml.QQmlComponent(self.engine)
        # self.modelObj = self.component.create()
        global guicontrol
        guicontrol = controlObj
        
    def run(self):
        self.window.show()
        self.app.exec_()
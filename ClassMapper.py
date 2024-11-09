import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from qfluentwidgets import FluentWindow
from qfluentwidgets import FluentIcon as FIF

from ui.GroupTable import GroupTable
from ui.StudentTable import StudentTable
from data.Database import createDatabase, addGroup, getGroups


class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        self.groupTable = GroupTable('Group')
        self.studentTable = StudentTable('Student')

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.groupTable, FIF.CALENDAR, 'Группы')
        self.addSubInterface(self.studentTable, FIF.EDUCATION, 'Обучающиеся')

        self.navigationInterface.addSeparator()

    def initWindow(self):
        self.resize(1400, 800)
        self.setWindowIcon(QIcon('./static/icon.png'))
        self.setWindowTitle('Class Mapper')

        desktop = QApplication.desktop().availableGeometry() # type: ignore
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.navigationInterface.setMinimumExpandWidth(900)
        self.navigationInterface.expand(useAni=False)



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) # type: ignore
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps) # type: ignore

    createDatabase()

    app = QApplication(sys.argv)
    
    window = Window()
    window.show()
    
    sys.exit(app.exec())
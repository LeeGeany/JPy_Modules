from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QStackedWidget


class CMainWindow(QtWidgets.QMainWindow):
    def __init__(self, _UIPath):
        super().__init__()
        self.ui = uic.loadUi(_UIPath, self)
        self.stacked_widget : QStackedWidget = self.findChild(QStackedWidget, "stackedWidget")

    # @brief stackedWidget을 등록한다.
    # @param _stackedWidget
    # @return None
    def addStackedWidget(self, _stackedWidget):
        #self.centralWidget.stackedWidget.addWidget(_stackedWidget)
        self.stacked_widget.addWidget(_stackedWidget)

    # @brief 현재 화면에 전시 할 stackedWidget을 선택한다.
    # @param _stackedWidget
    # @return None
    def showStackedWidget(self, _stackedWidgetNumber):
            self.stacked_widget.setCurrentIndex(_stackedWidgetNumber)

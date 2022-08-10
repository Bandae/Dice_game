from typing import Callable
from PyQt5 import QtCore, QtWidgets
import stylesheets
from PyQt5.QtWidgets import QWidget


class FrameWithLabel(QtWidgets.QFrame):
    def __init__(self, master: QWidget, text: str, frame_geo: list[int], label_geo: list[int]=None, style=None, hide: bool=True) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(*frame_geo))
        if not style:
            style = stylesheets.DEFAULT_FRAME
        self.setStyleSheet(style)

        if not label_geo:
            label_geo = [0, 0, frame_geo[2], frame_geo[3]]

        self.label = Label(self, text, label_geo)
        self.label.show()
        if hide:
            self.hide()


class Label(QtWidgets.QLabel):
    def __init__(self, master: QWidget, text: str, geo: list[int]) -> None:
        super().__init__(master)
        self.setGeometry(*geo)
        
        self.setFont(stylesheets.DEFAULT_FONT)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(text)


class Button(QtWidgets.QPushButton):
    def __init__(self, master: QWidget, text: str, callback: Callable, width: int, height: int) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(width, height, 200, 80))
        self.setFont(stylesheets.DEFAULT_FONT)
        self.setText(text)
        self.clicked.connect(callback)
        self.setStyleSheet(stylesheets.DEFAULT_BUTTON)


class Entry(QtWidgets.QLineEdit):
    def __init__(self, master: QWidget, height: int) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(150, height, 300, 50))
        self.setFont(stylesheets.DEFAULT_FONT)
        self.setMaxLength(16)
        self.setPlaceholderText("player's name")
        self.hide()


class SpinBox(QtWidgets.QSpinBox):
    def __init__(self, master: QWidget) -> None:
        super().__init__(master)
        self.setGeometry(QtCore.QRect(225, 500, 150, 40))
        self.setFont(stylesheets.DEFAULT_FONT)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setMaximum(5)

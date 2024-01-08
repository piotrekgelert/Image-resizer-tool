import os
import pathlib
import re
import sys

import PIL
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import PyQt6.QtWidgets as qtw
from PyQt6.QtCore import Qt
from UI.image_resize_ui import Ui_mw_resize_image


class ImageResizer(qtw.QMainWindow, Ui_mw_resize_image):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = ImageResizer()
    window.show()
    sys.exit(app.exec())
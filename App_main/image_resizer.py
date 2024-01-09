import os
import pathlib
import re
import sys

import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import PyQt6.QtWidgets as qtw
from PIL import Image
from PyQt6.QtCore import Qt
from UI.image_resize_ui import Ui_mw_resize_image


class ImageResizer(qtw.QMainWindow, Ui_mw_resize_image):
    asp_ratio = bool()
    im_width, im_height = 0, 0
    new_im_width, new_im_height = 0, 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pb_image_path.clicked.connect(self.path_to_image)
        self.pb_folder_path.clicked.connect(self.path_to_folder)
        self.cb_aspect_ratio.toggled.connect(self.aspect_ratio)

        self.pb_calculate_pixels.clicked.connect(self.pixels_setup)
        self.pb_calculate_percent.clicked.connect(self.percent_setup)
        self.pb_apply_size.clicked.connect(self.standard_dimentions_setup)
    
    def path_to_image(self):
        file_path = qtw.QFileDialog.getOpenFileName()
        self.lb_image_path.setText(file_path[0])
        with Image.open(file_path[0]) as im:
            self.im_width, self.im_height = im.size
            self.lb_current_width_height.setText(f'{self.im_width} px x {self.im_height} px')
    
    def path_to_folder(self):
        folder_path = qtw.QFileDialog.getExistingDirectory()
        self.lb_folder_path.setText(folder_path)
    
    def aspect_ratio(self):
        cbutton = self.sender()
        self.asp_ratio = cbutton.isChecked()
    
    def pixels_setup(self):
        if self.asp_ratio:
            if len(self.le_width_pixels.text()):
                new_height = int(self.le_width_pixels.text()) * self.im_height // self.im_width
                self.le_height_pixels.setText(str(new_height))
                self.lb_new_width_height.setText(f'{self.le_width_pixels.text()} px x {new_height} px')
            if len(self.le_height_pixels.text()):
                new_width = int(self.le_height_pixels.text()) * self.im_width // self.im_height
                self.le_width_pixels.setText(str(new_width))
                self.lb_new_width_height.setText(f'{new_width} px x {self.le_height_pixels.text()} px')
        else:
            if len(self.le_width_pixels.text()) and len(self.le_height_pixels.text()):
                self.lb_new_width_height.setText(
                    f'{self.le_width_pixels.text()} px x {self.le_height_pixels.text()} px')
            else:
                self.lb_pixel_message.setText('Both dimentions have to be filled in')
    
    def percent_setup(self):
        if len(self.le_width_percent.text()) and len(self.le_height_percent.text()):
            new_width = int(
                (float(self.le_width_percent.text()) / 100) * self.im_width)
            new_height = int(
                (float(self.le_height_percent.text()) / 100) * self.im_height)
            self.lb_new_width_height.setText(
                f'{new_width} px x {new_height} px'
            )
        else:
            self.lb_pixel_message.setText('Both dimentions have to be filled in')
    
    def standard_dimentions_setup(self):
        if self.rb_640_480.isChecked():
            self.lb_new_width_height.setText(f'640 px x 480 px')
        else:
            print('disabled')






if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = ImageResizer()
    window.show()
    sys.exit(app.exec())
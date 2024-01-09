import os
import sys

import PyQt6.QtWidgets as qtw
from PIL import Image
from UI.image_resize_ui import Ui_mw_resize_image


class ImageResizer(qtw.QMainWindow, Ui_mw_resize_image):
    im_path, save_path, im_name, im_extention = '', '', '', ''
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
        
        self.pb_resize.clicked.connect(self.resize_image)
        self.pb_cancel.clicked.connect(self.close)
    
    def path_to_image(self):
        file_path = qtw.QFileDialog.getOpenFileName()
        self.lb_image_path.setText(file_path[0])
        self.im_path = file_path[0]
        self.im_name, self.im_extention = file_path[0].split('/')[-1].split('.')
        with Image.open(file_path[0]) as im:
            self.im_width, self.im_height = im.size
            self.lb_current_width_height.setText(f'{self.im_width} px x {self.im_height} px')
    
    def path_to_folder(self):
        folder_path = qtw.QFileDialog.getExistingDirectory()
        self.save_path = folder_path
        self.lb_folder_path.setText(folder_path)
    
    def aspect_ratio(self):
        cbutton = self.sender()
        self.asp_ratio = cbutton.isChecked()
    
    def pixels_setup(self):
        if self.asp_ratio:
            if len(self.le_width_pixels.text()):
                new_height = int(self.le_width_pixels.text())\
                    * self.im_height // self.im_width
                self.le_height_pixels.setText(str(new_height))
                self.lb_new_width_height.setText(
                    f'{self.le_width_pixels.text()} px x {new_height} px')
                self.new_im_width = int(self.le_height_pixels.text())
                self.new_im_height = new_height
            
            if len(self.le_height_pixels.text()):
                new_width = int(self.le_height_pixels.text())\
                    * self.im_width // self.im_height
                self.le_width_pixels.setText(str(new_width))
                self.lb_new_width_height.setText(
                    f'{new_width} px x {self.le_height_pixels.text()} px')
                self.new_im_width = new_width
                self.new_im_height = int(self.le_height_pixels.text())
        else:
            if len(self.le_width_pixels.text()) \
                and len(self.le_height_pixels.text()):
                self.lb_new_width_height.setText(
                    f'{self.le_width_pixels.text()} px x {self.le_height_pixels.text()} px')
                self.new_im_width = int(self.le_width_pixels.text())
                self.new_im_height = int(self.le_height_pixels.text())
            else:
                self.lb_pixel_message.setText(
                    'Both dimentions have to be filled in')
    
    def percent_setup(self):
        if len(self.le_width_percent.text())\
            and len(self.le_height_percent.text()):
            new_width = int(
                (float(self.le_width_percent.text()) / 100) * self.im_width)
            new_height = int(
                (float(self.le_height_percent.text()) / 100) * self.im_height)
            self.lb_new_width_height.setText(
                f'{new_width} px x {new_height} px'
            )
            self.new_im_width = new_width
            self.new_im_height = new_height
        else:
            self.lb_perc_message.setText('Both dimentions have to be filled in')
    
    def standard_dimentions_setup(self):
        rb = self._dims_set()
        if self.rb_640_480.isChecked():
            rb(640, 480)
        
        elif self.rb_800_600.isChecked():
            rb(800, 600)
        
        elif self.rb_1024_768.isChecked():
            rb(1024, 768)

        elif self.rb_1280_720.isChecked():
            rb(1280, 720)

        elif self.rb_1920_1080.isChecked():
            rb(1920, 1080)

        elif self.rb_3840_2160.isChecked():
            rb(3840, 2160)
        
        elif self.rb_7680_4320.isChecked():
            rb(7680, 4320)

        elif self.rb_half.isChecked():
            rb(int(self.im_width//2), int(self.im_height//2))

        elif self.rb_double.isChecked():
            rb(self.im_width*2, self.im_height*2)
            
        else:
            self.lb_dims_message.setText('Something went wrong, try again')
    
    def _dims_set(self):
        def f(w:int, h:int):
            self.lb_new_width_height.setText(f'{w} px x {h} px')
            self.new_im_width = w
            self.new_im_height = h
        return f
    
    def resize_image(self):
        with Image.open(self.im_path) as im:
            img = im.resize(
                (self.new_im_width, self.new_im_height),
                Image.Resampling.LANCZOS
            )
            img_name = '{}_{}x{}.{}'.format(
                self.im_name,
                self.new_im_width,
                self.new_im_height,
                self.im_extention
            )
            img.save(
                os.path.join(self.save_path, img_name)
            )



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = ImageResizer()
    window.show()
    sys.exit(app.exec())
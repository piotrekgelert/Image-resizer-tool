import os
import sys

import PyQt6.QtWidgets as qtw
from PIL import Image, ImageEnhance
from UI.image_resize_ui import Ui_mw_resize_image


class ImageResizer(qtw.QMainWindow, Ui_mw_resize_image):
    im_path, save_path, im_name, im_extention = '', '', '', ''
    asp_ratio: bool = False
    gb_sharp_px: bool = False
    gb_sharp_prc: bool = False
    sharp: float = 0.0
    im_width, im_height = 0, 0
    new_im_width, new_im_height = 0, 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pb_image_path.clicked.connect(self.path_to_image)
        self.pb_folder_path.clicked.connect(self.path_to_folder)
        self.cb_aspect_ratio.toggled.connect(self.aspect_ratio)
        self.gb_sharp_pixels.toggled.connect(self.gb_sharp_pix)
        self.gb_sharp_percent.toggled.connect(self.gb_sharp_perc)

        self.pb_calculate_pixels.clicked.connect(self.pixels_setup)
        self.pb_calculate_percent.clicked.connect(self.percent_setup)
        self.pb_apply_size.clicked.connect(self.standard_dimentions_setup)
        
        self.pb_resize.clicked.connect(self.resize_image)
        self.pb_reset.clicked.connect(self.reset)
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
    
    def gb_sharp_pix(self):
        self.gb_sharp_px = self.gb_sharp_pixels.isChecked()
    
    def gb_sharp_perc(self):
        self.gb_sharp_prc = self.gb_sharp_percent.isChecked()
    
    def sharp_pixels(self):
        if self.gb_sharp_px:
            if self.rb_sharp_pix_04_px.isChecked():
                self.sharp = 0.4
            elif self.rb_sharp_pix_06_px.isChecked():
                self.sharp = 0.6
            elif self.rb_sharp_pix_08_px.isChecked():
                self.sharp = 0.8
            elif self.rb_sharp_pix_1_px.isChecked():
                self.sharp = 1.0

    def sharp_percent(self):
        if self.gb_sharp_prc:
            if self.rb_sharp_perc_04_px.isChecked():
                self.sharp = 0.4
            elif self.rb_sharp_perc_06_px.isChecked():
                self.sharp = 0.6
            elif self.rb_sharp_perc_08_px.isChecked():
                self.sharp = 0.8
            elif self.rb_sharp_perc_1_px.isChecked():
                self.sharp = 1.0
    
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
                self.lb_pixel_message.setText(
                    'Set proportional dimentions according to the width'
                    )
            
            if len(self.le_height_pixels.text()):
                new_width = int(self.le_height_pixels.text())\
                    * self.im_width // self.im_height
                self.le_width_pixels.setText(str(new_width))
                self.lb_new_width_height.setText(
                    f'{new_width} px x {self.le_height_pixels.text()} px')
                self.new_im_width = new_width
                self.new_im_height = int(self.le_height_pixels.text())
                self.lb_pixel_message.setText(
                    'Set proportional dimentions according to the height'
                    )
        else:
            if len(self.le_width_pixels.text()) \
                and len(self.le_height_pixels.text()):
                self.lb_new_width_height.setText(
                    f'{self.le_width_pixels.text()} px x {self.le_height_pixels.text()} px')
                self.new_im_width = int(self.le_width_pixels.text())
                self.new_im_height = int(self.le_height_pixels.text())
                self.lb_pixel_message.setText(
                    'Set dimentions according to the width and the height'
                    )
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
            self.lb_perc_message.setText(
                    'Set dimentions according to the percentage of width and height'
                    )
        else:
            self.lb_perc_message.setText('Both dimentions have to be filled in')
    
    def standard_dimentions_setup(self):
        rb = self._dims_set()
        if self.rb_640_480.isChecked():
            rb(640, 480)
            self.lb_dims_message.setText('Set width: 640 and height: 480')
        
        elif self.rb_800_600.isChecked():
            rb(800, 600)
            self.lb_dims_message.setText('Set width: 800 and height: 600')
        
        elif self.rb_1024_768.isChecked():
            rb(1024, 768)
            self.lb_dims_message.setText('Set width: 1024 and height: 768')

        elif self.rb_1280_720.isChecked():
            rb(1280, 720)
            self.lb_dims_message.setText('Set width: 1280 and height: 720')

        elif self.rb_1920_1080.isChecked():
            rb(1920, 1080)
            self.lb_dims_message.setText('Set width: 1920 and height: 1080')

        elif self.rb_3840_2160.isChecked():
            rb(3840, 2160)
            self.lb_dims_message.setText('Set width: 3840 and height: 2160')
        
        elif self.rb_7680_4320.isChecked():
            rb(7680, 4320)
            self.lb_dims_message.setText('Set width: 7680 and height: 4320')

        elif self.rb_half.isChecked():
            width_half = int(self.im_width//2)
            heigth_half = int(self.im_height//2)
            rb(width_half, heigth_half)
            self.lb_dims_message.setText(
                'Set width: {} and height: {}'.format(width_half, heigth_half))

        elif self.rb_double.isChecked():
            width_double = self.im_width*2
            height_double = self.im_height*2
            rb(width_double, height_double)
            self.lb_dims_message.setText(
                'Set width: {} and height: {}'.format(width_double, 
                                                      height_double))
            
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
            if self.sharp != 0:
                img = ImageEnhance.Sharpness(img)
                img = img.enhance(1+self.sharp)
            
            img_name = '{}_{}x{}.{}'.format(
                self.im_name,
                self.new_im_width,
                self.new_im_height,
                self.im_extention
            )
            img.save(
                os.path.join(self.save_path, img_name)
            )
        
        self.lb_main_window.setText('Image resized, check folder')
    
    def reset(self):
        self.lb_image_path.clear()
        self.lb_folder_path.clear()
        self.lb_main_window.clear()
        self.lb_current_width_height.setText('width x height')
        self.lb_new_width_height.setText('width x height')
        self.le_width_pixels.clear()
        self.le_height_pixels.clear()
        self.le_width_percent.clear()
        self.le_height_percent.clear()
        self.cb_aspect_ratio.setChecked(False)
        self.le_width_percent.clear()
        self.le_height_percent.clear()
        self.rb_640_480.setChecked(True)
        self.lb_dims_message.clear()
        self.rb_sharp_pix_04_px.setChecked(True)
        self.rb_sharp_perc_04_px.setChecked(True)
        self.gb_sharp_pixels.setChecked(False)
        self.gb_sharp_percent.setChecked(False)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = ImageResizer()
    window.show()
    sys.exit(app.exec())
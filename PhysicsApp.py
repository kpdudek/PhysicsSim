#!/usr/bin/env python3

from typing import Set
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from lib.GameManager import GameManager
from lib.Settings import Settings
from lib.Logger import Logger

import sys

class PhysicsApp(QMainWindow):
    '''
    This class initializes the window,
    '''

    def __init__(self,screen_resolution):
        super().__init__()
        window_size = [1400,800]
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((self.screen_width-window_size[0])/2)
        offset_y = int((self.screen_height-window_size[1])/2)
        self.setGeometry(offset_x,offset_y,window_size[0],window_size[1])
        self.setWindowTitle('Physics 2D')

        self.keys_pressed = []
        self.debug_mode = False

        self.logger = Logger()
        self.game_manager = GameManager(self.keys_pressed)
        self.game_manager.shutdown_signal.connect(self.shutdown)
        self.game_manager.resize_signal.connect(self.update_window_spinboxes)
        self.settings = Settings(self.game_manager)
        self.settings.shutdown_signal.connect(self.shutdown)
        self.settings.resize_window_signal.connect(self.resize_window)
        self.settings.apply_action()    

        self.setCentralWidget(self.game_manager)
        self.show()

    def update_window_spinboxes(self,x,y):
        self.settings.x_size_spinbox.setValue(x)
        self.settings.y_size_spinbox.setValue(y)

    def resize_window(self,x,y):
        self.game_manager.resize_canvas(x,y)
        offset_x = int((self.screen_width-x)/2)
        offset_y = int((self.screen_height-y)/2)
        QApplication.processEvents()
        self.setGeometry(offset_x,offset_y,x,y)

    def keyPressEvent(self, event):                
        if event.key() == Qt.Key_Escape:
            self.shutdown()
        else:
            if event.key() not in self.keys_pressed:
                self.keys_pressed.append(event.key())

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def closeEvent(self, e):
        self.game_manager.painter.end()
        self.game_manager.game_timer.stop()
        self.shutdown()

    def shutdown(self):
        self.settings.close()
        self.close()

def main():
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    physics_app = PhysicsApp(screen_resolution)
    app.exec_()

if __name__ == '__main__':
    main()
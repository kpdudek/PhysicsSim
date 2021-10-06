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
    This app...
    '''

    def __init__(self,screen_resolution):
        super().__init__()
        window_size = [1400,800]
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((screen_width-window_size[0])/2)
        offset_y = int((screen_height-window_size[1])/2)
        self.setGeometry(offset_x,offset_y,window_size[0],window_size[1])
        self.setWindowTitle('Physics 2D')

        self.logger = Logger()

        self.keys_pressed = []
        self.debug_mode = False

        self.game_manager = GameManager(self.keys_pressed,self.debug_mode)
        self.game_manager.shutdown_signal.connect(self.shutdown)
        self.setCentralWidget(self.game_manager)

        self.settings = Settings(self.game_manager)

        self.show()

    def keyPressEvent(self, event):                
        if event.key() == Qt.Key_Escape:
            self.shutdown()
        elif event.key() == Qt.Key_Space:
            self.game_manager.toggle_pause()
        elif event.key() == Qt.Key_D and event.key() not in self.keys_pressed:
            if self.debug_mode:
                self.logger.log(f'Disabling debug mode...')
                self.debug_mode = False
            else:
                self.logger.log(f'Enabling debug mode...')
                self.debug_mode = True
            self.keys_pressed.append(event.key())
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
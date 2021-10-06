#!/usr/bin/env python3

from PyQt5 import QtWidgets, uic

from lib.Logger import Logger, FilePaths

class Settings(QtWidgets.QWidget):

    def __init__(self,game_manager):
        super().__init__()
        self.game_manager = game_manager
        self.logger = Logger()
        self.file_paths = FilePaths()

        uic.loadUi(f'{self.file_paths.user_path}ui/settings_window.ui',self)

        self.apply_button.clicked.connect(self.apply)

        self.show()

    def apply(self):
        if self.game_manager.health_logger_timer.isActive() and not self.health_logger_checkbox.isChecked():
            self.game_manager.health_logger_timer.stop()
        elif not self.game_manager.health_logger_timer.isActive() and self.health_logger_checkbox.isChecked():
            self.game_manager.health_logger_timer.start(1000)
    

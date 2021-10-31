#!/usr/bin/env python3

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore

from lib.Logger import Logger, FilePaths

class Settings(QtWidgets.QWidget):
    resize_window_signal = QtCore.pyqtSignal(int,int)
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,game_manager):
        super().__init__()
        self.game_manager = game_manager
        self.logger = Logger()
        self.file_paths = FilePaths()

        uic.loadUi(f'{self.file_paths.user_path}ui/settings_window.ui',self)
        self.setWindowTitle('Game Configuration')

        self.apply_button.clicked.connect(self.apply_action)
        self.quit_button.clicked.connect(self.quit_action)
        self.pause_button.clicked.connect(self.pause_action)

        self.show()

    def toggle_health_timer(self):
        if self.game_manager.health_logger_timer.isActive() and not self.health_logger_checkbox.isChecked():
            self.game_manager.health_logger_timer.stop()
        elif not self.game_manager.health_logger_timer.isActive() and self.health_logger_checkbox.isChecked():
            self.game_manager.health_logger_timer.start(2000)

    def toggle_fps_overlay_display(self):
        if self.fps_overlay_checkbox.isChecked():
            self.game_manager.camera.display_fps_overlay = True
        else:
            self.game_manager.camera.display_fps_overlay = False

    def toggle_display_tails(self):
        if self.display_tails_checkbox.isChecked():
            self.game_manager.camera.display_tails = True
        else:
            self.game_manager.camera.display_tails = False
    
    def set_window_size(self):
        x = self.x_size_spinbox.value()
        y = self.y_size_spinbox.value()
        self.resize_window_signal.emit(x,y)

    def set_debug_mode(self):
        if self.debug_mode_checkbox.isChecked():
            self.game_manager.debug_mode = True
        else:
            self.game_manager.debug_mode = False
    
    def quit_action(self):
        self.shutdown_signal.emit()

    def pause_action(self):
        if self.game_manager.paused:
            self.game_manager.paused = False
        else:
            self.game_manager.paused = True
    
    def apply_action(self):
        self.toggle_health_timer()
        self.toggle_fps_overlay_display()
        self.toggle_display_tails()
        self.set_window_size()
        self.set_debug_mode()
    

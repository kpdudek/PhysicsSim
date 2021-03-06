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
        self.clear_scene_button.clicked.connect(self.clear_scene_action)
        self.reset_camera_button.clicked.connect(self.reset_camera_action)
        self.performance_test_button.clicked.connect(self.run_performance_test)

        self.entity_list_widget.currentItemChanged.connect(self.set_spawn_type)
        self.refresh_entity_type_list()

        for widget in self.mode_frame.children():
            if type(widget)==QtWidgets.QRadioButton:
                widget.toggled.connect(self.set_mode)
                if widget.isChecked():
                    self.game_manager.scene.mode = widget.text()

        for widget in self.spawn_physics_frame.children():
            if type(widget)==QtWidgets.QRadioButton:
                widget.toggled.connect(self.set_spawn_physics)
                if widget.isChecked():
                    self.game_manager.scene.entity_spawn_physics = widget.text()
        
        self.sync_pause_button()
        self.show()
    
    def set_mode(self):
        option = self.sender()
        if option.isChecked():
            self.game_manager.scene.mode = option.text()

    def set_spawn_type(self,item):
        self.game_manager.scene.entity_spawn_type = item.text()

    def set_spawn_physics(self):
        option = self.sender()
        if option.isChecked():
            self.game_manager.scene.entity_spawn_physics = option.text()

    def reset_camera_action(self):
        self.game_manager.camera.reset()

    def refresh_entity_type_list(self):
        entities = self.game_manager.scene.get_entity_types()
        row_set = False
        for entity in entities:
            self.entity_list_widget.addItem(entity)
            if entity == 'ball':
                self.entity_list_widget.setCurrentRow(self.entity_list_widget.count()-1)
                row_set = True

        # The active row must be set in order to trigger the set_mode() event and give the scene a default spawn type
        if not row_set:
            self.entity_list_widget.setCurrentRow(0)

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

    def sync_pause_button(self):
        if self.game_manager.paused:
            self.pause_button.setText('Play')
        else:
            self.pause_button.setText('Pause')

    def pause_action(self):
        if self.game_manager.paused:
            self.pause_button.setText('Pause')
            self.game_manager.paused = False
        else:
            self.pause_button.setText('Play')
            self.game_manager.paused = True

    def clear_scene_action(self):
        self.game_manager.scene.init_scene()

    def run_performance_test(self):
        self.game_manager.run_performance_test()
    
    def apply_action(self):
        self.toggle_health_timer()
        self.toggle_fps_overlay_display()
        self.toggle_display_tails()
        self.set_window_size()
        self.set_debug_mode()

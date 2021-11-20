#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from lib.GameManager import GameManager
import sys

def main():
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    game_manager = GameManager(screen_resolution)
    app.exec_()

if __name__ == '__main__':
    main()
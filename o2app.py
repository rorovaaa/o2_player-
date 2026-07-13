import sys
import os
from user.menu import MENUSKA
import json

def main():
    if '--gui' in sys.argv:
        from source.gui_test import RetroPlayer
        from PyQt6.QtWidgets import QApplication
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        player = RetroPlayer()
        player.show()
        sys.exit(app.exec())
    else:
        from user.menu import MENUSKA
        menu = MENUSKA()
        menu.start_menu()

if __name__ == '__main__':
    main()

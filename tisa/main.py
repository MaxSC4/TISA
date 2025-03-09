import sys
import time 

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt

from .gui import PetroSegGUI

from .utils.ui_utils import apply_fusion_dark_palette, create_splash_pix

def main():
    app = QApplication(sys.argv)

    apply_fusion_dark_palette(app)

    splash_pix = create_splash_pix("tisa/icons/tisa_icon.png", "TISA v1.0.0", text_color="black")
    if splash_pix is not None:
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.show()
        app.processEvents()
    else:
        splash = None

    time.sleep(5)

    window = PetroSegGUI()
    window.show()

    if splash:
        splash.finish(window)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


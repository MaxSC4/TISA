import time
import os
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPalette
from PyQt5.QtCore import Qt

def apply_fusion_dark_palette(app):
    """
    Dark theme for the UI
    """
    from PyQt5.QtWidgets import QApplication
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)


def create_splash_pix(image_path, splash_text="TISA v1.0.0", text_color="black"):
    """
    Create and return a QPixmap for the splash screen
    """
    pix = QPixmap(image_path)
    if pix.isNull():
        print(f"Impossible to load image: {image_path}")
        return None

    painter = QPainter(pix)
    painter.setPen(QColor(text_color))
    painter.setFont(QFont("Arial", 24, QFont.Bold))

    rect = pix.rect()
    painter.drawText(rect, Qt.AlignCenter | Qt.AlignBottom, splash_text)
    painter.end()

    return pix

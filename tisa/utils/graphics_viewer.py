from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QRectF

class GraphicsImageViewer(QGraphicsView):
    """
    Widget to display an image with QGraphicsScene with a mouse wheel zoom and panning
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self._pixmap_item = None  # contiendra l'image

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def load_image(self, img_path):
        """
        Load an image and display it in scene
        """
        pix = QPixmap(img_path)
        if pix.isNull():
            print(f"Impossible de charger l'image: {img_path}")
            return

        if self._pixmap_item:
            self._scene.removeItem(self._pixmap_item)
            self._pixmap_item = None

        self._pixmap_item = self._scene.addPixmap(pix)

        self.setSceneRect(self._scene.itemsBoundingRect())


    def wheelEvent(self, event):
        """
        Zoom in/out with mouse wheel
        """
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            scale_factor = zoom_in_factor
        else:
            scale_factor = zoom_out_factor

        self.scale(scale_factor, scale_factor)

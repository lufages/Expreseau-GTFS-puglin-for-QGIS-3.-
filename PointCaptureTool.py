from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.gui import QgsMapTool
from qgis.core import QgsPointXY

class PointCaptureTool(QgsMapTool):
    # Signal pour transmettre les coordonnées capturées
    pointCaptured = pyqtSignal(QgsPointXY)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas

    def canvasPressEvent(self, event):
        # Récupérer les coordonnées de la carte lors d'un clic
        point = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos().x(), event.pos().y())
        self.pointCaptured.emit(point)  # Émettre le signal avec les coordonnées

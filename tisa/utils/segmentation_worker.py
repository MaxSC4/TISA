from PyQt5.QtCore import QObject, pyqtSignal
from ..core.segmentation.automated import process_folder 

class SegmentationWorker(QObject):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, params, parent=None):
        super().__init__(parent)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.params = params

    def run(self):
        try:
            process_folder(self.input_dir, self.output_dir, self.params, progress_callback=self.progress_signal.emit)
            self.progress_signal.emit(100)
        except Exception as e:
            self.error_signal.emit(str(e))
        finally:
            self.finished_signal.emit()
# tisa/gui.py

import sys
import os
import pandas as pd

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QFileDialog, QSlider, QVBoxLayout, QWidget, 
    QHBoxLayout, QProgressBar, QAction, QSpinBox, QGroupBox, QFormLayout, 
    QSizePolicy, QInputDialog, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from .core.mosaic import split_image, reconstruct_mosaic
from .core.segmentation.automated import process_folder
from .core.analysis import calculate_label_percentages
from .utils.graphics_viewer import GraphicsImageViewer
from .utils.segmentation_worker import SegmentationWorker


class LabelsWindow(QWidget):
    """
    Window to display labels list, percentages and colors
    """
    def __init__(self, label_percentages, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Labels and Percentages")
        self.resize(400, 600)
        self.setStyleSheet("background-color: #2E3440; color: white;")

        from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
        from PyQt5.QtGui import QPixmap, QColor

        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        row, col = 0, 0
        for label, (percentage, hex_color) in label_percentages.items():
            color_label = QLabel()
            color_label.setFixedSize(30, 30)
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor(hex_color))
            color_label.setPixmap(pixmap)

            percentage_label = QLabel(f"{percentage:.2f}%")

            grid_layout.addWidget(color_label, row, col * 2)
            grid_layout.addWidget(percentage_label, row, col * 2 + 1)

            col += 1
            if col == 3:
                col = 0
                row += 1

        layout.addLayout(grid_layout)
        total_percentage = sum(percentage for percentage, _ in label_percentages.values())
        summary_label = QLabel(f"Total: {total_percentage:.2f}%")
        layout.addWidget(summary_label)

        self.setLayout(layout)


class PetroSegGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TISA - Thin-section Image Segmenter and Analyzer")
        self.setGeometry(100, 100, 1200, 700)

        icon_path = os.path.join(os.path.dirname(__file__), "icons", "tisa_icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.current_image_path = None

        self.initMenuBar()
        self.initUI()

    def initMenuBar(self):
        menu_bar = self.menuBar()

        # Menu File
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Help
        help_menu = menu_bar.addMenu("Help")
        doc_action = QAction("Documentation", self)
        doc_action.triggered.connect(self.show_documentation)
        help_menu.addAction(doc_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_documentation(self):
        QMessageBox.information(self, "Documentation", "Consultez le manuel utilisateur ou la doc en ligne.")

    def show_about(self):
        QMessageBox.information(self, "About TISA", "TISA - v1.0.0\nThin-section Image Segmenter and Analyzer.\n© M. SOARES CORREIA, 2025")

    def initUI(self):
        """
        Build main interface with QSplitter
        """
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        splitter = QSplitter(Qt.Horizontal)

        # ---- Left column ----
        controls_widget = QWidget()
        controls_layout = QVBoxLayout()

        # 1) GroupBox: Upload
        gb_original = QGroupBox("Original Mosaic")
        gb_original.setStyleSheet("QGroupBox { font-weight: bold; }")
        gb_layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload Mosaic")
        self.upload_btn.setIcon(QIcon("icons/upload.png"))
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC; 
                color: white; 
                border-radius: 5px; 
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4C70A2;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_image)

        self.split_btn = QPushButton("Split Mosaic")
        self.split_btn.setIcon(QIcon("icons/split.png"))
        self.split_btn.setStyleSheet("""
            QPushButton {
                background-color: #88C0D0; 
                color: black; 
                border-radius: 5px; 
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #76A0B0;
            }
        """)
        self.split_btn.clicked.connect(self.split_mosaic)

        self.split_progress_bar = QProgressBar()

        gb_layout.addWidget(self.upload_btn)
        gb_layout.addWidget(self.split_btn)
        gb_layout.addWidget(self.split_progress_bar)
        gb_original.setLayout(gb_layout)
        controls_layout.addWidget(gb_original)

        # 2) GroupBox: Segmentation
        gb_seg = QGroupBox("Segmentation")
        gb_seg.setStyleSheet("QGroupBox { font-weight: bold; }")
        seg_layout = QFormLayout()

        self.epoch_slider = QSlider(Qt.Horizontal)
        self.epoch_slider.setRange(1, 100)
        self.epoch_slider.setValue(10)
        self.epoch_label = QLabel(str(self.epoch_slider.value()))
        self.epoch_slider.valueChanged.connect(lambda: self.epoch_label.setText(str(self.epoch_slider.value())))

        self.mod_dim1 = QSlider(Qt.Horizontal)
        self.mod_dim1.setRange(1, 128)
        self.mod_dim1.setValue(64)
        self.mod_dim1_label = QLabel(str(self.mod_dim1.value()))
        self.mod_dim1.valueChanged.connect(lambda: self.mod_dim1_label.setText(str(self.mod_dim1.value())))

        self.mod_dim2 = QSlider(Qt.Horizontal)
        self.mod_dim2.setRange(1, 128)
        self.mod_dim2.setValue(32)
        self.mod_dim2_label = QLabel(str(self.mod_dim2.value()))
        self.mod_dim2.valueChanged.connect(lambda: self.mod_dim2_label.setText(str(self.mod_dim2.value())))

        self.min_label_spin = QSpinBox()
        self.min_label_spin.setRange(1, 10)
        self.min_label_spin.setValue(3)

        self.max_label_spin = QSpinBox()
        self.max_label_spin.setRange(10, 50)
        self.max_label_spin.setValue(25)

        seg_layout.addRow("Training Epochs:", self.epoch_slider)
        seg_layout.addRow("", self.epoch_label)
        seg_layout.addRow("Mod Dim1:", self.mod_dim1)
        seg_layout.addRow("", self.mod_dim1_label)
        seg_layout.addRow("Mod Dim2:", self.mod_dim2)
        seg_layout.addRow("", self.mod_dim2_label)
        seg_layout.addRow("Min Labels:", self.min_label_spin)
        seg_layout.addRow("Max Labels:", self.max_label_spin)

        self.start_seg_btn = QPushButton("Start Segmentation")
        self.start_seg_btn.setStyleSheet("background-color: #A3BE8C; color: black; border-radius: 5px; padding: 8px;")
        self.start_seg_btn.setIcon(QIcon("icons/segment.png"))
        self.start_seg_btn.clicked.connect(self.start_segmentation)
        seg_layout.addRow(self.start_seg_btn)

        self.progress_bar = QProgressBar()
        seg_layout.addRow(self.progress_bar)

        gb_seg.setLayout(seg_layout)
        controls_layout.addWidget(gb_seg)

        # 3) GroupBox: Post-process
        gb_post = QGroupBox("Post-processing")
        gb_post.setStyleSheet("QGroupBox { font-weight: bold; }")

        post_layout = QVBoxLayout()

        self.build_mosaic_btn = QPushButton("Build Mosaic")
        self.build_mosaic_btn.setIcon(QIcon("icons/mosaic.png"))
        self.build_mosaic_btn.setStyleSheet("background-color: #EBCB8B; color: black; border-radius: 5px; padding: 8px;")
        self.build_mosaic_btn.clicked.connect(self.build_mosaic)

        self.download_data_btn = QPushButton("Download Data")
        self.download_data_btn.setIcon(QIcon("icons/download.png"))
        self.download_data_btn.setStyleSheet("background-color: #D08770; color: black; border-radius: 5px; padding: 8px;")
        self.download_data_btn.clicked.connect(self.download_data)

        self.show_labels_btn = QPushButton("Show Labels %")
        self.show_labels_btn.setStyleSheet("background-color: #A3BE8C; color: black; border-radius: 5px; padding: 8px;")
        self.show_labels_btn.setIcon(QIcon("icons/labels.png"))
        self.show_labels_btn.clicked.connect(self.show_labels)

        post_layout.addWidget(self.build_mosaic_btn)
        post_layout.addWidget(self.download_data_btn)
        post_layout.addWidget(self.show_labels_btn)
        gb_post.setLayout(post_layout)
        controls_layout.addWidget(gb_post)

        controls_widget.setLayout(controls_layout)

        # ---- Image display area ----
        display_widget = QWidget()
        display_layout = QHBoxLayout(display_widget)

        # ---- Image viewer ----
        self.original_viewer = GraphicsImageViewer()
        self.original_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.segmented_viewer = GraphicsImageViewer()
        self.segmented_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ---- 1) Original container ----
        original_container = QWidget()
        orig_vlayout = QVBoxLayout(original_container)

        orig_title = QLabel("Original Image")
        orig_title.setAlignment(Qt.AlignCenter)
        orig_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")

        orig_vlayout.addWidget(orig_title)
        orig_vlayout.addWidget(self.original_viewer)

        original_container.setLayout(orig_vlayout)

        # ---- 2) Segmented container ----
        seg_container = QWidget()
        seg_vlayout = QVBoxLayout(seg_container)

        seg_title = QLabel("Segmented Image")
        seg_title.setAlignment(Qt.AlignCenter)
        seg_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")

        seg_vlayout.addWidget(seg_title)
        seg_vlayout.addWidget(self.segmented_viewer)

        seg_container.setLayout(seg_vlayout)

        # ---- On place ces deux containers côte à côte ----
        display_layout.addWidget(original_container)
        display_layout.addWidget(seg_container)

        splitter.addWidget(controls_widget)
        splitter.addWidget(display_widget)

        splitter.setStretchFactor(0, 0) 
        splitter.setStretchFactor(1, 1) 

        central_layout.addWidget(splitter)

    # ================== CALLBACKS ==================
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.tiff)")
        if file_path:
            self.current_image_path = file_path
            self.original_viewer.load_image(file_path)

    def split_mosaic(self):
        self.split_progress_bar.setValue(0)
        rows, ok = QInputDialog.getInt(self, "Rows", "Enter rows:", 5, 1, 100, 1)
        if not ok:
            return
        cols, ok = QInputDialog.getInt(self, "Columns", "Enter columns:", 5, 1, 100, 1)
        if not ok:
            return
        out_dir = QFileDialog.getExistingDirectory(self, "Select output directory")
        if not out_dir or not self.current_image_path:
            return

        def update_split(val):
            self.split_progress_bar.setValue(int(val))

        split_image(self.current_image_path, rows, cols, out_dir, progress_callback=update_split)
        self.statusBar().showMessage("Mosaic split completed!")

    def start_segmentation(self):
        params = {
            "train_epoch": self.epoch_slider.value(),
            "mod_dim1": self.mod_dim1.value(),
            "mod_dim2": self.mod_dim2.value(),
            "min_label_num": self.min_label_spin.value(),
            "max_label_num": self.max_label_spin.value(),
            "segmentation_method": "kmeans"  # or 'felzenszwalb'
        }

        in_dir = QFileDialog.getExistingDirectory(self, "Select folder with tiles")
        out_dir = QFileDialog.getExistingDirectory(self, "Select output folder for segmented tiles")
        if not in_dir or not out_dir:
            return

        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Segmentation in progress...")

        self.thread = QThread()
        self.worker = SegmentationWorker(in_dir, out_dir, params)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.error_signal.connect(lambda err: QMessageBox.critical(self, "Error", err))
        self.worker.finished_signal.connect(self.thread.quit)
        self.worker.finished_signal.connect(lambda: self.statusBar().showMessage("Segmentation completed!"))
        self.worker.finished_signal.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def build_mosaic(self):
        in_dir = QFileDialog.getExistingDirectory(self, "Select folder with segmented tiles")
        out_file, _ = QFileDialog.getSaveFileName(self, "Save mosaic", "", "Images (*.png *.jpg)")
        if not in_dir or not out_file:
            return

        try:
            reconstruct_mosaic(in_dir, out_file)
            self.segmented_viewer.load_image(out_file)
            self.statusBar().showMessage(f"Mosaic built at: {out_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Mosaic reconstruction failed: {e}")

    def download_data(self):
        choice, ok = QInputDialog.getItem(self, "Process Type", "Folder or single image?", ["Folder", "Single Image"], 0, False)
        if not ok:
            return

        if choice == "Folder":
            input_path = QFileDialog.getExistingDirectory(self, "Select folder with segmented tiles")
        else:
            input_path, _ = QFileDialog.getOpenFileName(self, "Select segmented image", "", "Images (*.png *.jpg *.jpeg *.tiff)")
        if not input_path:
            return

        out_csv, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not out_csv:
            return

        try:
            all_data = []
            if choice == "Folder":
                for fname in os.listdir(input_path):
                    if fname.endswith(".png"):
                        tile_path = os.path.join(input_path, fname)
                        pcts = calculate_label_percentages(tile_path)
                        for label, (perc, color) in pcts.items():
                            all_data.append({"Tile": fname, "Label": label, "Percentage": perc, "Color": color})
            else:
                pcts = calculate_label_percentages(input_path)
                bname = os.path.basename(input_path)
                for label, (perc, color) in pcts.items():
                    all_data.append({"Tile": bname, "Label": label, "Percentage": perc, "Color": color})

            df = pd.DataFrame(all_data)
            df.to_csv(out_csv, index=False)
            self.statusBar().showMessage(f"Data saved to {out_csv}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Data extraction failed: {e}")

    def show_labels(self):
        csv_file, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not csv_file:
            return

        try:
            df = pd.read_csv(csv_file)
            label_percentages = {}
            for _, row in df.iterrows():
                label = row['Label']
                perc = row['Percentage']
                color = row['Color']
                label_percentages[label] = (perc, color)

            lw = LabelsWindow(label_percentages, self)
            lw.setAttribute(Qt.WA_DeleteOnClose)
            lw.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV: {e}")




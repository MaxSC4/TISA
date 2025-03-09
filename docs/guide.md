# TISA User Guide

## 📌 Introduction
TISA (**Thin-section Image Segmenter & Analyzer**) is a tool designed for the **automatic segmentation and analysis of petrographic thin sections**. It enables the identification and classification of mineral grains within thin-section images using advanced segmentation techniques.

This guide provides step-by-step instructions for installing, configuring, and using TISA effectively.

---

## 🏗️ Installation

### **1️⃣ Prerequisites**
Ensure you have **Python 3.8+** installed. Then, install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### **2️⃣ Running the Application**
To launch TISA's graphical interface, run:
```bash
python -m tisa.main
```

---

## 🖥️ Graphical Interface Overview

TISA features an intuitive **Graphical User Interface (GUI)** built with `PyQt5`. The interface is divided into the following sections:

### **1️⃣ Image Loading**
- Click **"Upload Mosaic"** to load a petrographic thin-section image.
- Supported formats: `.png`, `.jpg`, `.tiff`, `.bmp`.
- Click **"Split Mosaic"** to split a mosaic into tiles. TISA will ask you to choose the number of rows and columns so you want to split your image into.
- The tiles will be saved in the folder you choose.

### **2️⃣ Segmentation Parameters**
Adjust the segmentation settings before starting the automatic analysis:
- **`mod_dim1`**: Number of filters in the first convolutional layer.
- **`mod_dim2`**: Number of filters in the second convolutional layer.
- **`train_epoch`**: Number of training iterations for machine-learning-based segmentation.
- **`max_label_num`**: Maximum number of labels for segmentation classification.

### **3️⃣ Running the Segmentation**
- Click **"Start Segmentation"** to process the image.
- A **progress bar** updates in real time as the segmentation is performed.
- Click **"Build Mosaic"** and chose the segmented tiles to rebuild the segmented mosaic.
- The **resulting segmented image** is displayed on the right side of the interface.

### **4️⃣ Display labels**
- Click **"Show Labels %"** to see the percentage each label (color) represents on the segmented mosaic.

### **5️⃣ Exporting Results**
- Click **"Save Results"** to export the segmented image.
- Data and statistical analysis can be saved in `.csv` format.

---

## 🛠️ Advanced Settings

### **Threshold Adjustments**
If some grains are not well detected, adjust:
- **Threshold values** to refine the segmentation.

### **Artifact Removal**
TISA includes automatic edge detection and cleanup:
- **Auto-crop:** Removes unwanted black or bright borders.

### **Using a Fixed Palette**
TISA applies a **fixed color mapping** to segmentation results to ensure consistency across images.

---

## 📂 File Outputs

After running the segmentation, TISA generates:
- **Segmented Image** (`.png` or `.jpg`) in the output folder.
- **Label Statistics** (`.csv`) containing the percentage of detected mineral phases.

---

## 🔥 Troubleshooting

### **1️⃣ Segmentation Takes Too Much Time**
- Reduce `train_epoch` or lower `mod_dim1/mod_dim2` values.
- Resize the input image to a lower resolution before running segmentation.

### **2️⃣ Memory Usage is Too High**
- Reduce image dimensions or use more tiles.


---

## 📬 Contributing
If you’d like to contribute to **TISA**, feel free to:
- Report bugs or suggest features via **GitHub Issues**.
- Contribute code via **Pull Requests**.
- Provide petrographic datasets to improve segmentation performance.

---

## 📄 License
TISA is distributed under the **GNU GPL v3 License**, meaning you are free to use, modify, and distribute it but it needs to be open-source.

---

## **📢 Final Words**
TISA is designed to make thin-section analysis easier and more efficient. If you have any questions or suggestions, feel free to reach out!

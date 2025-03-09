# Segmentation in TISA

## 📌 Introduction
TISA (**Thin-section Image Segmenter & Analyzer**) uses advanced **segmentation algorithms** to analyze petrographic thin sections. This document explains how segmentation works in TISA, including the available methods, parameters, and best practices.

---

## 🔍 How Segmentation Works

Segmentation is the process of dividing an image into **distinct regions** based on mineralogical and textural properties. In petrography, segmentation helps in:
- Identifying different mineral grains.
- Measuring grain sizes and distributions.
- Removing unwanted artifacts (thin-section borders, light reflections, etc.).

TISA provides both **machine-learning-based segmentation** and **traditional image processing techniques**.

---

## ⚙️ Available Segmentation Methods

TISA offers multiple segmentation techniques, each suited for different petrographic analyses.

### **1️⃣ K-Means Clustering**
- A clustering algorithm that groups pixels based on their color similarity.
- Best suited for **simple thin sections** with clear color contrasts.
- Parameter: **`max_label_num`** controls the number of segments.

### **2️⃣ Deep Learning-Based Segmentation**
- Uses a convolutional neural network (CNN) for pixel-wise classification.
- More robust for complex samples with overlapping grains.
- Adjustable via **`mod_dim1`**, **`mod_dim2`**, and **`train_epoch`**.

### **3️⃣ Felzenszwalb Algorithm**
- A graph-based segmentation method that adapts to texture and color variations.
- Good for images where mineral boundaries are not purely color-based.

---

## 🛠️ Key Segmentation Parameters

| Parameter        | Description |
|-----------------|------------|
| `mod_dim1`      | Number of filters in the first CNN layer. |
| `mod_dim2`      | Number of filters in the second CNN layer. |
| `train_epoch`   | Number of training iterations for the segmentation model. |
| `max_label_num` | Maximum number of clusters for K-Means segmentation. |

### **Best Practices for Choosing Parameters**
- **Use `max_label_num` carefully** in K-Means: too high values may over-segment the image.
- **For deep learning segmentation**, increase `train_epoch` if segmentation quality is poor.
- **Adjust `mod_dim1` and `mod_dim2`** to balance segmentation quality and memory usage.

---

## 🎨 Applying Fixed Color Mapping

To ensure **consistent visualization**, TISA applies a **fixed palette mapping** to segmentation results. This avoids cases where similar minerals receive different colors in different images.

Each label in the segmentation map corresponds to a **predefined color**, ensuring that the output images remain visually interpretable.

### **Example Palette Mapping**
| Label | Mineral Phase | Color |
|-------|--------------|-------|
| 0     | Background   | Black |
| 1     | Quartz      | Red |
| 2     | Feldspar    | Green |
| 3     | Mica        | Blue |

---

## 🛑 Common Segmentation Issues & Fixes

### **1️⃣ Segmentation Produces Too Many Small Regions**
- Solution: Increase `max_label_num` in K-Means to merge similar clusters.

### **2️⃣ The Algorithm Fails to Detect Certain Phases**
- Solution: Increase **training epochs** in deep learning-based segmentation.
- Solution: Adjust **contrast and brightness** in preprocessing.

### **3️⃣ Thin-Section Borders are Detected as Regions**
- Solution: Use **automatic border removal (`auto_crop()`, `remove_mosaic_edges()`)** before applying segmentation.

### **4️⃣ Segmentation Colors Change Between Runs**
- Solution: Ensure **label normalization** is applied so that labels are mapped consistently.
- Solution: Use a **fixed color palette** across images.

---

## 📈 Exporting Segmentation Results

TISA saves segmented results in:
- **Image format (`.png`, `.jpg`)**: For visual interpretation.
- **CSV format (`.csv`)**: Containing statistics such as grain sizes and phase proportions.

---

## 📬 Contributing to Segmentation Improvements

If you want to help improve segmentation in TISA:
- Provide high-quality **thin-section datasets** for training.
- Test different segmentation models and report **accuracy issues**.
- Optimize parameters for **better speed-memory tradeoff**.

---

## 📄 License
TISA is distributed under the **GNU GPL v3 License**, allowing free use, modification, and redistribution (open-source).

---

## **📢 Final Words**
Segmentation is a crucial step in thin-section analysis. With TISA, users can apply advanced algorithms to obtain high-quality, reproducible results. If you need support, check out the documentation or reach out!

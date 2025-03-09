# TISA (Thin-section Image Segmenter & Analyzer)

## 📌 Introduction
TISA (Thin-section Image Segmenter & Analyzer) is an advanced tool for automated segmentation of petrographic thin sections. It enables systematic analysis of thin-section images using cutting-edge segmentation and classification algorithms.

With a modern graphical interface and optimized performance, TISA streamlines the analysis and interpretation of mineral textures and structures.

---

## 🏛️ Based on PetroSeg by Azzam et al.
TISA is a modified and improved version of **PetroSeg**, originally developed by **Azzam et al.** for petrographic image segmentation. 
The original work on **PetroSeg** laid the foundation for thin-section segmentation, and TISA builds upon it.

Reference to the original work:
📄 *Azzam et al., 2024 - Automated petrographic image analysis by supervised and*
*unsupervised machine learning methods - Sedimentologika*

---

## 🚀 Key Features
- **📸 Image Loading:** Supports `.png`, `.jpg`, `.tiff`, `.bmp` formats.
- **🖥️ Modern GUI:** Built with `PyQt5` for a smooth user experience.
- **🧩 Automated Segmentation:** Uses advanced algorithms (`K-means`, `FastSAM`).
- **🎨 Custom Palette Mapping:** Assigns fixed colors to segmentation labels.
- **🛠️ Automatic Artifact Removal:** Eliminates thin-section edges and unwanted lighting effects.
- **📊 Result Analysis:** Generates statistics and data exports.

---

## 🏗️ Installation
### **1️⃣ Prerequisites**
Ensure you have **Python 3.8+** and install dependencies:
```bash
pip install -r requirements.txt
```

### **2️⃣ Run the Application**
Launch the graphical interface with:
```bash
python -m tisa.main
```

---

## 📖 Quick User Guide

1️⃣ **Open an Image**  
   - Load a thin-section image from your computer. 
   - Split the mosaic in tiles. 

2️⃣ **Start Segmentation**  
   - Adjust parameters (`mod_dim1`, `mod_dim2`, `epochs`).  
   - Start automatic segmentation.  

3️⃣ **Export Results**  
   - Save segmented images and statistics.

---

## 🛠️ Advanced Parameters
| Parameter        | Description |
|-----------------|------------|
| `mod_dim1`      | Number of filters in the first convolutional layer. |
| `mod_dim2`      | Number of filters in the second convolutional layer. |
| `train_epoch`   | Number of iterations for training. |
| `max_label_num` | Maximum number of labels in segmentation. |

---

## 📌 Project Structure
```
TISA/
│── tisa/                       # Main source code
│   ├── core/
│       ├── analysis.py         # Calculate label percentages
│       ├── mosaic.py           # Build mosaic and split images
│       ├── segmentation/
│           ├── automated.py    # Automated segmentation
│           ├── models_tf.py    # From PetroSeg
│   ├── icons/                  # Icons
│   ├── utils/                  # Utilities
│   ├── gui.py                  # Graphical User Interface (PyQt)
│   ├── main.py                 # Application entry point
│── docs/                       # Documentation
│   ├── index.md                # Main documentation page
│   ├── guide.md                # User guide
│   ├── segmentation.md         # Segmentation explanation
│── requirements.txt            # Dependency list
│── README.md                   # Quick project overview
```

---

## 📬 Contributing
If you'd like to contribute to **TISA**, feel free to:
- Report issues or suggest improvements via **GitHub Issues**.
- Contribute code by **forking the repository and submitting Pull Requests**.
- Share datasets to improve testing and segmentation capabilities.

---

## 🔗 Useful Resources
- 📜 [Complete User Guide](docs/guide.md)
- 🎓 [Image Segmentation Concepts](docs/segmentation.md)
- 📩 Contact: [maxime.soares-correia@universite-paris-saclay.fr](mailto:maxime.soares-correia@universite-paris-saclay.fr)

---

## 📄 License
TISA is distributed under the **GNU GPL v3 License**, meaning you are free to use, modify, and distribute it but it needs to be open-source.

---

## **📢 Final Words**
TISA is designed to make thin-section analysis faster and more intuitive. If you have any questions or suggestions, join our community!

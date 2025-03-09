# TISA - Thin-section Image Segmenter & Analyzer

🚀 **TISA** (Thin-section Image Segmenter & Analyzer) is an advanced tool for automated segmentation and analysis of petrographic thin sections. It enables efficient identification and classification of mineral grains using state-of-the-art segmentation algorithms.

---

## 📸 Key Features
- **🖥️ Modern GUI:** Built with `PyQt5` for an intuitive user experience.
- **🧩 Automated Segmentation:** Supports multiple segmentation techniques (`K-means`, `Deep Learning`).
- **🎨 Fixed Color Palette Mapping:** Ensures consistent label visualization across images.
- **🛠️ Automatic Artifact Removal:** Detects and removes thin-section edges and unwanted lighting effects.
- **📊 Data Export:** Saves segmented images and statistical analyses in `.csv` format.

---

## 🏗️ Installation

### **1️⃣ Prerequisites**
Ensure you have **Python 3.8+** installed. Then, install dependencies:
```bash
pip install -r requirements.txt
```

### **2️⃣ Running the Application**
To launch TISA’s graphical interface:
```bash
python -m tisa.main
```

---

## 📖 Documentation
For detailed usage instructions and advanced settings, check out the full documentation:

📚 [TISA Documentation](docs/index.md)

---

## ⚙️ Segmentation Methods

TISA provides multiple segmentation algorithms:
- **K-Means Clustering:** Groups pixels based on color similarity.
- **Deep Learning-Based Segmentation:** Uses CNNs for precise mineral identification.
- **Felzenszwalb Algorithm:** Graph-based segmentation suited for texture variations.

Each method is **adjustable through parameters** such as:
| Parameter        | Description |
|-----------------|------------|
| `mod_dim1`      | Number of filters in the first convolutional layer. |
| `mod_dim2`      | Number of filters in the second convolutional layer. |
| `train_epoch`   | Number of training iterations. |
| `max_label_num` | Maximum number of segmentation classes. |

---

## 📂 Project Structure
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

## 🏛️ Based on PetroSeg by Azzam et al.
TISA builds upon **PetroSeg**, originally developed by **Azzam et al.** 

Reference:
📄 *Azzam et al.,- Automated petrographic image analysis by supervised and* 
*unsupervised machine learning methods - 2024 - Sedimentologika*

---

## 📬 Contributing
If you’d like to contribute to **TISA**, feel free to:
- Report issues or suggest improvements via **GitHub Issues**.
- Contribute code by **forking the repository and submitting Pull Requests**.
- Share petrographic datasets to enhance segmentation capabilities.

---

## 📄 License
TISA is distributed under the **GNU GPL v3 License**, allowing free use, modification, and redistribution.

---

## **📢 Final Words**
TISA is designed to make thin-section analysis faster and more efficient. If you have any questions or suggestions, feel free to reach out! 🚀

# 👁️ MultiVision AI & Audio Intelligence Assistant

A comprehensive, modular AI suite developed in Python using Streamlit, combining cutting-edge deep learning models for various vision and audio intelligence tasks.

---

## 📌 Project Overview

This platform is a unified web application consisting of 6 distinct AI modules:
1. **Facial Emotion Recognition:** Predicts human emotions from facial expressions using CNNs.
2. **Animal Detection *(Upcoming)*:** Detects and classifies multiple animals using YOLO object detection.
3. **Car Color & Person Detection *(Upcoming)*:** Identifies cars, classifies their colors via CNN, and detects people using YOLO.
4. **Voice Emotion Recognition *(Upcoming)*:** Predicts emotions from speech using audio features.
5. **Sign Language Recognition *(Upcoming)*:** Classifies specific ASL words using sequence modeling.
6. **Drowsiness & Age Estimation *(Upcoming)*:** Detects sleep/fatigue via Eye Aspect Ratio (EAR) and estimates age.

---

## 🗂️ Folder Structure

The project strictly follows a scalable, modular software engineering architecture:

```
MultiVision-AI-Assistant/
├── app.py                     # Main Streamlit multipage entry point
├── config.py                  # Global settings and hyperparameters
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── notebooks/                 # Jupyter notebooks for model training and fine-tuning
├── reports/                   # Performance metrics, confusion matrices, and plots
└── modules/                   # Self-contained logic for each ML task
    ├── emotion/               # (Completed) Facial Emotion module
    ├── animal/                # (In Progress)
    ├── car/                   # (In Progress)
    ├── voice/                 # (In Progress)
    ├── sign/                  # (In Progress)
    ├── drowsiness/            # (In Progress)
    └── nationality/           # (In Progress)
```

Each module contains its own isolated inference (`predict.py`), UI (`page.py`), and `weights/` directory for maximum maintainability.

---

## ⚙️ Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/swayamworks/facial-emotion-recog.git
cd facial-emotion-recog
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 🚀 Models Used & Datasets

*(This section is updated iteratively as modules are completed)*

| Module | Dataset | Model Architecture | Status |
|---|---|---|---|
| **Facial Emotion** | RAF-DB | CNN | ✅ Complete |
| **Animal Detection** | COCO / Animals-10 | YOLOv8 | 🔄 Pending |
| **Car Color** | Vehicle Color Dataset | YOLOv8 + CNN | 🔄 Pending |
| **Voice Emotion** | RAVDESS / TESS | RF + MFCC (or Wav2Vec2) | 🔄 Pending |
| **Sign Language** | WLASL (Filtered) | MediaPipe + LSTM | 🔄 Pending |
| **Drowsiness & Age**| MRL Eye / UTKFace | MediaPipe + DeepFace | 🔄 Pending |

---

## 📊 Training Process & Results

All training notebooks can be found in the `notebooks/` directory. 
Performance metrics, loss curves, and screenshots for each completed module are archived in the `reports/` folder.

---

## 👤 Developed by

**Swayam Netke**

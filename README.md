# 😊 Facial Emotion Recognition using Deep Learning

A modern, professional **Streamlit** web application that predicts human facial emotions
from uploaded images using a **Convolutional Neural Network (CNN)** trained on the
**RAF-DB (Real-world Affective Faces Database)** dataset.

---

## 📌 Project Overview

- **Dataset:** RAF-DB
- **Model:** CNN (Baseline) — `emotion_cnn_baseline.keras`
- **Input:** RGB images, resized to 100x100, normalized to [0, 1]
- **Output Classes:** `surprise`, `fear`, `disgust`, `happy`, `sad`, `angry`, `neutral`
- **Framework:** TensorFlow (Keras) + Streamlit

---

## 🗂️ Project Structure

```
emotion_recognition_app/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── emotion_cnn_baseline.keras # Trained model (add this file yourself)
```

> ⚠️ **Important:** The trained model file `emotion_cnn_baseline.keras` is **not included**
> in this package. Place your trained model file in the same directory as `app.py`
> before running the app.

---

## ⚙️ Local Setup & Installation

### 1. Clone or copy the project files
Make sure `app.py`, `requirements.txt`, and `emotion_cnn_baseline.keras` are in the
same folder.

### 2. Create a virtual environment (recommended)
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

## ☁️ Deployment Instructions

### Option 1: Streamlit Community Cloud (Free & Easiest)
1. Push your project (including `emotion_cnn_baseline.keras`) to a **GitHub repository**.
   - If the model file is large (>100 MB), use [Git LFS](https://git-lfs.com/).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"**, select your repository, branch, and set the main file path to
   `app.py`.
4. Click **Deploy**. Streamlit Cloud will automatically install dependencies from
   `requirements.txt`.

### Option 2: Hugging Face Spaces
1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space).
2. Choose **Streamlit** as the Space SDK.
3. Upload `app.py`, `requirements.txt`, and `emotion_cnn_baseline.keras`.
4. The Space will build and launch automatically.

### Option 3: Docker
Create a `Dockerfile` in the project root:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Then build and run:
```bash
docker build -t emotion-recognition-app .
docker run -p 8501:8501 emotion-recognition-app
```

### Option 4: Cloud VM (AWS EC2 / GCP / Azure)
1. Provision a VM and install Python 3.10+.
2. Copy project files to the VM.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run with a process manager (e.g., `tmux`, `screen`, or `systemd`):
   ```bash
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```
5. Open port `8501` in your firewall/security group settings.

---

## 🧠 How It Works

1. **Upload** — User uploads a JPG, JPEG, or PNG facial image.
2. **Preprocess** — Image is converted to RGB, resized to 100x100, normalized (÷255.0),
   and a batch dimension is added.
3. **Predict** — The cached CNN model runs inference and returns a probability
   distribution across the seven emotion classes.
4. **Display** — The app shows the predicted emotion, confidence percentage, and a
   horizontal confidence bar for all classes.

---

## 🛠️ Troubleshooting

| Issue | Solution |
|---|---|
| `Failed to load model` error | Ensure `emotion_cnn_baseline.keras` is in the same directory as `app.py`. |
| Invalid image error | Upload a valid `.jpg`, `.jpeg`, or `.png` file. |
| Slow first prediction | This is normal — TensorFlow initializes on first run. Subsequent predictions are faster due to model caching. |
| Model/TensorFlow version mismatch | Re-save the model using the same TensorFlow version listed in `requirements.txt`. |

---

## 👤 Developed by

**Swayam Netke**

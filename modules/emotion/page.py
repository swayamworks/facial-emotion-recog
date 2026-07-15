import os
import streamlit as st
import numpy as np
from PIL import Image, UnidentifiedImageError
from modules.emotion.predict import (
    load_model,
    preprocess_image,
    predict_emotion,
    CLASS_NAMES,
)

EMOTION_EMOJIS = {
    "surprise": "😲",
    "fear": "😨",
    "disgust": "🤢",
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}

# The model path is now relative to this module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "weights", "emotion_cnn_baseline.keras")

@st.cache_resource(show_spinner="Loading emotion recognition model...")
def get_model():
    try:
        return load_model(MODEL_PATH)
    except Exception as e:
        st.error(str(e))
        return None

def render_sidebar(model):
    _, h, w, _ = model.input_shape
    with st.sidebar:
        st.header("📌 Module Overview")
        st.markdown(
            "This application uses a **Convolutional Neural Network (CNN)** to recognize facial emotions."
        )
        st.subheader("⚙️ Technical Details")
        st.markdown(
            f"""
- 📂 Dataset: RAF-DB
- 🧠 Model: CNN
- 🖼️ Input Size: **{w} × {h} RGB**
"""
        )
        st.subheader("🎭 Emotion Classes")
        st.markdown(", ".join(f"{EMOTION_EMOJIS[c]} {c.capitalize()}" for c in CLASS_NAMES))
        st.markdown("---")
        st.caption("Upload a clear front-facing facial image.")

def render_confidence_chart(probabilities):
    st.subheader("📊 Confidence Scores")
    order = np.argsort(probabilities)[::-1]
    for idx in order:
        emotion = CLASS_NAMES[idx]
        prob = float(probabilities[idx])
        st.write(f"{EMOTION_EMOJIS[emotion]} **{emotion.capitalize()}** — {prob*100:.2f}%")
        st.progress(prob)

def render_page():
    st.title("😊 Facial Emotion Recognition")
    st.write("Upload a face image and the CNN will predict the person's emotion.")

    model = get_model()
    if model is None:
        st.stop()

    render_sidebar(model)
    st.success(f"Model Input Shape: {model.input_shape}")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is None:
        st.info("Upload an image to begin.")
        return

    try:
        image = Image.open(uploaded_file)
    except UnidentifiedImageError:
        st.error("Invalid image.")
        return
    except Exception as e:
        st.error(e)
        return

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, use_container_width=True)

    try:
        processed = preprocess_image(image, model)
        emotion, confidence, probs = predict_emotion(model, processed)
    except Exception as e:
        st.error(f"Prediction failed.\n\n{e}")
        return

    with col2:
        st.success(f"{EMOTION_EMOJIS[emotion]} **{emotion.capitalize()}**")
        st.info(f"Confidence: **{confidence:.2f}%**")

    st.divider()
    render_confidence_chart(probs)
    st.divider()
    st.caption("Developed by Swayam Netke")

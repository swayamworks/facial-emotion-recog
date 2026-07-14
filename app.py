"""
Facial Emotion Recognition using Deep Learning
------------------------------------------------
A Streamlit web application that uses a CNN trained on the RAF-DB dataset
to predict human facial emotions from uploaded images.

Author: Swayam Netke
"""

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

# =========================================================
# 1. APP CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Facial Emotion Recognition",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="expanded",
)

MODEL_PATH = "emotion_cnn_baseline.keras"

CLASS_NAMES = [
    "surprise",
    "fear",
    "disgust",
    "happy",
    "sad",
    "angry",
    "neutral",
]

EMOTION_EMOJIS = {
    "surprise": "😲",
    "fear": "😨",
    "disgust": "🤢",
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}


# =========================================================
# 2. MODEL LOADING
# =========================================================
@st.cache_resource(show_spinner="Loading emotion recognition model...")
def load_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model.\n\n{e}")
        return None


# =========================================================
# 3. IMAGE PREPROCESSING
# =========================================================
def preprocess_image(image: Image.Image, model):
    """
    Automatically resizes the image to whatever size
    the loaded model expects.
    """
    _, height, width, channels = model.input_shape

    image = image.convert("RGB")
    image = image.resize((width, height))

    img = np.array(image, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    return img


# =========================================================
# 4. PREDICTION
# =========================================================
def predict_emotion(model, image):

    prediction = model.predict(image, verbose=0)[0]

    idx = np.argmax(prediction)

    emotion = CLASS_NAMES[idx]
    confidence = float(prediction[idx]) * 100

    return emotion, confidence, prediction


# =========================================================
# 5. SIDEBAR
# =========================================================
def render_sidebar(model):

    _, h, w, _ = model.input_shape

    with st.sidebar:

        st.header("📌 Project Overview")

        st.markdown(
            """
This application uses a **Convolutional Neural Network (CNN)** to recognize facial emotions.
"""
        )

        st.subheader("⚙️ Technical Details")

        st.markdown(
            f"""
- 📂 Dataset: RAF-DB
- 🧠 Model: CNN
- 🖼️ Input Size: **{w} × {h} RGB**
- 🛠️ Framework: TensorFlow + Streamlit
"""
        )

        st.subheader("🎭 Emotion Classes")

        st.markdown(
            ", ".join(
                f"{EMOTION_EMOJIS[c]} {c.capitalize()}" for c in CLASS_NAMES
            )
        )

        st.markdown("---")
        st.caption("Upload a clear front-facing facial image.")


# =========================================================
# 6. CONFIDENCE CHART
# =========================================================
def render_confidence_chart(probabilities):

    st.subheader("📊 Confidence Scores")

    order = np.argsort(probabilities)[::-1]

    for idx in order:

        emotion = CLASS_NAMES[idx]
        prob = float(probabilities[idx])

        st.write(
            f"{EMOTION_EMOJIS[emotion]} **{emotion.capitalize()}** — {prob*100:.2f}%"
        )

        st.progress(prob)


# =========================================================
# 7. MAIN
# =========================================================
def main():

    st.title("😊 Facial Emotion Recognition")

    st.write(
        """
Upload a face image and the CNN will predict the person's emotion.
"""
    )

    model = load_model(MODEL_PATH)

    if model is None:
        st.stop()

    render_sidebar(model)

    st.success(f"Model Input Shape: {model.input_shape}")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"],
    )

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

        emotion, confidence, probs = predict_emotion(
            model,
            processed,
        )

    except Exception as e:

        st.error(f"Prediction failed.\n\n{e}")

        return

    with col2:

        st.success(
            f"{EMOTION_EMOJIS[emotion]} **{emotion.capitalize()}**"
        )

        st.info(f"Confidence: **{confidence:.2f}%**")

    st.divider()

    render_confidence_chart(probs)

    st.divider()

    st.caption("Developed by Swayam Netke")


if __name__ == "__main__":
    main()
import os
import time
import streamlit as st
import numpy as np
from PIL import Image, UnidentifiedImageError
from modules.emotion.predict import (
    load_model,
    preprocess_image,
    predict_emotion,
    CLASS_NAMES,
)
from ui_components import (
    render_hero,
    render_empty_state,
    render_result_card,
    render_model_info,
    render_inference_time,
    render_footer,
    ACCENT_COLORS,
)

ACCENT = ACCENT_COLORS["emotion"]

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


def render_page():
    render_hero("😊", "Facial Emotion Recognition", "Predict human emotions from facial expressions using a CNN.")

    model = get_model()
    if model is None:
        st.stop()

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is None:
        render_empty_state("📸", "Upload a face image to begin analysis", "JPG · JPEG · PNG")
        # Model info
        st.markdown("")
        with st.expander("📋 Model Information"):
            render_model_info([
                {"label": "Model", "value": "CNN"},
                {"label": "Dataset", "value": "RAF-DB"},
                {"label": "Input Size", "value": f"{model.input_shape[2]}×{model.input_shape[1]} RGB"},
                {"label": "Classes", "value": str(len(CLASS_NAMES))},
            ])
        render_footer()
        return

    try:
        image = Image.open(uploaded_file)
    except UnidentifiedImageError:
        st.error("Invalid image file.")
        return
    except Exception as e:
        st.error(f"Error opening image: {e}")
        return

    # Run prediction with timing
    start = time.time()
    try:
        processed = preprocess_image(image, model)
        emotion, confidence, probs = predict_emotion(model, processed)
    except Exception as e:
        st.error(f"Prediction failed.\n\n{e}")
        return
    elapsed = time.time() - start

    # Results
    col_img, col_result = st.columns([1, 1], gap="large")

    with col_img:
        st.image(image, use_container_width=True)

    with col_result:
        render_result_card("Emotion", f"{EMOTION_EMOJIS.get(emotion, '')} {emotion.capitalize()}", confidence, ACCENT)
        st.markdown("")
        render_inference_time(elapsed)

    # Confidence breakdown
    st.markdown("")
    st.markdown("##### All Emotions")
    order = np.argsort(probs)[::-1]
    for idx in order:
        em = CLASS_NAMES[idx]
        prob = float(probs[idx])
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(prob, text=f"{EMOTION_EMOJIS.get(em, '')} {em.capitalize()}")
        with col2:
            st.markdown(f"**{prob*100:.1f}%**")

    # Technical details
    with st.expander("🔧 Technical Details"):
        render_model_info([
            {"label": "Predicted", "value": emotion.capitalize()},
            {"label": "Confidence", "value": f"{confidence:.1f}%"},
            {"label": "Model", "value": "CNN"},
            {"label": "Input Shape", "value": str(model.input_shape)},
        ])

    render_footer()

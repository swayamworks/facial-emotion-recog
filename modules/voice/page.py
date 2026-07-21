import streamlit as st
import tempfile
import os
import time

from modules.voice.predictor import VoicePredictor
from ui_components import (
    render_hero,
    render_empty_state,
    render_result_card,
    render_warning_card,
    render_model_info,
    render_inference_time,
    render_footer,
    ACCENT_COLORS,
)

ACCENT = ACCENT_COLORS["voice"]


@st.cache_resource(show_spinner="Loading voice recognition models...")
def get_predictor():
    """Load all voice models once and cache them."""
    try:
        return VoicePredictor()
    except Exception as e:
        st.error(f"Failed to load voice models: {e}")
        return None


def render_page():
    render_hero("🎤", "Speech Emotion Recognition", "Detect speaker gender and emotional state from speech.")

    predictor = get_predictor()
    if predictor is None:
        st.stop()

    uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"], label_visibility="collapsed")

    if uploaded_file is None:
        render_empty_state("🎵", "Upload an audio file to begin analysis", "WAV")
        with st.expander("📋 Model Information"):
            render_model_info([
                {"label": "Gender Classifier", "value": "Random Forest"},
                {"label": "Emotion Classifier", "value": "XGBoost"},
                {"label": "Features", "value": "MFCC + Chroma + Mel"},
                {"label": "Dataset", "value": "RAVDESS"},
            ])
        render_footer()
        return

    # Audio player
    st.audio(uploaded_file, format="audio/wav")

    # Save to temp file for librosa
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        temp_path = tmp.name
        tmp.write(uploaded_file.getbuffer())

    # Progress steps
    progress_area = st.empty()
    start = time.time()

    try:
        progress_area.markdown("⏳ Extracting audio features...")
        result = predictor.predict(temp_path)
        elapsed = time.time() - start
        progress_area.markdown("✅ Analysis complete")
    except Exception as e:
        progress_area.empty()
        st.error(f"Prediction failed.\n\n{e}")
        return
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    time.sleep(0.3)  # Brief pause so user sees the completion message
    progress_area.empty()

    # =====================================
    # Results
    # =====================================

    if result["gender"] == "Male":
        render_warning_card(
            "Male speaker detected",
            "This module currently supports emotion prediction for female voices only."
        )
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            render_result_card("Gender", "Male", result["gender_confidence"], ACCENT)
        with col2:
            render_result_card("Emotion", "—", accent_color=ACCENT)
        render_inference_time(elapsed)
        render_footer()
        return

    # Female voice — show full results
    col1, col2 = st.columns(2)
    with col1:
        render_result_card("Gender", "Female", result["gender_confidence"], ACCENT)
    with col2:
        render_result_card("Emotion", f"{result['emotion']}", result["emotion_confidence"], ACCENT)

    render_inference_time(elapsed)

    # Technical details
    with st.expander("🔧 Technical Details"):
        details = [
            {"label": "Gender", "value": result["gender"]},
            {"label": "Gender Conf.", "value": f"{result['gender_confidence']}%"},
            {"label": "Emotion", "value": result["emotion"] or "—"},
        ]
        if result["emotion_confidence"]:
            details.append({"label": "Emotion Conf.", "value": f"{result['emotion_confidence']}%"})
        details.append({"label": "Feature Count", "value": "262"})
        details.append({"label": "Inference", "value": f"{elapsed:.2f}s"})
        render_model_info(details)

    render_footer()

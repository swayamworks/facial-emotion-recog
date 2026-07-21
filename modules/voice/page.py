import streamlit as st
import tempfile
import os

from modules.voice.predictor import VoicePredictor


@st.cache_resource(show_spinner="Loading voice recognition models...")
def get_predictor():
    """Load all voice models once and cache them."""
    try:
        return VoicePredictor()
    except Exception as e:
        st.error(f"Failed to load voice models: {e}")
        return None


def render_page():
    st.title("🎙️ Voice Emotion Recognition")
    st.markdown(
        "Detects gender and emotion from speech using a deep learning "
        "feature extraction pipeline and machine learning classifiers."
    )

    predictor = get_predictor()
    if predictor is None:
        st.stop()

    uploaded_file = st.file_uploader(
        "Upload a WAV audio file",
        type=["wav"],
        help="Only .wav files are supported."
    )

    if uploaded_file is None:
        st.info("📤 Upload a .wav audio file to begin.")
        return

    # Audio player
    st.audio(uploaded_file, format="audio/wav")

    # Save to temp file for librosa
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        temp_path = tmp.name
        tmp.write(uploaded_file.getbuffer())

    with st.spinner("🔍 Analyzing voice..."):
        try:
            result = predictor.predict(temp_path)
        except Exception as e:
            st.error(f"Prediction failed.\n\n{e}")
            return
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # =====================================
    # Display Results
    # =====================================

    if result["gender"] == "Male":
        st.warning("❌ Please upload a female voice.")
        st.metric("🧑 Gender", result["gender"])
        st.caption(f"Gender Confidence: {result['gender_confidence']}%")
        return

    # Female voice — show full results
    st.success("✅ Analysis Complete")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🧑 Gender", result["gender"])
        st.caption(f"Confidence: {result['gender_confidence']}%")

    with col2:
        st.metric("🎭 Emotion", result["emotion"])
        st.caption(f"Confidence: {result['emotion_confidence']}%")

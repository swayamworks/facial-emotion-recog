import streamlit as st
from ui_components import (
    inject_global_css,
    render_module_card,
    render_footer,
    render_tech_stack,
    ACCENT_COLORS,
)

# =============================================
# Page Config
# =============================================

st.set_page_config(
    page_title="MultiVision AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# =============================================
# Module Definitions
# =============================================

MODULES = [
    {
        "key": "Facial Emotion",
        "icon": "😊",
        "title": "Facial Emotion",
        "desc": "Predict facial expressions using CNNs.",
        "accent": ACCENT_COLORS["emotion"],
    },
    {
        "key": "Animal Detection",
        "icon": "🐾",
        "title": "Animal Detection",
        "desc": "Detect 80 animal species with YOLOv8.",
        "accent": ACCENT_COLORS["animal"],
    },
    {
        "key": "Vehicle Color Detection",
        "icon": "🚗",
        "title": "Vehicle Color Detection",
        "desc": "Detect cars and highlight blue vehicles.",
        "accent": ACCENT_COLORS["car"],
    },
    {
        "key": "Speech Emotion Recognition",
        "icon": "🎤",
        "title": "Speech Emotion Recognition",
        "desc": "Detect speaker gender and emotion.",
        "accent": ACCENT_COLORS["voice"],
    },
    {
        "key": "Sign Language",
        "icon": "🤟",
        "title": "Sign Language",
        "desc": "Coming soon.",
        "accent": ACCENT_COLORS["sign"],
    },
    {
        "key": "Drowsiness & Age",
        "icon": "😴",
        "title": "Drowsiness & Age",
        "desc": "Coming soon.",
        "accent": ACCENT_COLORS["drowsiness"],
    },
]

# =============================================
# Sidebar
# =============================================

SIDEBAR_ITEMS = [
    ("🏠", "Home"),
    ("😊", "Facial Emotion"),
    ("🐾", "Animal Detection"),
    ("🚗", "Vehicle Color Detection"),
    ("🎤", "Speech Emotion Recognition"),
    ("🤟", "Sign Language"),
    ("😴", "Drowsiness & Age"),
]

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.markdown("### 👁️ MultiVision AI")
    st.markdown("---")
    for icon, label in SIDEBAR_ITEMS:
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if st.session_state.page == label else "secondary",
        ):
            st.session_state.page = label
            st.rerun()


# =============================================
# Homepage
# =============================================

def render_home():
    st.markdown("")  # spacing

    # Hero
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div style="font-size: 2rem; font-weight: 700; color: #f1f5f9;">
            MultiVision AI
        </div>
        <div style="font-size: 1rem; color: #94a3b8; font-weight: 300; margin-top: 0.25rem; max-width: 500px; margin-left: auto; margin-right: auto;">
            Analyze images, video and speech using multiple AI models from one unified interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")  # spacing

    # Module cards — 3 per row
    rows = [MODULES[i:i+3] for i in range(0, len(MODULES), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, mod in zip(cols, row):
            with col:
                render_module_card(mod["icon"], mod["title"], mod["desc"])
                if st.button(
                    "Open →",
                    key=f"card_{mod['key']}",
                    use_container_width=True,
                ):
                    st.session_state.page = mod["key"]
                    st.rerun()

    # Tech Stack
    st.markdown("")
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem;">
        <div style="font-size: 0.75rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">
            Powered By
        </div>
    </div>
    """, unsafe_allow_html=True)
    render_tech_stack(["YOLOv8", "TensorFlow", "OpenCV", "XGBoost", "Streamlit", "Librosa"])

    render_footer()


# =============================================
# Routing
# =============================================

def main():
    page = st.session_state.page

    if page == "Home":
        render_home()
    elif page == "Facial Emotion":
        # Lazy import — TensorFlow only loads when user clicks this tab
        from modules.emotion.page import render_page as render_emotion_page
        render_emotion_page()
    elif page == "Animal Detection":
        # Lazy import — YOLO/OpenCV only loads when user clicks this tab
        from modules.animal.page import render_page as render_animal_page
        render_animal_page()
    elif page == "Vehicle Color Detection":
        # Lazy import — YOLO/OpenCV only loads when user clicks this tab
        from modules.car.page import render_page as render_car_page
        render_car_page()
    elif page == "Speech Emotion Recognition":
        # Lazy import — librosa/sklearn only loads when user clicks this tab
        from modules.voice.page import render_page as render_voice_page
        render_voice_page()
    else:
        st.markdown("")
        st.markdown(f"""
        <div style="text-align: center; padding: 3rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🚧</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #e2e8f0;">{page}</div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 0.25rem;">This module is currently under development.</div>
        </div>
        """, unsafe_allow_html=True)
        render_footer()

if __name__ == "__main__":
    main()
import streamlit as st

# Setup page config once at the top level
st.set_page_config(
    page_title="MultiVision AI Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import the module pages
from modules.emotion.page import render_page as render_emotion_page

def render_home():
    st.title("👁️ MultiVision AI Assistant")
    st.markdown("### Welcome to the comprehensive AI Vision & Audio Intelligence Platform")
    st.write(
        "This platform is designed to house multiple state-of-the-art AI modules. "
        "Use the sidebar to navigate between different functionalities."
    )
    
    st.info(
        "**Available Modules:**\n"
        "- 🎭 **Emotion Detector:** Predicts human emotions from facial expressions using CNNs.\n"
        "- *(More modules coming soon)*"
    )

def main():
    st.sidebar.title("Navigation")
    
    # Simple navigation state
    page = st.sidebar.radio(
        "Select Module:",
        ["Home", "Facial Emotion", "Animal Detection", "Car Color", "Voice Emotion", "Sign Language", "Drowsiness & Age"]
    )
    
    if page == "Home":
        render_home()
    elif page == "Facial Emotion":
        render_emotion_page()
    else:
        st.title(page)
        st.warning(f"The {page} module is currently under development! Please check back later.")

if __name__ == "__main__":
    main()
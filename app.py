import streamlit as st

# Setup page config once at the top level
st.set_page_config(
    page_title="MultiVision AI Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        "- 🐾 **Animal Detection:** Detects 80 animal species using a custom-trained YOLOv8 model.\n"
        "- 🚗 **Car Color:** Detects cars and people, highlighting blue cars using YOLOv8.\n"
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
        # Lazy import — TensorFlow only loads when user clicks this tab
        from modules.emotion.page import render_page as render_emotion_page
        render_emotion_page()
    elif page == "Animal Detection":
        # Lazy import — YOLO/OpenCV only loads when user clicks this tab
        from modules.animal.page import render_page as render_animal_page
        render_animal_page()
    elif page == "Car Color":
        # Lazy import — YOLO/OpenCV only loads when user clicks this tab
        from modules.car.page import render_page as render_car_page
        render_car_page()
    else:
        st.title(page)
        st.warning(f"The {page} module is currently under development! Please check back later.")

if __name__ == "__main__":
    main()
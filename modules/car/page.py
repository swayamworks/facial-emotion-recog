import streamlit as st
import numpy as np
from PIL import Image, UnidentifiedImageError
from modules.car.predict import detect_car_colors
import cv2

def render_sidebar():
    with st.sidebar:
        st.header("📌 Module Overview")
        st.markdown(
            "This application uses **YOLOv8** to detect cars and people, "
            "and uses **HSV Color Masking** to determine if a car is blue."
        )
        st.subheader("⚙️ Technical Details")
        st.markdown(
            """
- 📂 Dataset: COCO (Pretrained)
- 🧠 Model: YOLOv8 Nano
- 🎨 Color Mask: OpenCV HSV
"""
        )
        st.subheader("🖍️ Bounding Boxes")
        st.markdown(
            """
- 🟥 **Red Box:** Blue Cars
- 🟦 **Blue Box:** Other Cars
- 🟩 **Green Box:** People
"""
        )
        st.markdown("---")
        st.caption("Upload an image of a street or parking lot.")

def render_page():
    st.title("🚗 Car Color & Person Detection")
    st.write("Upload an image to detect cars and people, and specifically highlight blue cars.")

    render_sidebar()

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is None:
        st.info("Upload an image to begin.")
        return

    try:
        # Load image with PIL
        pil_image = Image.open(uploaded_file)
        # Convert to numpy array (RGB)
        image_rgb = np.array(pil_image.convert("RGB"))
    except UnidentifiedImageError:
        st.error("Invalid image.")
        return
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return

    with st.spinner("Running YOLOv8 Object Detection..."):
        try:
            annotated_image_rgb, car_count, person_count = detect_car_colors(image_rgb)
        except Exception as e:
            st.error(f"Prediction failed.\n\n{e}")
            return

    # Display metrics
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(label="🚗 Cars Detected", value=car_count)
    with col_m2:
        st.metric(label="🚶 People Detected", value=person_count)

    st.divider()

    # Display images side by side
    st.subheader("Detection Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Original Image**")
        st.image(image_rgb, use_container_width=True)

    with col2:
        st.write("**Annotated Output**")
        st.image(annotated_image_rgb, use_container_width=True)

    st.divider()
    st.caption("Developed by Swayam Netke")

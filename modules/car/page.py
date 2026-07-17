import streamlit as st
import tempfile
import os
from pathlib import Path
from PIL import Image

# Import the user's EXACT original detector code
from modules.car.detector import process_image

def show_page():
    st.title("Car Detection Module")
    st.markdown("Upload an image to detect cars and people.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        
        # Save the uploaded file to disk so OpenCV can read it exactly like in the terminal
        temp_input = Path("temp_input.jpg")
        temp_output = Path("temp_output.jpg")
        
        with open(temp_input, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="Original Image", use_container_width=True)

        with st.spinner("Running exact terminal detector.py logic..."):
            try:
                # Run the exact original logic from detector.py
                car_count, person_count = process_image(temp_input, temp_output)
                
                st.success("Detection complete!")
                
                # Load the output image written by cv2.imwrite
                output_image = Image.open(temp_output)
                
                st.image(output_image, caption="Annotated Image", use_container_width=True)

                st.subheader("Results")
                col1, col2 = st.columns(2)
                col1.metric("Cars Detected", car_count)
                col2.metric("People Detected", person_count)
                
            except Exception as e:
                st.error(f"Detection failed.\n\n{e}")

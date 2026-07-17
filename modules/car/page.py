import streamlit as st
import tempfile
import os
from pathlib import Path
from PIL import Image

# Import the user's EXACT original detector code
from modules.car.detector import process_image

def render_page():
    st.title("Car Detection Module")
    st.markdown("Upload an image to detect cars and people.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        
        # Create unique temporary files that automatically clean themselves up
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_in, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_out:
            
            temp_input = tmp_in.name
            temp_output = tmp_out.name
            
            tmp_in.write(uploaded_file.getbuffer())

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
                
            finally:
                # Always clean up the files so the server doesn't run out of disk space
                if os.path.exists(temp_input):
                    os.remove(temp_input)
                if os.path.exists(temp_output):
                    os.remove(temp_output)

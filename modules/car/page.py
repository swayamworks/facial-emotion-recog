import streamlit as st
import tempfile
import os
import time
from pathlib import Path
from PIL import Image

# Import the user's EXACT original detector code
from modules.car.detector import process_image
from ui_components import (
    render_hero,
    render_empty_state,
    render_result_card,
    render_model_info,
    render_inference_time,
    render_footer,
    ACCENT_COLORS,
    upload_card,
    close_upload_card,
    render_progress_steps,
    render_workflow_summary,
)

ACCENT = ACCENT_COLORS["car"]


def render_page():
    render_hero("🚗", "Vehicle Color Detection", "Detect cars and people, highlighting blue vehicles using YOLOv8.")

    render_workflow_summary("A focused road-scene analyser that detects cars and people, then identifies blue vehicles through HSV colour analysis.", ["Image input", "YOLOv8n", "COCO classes", "HSV colour analysis"])
    upload_card("Upload an image", "JPG · JPEG · PNG", "🚗")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    close_upload_card()

    if uploaded_file is None:
        render_empty_state("🖼️", "Upload an image to begin detection", "JPG · JPEG · PNG")
        with st.expander("📋 Model Information"):
            render_model_info([
                {"label": "Model", "value": "YOLOv8n"},
                {"label": "Dataset", "value": "COCO"},
                {"label": "Task", "value": "Object Detection"},
                {"label": "Color", "value": "HSV Analysis"},
            ])
        render_footer()
        return

    # Create unique temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_in, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_out:
        temp_input = tmp_in.name
        temp_output = tmp_out.name
        tmp_in.write(uploaded_file.getbuffer())

    start = time.time()
    with st.spinner("Running detection..."):
        try:
            # Run the exact original logic from detector.py
            car_count, person_count = process_image(temp_input, temp_output)
            elapsed = time.time() - start
            render_progress_steps([("Objects detected", True), ("Vehicle color analysis complete", True)])

            # Display images side by side
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                st.image(uploaded_file, caption="Original", use_container_width=True)
            with col2:
                output_image = Image.open(temp_output)
                st.image(output_image, caption="Detected", use_container_width=True)

            # Results
            st.markdown("")
            r1, r2, r3 = st.columns(3)
            with r1:
                render_result_card("Cars Detected", str(car_count))
            with r2:
                render_result_card("People Detected", str(person_count))
            with r3:
                render_result_card("Total Objects", str(car_count + person_count))

            render_inference_time(elapsed)

            # Technical details
            with st.expander("🔧 Technical Details"):
                render_model_info([
                    {"label": "Cars", "value": str(car_count)},
                    {"label": "People", "value": str(person_count)},
                    {"label": "Model", "value": "YOLOv8n"},
                    {"label": "Inference", "value": f"{elapsed:.2f}s"},
                ])

        except Exception as e:
            st.error(f"Detection failed.\n\n{e}")

        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if os.path.exists(temp_output):
                os.remove(temp_output)

    render_footer()

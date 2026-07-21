import streamlit as st
import tempfile
import os
import time
from pathlib import Path
from PIL import Image

# Import the animal detector
from modules.animal.detector import process_image
from ui_components import (
    render_hero,
    render_empty_state,
    render_result_card,
    render_model_info,
    render_inference_time,
    render_footer,
    ACCENT_COLORS,
)

ACCENT = ACCENT_COLORS["animal"]


def render_page():
    render_hero("🐾", "Animal Detection", "Detect 80 animal species using a custom-trained YOLOv8 model.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is None:
        render_empty_state("🖼️", "Upload an image to begin detection", "JPG · JPEG · PNG")
        with st.expander("📋 Model Information"):
            render_model_info([
                {"label": "Model", "value": "YOLOv8 (Custom)"},
                {"label": "Classes", "value": "80 Species"},
                {"label": "Training", "value": "10 Epochs"},
                {"label": "Input Size", "value": "416×416"},
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
    with st.spinner("Running animal detection..."):
        try:
            animal_counts = process_image(temp_input, temp_output)
            elapsed = time.time() - start

            # Display images side by side
            col1, col2 = st.columns(2, gap="medium")
            with col1:
                st.image(uploaded_file, caption="Original", use_container_width=True)
            with col2:
                output_image = Image.open(temp_output)
                st.image(output_image, caption="Detected", use_container_width=True)

            # Results
            st.markdown("")
            if animal_counts:
                total = sum(animal_counts.values())
                cols = st.columns(min(len(animal_counts) + 1, 4))
                with cols[0]:
                    render_result_card("Total Detected", str(total))
                for i, (animal, count) in enumerate(sorted(animal_counts.items())):
                    with cols[(i + 1) % len(cols)]:
                        render_result_card(animal, str(count))
            else:
                render_empty_state("🔍", "No animals detected in this image", "")

            render_inference_time(elapsed)

            # Technical details
            with st.expander("🔧 Technical Details"):
                details = [{"label": "Model", "value": "YOLOv8 (Custom)"}]
                if animal_counts:
                    details.append({"label": "Species Found", "value": str(len(animal_counts))})
                    details.append({"label": "Total Objects", "value": str(sum(animal_counts.values()))})
                details.append({"label": "Inference", "value": f"{elapsed:.2f}s"})
                render_model_info(details)

        except Exception as e:
            st.error(f"Detection failed.\n\n{e}")

        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if os.path.exists(temp_output):
                os.remove(temp_output)

    render_footer()

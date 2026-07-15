import os

# ==========================================
# MULTIVISION AI ASSISTANT CONFIGURATION
# ==========================================

# 1. Global Settings
USE_GPU = True
DEVICE = "cuda" if USE_GPU else "cpu"

# 2. Object Detection & Inference Settings
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# 3. Image Preprocessing
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

# 4. Global Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

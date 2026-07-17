from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

# Load YOLO model globally so it isn't reloaded on every inference
model = YOLO("yolov8n.pt")

def is_blue_car(car_image):
    """
    Determines if a cropped car image is primarily blue using HSV color masking.
    """
    if car_image.size == 0:
        return False

    # Convert RGB to HSV
    hsv = cv2.cvtColor(car_image, cv2.COLOR_RGB2HSV)

    # Define range of blue color in HSV (lowered saturation to catch dull/shadowy blue cars)
    lower_blue = (100, 30, 40)
    upper_blue = (140, 255, 255)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    blue_pixels = cv2.countNonZero(mask)
    total_pixels = car_image.shape[0] * car_image.shape[1]

    if total_pixels == 0:
        return False

    blue_ratio = blue_pixels / total_pixels

    return blue_ratio > 0.10


def create_box(image, x1, y1, x2, y2, color):
    """
    Draws a bounding box on the image.
    """
    cv2.rectangle(
        image,
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        color,
        2
    )


def detect_car_colors(image: np.ndarray):
    """
    Runs YOLOv8 object detection on an image.
    Returns the annotated image, the number of cars, and the number of people.
    
    Args:
        image: A numpy array representing an RGB or BGR image.
    Returns:
        tuple: (annotated_image, car_count, person_count)
    """
    # Make a copy so we don't modify the original reference
    annotated_image = image.copy()
    
    # Run YOLO inference
    results = model(annotated_image)
    result = results[0]

    car_count = 0
    person_count = 0

    # Iterate through all detected bounding boxes
    for box in result.boxes:
        class_id = int(box.cls[0])
        x1, y1, x2, y2 = box.xyxy[0]

        # 0 corresponds to 'person' in COCO dataset
        if class_id == 0:
            person_count += 1
            # Draw green box for people (BGR format: 0,255,0)
            create_box(annotated_image, x1, y1, x2, y2, (0, 255, 0))

        # 2 corresponds to 'car' in COCO dataset
        elif class_id == 2:
            car_count += 1

            # Crop the car for color analysis from the clean original image
            car_crop = image[
                int(y1):int(y2),
                int(x1):int(x2)
            ]

            # Check if car is blue
            if is_blue_car(car_crop):
                # Red box for blue cars (RGB format: 255,0,0)
                create_box(annotated_image, x1, y1, x2, y2, (255, 0, 0))
            else:
                # Blue box for other cars (RGB format: 0,0,255)
                create_box(annotated_image, x1, y1, x2, y2, (0, 0, 255))

    return annotated_image, car_count, person_count

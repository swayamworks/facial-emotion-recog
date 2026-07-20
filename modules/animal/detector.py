from ultralytics import YOLO
import cv2
from pathlib import Path

# Load the trained animal detection model
MODEL_PATH = Path(__file__).resolve().parent / "best.pt"
model = YOLO(str(MODEL_PATH))


def detect_animals(img_path):
    """Run inference on an image using the trained animal YOLO model."""
    results = model(img_path)
    return results


def process_image(img_path, output_path):
    """
    Runs animal detection on the input image, draws bounding boxes,
    and saves the annotated image to output_path.
    Returns a dict with animal name -> count.
    """
    results = detect_animals(str(img_path))
    image = cv2.imread(str(img_path))

    result = results[0]

    animal_counts = {}

    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0]

        # Count each animal type
        animal_counts[class_name] = animal_counts.get(class_name, 0) + 1

        # Draw bounding box (green)
        cv2.rectangle(
            image,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2
        )

        # Label with class name and confidence
        label = f"{class_name} {confidence:.2f}"

        # Black outline
        cv2.putText(
            image,
            label,
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            4,
            cv2.LINE_AA
        )

        # Green text
        cv2.putText(
            image,
            label,
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    # Save Output
    cv2.imwrite(str(output_path), image)

    return animal_counts


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    IMAGE_PATH = PROJECT_ROOT / "images" / "test.jpg"
    OUTPUT_PATH = PROJECT_ROOT / "images" / "animal_output.jpg"

    counts = process_image(str(IMAGE_PATH), str(OUTPUT_PATH))
    print(f"Detected animals: {counts}")
    print(f"Output image saved to: {OUTPUT_PATH}")

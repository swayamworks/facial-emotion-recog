from ultralytics import YOLO
import cv2
from pathlib import Path

# Load YOLO model
model = YOLO("yolov8n.pt")

# Get project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Image paths
IMAGE_PATH = PROJECT_ROOT / "images" / "test.jpg"
OUTPUT_PATH = PROJECT_ROOT / "images" / "output.jpg"


def detect_objects(img_path):
    return model(img_path)


def create_box(image, x1, y1, x2, y2, color):
    cv2.rectangle(
        image,
        (int(x1), int(y1)),
        (int(x2), int(y2)),
        color,
        2
    )


def create_label(image, text, x, y, color):
    # Black outline
    cv2.putText(
        image,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        4,
        cv2.LINE_AA
    )

    # Colored text
    cv2.putText(
        image,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2,
        cv2.LINE_AA
    )


def is_blue_car(car_image):

    if car_image.size == 0:
        return False

    hsv = cv2.cvtColor(car_image, cv2.COLOR_BGR2HSV)

    lower_blue = (100, 100, 50)
    upper_blue = (140, 255, 255)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    blue_pixels = cv2.countNonZero(mask)
    total_pixels = car_image.shape[0] * car_image.shape[1]

    if total_pixels == 0:
        return False

    blue_ratio = blue_pixels / total_pixels

    # Uncomment for debugging
    # print(f"Blue Ratio: {blue_ratio:.3f}")

    return blue_ratio > 0.10


def process_image(img_path, output_path):
    results = detect_objects(str(img_path))
    image = cv2.imread(str(img_path))

    result = results[0]

    car_count = 0
    person_count = 0

    for box in result.boxes:

        class_id = int(box.cls[0])

        x1, y1, x2, y2 = box.xyxy[0]

        # Person
        if class_id == 0:
            person_count += 1

        # Car
        elif class_id == 2:

            car_count += 1

            car_image = image[
                int(y1):int(y2),
                int(x1):int(x2)
            ]

            blue_car = is_blue_car(car_image)

            if blue_car:

                # Red box for blue cars
                create_box(image, x1, y1, x2, y2, (0, 0, 255))

            else:

                # Blue box for other cars
                create_box(image, x1, y1, x2, y2, (255, 0, 0))


    # -----------------------------
    # Statistics
    # -----------------------------

    # Cars Count (Outline)
    cv2.putText(
        image,
        f"Cars: {car_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 0),
        5,
        cv2.LINE_AA
    )

    # Cars Count (Green)
    cv2.putText(
        image,
        f"Cars: {car_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    # People Count (Outline)
    cv2.putText(
        image,
        f"People: {person_count}",
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 0),
        5,
        cv2.LINE_AA
    )

    # People Count (Green)
    cv2.putText(
        image,
        f"People: {person_count}",
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    # Save Output
    cv2.imwrite(str(output_path), image)

    return car_count, person_count

if __name__ == "__main__":
    c, p = process_image(str(IMAGE_PATH), str(OUTPUT_PATH))
    print(f"Cars: {c}")
    print(f"People: {p}")
    print(f"Output image saved to: {OUTPUT_PATH}")
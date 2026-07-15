import os
import numpy as np
import tensorflow as tf
from PIL import Image

CLASS_NAMES = [
    "surprise",
    "fear",
    "disgust",
    "happy",
    "sad",
    "angry",
    "neutral",
]

def load_model(model_path):
    """Loads the keras model from the given path."""
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

def preprocess_image(image: Image.Image, model):
    """
    Automatically resizes the image to whatever size
    the loaded model expects.
    """
    _, height, width, channels = model.input_shape

    image = image.convert("RGB")
    image = image.resize((width, height))

    img = np.array(image, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    return img

def predict_emotion(model, image):
    """
    Predicts the emotion of a preprocessed image.
    Returns (emotion_label, confidence_percentage, full_prediction_array).
    """
    prediction = model.predict(image, verbose=0)[0]
    idx = np.argmax(prediction)

    emotion = CLASS_NAMES[idx]
    confidence = float(prediction[idx]) * 100

    return emotion, confidence, prediction

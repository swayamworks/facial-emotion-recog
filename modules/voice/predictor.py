import os
import joblib
import numpy as np
from pathlib import Path

from modules.voice.feature_extractor import AudioFeatureExtractor


# =====================================
# Paths
# =====================================

MODEL_DIR = Path(__file__).resolve().parent / "models"


class VoicePredictor:
    """
    Reusable inference class for voice-based gender and emotion prediction.

    Loads all models once during initialization.
    Gender: RandomForestClassifier (male / female)
    Emotion: XGBClassifier (multi-class, female voices only)
    """

    def __init__(self):

        # Feature extractor
        self.extractor = AudioFeatureExtractor()

        # Gender model + scaler
        self.gender_model = joblib.load(MODEL_DIR / "gender_model.pkl")
        self.gender_scaler = joblib.load(MODEL_DIR / "gender_scaler.pkl")

        # Emotion model + scaler + label encoder
        self.emotion_model = joblib.load(MODEL_DIR / "emotion_model.pkl")
        self.emotion_scaler = joblib.load(MODEL_DIR / "emotion_scaler.pkl")
        self.emotion_encoder = joblib.load(MODEL_DIR / "emotion_encoder.pkl")

    def predict(self, audio_path):
        """
        Run gender and emotion prediction on an audio file.

        Returns:
            dict with keys:
                - gender (str): "Male" or "Female"
                - gender_confidence (float): confidence percentage
                - emotion (str or None): emotion label if female, None if male
                - emotion_confidence (float or None): confidence % if female
        """

        # Extract features
        features = self.extractor.extract_features(audio_path)
        features = features.reshape(1, -1)

        # =====================================
        # Gender Prediction
        # =====================================

        gender_features = self.gender_scaler.transform(features)
        gender_proba = self.gender_model.predict_proba(gender_features)[0]
        gender_idx = int(np.argmax(gender_proba))
        gender_confidence = float(gender_proba[gender_idx]) * 100

        # Labels: 0 = male, 1 = female (from train_gender.py)
        gender = "Female" if gender_idx == 1 else "Male"

        # =====================================
        # Emotion Prediction (female only)
        # =====================================

        if gender == "Male":
            return {
                "gender": gender,
                "gender_confidence": round(gender_confidence, 1),
                "emotion": None,
                "emotion_confidence": None,
            }

        emotion_features = self.emotion_scaler.transform(features)
        emotion_proba = self.emotion_model.predict_proba(emotion_features)[0]
        emotion_idx = int(np.argmax(emotion_proba))
        emotion_confidence = float(emotion_proba[emotion_idx]) * 100

        emotion = self.emotion_encoder.inverse_transform([emotion_idx])[0]

        return {
            "gender": gender,
            "gender_confidence": round(gender_confidence, 1),
            "emotion": emotion.capitalize(),
            "emotion_confidence": round(emotion_confidence, 1),
        }


# =====================================
# Test
# =====================================

if __name__ == "__main__":

    predictor = VoicePredictor()

    # Test with a sample file if available
    test_file = Path(__file__).resolve().parent / "dataset" / "Actor_01" / "03-01-01-01-01-01-01.wav"

    if test_file.exists():
        result = predictor.predict(str(test_file))
        print(result)
    else:
        print("No test file found. Predictor loaded successfully.")

import librosa
import numpy as np


class AudioFeatureExtractor:

    def __init__(self,
                 sample_rate=22050,
                 duration=3,
                 n_mfcc=40):

        self.sample_rate = sample_rate
        self.duration = duration
        self.n_mfcc = n_mfcc

    def extract_features(self, audio_path):

        # Load audio
        y, sr = librosa.load(
            audio_path,
            sr=self.sample_rate,
            duration=self.duration
        )

        # ==========================
        # MFCC
        # ==========================

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=self.n_mfcc
        )

        # Delta MFCC
        delta = librosa.feature.delta(mfcc)

        # Delta-Delta MFCC
        delta2 = librosa.feature.delta(
            mfcc,
            order=2
        )

        # Mean pooling
        mfcc = np.mean(mfcc, axis=1)
        delta = np.mean(delta, axis=1)
        delta2 = np.mean(delta2, axis=1)

        # ==========================
        # Chroma
        # ==========================

        chroma = librosa.feature.chroma_stft(
            y=y,
            sr=sr
        )

        chroma = np.mean(chroma, axis=1)

        # ==========================
        # Mel Spectrogram
        # ==========================

        mel = librosa.feature.melspectrogram(
            y=y,
            sr=sr
        )

        mel = np.mean(mel, axis=1)

        # ==========================
        # Zero Crossing Rate
        # ==========================

        zcr = librosa.feature.zero_crossing_rate(y)
        zcr = np.mean(zcr)

        # ==========================
        # RMS Energy
        # ==========================

        rms = librosa.feature.rms(y=y)
        rms = np.mean(rms)

        # ==========================
        # Final Feature Vector
        # ==========================

        features = np.concatenate([
            mfcc,
            delta,
            delta2,
            chroma,
            mel,
            np.array([zcr]),
            np.array([rms])
        ])

        return features


# =====================================
# Test
# =====================================

if __name__ == "__main__":

    extractor = AudioFeatureExtractor()

    features = extractor.extract_features(
        "dataset/Actor_01/03-01-01-01-01-01-01.wav"
    )

    print("Feature Shape:", features.shape)
    print(features)
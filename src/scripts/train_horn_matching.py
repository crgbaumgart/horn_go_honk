import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def extract_features(filename):
    y, sr = librosa.load(filename)
    y = y / np.max(np.abs(y))

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    features = np.concatenate((mfccs_mean, chroma_mean))
    return features


def main():
    # Specify the paths to your train horn and non-train horn audio files
    train_horn_files = [
        'path_to_train_horn_file1.wav',
        'path_to_train_horn_file2.wav',
        # Add more file paths
    ]

    non_train_horn_files = [
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_1_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_2_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_3_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_4_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_5_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_6_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_7_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_8_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_9_NT.wav',
        'C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_10_NT.wav',
        # Add more file paths
    ]

    # Load your dataset
    X = []
    y = []

    # Extract features for train horn files
    for file in train_horn_files:
        features = extract_features(file)
        X.append(features)
        y.append(1)  # Label for train horn

    # Extract features for non-train horn files
    for file in non_train_horn_files:
        features = extract_features(file)
        X.append(features)
        y.append(0)  # Label for no train horn

    X = np.array(X)
    y = np.array(y)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the classifier
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Predict on new audio sample
    new_audio_file = 'path_to_new_audio_sample.wav'  # Replace with your new audio file path
    new_audio_features = extract_features(new_audio_file)
    new_audio_features = new_audio_features.reshape(1, -1)
    is_train_horn = clf.predict(new_audio_features)

    # Store the event if a train horn is detected
    if is_train_horn[0] == 1:
        """
        This is where we will add our SQL server code. I think this should work by using a CREATE TABLE statement
        and then logging each time true or false shows up.
        """
        with open("train_horn_events.txt", "a") as f:
            f.write(f"Train horn detected in: {new_audio_file}\n")

    print("Train horn detected:", bool(is_train_horn[0]))

if __name__ == "__main__":
    main()


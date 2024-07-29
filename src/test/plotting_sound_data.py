import librosa.display
import matplotlib.pyplot as plt


def plot_features(file, label):
    y, sr = librosa.load(file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.colorbar()
    plt.title(f'MFCC - {label}')

    plt.subplot(2, 1, 2)
    librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
    plt.colorbar()
    plt.title(f'Chroma - {label}')

    plt.tight_layout()
    plt.show()


# Plot features for a known train horn file
plot_features('C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/TRAIN/audio_recording_2_TP.wav', 'Train Horn')

# Plot features for a known non-train horn file
plot_features('C:/Users/donte/Documents/horn_go_honk_testing/Audio_training/No Train/audio_recording_1_NT.wav', 'Non-Train Horn')

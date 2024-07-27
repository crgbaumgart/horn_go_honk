import pyaudio
import wave
import os
from datetime import datetime


def create_directory_if_not_exists(directory):
    """
    checks to see if a directory exists for the files, if not it will create one

    """
    if not os.path.exists(directory):
        print("Creating Directory...")
        os.makedirs(directory)
        print(f"Directory created at {directory}")


def record_audio(filename, duration, rate=44100, channels=2, chunk_size=1024, device_index=None):
    # Initialize pyaudio
    p = pyaudio.PyAudio()

    # Open a new stream for recording
    stream = p.open(format=pyaudio.paInt16,  # 16 bits per sample
                    channels=channels,
                    rate=rate,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=chunk_size)

    print("Recording...")

    # List to hold recorded frames
    frames = []

    # Record for the given duration
    for _ in range(0, int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Recording finished")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the pyaudio instance
    p.terminate()

    # Write the recorded frames to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def main():
    device_index = 1  # Replace with the actual device index from the list
    duration = 30
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    desktop_directory = os.path.join(os.path.expanduser("~"), "Documents", "horn_go_honk_testing", "Audio")
    create_directory_if_not_exists(desktop_directory)
    filename = f"{desktop_directory}/audio_recording_{timestamp}.wav"
    record_audio(filename, duration)


if __name__ == "__main__":
    main()
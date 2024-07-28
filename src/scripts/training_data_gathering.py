import pyaudio
import wave
import os
from datetime import datetime


def list_audio_devices():
    """
    Lists audio devices from the os and generates a list. Change the "device_index" param in the main
        function to use a different device from the OS default
    """
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Input Device id {i} - {device_info.get('name')}")
    p.terminate()






def create_directory_if_not_exists(directory):
    """
    checks to see if a directory exists for the audio files, if not it will create one

    """
    if not os.path.exists(directory):
        print("Creating Directory...")
        os.makedirs(directory)
        print(f"Directory created at {directory}")


def record_audio(filename, duration, rate=44100, channels=2, chunk_size=1024, device_index=None):
    """
    Function to record audio and store in a local file.
    params::
    filename: filename specified in the main function of the script where this function is called
        duration: duration of recording, specified in seconds. Declare value in the main  script where this
        function is called
    rate: sampling rate of recording. in kHz.
    channels: number of recording channels. 1 is mono, 2 is stereo
    chunk_size: defines how many frames of audio are held in the buffer before being written to the file. High
        chunk_size will result in higher latency but lower cpu usage (we might want to experiment depending on
        CPU speed of the rpi
    device_index: index number to specify which audio device to use. "1" will use the default audio device
        selected by the OS
    """
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
    """Main function to record audio and write the audio to a file
    params::
    duration: length of audio recording in seconds
    timestamp: current time stamp at the time of execution. It is appened to the end of the file name to
        version the files to avoid confusion
    desktop_directory: directory for storing the audio files
    filename: the file name for the audio file
    """
    list_audio_devices()
    device_index = 1  # Replace with the actual device index from the list
    duration = 30
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    desktop_directory = os.path.join(os.path.expanduser("~"), "Documents", "horn_go_honk_testing", "Audio_training")
    create_directory_if_not_exists(desktop_directory)
    filename = f"{desktop_directory}/audio_recording_{timestamp}_NT.wav"
    #  call recording function, passes file_name and duration back to the record_audio function
    record_audio(filename, duration)


if __name__ == "__main__":
    main()
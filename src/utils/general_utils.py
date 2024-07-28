from geopy.geocoders import Nominatim
import time
import pyaudio
import wave
import os



def geocode_address(address):
    """This function is going to call the GPS coordinates that we specify.
     You must pass the "address" param from the main function.
    params:
    geolocator: We have to name the app that we are using this information in. I chose "horn_goes_honk"
    """

    # Initialize the Nominatim geocoder with a descriptive user agent
    geolocator = Nominatim(user_agent="horn_goes_honk")

    # Attempt to get the location of the specified address with retry logic
    for attempt in range(5):
        try:
            location = geolocator.geocode(address)
            if location:
                return location. address, location.latitude, location.longitude
            else:
                print("Address not found")
                return None
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Retrying...")
            # Wait for 2 seconds before retrying (Nominatim has a 1 sec rate limit for the api)
            time.sleep(2)
    return None, None, None


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
        selected by the OS.
    TODO: Add a "list_devices" function to allow users to select which audio device they want to use.
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
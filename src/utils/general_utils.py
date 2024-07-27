from geopy.geocoders import Nominatim
import time


def geocode_address(address):
    """This function is going to call the GPS coordinates that we specify. We can hard code it, or we can pass the
    address from something else, like a keyboard input if that is what we want to do. Once tested I will move into
    general_utils.py, so we can use it for other things. You must pass the "address" param from the main function.
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
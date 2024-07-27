from geopy.geocoders import Nominatim
import time
import pandas as pd


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


def main():
    """ Passes the "address" param to the geo_code function and returns GPS coordinates"""
    # Specify our address (using kava as for testing)
    address = "109 Industrial St, Denton, TX 76201"

    #  storing the location result to be used in the pandas df
    location_result = geocode_address(address)

    data = []

    if location_result:
        full_address, latitude, longitude = location_result
        data.append({"Address:": full_address, "Latitude:": latitude, "Longitude:": longitude})
    #  else case to return nothing if the address isn't found
    else:
        data.append({"Address:": address, "Latitude:": None, "Longitude:": None})

    df = pd.DataFrame(data)

    #  print the data frame to the console
    print(df)


if __name__ == "__main__":
    main()

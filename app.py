from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
from requests.exceptions import RequestException

app = Flask(__name__)

# Function to fetch weather data from API


def fetch_weather_data(latitude, longitude):
    # Form the URL with the provided latitude and longitude
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,precipitation_probability,relativehumidity_2m&daily=sunrise,sunset&timezone=auto"

    # Send GET request to the URL
    weather_response = requests.get(weather_url)

    # Parse the response to JSON
    weather_data = weather_response.json()

    # Return the parsed data
    return weather_data


# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route for the weather page
@app.route('/weather', methods=['GET'])
def get_weather():
    # Get the location from the request parameters
    location = request.args.get('location')

    try:
        # Form the geocoding URL with the provided location
        geocoding_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"

        # Send GET request to the geocoding URL
        geocoding_response = requests.get(geocoding_url)

        # Parse the response to JSON
        geocoding_data = geocoding_response.json()

        # If the geocoding data is empty, redirect to the main page
        if not geocoding_data:
            print("Location not found. Please try again.", "error")
            return redirect(url_for('index'))

        # Get the latitude and longitude from the geocoding data
        latitude = geocoding_data[0]["lat"]
        longitude = geocoding_data[0]["lon"]

        # Fetch the weather data from the Open-Meteo API using the latitude and longitude
        weather_data = fetch_weather_data(latitude, longitude)

        # Calculate the timezone offset
        timezone_offset = weather_data["utc_offset_seconds"]
        timezone_offset = timezone_offset / 3600
        current_time = datetime.now().time()
        idx = current_time.hour + timezone_offset
        idx = int(idx % 24)
        if current_time.minute > 30:
            idx += 1

        # Extract the required data from the weather data
        temperature = weather_data["hourly"]["temperature_2m"][idx]
        precipitation = weather_data["hourly"]["precipitation"][idx]
        sunset = weather_data["daily"]["sunset"][0]
        sunrise = weather_data["daily"]["sunrise"][0]
        relative_humidity = weather_data["hourly"]["relativehumidity_2m"][idx]
        percipitation_probability = weather_data["hourly"]["precipitation_probability"][idx]

        # Render the weather page with the extracted data
        return render_template('weather.html', location=location, temperature=temperature, precipitation=precipitation, sunset=sunset, sunrise=sunrise, relative_humidity=relative_humidity, percipitation_probability=percipitation_probability)

    except RequestException:
        # Handle request exceptions
        print("An error occurred while fetching data from the API. Please try again later.", "error")
        return redirect(url_for('index'))

    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}", "error")
        return redirect(url_for('index'))


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

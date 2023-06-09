# Weather Forecast Flask Application

This is a simple Flask application that provides weather forecasts for any location entered by the user. It uses the Open-Meteo API for weather data and the Nominatim OpenStreetMap API for geocoding.

## Features

- Get the current weather conditions for any location.
- Displays temperature, relative humidity, precipitation in the past hour, chance of precipitation, sunrise and sunset times.

## Project Structure

```
/my_project
  |-- app.py
  |-- /templates
      |-- index.html
      |-- weather.html
  |-- /static
      |-- styles.css
```

## Installation

1. Clone this repository or download the ZIP file.
2. Navigate to the project directory.

```
cd my_project
```

3. Install the requirements.

```
pip install -r requirements.txt
```

4. Run the application.

```
python app.py
```

5. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Dependencies

- Flask
- requests

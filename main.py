import datetime
import os

import requests
from flask import Flask, render_template, request

app = Flask(__name__)
api_key = os.environ['API_KEY']


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/forecast', methods=['POST'])
def forecast():
  if request.method != 'POST':
    return 'Invalid request method'

  city = request.form['city']

  try:
    api_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}'
    response = requests.get(api_url)
    data = response.json()

    if response.status_code != 200:
      raise Exception('API call failed')

    # Process weather data
    temperature = data['current']['temperature']
    description = data['current']['weather_descriptions'][0]
    humidity = data['current']['humidity']
    wind_speed = data['current']['wind_speed']
    pressure = data['current']['pressure']

    # Calculate temperature in Fahrenheit and Celsius
    temperature_fahrenheit = (temperature * 9 / 5) + 32
    temperature_celsius = (temperature - 273.15)

    today_date = datetime.datetime.now().strftime("Today, %d %B")

    # Extract country and weather icon information from the API response
    country = data['location']['country']
    weather_icons = data['current']['weather_icons']

    return render_template('forecast.html',
                           city=city,
                           temperature=temperature,
                           description=description,
                           humidity=humidity,
                           wind_speed=wind_speed,
                           pressure=pressure,
                           temperature_fahrenheit=temperature_fahrenheit,
                           temperature_celsius=temperature_celsius,
                           today_date=today_date,
                           country=country,
                           weather_icons=weather_icons)

  except Exception as e:
    return render_template('error.html', error_message=str(e))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

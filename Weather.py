import requests
API_KEY="74449a011308459698b83538252204"

def get_weather(city_name):
    url = f'http://api.weatherapi.com/v1/current.json?q={city_name}&key={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        city = data['location']['name']
        country = data['location']['country']
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']

        match description:
            case 'Sunny': description+="🌞"
            case 'Clear': description+="☀️"
            case 'Partly cloudy': description+="🌤️"
            case 'Partly Cloudy': description+="🌤️"
            case 'Cloudy': description+="🌥️"
            case 'Overcast': description+="☁️"
            case 'Mist': description+="🌫️"
            case 'Fog': description+="🌫️"
            case 'Freezing fog': description+="🌫️"
            case 'Patchy rain nearby': description+="🌧️"
            case 'Light rain shower': description+="🌧️"
            case 'Light rain': description+="🌧️"
            case 'Moderate rain': description+="🌧️"
            case 'Heavy rain': description+="🌧️"
            case 'Light sleet': description+="🌨️"
            case 'Light snow': description+="🌨️"
            case 'Moderate snow': description+="🌨️"
            case 'Heavy snow': description+="🌨️"
            case 'Blizzard': description+="🌨️"
            case 'Thundery outbreaks in nearby': description+="🌩️"
            case 'Patchy light rain in area with thunder': description+="⛈️"
            case 'Moderate or heavy rain with thunder': description+="⛈️"
            case 'Moderate rain with thunder': description+="⛈️"
            case 'Heavy rain with thunder': description+="⛈️"
            case 'Thunderstorm': description+="⛈️"

        print(f"\nWeather in {city}, {country}:")
        print(f"Temperature: {temperature}°C🌡️")
        print(f"Weather: {description}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} kph")
    else:
        print("Sorry, couldn't fetch weather data. Please check the city name and try again.")

def main():
    print("Welcome to the Weather Forecast App!")
    while True:
        city_name = input("\nEnter the name of a city to get the weather (or type 'exit' to quit): ")
        if city_name.lower() == 'exit':
            print("Goodbye!")
            break
        get_weather(city_name)

if __name__ == "__main__":
    main()
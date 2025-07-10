import tkinter as tk
from tkinter import messagebox
import requests

# Replace with your OpenWeatherMap API key
API_KEY = 'your_api_key_here'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Change to 'imperial' for Fahrenheit
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'condition': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        else:
            return {'error': data.get('message', 'API error')}
    except Exception as e:
        return {'error': str(e)}

def show_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    weather = get_weather(city)
    if 'error' in weather:
        messagebox.showerror("Error", weather['error'])
    else:
        result = (
            f"📍 {weather['city']}, {weather['country']}\n"
            f"🌡️ {weather['temperature']}°C\n"
            f"🌤️ {weather['condition'].capitalize()}\n"
            f"💧 Humidity: {weather['humidity']}%\n"
            f"🌬️ Wind: {weather['wind_speed']} m/s"
        )
        result_label.config(text=result)

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("300x300")
root.resizable(False, False)

# Widgets
tk.Label(root, text="Enter city:", font=('Arial', 12)).pack(pady=10)
city_entry = tk.Entry(root, width=25, font=('Arial', 12))
city_entry.pack()

tk.Button(root, text="Get Weather", command=show_weather, font=('Arial', 12)).pack(pady=10)

result_label = tk.Label(root, text="", font=('Arial', 11), justify="left")
result_label.pack(pady=10)

# Run the app
root.mainloop()
import requests
import tkinter as tk
from tkinter import messagebox

API_KEY = "21e2e0bfffde483628df2b9b19919f2d"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

BACKGROUND_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"  # Green
LABEL_COLOR = "#333333"  # Dark gray
TEXT_COLOR = "#000000"  # Black

def fetch_weather_data(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # Change to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")


def fetch_current_city_weather():
    try:
        # Use IP geolocation to get user's current city
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        city = data["city"]
        return fetch_weather_data(city)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch current city weather: {e}")


def display_weather(num_cities):
    if num_cities == 1:
        city_name = city1_entry.get()

        if not city_name:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        current_city_weather = fetch_current_city_weather()
        user_city_weather = fetch_weather_data(city_name)

        if current_city_weather and user_city_weather:
            current_temperature = current_city_weather['main']['temp']
            current_description = current_city_weather['weather'][0]['description']

            user_temperature = user_city_weather['main']['temp']
            user_description = user_city_weather['weather'][0]['description']

            weather_label.config(text=f"{city_name}:\nTemperature: {user_temperature}°C\nDescription: {user_description}\n\nCurrent City:\nTemperature: {current_temperature}°C\nDescription: {current_description}")
        else:
            messagebox.showerror("Error", "Failed to fetch weather data.")
    elif num_cities == 2:
        city1_name = city1_entry.get()
        city2_name = city2_entry.get()

        if not city1_name or not city2_name:
            messagebox.showwarning("Warning", "Please enter both city names.")
            return

        city1_weather = fetch_weather_data(city1_name)
        city2_weather = fetch_weather_data(city2_name)

        if city1_weather and city2_weather:
            city1_temperature = city1_weather['main']['temp']
            city1_description = city1_weather['weather'][0]['description']

            city2_temperature = city2_weather['main']['temp']
            city2_description = city2_weather['weather'][0]['description']

            weather_label.config(text=f"{city1_name}:\nTemperature: {city1_temperature}°C\nDescription: {city1_description}\n\n{city2_name}:\nTemperature: {city2_temperature}°C\nDescription: {city2_description}")
        else:
            messagebox.showerror("Error", "Failed to fetch weather data.")


def switch_city_mode():
    num_cities = city_mode_var.get()

    if num_cities == 1:
        city2_label.grid_forget()
        city2_entry.grid_forget()
    elif num_cities == 2:
        city2_label.grid(row=3, column=0, pady=5)
        city2_entry.grid(row=4, column=0)


root = tk.Tk()
root.title("Weather App")
root.configure(bg=BACKGROUND_COLOR)

city_mode_var = tk.IntVar()
city_mode_var.set(1)  # Default to 1 city

city1_label = tk.Label(root, text="Enter city name:", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
city1_label.grid(row=0, column=0, pady=5)

city1_entry = tk.Entry(root)
city1_entry.grid(row=1, column=0, pady=5)

city2_label = tk.Label(root, text="Enter city 2 name:", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
city2_entry = tk.Entry(root)

city_mode_radio1 = tk.Radiobutton(root, text="Search for 1 city", variable=city_mode_var, value=1, command=switch_city_mode, bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
city_mode_radio1.grid(row=2, column=0, pady=5)

city_mode_radio2 = tk.Radiobutton(root, text="Search for 2 cities", variable=city_mode_var, value=2, command=switch_city_mode, bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
city_mode_radio2.grid(row=2, column=1, pady=5)

fetch_button = tk.Button(root, text="Fetch Weather", command=lambda: display_weather(city_mode_var.get()), bg=BUTTON_COLOR, fg=TEXT_COLOR)
fetch_button.grid(row=5, column=0, pady=5)

weather_label = tk.Label(root, text="", bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
weather_label.grid(row=6, column=0, pady=5)

root.mainloop()

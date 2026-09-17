
import tkinter as tk
from tkinter import messagebox
import requests


# ============================================================
# API SETTINGS
# ============================================================


API_KEY = "USE YOUR API"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ============================================================
# COLORS
# ============================================================

BACKGROUND = "#EAF6FF"       # Light sky blue
CARD = "#FFFFFF"             # White
PRIMARY = "#2563EB"          # Blue
ACCENT = "#60A5FA"           # Light blue
TEXT = "#1E293B"             # Dark text
SECONDARY = "#64748B"        # Gray text
BORDER = "#D7EAF7"            # Very light blue


# ============================================================
# WEATHER EMOJI
# ============================================================

def get_weather_emoji(condition):

    condition = condition.lower()

    if "thunderstorm" in condition:
        return "⛈️"

    elif "rain" in condition:
        return "🌧️"

    elif "snow" in condition:
        return "❄️"

    elif "clear" in condition:
        return "☀️"

    elif "cloud" in condition:
        return "☁️"

    elif "mist" in condition or "fog" in condition:
        return "🌫️"

    else:
        return "🌤️"


# ============================================================
# GET WEATHER DATA
# ============================================================

def get_weather():

    city = city_entry.get().strip()

    # Check empty input
    if city == "":
        messagebox.showwarning(
            "Missing City",
            "Please enter a city name."
        )
        return

    try:

        # Create API URL
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

        # Send request
        response = requests.get(url)

        # City not found
        if response.status_code == 404:
            messagebox.showerror(
                "City Not Found",
                "Please enter a valid city name."
            )
            return

        # Other API error
        if response.status_code != 200:
            messagebox.showerror(
                "Error",
                "Unable to get weather information."
            )
            return

        # Convert JSON response into Python dictionary
        data = response.json()

        # ====================================================
        # EXTRACT DATA
        # ====================================================

        city_name = data["name"]
        country = data["sys"]["country"]

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        wind_speed = data["wind"]["speed"]

        condition = data["weather"][0]["description"]

        # Get weather emoji
        weather_icon = get_weather_emoji(condition)

        # ====================================================
        # UPDATE SCREEN
        # ====================================================

        city_label.config(
            text=f"📍 {city_name}, {country}"
        )

        emoji_label.config(
            text=weather_icon
        )

        temperature_label.config(
            text=f"{temperature:.1f}°C"
        )

        condition_label.config(
            text=condition.title()
        )

        feels_label.config(
            text=f"🌡️  Feels Like\n{feels_like:.1f}°C"
        )

        humidity_label.config(
            text=f"💧  Humidity\n{humidity}%"
        )

        wind_label.config(
            text=f"💨  Wind\n{wind_speed} m/s"
        )

    # Internet / API connection error
    except requests.exceptions.RequestException:

        messagebox.showerror(
            "Network Error",
            "Please check your internet connection."
        )

    # Any unexpected error
    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Weather App")
root.geometry("620x720")

root.resizable(False, False)

root.configure(
    bg=BACKGROUND
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=BACKGROUND
)

header.pack(
    pady=(28, 10)
)


title_label = tk.Label(
    header,
    text="🌤️ Weather App",
    font=("Arial", 28, "bold"),
    bg=BACKGROUND,
    fg=TEXT
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Check live weather conditions anywhere",
    font=("Arial", 12),
    bg=BACKGROUND,
    fg=SECONDARY
)

subtitle_label.pack(
    pady=(5, 0)
)


# ============================================================
# SEARCH SECTION
# ============================================================

search_frame = tk.Frame(
    root,
    bg=BACKGROUND
)

search_frame.pack(
    pady=15
)


# Search box
city_entry = tk.Entry(
    search_frame,
    font=("Arial", 15),
    width=24,
    bg=CARD,
    fg=TEXT,
    insertbackground=TEXT,
    relief="solid",
    bd=1
)

city_entry.grid(
    row=0,
    column=0,
    ipady=10,
    padx=(0, 8)
)


# Search button
search_button = tk.Button(
    search_frame,
    text="🔎  Search",
    font=("Arial", 13, "bold"),
    bg=PRIMARY,
    fg="white",
    activebackground=ACCENT,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=get_weather
)

search_button.grid(
    row=0,
    column=1,
    ipadx=12,
    ipady=8
)


# ============================================================
# WEATHER CARD
# ============================================================

weather_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

weather_card.pack(
    padx=45,
    pady=15,
    fill="x"
)


# ============================================================
# CITY
# ============================================================

city_label = tk.Label(
    weather_card,
    text="📍  Enter a city",
    font=("Arial", 19, "bold"),
    bg=CARD,
    fg=TEXT
)

city_label.pack(
    pady=(25, 5)
)


# ============================================================
# WEATHER ICON
# ============================================================

emoji_label = tk.Label(
    weather_card,
    text="🌎",
    font=("Segoe UI Emoji", 55),
    bg=CARD
)

emoji_label.pack(
    pady=5
)


# ============================================================
# TEMPERATURE
# ============================================================

temperature_label = tk.Label(
    weather_card,
    text="--°C",
    font=("Arial", 42, "bold"),
    bg=CARD,
    fg=PRIMARY
)

temperature_label.pack(
    pady=2
)


# ============================================================
# WEATHER CONDITION
# ============================================================

condition_label = tk.Label(
    weather_card,
    text="Weather Condition",
    font=("Arial", 17),
    bg=CARD,
    fg=TEXT
)

condition_label.pack(
    pady=(2, 25)
)


# ============================================================
# WEATHER DETAILS
# ============================================================

details_frame = tk.Frame(
    weather_card,
    bg=CARD
)

details_frame.pack(
    pady=(0, 30)
)


# Feels Like
feels_label = tk.Label(
    details_frame,
    text="🌡️  Feels Like\n--°C",
    font=("Segoe UI Emoji", 12),
    bg=CARD,
    fg=SECONDARY,
    width=16
)

feels_label.grid(
    row=0,
    column=0,
    padx=5
)


# Humidity
humidity_label = tk.Label(
    details_frame,
    text="💧  Humidity\n--%",
    font=("Segoe UI Emoji", 12),
    bg=CARD,
    fg=SECONDARY,
    width=16
)

humidity_label.grid(
    row=0,
    column=1,
    padx=5
)


# Wind
wind_label = tk.Label(
    details_frame,
    text="💨  Wind\n-- m/s",
    font=("Segoe UI Emoji", 12),
    bg=CARD,
    fg=SECONDARY,
    width=16
)

wind_label.grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# FOOTER
# ============================================================

footer_label = tk.Label(
    root,
    text="Powered by OpenWeatherMap  🌎",
    font=("Segoe UI Emoji", 10),
    bg=BACKGROUND,
    fg=SECONDARY
)

footer_label.pack(
    pady=15
)


# ============================================================
# ENTER KEY SUPPORT
# ============================================================

city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()




---

# 🌦️ Weather App (with Air Quality) - CustomTkinter GUI

This is a sleek, Python-based desktop weather application built using `CustomTkinter`, which displays real-time weather and air quality data for any location using the [WeatherAPI](https://www.weatherapi.com/) service. It features:

* Local weather data based on IP
* Temperature, wind, humidity, pressure, and condition
* Air quality readings (PM2.5, PM10, CO, NO₂, O₃, SO₂, Defra Index)
* Switch between °C and °F
* API key management via `.env`
* Local response caching for faster performance

---

## 📸 Screenshot

> *Include a screenshot here of the app UI if available.*

---

## 🛠️ Features

* ✅ **Modern GUI** with `CustomTkinter`
* ✅ **Auto-location detection** using `ipinfo.io`
* ✅ **Accurate weather & air quality** from WeatherAPI
* ✅ **Dynamic AQI coloring** (Low / Moderate / High / Very High)
* ✅ **Caching system** to reduce API calls (10-minute validity)
* ✅ **Graceful error handling** for invalid input or network issues

---

## 📦 Requirements

* Python 3.8+
* [weatherapi.com](https://www.weatherapi.com/) API Key (Free Tier works)
* Libraries:

  * `customtkinter`
  * `requests`
  * `Pillow`
  * `python-dotenv`

Install dependencies using:

```bash
pip install customtkinter requests pillow python-dotenv
```

---

## 🔑 Setup

1. Clone the repository.
2. Install dependencies.
3. Run the app once; it will prompt you to enter your name and API key.
4. Your API key will be saved in a `.env` file for future use.

Example `.env` file:

```
API_KEY="your_api_key_here"
```

---

## 🚀 Running the App

```bash
python your_main_file.py
```

Once launched:

* Type a location and hit Enter to fetch weather and AQI.
* Or leave it blank to auto-detect your current location.

---

## 🧠 Caching System

* Cache file: `cache.dat`
* Stores responses for locations with a timestamp.
* Data is valid for **10 minutes**, then automatically refreshed.

---

## ❌ Error Handling

* If location is invalid or API limit is exceeded:

  * App shows "ERROR" and disables AQI display temporarily.
* If `.env` is missing or incorrect:

  * App opens a setup window to input a valid API key.

---

## 📁 Folder Structure

```bash
weather-app/
├── main.py
├── .env
├── cache.dat
├── png files/
│   ├── icon.png
│   ├── information_icon.png
│   ├── location_icon.png
│   ├── search_icon.png
│   └── weather_icon.png
└── README.md

```

---

## 📃 License

MIT License – feel free to use, modify, and distribute this app.

---


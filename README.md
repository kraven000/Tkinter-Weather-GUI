# Weather App

This is a simple weather application built using Tkinter, a GUI toolkit for Python. The app allows users to check the current weather conditions for a given city. It uses the [WeatherAPI](https://www.weatherapi.com/) to fetch real-time weather data.

## Features

- **Automatic Location Detection:** By default, the app detects the user's location using their IP address and displays the weather information for that location.
- **Custom Location Search:** Users can enter a specific city in the entry field and click the "SUBMIT!!" button to get weather information for that city.
- **Background Images:** The app has a visually appealing background that changes each time the application is launched. The background images are randomly selected from a predefined list.

## Prerequisites

Before running the application, make sure to set up your environment by following these steps:

1. **Get API Key:** Sign up on [WeatherAPI](https://www.weatherapi.com/) to obtain an API key. Add this key to the `.env` file in the project directory.

    ```plaintext
    api_key=your_weatherapi_key
    ```

2. **Install Dependencies:** Make sure to install the required Python packages. You can install them using the following command:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/weather-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd weather-app
    ```

3. Run the application:

    ```bash
    python weather_app.py
    ```

4. The Tkinter window will appear, allowing you to interact with the weather application.

## Screenshots

Include screenshots of the application to give users a visual preview of how the app looks.

## Contributing

If you would like to contribute to this project, please open an issue or submit a pull request. We welcome contributions and feedback.

## Acknowledgments

- **Tkinter:** Thanks to the Tkinter library for providing the tools to create the graphical user interface.
- **WeatherAPI:** Special thanks to WeatherAPI for providing accurate and up-to-date weather information.

Feel free to customize this README according to your preferences and add any additional information or sections that you find relevant.
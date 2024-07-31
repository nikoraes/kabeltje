# Kabeltje - iOS Location Simulator

Kabeltje is a Python-based application that allows you to simulate different locations on iOS 17.4+ devices. It provides a simple web interface for interacting with connected iOS devices, enabling developer mode, and simulating GPS locations.

## Features

- Start a RemoteXPC tunnel (Windows only)
- Display connected device information
- Enable developer mode on connected devices
- Simulate GPS locations on connected devices
- Interactive map for selecting locations
- Search functionality for finding locations
- Retrieve current device location

## Prerequisites

- Python 3.7+
- iOS device running iOS 17.4 or later
- Google Maps API key

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/kabeltje.git
   cd kabeltje
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

   This will install the following dependencies:
   - Flask
   - pymobiledevice3
   - python-dotenv

3. Create a `.env` file in the project root and add your Google Maps API key:

   ```
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

## Usage

1. Run the application:

   ```
   python kabeltje.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` (a browser window should open automatically).

3. Use the web interface to interact with your connected iOS device:
   - Start a tunnel (Windows only)
   - View device information
   - Enable developer mode
   - Simulate locations
   - Retrieve current device location

## Development

To contribute to Kabeltje:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your fork
5. Submit a pull request

If you add new dependencies to the project, remember to update the `requirements.txt` file:

```
pip freeze > requirements.txt
```

## License

[MIT License](https://opensource.org/licenses/MIT)

## Disclaimer

This tool is for development and testing purposes only. Be sure to comply with all relevant laws and regulations when using location simulation features.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

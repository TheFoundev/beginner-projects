# Project 16 - Weather Checker (Flutter with API)

## 1. Project Title
**Weather Checker**

## 2. The Concept
This app fetches real weather data from a public weather service over the internet and displays it for a city you can change. Think of it like checking the weather on your phone's built-in weather app — behind the scenes, your phone sends a request to a weather server (like asking a meteorologist), and that server sends back today's forecast. The app then takes that data and displays it with a nice icon and temperature, similar to how a news channel displays the weather report.

## 3. What You Will Build/Do
You'll build an app with a city search bar. Type a city name (like "London" or "Tokyo"), and the app displays the current temperature, weather condition (sunny, rainy, etc.), and an icon representing it. The final app looks like a mini weather station — perfect for checking if you need an umbrella before you leave the house!

## 4. Core App Concept
**API Calls and JSON Data Parsing** — The app sends a web request to a weather server (API), receives a structured data response (JSON — like a neatly organized text document), and extracts the specific information it needs (temperature, condition). It's like asking a restaurant for their menu — you send a request, they send back a list, and you pick what you want.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone with internet access
- A free [OpenWeatherMap](https://openweathermap.org/api) API key (free tier)

## 6. What You Will Learn
- Making HTTP requests from a mobile app
- Parsing JSON (structured data) responses from web APIs
- Displaying weather data with icons and styling
- Building a search feature with user input

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create weather_checker
cd weather_checker
```

### Step 2: Add Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.4
```

### Step 3: Get API Key
1. Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to "API keys" in your account
4. Copy your API key (it looks like a long string)

### Step 4: Complete Source Code
Create `lib/weather_service.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class WeatherService {
  final String apiKey;
  final String baseUrl = 'https://api.openweathermap.org/data/2.5';

  WeatherService({required this.apiKey});

  Future<WeatherData> getWeather(String city) async {
    final url = Uri.parse('$baseUrl/weather?q=$city&units=metric&appid=$apiKey');
    
    final response = await http.get(url);
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return WeatherData.fromJson(data);
    } else {
      final data = json.decode(response.body);
      throw Exception(data['message'] ?? 'Failed to fetch weather');
    }
  }
}

class WeatherData {
  final String cityName;
  final double temperature;
  final String description;
  final String iconCode;
  final double humidity;
  final double windSpeed;

  WeatherData({
    required this.cityName,
    required this.temperature,
    required this.description,
    required this.iconCode,
    required this.humidity,
    required this.windSpeed,
  });

  factory WeatherData.fromJson(Map<String, dynamic> json) {
    return WeatherData(
      cityName: json['name'] ?? 'Unknown',
      temperature: (json['main']['temp'] as num).toDouble(),
      description: json['weather'][0]['description'] ?? '',
      iconCode: json['weather'][0]['icon'] ?? '01d',
      humidity: (json['main']['humidity'] as num?)?.toDouble() ?? 0.0,
      windSpeed: (json['wind']['speed'] as num?)?.toDouble() ?? 0.0,
    );
  }
}
```

Create `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'weather_service.dart';

void main() {
  runApp(const WeatherCheckerApp());
}

class WeatherCheckerApp extends StatelessWidget {
  const WeatherCheckerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Weather Checker',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const WeatherHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class WeatherHomePage extends StatefulWidget {
  const WeatherHomePage({super.key});

  @override
  State<WeatherHomePage> createState() => _WeatherHomePageState();
}

class _WeatherHomePageState extends State<WeatherHomePage> {
  final TextEditingController _cityController = TextEditingController();
  WeatherService? _weatherService;
  WeatherData? _weatherData;
  bool _isLoading = false;
  String _errorMessage = '';

  // Replace with your OpenWeatherMap API key
  static const String _apiKey = 'YOUR_API_KEY_HERE';

  @override
  void initState() {
    super.initState();
    _weatherService = WeatherService(apiKey: _apiKey);
  }

  Future<void> _searchWeather() async {
    final city = _cityController.text.trim();
    if (city.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a city name';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = '';
      _weatherData = null;
    });

    try {
      final data = await _weatherService!.getWeather(city);
      setState(() {
        _weatherData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  String _getWeatherIconUrl(String iconCode) {
    return 'https://openweathermap.org/img/wn/$iconCode@2x.png';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Weather Checker'),
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.blue[300]!,
              Colors.blue[500]!,
              Colors.blue[700]!,
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                // Search bar
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.9),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _cityController,
                          decoration: InputDecoration(
                            hintText: 'Enter city name (e.g., London)',
                            border: InputBorder.none,
                            hintStyle: TextStyle(color: Colors.grey[500]),
                          ),
                          onSubmitted: (_) => _searchWeather(),
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.search, color: Colors.blue),
                        onPressed: _searchWeather,
                      ),
                    ],
                  )),
              
                const SizedBox(height: 20),
              
                // Loading indicator
                if (_isLoading)
                  const Center(child: CircularProgressIndicator(color: Colors.white)),
              
                // Error message
                if (_errorMessage.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text(
                      _errorMessage,
                      style: const TextStyle(color: Colors.white, fontSize: 16),
                      textAlign: TextAlign.center,
                    ),
                  ),
              
                // Weather display
                if (_weatherData != null) _buildWeatherCard(_weatherData!),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildWeatherCard(WeatherData data) {
    final isDay = data.iconCode.endsWith('d');
    final bgColor = isDay ? Colors.orange[300] : Colors.blueGrey[700];

    return Card(
      elevation: 10,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      color: bgColor,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            // City name
            Text(
              data.cityName,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          
            const SizedBox(height: 16),
          
            // Weather icon and temperature
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.network(
                  _getWeatherIconUrl(data.iconCode),
                  width: 100,
                  height: 100,
                ),
                Text(
                  '${data.temperature.round()}°C',
                  style: const TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          
            const SizedBox(height: 8),
          
            // Description
            Text(
              data.description.toUpperCase(),
              style: const TextStyle(
                fontSize: 18,
                color: Colors.white70,
                fontWeight: FontWeight.w500,
              ),
            ),
          
            const SizedBox(height: 20),
          
            // Additional details
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildDetailItem(Icons.water_drop, '${data.humidity.round()}%', 'Humidity'),
                _buildDetailItem(Icons.wind_power, '${data.windSpeed.toStringAsFixed(1)} m/s', 'Wind'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailItem(IconData icon, String value, String label) {
    return Column(
      children: [
        Icon(icon, color: Colors.white, size: 28),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
        Text(
          label,
          style: TextStyle(color: Colors.white70, fontSize: 12),
        ),
      ],
    );
  }
}
```

### Step 5: Replace API Key
Replace `'YOUR_API_KEY_HERE'` with your actual OpenWeatherMap API key from Step 3.

### Step 6: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add a "recent cities" list
- Add a forecast for the next 5 days
- Add geolocation to get local weather automatically
- Add temperature unit toggle (Celsius/Fahrenheit)
- Add a dark/light mode based on time of day

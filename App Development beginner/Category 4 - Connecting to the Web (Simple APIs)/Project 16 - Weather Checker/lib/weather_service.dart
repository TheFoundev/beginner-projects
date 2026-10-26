import 'dart:convert';
import 'package:http/http.dart' as http;

class WeatherService {
  final String apiKey;
  static const String _baseUrl = 'https://api.openweathermap.org/data/2.5';

  WeatherService({required this.apiKey});

  Future<WeatherData> getWeather(String city) async {
    final url = Uri.parse('$_baseUrl/weather?q=$city&units=metric&appid=$apiKey');
    
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

  String get iconUrl => 'https://openweathermap.org/img/wn/$iconCode@2x.png';
}

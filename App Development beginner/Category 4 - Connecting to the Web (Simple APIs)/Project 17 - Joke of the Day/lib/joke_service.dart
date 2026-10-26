import 'dart:convert';
import 'package:http/http.dart' as http;

class JokeService {
  static const String _baseUrl = 'https://official-joke-api.appspot.com';

  Future<Joke> fetchRandomJoke() async {
    final url = Uri.parse('$_baseUrl/random_joke');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Joke.fromJson(data);
    } else {
      throw Exception('Failed to load joke');
    }
  }

  Future<List<Joke>> fetchTenJokes() async {
    final url = Uri.parse('$_baseUrl/jokes/ten');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((json) => Joke.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load jokes');
    }
  }
}

class Joke {
  final int id;
  final String type;
  final String setup;
  final String punchline;

  Joke({
    required this.id,
    required this.type,
    required this.setup,
    required this.punchline,
  });

  factory Joke.fromJson(Map<String, dynamic> json) {
    return Joke(
      id: json['id'] ?? 0,
      type: json['type'] ?? 'general',
      setup: json['setup'] ?? '',
      punchline: json['punchline'] ?? '',
    );
  }
}

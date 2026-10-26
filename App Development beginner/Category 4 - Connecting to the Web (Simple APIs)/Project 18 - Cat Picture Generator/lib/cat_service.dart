import 'dart:convert';
import 'package:http/http.dart' as http;

class CatService {
  static const String _baseUrl = 'https://api.thecatapi.com/v1';

  Future<String> fetchRandomCatImageUrl() async {
    final url = Uri.parse('$_baseUrl/images/search');
    
    try {
      final response = await http.get(url).timeout(
        const Duration(seconds: 10),
      );

      if (response.statusCode == 200) {
        final List data = json.decode(response.body);
        if (data.isNotEmpty) {
          final imageUrl = data[0]['url'] as String;
          return imageUrl;
        }
        throw Exception('No cat images available');
      } else {
        throw Exception('Failed to fetch cat image');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  // Fallback cat URLs for when the API is unavailable
  static const List<String> fallbackCats = [
    'https://place.cat/400/300',
    'https://place.cat/400/301',
    'https://place.cat/400/302',
    'https://place.cat/400/303',
    'https://place.cat/400/304',
  ];
}

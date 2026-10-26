import 'dart:convert';
import 'package:http/http.dart' as http;

class NewsService {
  final String apiKey;
  static const String _baseUrl = 'https://newsapi.org/v2';

  NewsService({required this.apiKey});

  Future<List<NewsArticle>> fetchTopHeadlines() async {
    final url = Uri.parse('$_baseUrl/top-headlines?country=us&category=technology&apiKey=$apiKey');

    try {
      final response = await http.get(url).timeout(
        const Duration(seconds: 15),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List articles = data['articles'] ?? [];
        return articles.map((json) => NewsArticle.fromJson(json)).toList();
      } else {
        final data = json.decode(response.body);
        throw Exception(data['message'] ?? 'Failed to load news');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  // Mock data for when API is unavailable
  static List<NewsArticle> getMockArticles() {
    return [
      NewsArticle(
        title: 'Flutter 3.22 Released with Major Performance Improvements',
        description: 'Google today announced the release of Flutter 3.22, bringing significant performance enhancements and new features for developers.',
        urlToImage: 'https://placehold.co/600x400?text=Flutter+News',
        source: 'Tech News',
        publishedAt: DateTime.now().subtract(const Duration(hours: 2)),
      ),
      NewsArticle(
        title: 'New AI Features Coming to Mobile Development Tools',
        description: 'Major IDE vendors are integrating AI assistance into their mobile development environments.',
        urlToImage: 'https://placehold.co/600x400?text=AI+News',
        source: 'Dev Weekly',
        publishedAt: DateTime.now().subtract(const Duration(hours: 5)),
      ),
      NewsArticle(
        title: 'Apple Announces New Swift Student Challenge',
        description: 'Apple has launched its annual Swift Student Challenge to encourage young developers.',
        urlToImage: 'https://placehold.co/600x400?text=Swift+News',
        source: 'iOS Dev',
        publishedAt: DateTime.now().subtract(const Duration(days: 1)),
      ),
    ];
  }
}

class NewsArticle {
  final String title;
  final String description;
  final String urlToImage;
  final String source;
  final DateTime publishedAt;

  NewsArticle({
    required this.title,
    required this.description,
    required this.urlToImage,
    required this.source,
    required this.publishedAt,
  });

  factory NewsArticle.fromJson(Map<String, dynamic> json) {
    final sourceObj = json['source'] as Map<String, dynamic>?;
    return NewsArticle(
      title: json['title'] ?? 'Untitled',
      description: json['description'] ?? 'No description available',
      urlToImage: json['urlToImage'] ?? '',
      source: sourceObj?['name'] ?? 'Unknown',
      publishedAt: DateTime.tryParse(json['publishedAt'] ?? '') ?? DateTime.now(),
    );
  }
}

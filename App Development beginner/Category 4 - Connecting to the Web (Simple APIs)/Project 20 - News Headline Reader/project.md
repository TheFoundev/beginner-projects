# Project 20 - News Headline Reader (Flutter with API)

## 1. Project Title
**News Headline Reader**

## 2. The Concept
This app fetches the latest technology news headlines from a public news API and displays them in a scrollable list. Each headline shows a title, a short description, and sometimes a thumbnail image. It works like checking the news on a website — your phone sends a request to a news server, which sends back the latest headlines, and the app formats them into a clean, easy-to-read list. No ads, no clutter, just the headlines you care about.

## 3. What You Will Build/Do
You'll build an app with a scrollable list of news articles. Each item shows the headline, a short description, and the source. A refresh indicator at the top shows the last updated time. The final app looks like a clean news reader — swipe to scroll through headlines, tap to see more details.

## 4. Core App Concept
**List Data from API with Multiple Fields** — The app fetches a list of articles from a server, where each article has multiple pieces of information (title, description, image, source), and displays them in a repeating list format. Like a newspaper rack — each paper has a headline, subheading, and byline, and the rack shows many papers at once in an organized fashion.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone with internet access
- A free [NewsAPI](https://newsapi.org/) key (free tier available)

## 6. What You Will Learn
- Working with paginated list APIs
- Displaying heterogeneous data (text + images) in a list
- Pull-to-refresh for real-time data updates
- Building a scrollable, data-rich UI

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create news_headline_reader
cd news_headline_reader
```

### Step 2: Add Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.4
  cached_network_image: ^3.3.1
  timeago: ^3.2.4
```

### Step 3: Get API Key
1. Go to [https://newsapi.org/](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Note: The free tier has rate limits (100 requests/day)

### Step 4: Complete Source Code
Create `lib/news_service.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class NewsService {
  final String apiKey;
  static const String _baseUrl = 'https://newsapi.org/v2';

  NewsService({required this.apiKey});

  Future<List<NewsArticle>> fetchTopHeadlines() async {
    final url = Uri.parse('$_baseUrl/top-headlines?country=us&category=technology&apiKey=$apiKey&pageSize=20');

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
```

Create `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:intl/intl.dart';
import 'news_service.dart';

void main() {
  runApp(const NewsReaderApp());
}

class NewsReaderApp extends StatelessWidget {
  const NewsReaderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'News Headline Reader',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const NewsHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class NewsHomePage extends StatefulWidget {
  const NewsHomePage({super.key});

  @override
  State<NewsHomePage> createState() => _NewsHomePageState();
}

class _NewsHomePageState extends State<NewsHomePage> {
  final NewsService _newsService = NewsService(
    apiKey: 'YOUR_API_KEY_HERE', // Replace with your NewsAPI key
  );
  
  late Future<List<NewsArticle>> _articlesFuture;
  DateTime _lastUpdated = DateTime.now();

  @override
  void initState() {
    super.initState();
    _fetchNews();
  }

  void _fetchNews() {
    setState(() {
      _articlesFuture = _newsService.fetchTopHeadlines().catchError((_) {
        return NewsService.getMockArticles();
      });
      _lastUpdated = DateTime.now();
    });
  }

  String _formatTimeAgo(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h ago';
    } else {
      return '${difference.inDays}d ago';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tech News Headlines'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchNews,
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: Column(
        children: [
          // Last updated bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            color: Colors.blue[50],
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Updated ${_formatTimeAgo(_lastUpdated)}',
                  style: TextStyle(color: Colors.grey[600]),
                ),
                const SizedBox(width: 8),
                const Icon(Icons.refresh, size: 14, color: Colors.grey),
              ],
            ),
          ),
          
          // News list
          Expanded(
            child: RefreshIndicator(
              onRefresh: () async {
                _fetchNews();
              },
              child: FutureBuilder<List<NewsArticle>>(
                future: _articlesFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  
                  if (snapshot.hasError) {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.error, size: 60, color: Colors.red),
                          const SizedBox(height: 16),
                          Text(
                            'Error: ${snapshot.error}',
                            textAlign: TextAlign.center,
                            style: const TextStyle(color: Colors.red),
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: _fetchNews,
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    );
                  }
                  
                  if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return const Center(child: Text('No news available'));
                  }
                  
                  final articles = snapshot.data!;
                  
                  return ListView.separated(
                    itemCount: articles.length,
                    padding: const EdgeInsets.all(8),
                    separatorBuilder: (context, index) => const SizedBox(height: 8),
                    itemBuilder: (context, index) {
                      return _buildArticleCard(articles[index]);
                    },
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildArticleCard(NewsArticle article) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Image
          if (article.urlToImage.isNotEmpty)
            SizedBox(
              width: double.infinity,
              height: 180,
              child: CachedNetworkImage(
                imageUrl: article.urlToImage,
                placeholder: (context, url) => Container(
                  color: Colors.grey[300],
                  child: const Center(child: CircularProgressIndicator(strokeWidth: 2)),
                ),
                errorWidget: (context, url, error) => Container(
                  color: Colors.grey[300],
                  child: const Center(child: Icon(Icons.broken_image, size: 40)),
                ),
                fit: BoxFit.cover,
              ),
            ),
          
          // Content
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Source and time
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      article.source,
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue[700],
                      ),
                    ),
                    Text(
                      _formatTimeAgo(article.publishedAt),
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
              
                // Title
                Text(
                  article.title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    height: 1.2,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 8),
              
                // Description
                Text(
                  article.description,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[700],
                    height: 1.4,
                  ),
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Step 5: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add category filtering (sports, business, science)
- Add a search bar to search headlines
- Add article detail view showing full content
- Add bookmarking/saving feature for offline reading
- Add dark mode support

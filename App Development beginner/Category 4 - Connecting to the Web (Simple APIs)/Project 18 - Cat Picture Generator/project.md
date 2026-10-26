# Project 18 - Cat Picture Generator (Flutter with API)

## 1. Project Title
**Cat Picture Generator**

## 2. The Concept
This app fetches random cat pictures from an online API and displays them in a beautiful card. Every time you tap the "New Cat!" button, the app sends a request to a cat image server on the internet, gets back a URL pointing to a new cat photo, downloads it, and displays it. It's like ordering from a cat picture delivery service — you don't need to know which specific photo you'll get, but you know it'll be adorable!

## 3. What You Will Build/Do
You'll build an app with a central image display area and a "Generate New Cat" button. When you tap the button, a loading spinner shows briefly, then a new cat picture fades in. The final app looks like a pocket-sized cat gallery — perfect for instantly boosting your mood!

## 4. Core App Concept
**Image Loading from Network (URLs)** — The app requests an image URL from an API, then tells the screen to download and display that image from the internet. Like ordering a book from an online store: you order (get the URL), they ship it (download the image), and you receive it (see it on screen).

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone with internet access
- No API key required — uses a free public cat API

## 6. What You Will Learn
- Fetching data from public REST APIs
- Loading and displaying network images with loading states
- Building a visually clean photo-display app
- Handling loading and error states gracefully

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create cat_picture_generator
cd cat_picture_generator
```

### Step 2: Add Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.4
  cached_network_image: ^3.3.1
```

### Step 3: Complete Source Code
Create `lib/cat_service.dart`:

```dart
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

  // Fallback cat URLs for offline/demo
  static const List<String> fallbackCats = [
    'https://place.cat/400/300',
    'https://place.cat/400/301',
    'https://place.cat/400/302',
    'https://place.cat/400/303',
    'https://place.cat/400/304',
  ];
}
```

Create `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'cat_service.dart';

void main() {
  runApp(const CatPictureApp());
}

class CatPictureApp extends StatelessWidget {
  const CatPictureApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cat Picture Generator',
      theme: ThemeData(
        primarySwatch: Colors.orange,
        useMaterial3: true,
      ),
      home: const CatHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class CatHomePage extends StatefulWidget {
  const CatHomePage({super.key});

  @override
  State<CatHomePage> createState() => _CatHomePageState();
}

class _CatHomePageState extends State<CatHomePage> {
  final CatService _catService = CatService();
  String? _catImageUrl;
  bool _isLoading = false;
  String _errorMessage = '';
  int _catsGenerated = 0;

  @override
  void initState() {
    super.initState();
    _fetchNewCat();
  }

  Future<void> _fetchNewCat() async {
    setState(() {
      _isLoading = true;
      _errorMessage = '';
      _catImageUrl = null;
    });

    try {
      final imageUrl = await _catService.fetchRandomCatImageUrl();
      setState(() {
        _catImageUrl = imageUrl;
        _isLoading = false;
        _catsGenerated++;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to load cat picture';
        _isLoading = false;
        // Try fallback
        _loadFallbackCat();
      });
    }
  }

  void _loadFallbackCat() {
    Future.delayed(const Duration(milliseconds: 500), () {
      final random = DateTime.now().millisecondsSinceEpoch %
          CatService.fallbackCats.length;
      setState(() {
        _catImageUrl = CatService.fallbackCats[random];
        _errorMessage = '';
        _catsGenerated++;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cat Picture Generator'),
        centerTitle: true,
        backgroundColor: Colors.orange[300],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.orange[50]!, Colors.yellow[50]!],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Stats counter
              Padding(
                padding: const EdgeInsets.all(16),
                child: Chip(
                  backgroundColor: Colors.orange[100],
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  avatar: const Icon(Icons.favorite, color: Colors.orange, size: 18),
                  label: Text(
                    'Cats generated: $_catsGenerated',
                    style: const TextStyle(
                      color: Colors.orange,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            
              // Cat image display
              Expanded(
                child: Center(
                  child: _isLoading
                      ? const Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            CircularProgressIndicator(
                              color: Colors.orange,
                              strokeWidth: 3,
                            ),
                            SizedBox(height: 20),
                            Text(
                              'Fetching a fresh cat...',
                              style: TextStyle(
                                fontSize: 18,
                                color: Colors.orange,
                              ),
                            ),
                          ],
                        )
                      : _errorMessage.isNotEmpty
                          ? _buildErrorState()
                          : _catImageUrl != null
                              ? _buildCatCard(_catImageUrl!)
                              : const Text('No cat available'),
                ),
              ),
            
              // Action button
              Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    ElevatedButton.icon(
                      onPressed: _isLoading ? null : _fetchNewCat,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.orange,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 40,
                          vertical: 20,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                        elevation: 5,
                      ),
                      icon: const Icon(Icons.refresh, size: 26),
                      label: const Text(
                        'Generate New Cat!',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Swipe down to refresh • Tap button for new cat',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCatCard(String imageUrl) {
    return AnimatedOpacity(
      opacity: _isLoading ? 0.0 : 1.0,
      duration: const Duration(milliseconds: 300),
      child: Card(
        elevation: 15,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(25),
        ),
        margin: const EdgeInsets.symmetric(horizontal: 20),
        clipBehavior: Clip.antiAlias,
        child: CachedNetworkImage(
          imageUrl: imageUrl,
          placeholder: (context, url) => Container(
            width: 300,
            height: 300,
            color: Colors.orange[100],
            child: const Center(
              child: CircularProgressIndicator(
                color: Colors.orange,
                strokeWidth: 3,
              ),
            ),
          ),
          errorWidget: (context, url, error) => Container(
            width: 300,
            height: 300,
            color: Colors.orange[100],
            child: const Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.broken_image, size: 60, color: Colors.orange),
                SizedBox(height: 10),
                Text('Image failed to load'),
              ],
            ),
          ),
          fit: BoxFit.cover,
          width: double.infinity,
          height: 350,
        ),
      ),
    );
  }

  Widget _buildErrorState() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Icon(
          Icons.error_outline,
          size: 60,
          color: Colors.orange,
        ),
        const SizedBox(height: 12),
        Text(
          _errorMessage,
          style: const TextStyle(fontSize: 18, color: Colors.orange),
        ),
        const SizedBox(height: 16),
        TextButton.icon(
          onPressed: _fetchNewCat,
          icon: const Icon(Icons.refresh),
          label: const Text('Try Again'),
        ),
      ],
    );
  }
}
```

### Step 4: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add a "favorite cats" feature to save liked images
- Add cats by breed (fetch from the same API)
- Add zoom/pinch gesture support
- Add a slideshow mode that auto-loads cats
- Add a "cat facts" section alongside the image

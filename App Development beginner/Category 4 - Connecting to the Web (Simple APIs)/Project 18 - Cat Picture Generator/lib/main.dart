import 'dart:math';
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
        primarySwatch: Colors.pink,
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
  final Random _random = Random();
  
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
        _errorMessage = 'Failed to load cat. Showing fallback!';
        _isLoading = false;
      });
      // Use a fallback cat image
      _loadFallbackCat();
    }
  }

  void _loadFallbackCat() {
    Future.delayed(const Duration(milliseconds: 500), () {
      final randomIndex = _random.nextInt(CatService.fallbackCats.length);
      setState(() {
        _catImageUrl = CatService.fallbackCats[randomIndex];
        _errorMessage = '';
        _catsGenerated++;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Random Cat Generator'),
        centerTitle: true,
        backgroundColor: Colors.pink[200],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.pink[50]!, Colors.purple[50]!],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Counter
              Padding(
                padding: const EdgeInsets.all(16),
                child: Chip(
                  backgroundColor: Colors.pink[100],
                  avatar: const Icon(Icons.favorite, color: Colors.pink, size: 18),
                  label: Text(
                    'Cats generated: $_catsGenerated',
                    style: const TextStyle(
                      color: Colors.pink,
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
                              color: Colors.pink,
                              strokeWidth: 3,
                            ),
                            SizedBox(height: 20),
                            Text(
                              'Fetching a fresh cat...',
                              style: TextStyle(fontSize: 16, color: Colors.pink),
                            ),
                          ],
                        )
                      : _errorMessage.isNotEmpty
                          ? Padding(
                              padding: const EdgeInsets.all(24),
                              child: Text(
                                _errorMessage,
                                style: const TextStyle(
                                  color: Colors.red,
                                  fontSize: 18,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            )
                          : _catImageUrl != null
                              ? _buildCatCard(_catImageUrl!)
                              : const Text('No cat available'),
                ),
              ),
      
              // Action button
              Padding(
                padding: const EdgeInsets.all(24),
                child: SizedBox(
                  width: 240,
                  child: ElevatedButton.icon(
                    onPressed: _isLoading ? null : _fetchNewCat,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.pink,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 18),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                      elevation: 5,
                    ),
                    icon: const Icon(Icons.refresh, size: 26),
                    label: const Text(
                      'Generate New Cat!',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCatCard(String imageUrl) {
    return AnimatedFadeEffect(
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
            color: Colors.pink[100],
            child: const Center(
              child: CircularProgressIndicator(
                color: Colors.pink,
                strokeWidth: 3,
              ),
            ),
          ),
          errorWidget: (context, url, error) => Container(
            width: 300,
            height: 300,
            color: Colors.pink[100],
            child: const Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.broken_image, size: 60, color: Colors.pink),
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
}

// Simple fade animation wrapper
class AnimatedFadeEffect extends StatelessWidget {
  final Widget child;
  final Duration duration;

  const AnimatedFadeEffect({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 300),
  });

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0.0, end: 1.0),
      duration: duration,
      builder: (context, value, child) {
        return Opacity(opacity: value, child: child);
      },
    );
  }
}

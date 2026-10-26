import 'dart:math';
import 'package:flutter/material.dart';
import 'joke_service.dart';

void main() {
  runApp(const JokeApp());
}

class JokeApp extends StatelessWidget {
  const JokeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Joke of the Day',
      theme: ThemeData(
        primarySwatch: Colors.orange,
        useMaterial3: true,
      ),
      home: const JokeHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class JokeHomePage extends StatefulWidget {
  const JokeHomePage({super.key});

  @override
  State<JokeHomePage> createState() => _JokeHomePageState();
}

class _JokeHomePageState extends State<JokeHomePage> {
  final JokeService _jokeService = JokeService();
  Joke? _currentJoke;
  bool _isLoading = false;
  String _errorMessage = '';
  int _jokesViewed = 0;

  @override
  void initState() {
    super.initState();
    _fetchNewJoke();
  }

  Future<void> _fetchNewJoke() async {
    setState(() {
      _isLoading = true;
      _errorMessage = '';
    });

    try {
      final joke = await _jokeService.fetchRandomJoke();
      setState(() {
        _currentJoke = joke;
        _isLoading = false;
        _jokesViewed++;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to load joke. Try again!';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Joke of the Day'),
        centerTitle: true,
        backgroundColor: Colors.orange[300],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.yellow[100]!, Colors.orange[100]!],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Counter
              Padding(
                padding: const EdgeInsets.all(16),
                child: Chip(
                  backgroundColor: Colors.orange[100],
                  avatar: const Icon(Icons.favorite, color: Colors.orange, size: 18),
                  label: Text(
                    'Jokes viewed: $_jokesViewed',
                    style: const TextStyle(
                      color: Colors.orange,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            
              // Joke display
              Expanded(
                child: Center(
                  child: _isLoading
                      ? const Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            CircularProgressIndicator(color: Colors.orange),
                            SizedBox(height: 20),
                            Text(
                              'Loading a fresh joke...',
                              style: TextStyle(fontSize: 16, color: Colors.orange),
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
                          : _currentJoke != null
                              ? _buildJokeCard(_currentJoke!)
                              : const Text('No joke available'),
                ),
              ),
            
              // Action button
              Padding(
                padding: const EdgeInsets.all(24),
                child: SizedBox(
                  width: 240,
                  child: ElevatedButton.icon(
                    onPressed: _isLoading ? null : _fetchNewJoke,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orange,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 18),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                      elevation: 5,
                    ),
                    icon: const Icon(Icons.refresh, size: 26),
                    label: const Text(
                      'Tell Me Another!',
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

  Widget _buildJokeCard(Joke joke) {
    return Card(
      elevation: 10,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      margin: const EdgeInsets.symmetric(horizontal: 24),
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.format_quote,
              size: 50,
              color: Colors.orange,
            ),
            const SizedBox(height: 16),
            Text(
              joke.setup,
              style: const TextStyle(
                fontSize: 22,
                fontStyle: FontStyle.italic,
                height: 1.4,
                color: Colors.black87,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            Text(
              joke.punchline,
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Colors.orange,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            Text(
              '- ${joke.type}',
              style: TextStyle(color: Colors.grey[600]),
            ),
          ],
        ),
      ),
    );
  }
}

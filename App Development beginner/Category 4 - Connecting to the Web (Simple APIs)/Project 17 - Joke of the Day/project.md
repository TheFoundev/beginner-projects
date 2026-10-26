# Project 17 - Joke of the Day (Flutter with API)

## 1. Project Title
**Joke of the Day**

## 2. The Concept
This app fetches a random joke from an online joke API and displays it with a big smile. Each time you tap the "Another Joke" button, the app sends a request to a joke server (like calling a friend who tells jokes), gets back a setup and punchline, and shows them to you. It's like having a digital joke book that refreshes itself with new content over the internet — no need to install joke packs, the jokes stream in automatically!

## 3. What You Will Build/Do
You'll build an app with a joke display area and a "Tell Me Another" button. When you start the app, it fetches your first joke. Tap the button, and a new joke loads in with a smooth animation. The final app looks like a cheerful joke dispenser — perfect for breaking the ice or making your friends laugh.

## 4. Core App Concept
**Fetching and Displaying Dynamic Content** — The app requests fresh data from the internet each time, rather than using pre-stored content. Like ordering food delivery: you don't cook at home, instead you request from a restaurant and your order arrives ready to enjoy.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone with internet access
- No API key required — uses a free public API

## 6. What You Will Learn
- Making HTTP requests to public APIs without authentication
- Handling different response formats (setup/punchline jokes)
- Implementing loading states and error handling
- Building a fun, animated UI with joke reveal effects

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create joke_of_the_day
cd joke_of_the_day
```

### Step 2: Add Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.4
  google_fonts: ^6.0.0
```

### Step 3: Complete Source Code
Create `lib/joke_service.dart`:

```dart
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

  // Fetch 10 jokes at once for variety
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
```

Create `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
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
        primarySwatch: Colors.yellow,
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
  bool _showPunchline = false;
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
      _showPunchline = false;
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

  void _revealPunchline() {
    setState(() {
      _showPunchline = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Joke of the Day',
          style: GoogleFonts.poppins(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        backgroundColor: Colors.yellow[300],
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
              // Joke counter
              Padding(
                padding: const EdgeInsets.all(16),
                child: Chip(
                  backgroundColor: Colors.orange[100],
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  label: Text(
                    'Jokes viewed: $_jokesViewed',
                    style: GoogleFonts.poppins(
                      color: Colors.orange[800],
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ),
            
              // Joke card
              Expanded(
                child: _isLoading
                    ? const Center(child: CircularProgressIndicator(color: Colors.orange))
                    : _errorMessage.isNotEmpty
                        ? Center(
                            child: Text(
                              _errorMessage,
                              style: GoogleFonts.poppins(color: Colors.red, fontSize: 18),
                              textAlign: TextAlign.center,
                            ),
                          )
                        : _currentJoke != null
                            ? _buildJokeCard(_currentJoke!)
                            : const Center(child: Text('No joke available')),
              ),
            
              // Action buttons
              Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    if (_currentJoke != null && !_showPunchline)
                      ElevatedButton.icon(
                        onPressed: _revealPunchline,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.orange,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 32,
                            vertical: 16,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(30),
                          ),
                        ),
                        icon: const Icon(Icons.visibility),
                        label: Text(
                          'Show Punchline',
                          style: GoogleFonts.poppins(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    const SizedBox(height: 12),
                    ElevatedButton.icon(
                      onPressed: _isLoading ? null : _fetchNewJoke,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 32,
                          vertical: 16,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      icon: const Icon(Icons.refresh),
                      label: Text(
                        'Another Joke',
                        style: GoogleFonts.poppins(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
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

  Widget _buildJokeCard(Joke joke) {
    return Center(
      child: Card(
        elevation: 10,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        margin: const EdgeInsets.symmetric(horizontal: 16),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          padding: const EdgeInsets.all(32),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Colors.orange[50]!,
                Colors.yellow[50]!,
              ],
            ),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Setup text
              Text(
                joke.setup,
                style: GoogleFonts.poppins(
                  fontSize: 22,
                  fontWeight: FontWeight.w600,
                  color: Colors.black87,
                  height: 1.4,
                ),
                textAlign: TextAlign.center,
              ),
          
              const SizedBox(height: 30),
          
              // Punchline (revealed after tap)
              if (_showPunchline)
                AnimatedOpacity(
                  opacity: _showPunchline ? 1.0 : 0.0,
                  duration: const Duration(milliseconds: 500),
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.yellow[200],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.coronation, color: Colors.orange, size: 30),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            joke.punchline,
                            style: GoogleFonts.poppins(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: Colors.orange[800],
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
          
              // Hint to reveal
              if (!_showPunchline)
                const Text(
                  'Tap below to reveal the punchline!',
                  style: TextStyle(color: Colors.grey, fontSize: 14),
                ),
          
              const SizedBox(height: 16),
          
              // Joke type badge
              Chip(
                backgroundColor: Colors.orange[100],
                label: Text(
                  joke.type.toUpperCase(),
                  style: GoogleFonts.poppins(
                    color: Colors.orange[800],
                    fontSize: 12,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
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
- Add joke categories (programming, dad jokes, etc.)
- Add a "favorite jokes" feature
- Add share functionality to send jokes to friends
- Add offline joke storage for when internet is unavailable
- Add a "joke of the hour" timer for automatic refresh

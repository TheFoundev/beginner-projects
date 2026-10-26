# Project 14 - Whack-a-Mole (Flutter)

## 1. Project Title
**Whack-a-Mole**

## 2. The Concept
This app is a speed-based reflex game where cartoon moles pop up from holes, and you tap them as fast as you can to earn points. The faster you tap, the higher your score. Behind the scenes, the app uses a timer to randomly decide which "hole" a mole should appear in, keeps the mole visible for a few seconds, then removes it — like a pigeon racing game where you need quick reflexes to catch them before they duck back.

## 3. What You Will Build/Do
You'll create a 3x3 grid of holes. Random moles pop up for 2-3 seconds each, and you tap them to score points. A countdown timer adds pressure — you try to score as many points as possible in 30 seconds. The final app looks like a carnival whack-a-mole machine, complete with score and timer displays!

## 4. Core App Concept
**Timer-Based Game Loops with Random Spawning** — The app runs repeatedly (like a metronome) checking "every second, should a mole appear?" It picks a random hole, shows the mole, and after a few seconds, removes it. Just like a carnival game operator who pops moles up and down on a schedule.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone

## 6. What You Will Learn
- Using timers (`Timer.periodic`) for game loops
- Managing dynamic content (showing/hiding items)
- Tracking scores and game state
- Building a responsive grid with animations

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create whack_a_mole
cd whack_a_mole
```

### Step 2: Complete Source Code

```dart
import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const WhackAMoleApp());
}

class WhackAMoleApp extends StatelessWidget {
  const WhackAMoleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Whack-a-Mole',
      theme: ThemeData(
        primarySwatch: Colors.brown,
        useMaterial3: true,
      ),
      home: const WhackAMoleHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class WhackAMoleHome extends StatefulWidget {
  const WhackAMoleHome({super.key});

  @override
  State<WhackAMoleHome> createState() => _WhackAMoleHomeState();
}

class _WhackAMoleHomeState extends State<WhackAMoleHome> {
  final Random _random = Random();
  
  // Game state
  List<bool> _molesVisible = List.filled(9, false);
  int _score = 0;
  int _timeLeft = 30;
  bool _isGameActive = false;
  Timer? _gameTimer;
  Timer? _spawnTimer;
  
  static const int gridSize = 3; // 3x3 grid
  static const int gameDuration = 30; // 30 seconds

  @override
  void dispose() {
    _gameTimer?.cancel();
    _spawnTimer?.cancel();
    super.dispose();
  }

  void _startGame() {
    setState(() {
      _score = 0;
      _timeLeft = gameDuration;
      _isGameActive = true;
      _molesVisible = List.filled(9, false);
    });

    // Main game timer (counts down)
    _gameTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _timeLeft--;
      });
      
      if (_timeLeft <= 0) {
        timer.cancel();
        _spawnTimer?.cancel();
        setState(() {
          _isGameActive = false;
          _molesVisible = List.filled(9, false);
        });
        _showGameOverDialog();
      }
    });

    // Mole spawn timer
    _spawnTimer = Timer.periodic(const Duration(milliseconds: 800), (timer) {
      _spawnRandomMole();
    });
  }

  void _spawnRandomMole() {
    // Hide all moles first
    setState(() {
      _molesVisible = List.filled(9, false);
    });
    
    // Show a random mole
    final randomIndex = _random.nextInt(9);
    setState(() {
      _molesVisible[randomIndex] = true;
    });
    
    // Hide after 2 seconds
    Timer(const Duration(milliseconds: 1500), () {
      if (_isGameActive) {
        setState(() {
          _molesVisible = List.filled(9, false);
        });
      }
    });
  }

  void _whackMole(int index) {
    if (!_molesVisible[index] || !_isGameActive) return;
    
    setState(() {
      _molesVisible[index] = false;
      _score += 10; // 10 points per mole
    });
  }

  void _showGameOverDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          backgroundColor: Colors.brown[100],
          title: const Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.emoji_events, size: 40, color: Colors.amber),
              SizedBox(width: 8),
              Text('Game Over!'),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Your Score: $_score',
                style: const TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Colors.brown,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Moles whacked per second: ${(_score / 10 / gameDuration).toStringAsFixed(1)}',
                style: const TextStyle(fontSize: 14),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                _startGame();
              },
              child: const Text(
                'Play Again',
                style: TextStyle(color: Colors.brown, fontSize: 16),
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Whack-a-Mole'),
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.brown[200]!, Colors.brown[400]!],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Stats row
              Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildStat('Score', _score, Colors.green),
                    _buildStat('Time', _timeLeft, _timeLeft > 10 ? Colors.orange : Colors.red),
                  ],
                )),
              
              // Game grid
              Expanded(
                child: GridView.builder(
                  padding: const EdgeInsets.all(16),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: gridSize,
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.0,
                  ),
                  itemCount: 9,
                  itemBuilder: (context, index) {
                    return GestureDetector(
                      onTap: () => _whackMole(index),
                      child: Container(
                        decoration: BoxDecoration(
                          color: Colors.brown[600],
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: Colors.brown[800]!,
                            width: 3,
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.3),
                              blurRadius: 8,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: _molesVisible[index]
                            ? Stack(
                                alignment: Alignment.bottomCenter,
                                children: [
                                  AnimatedContainer(
                                    duration: const Duration(milliseconds: 200),
                                    curve: Curves.elasticOut,
                                    transform: Matrix4.diagonal3Values(1.2, 1.2, 1.0),
                                    child: const CircleAvatar(
                                      radius: 35,
                                      backgroundColor: Colors.brown,
                                      child: Icon(
                                        Icons.pets,
                                        size: 40,
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                  Positioned(
                                    bottom: 0,
                                    child: Container(
                                      width: 30,
                                      height: 15,
                                      decoration: BoxDecoration(
                                        color: Colors.brown[800],
                                        borderRadius: BorderRadius.circular(15),
                                      ),
                                    ),
                                  ),
                                ],
                              )
                            : const Icon(Icons.grade, size: 30, color: Colors.brown[300]),
                      ),
                    );
                  },
                ),
              ),
              
              // Start/Stop button
              if (!_isGameActive)
                Padding(
                  padding: const EdgeInsets.all(24),
                  child: ElevatedButton.icon(
                    onPressed: _startGame,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 40,
                        vertical: 20,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                    ),
                    icon: const Icon(Icons.play_arrow, size: 30),
                    label: const Text(
                      'Start Game',
                      style: TextStyle(fontSize: 20, color: Colors.white),
                    ),
                  ),
                ),
              
              if (_isGameActive)
                const SizedBox(height: 80),
            ],
          ),
        ),
      ));
  }

  Widget _buildStat(String label, int value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            blurRadius: 8,
          ),
        ],
      ),
      child: Row(
        children: [
          Icon(
            label == 'Score' ? Icons.stars : Icons.timer,
            color: color,
            size: 24,
          ),
          const SizedBox(width: 8),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
              Text(
                value.toString(),
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
            ],
          ),
        ],
      ));
  }
}
```

### Step 3: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add levels with faster mole spawns
- Add a high score tracking system
- Add sound effects for whacks and misses
- Add different mole types with different point values
- Add a "double points" power-up mode

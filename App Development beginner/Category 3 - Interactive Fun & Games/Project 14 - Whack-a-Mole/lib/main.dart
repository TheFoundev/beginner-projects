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
  
  List<bool> _molesVisible = List.filled(9, false);
  int _score = 0;
  int _timeLeft = 30;
  bool _isGameActive = false;
  Timer? _gameTimer;
  Timer? _spawnTimer;
  
  static const int gridSize = 3;
  static const int gameDuration = 30;

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

    _spawnTimer = Timer.periodic(const Duration(milliseconds: 800), (timer) {
      _spawnRandomMole();
    });
  }

  void _spawnRandomMole() {
    setState(() {
      _molesVisible = List.filled(9, false);
    });
    
    final randomIndex = _random.nextInt(9);
    setState(() {
      _molesVisible[randomIndex] = true;
    });
    
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
      _score += 10;
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
              Text(
                'Game Over!',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.brown,
                ),
              ),
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
                'Whacks per second: ${(_score / 10 / gameDuration).toStringAsFixed(1)}',
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
                    _buildStat('Time', _timeLeft, _timeLeft > 10 ? Colors.green : Colors.red),
                  ],
                ),
              ),
          
              // Game grid
              Expanded(
                child: GridView.builder(
                  padding: const EdgeInsets.all(16),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: gridSize,
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                  ),
                  itemCount: 9,
                  itemBuilder: (context, index) {
                    return GestureDetector(
                      onTap: () => _whackMole(index),
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 200),
                        decoration: BoxDecoration(
                          color: Colors.brown[600],
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: Colors.brown[800]!,
                            width: 2,
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.2),
                              blurRadius: 4,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        child: _molesVisible[index]
                            ? Stack(
                                alignment: Alignment.bottomCenter,
                                children: [
                                  const CircleAvatar(
                                    radius: 28,
                                    backgroundColor: Colors.brown,
                                    child: Icon(
                                      Icons.pets,
                                      size: 32,
                                      color: Colors.white,
                                    ),
                                  ),
                                  Positioned(
                                    bottom: 0,
                                    child: Container(
                                      width: 24,
                                      height: 10,
                                      decoration: BoxDecoration(
                                        color: Colors.brown[800],
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                    ),
                                  ),
                                ],
                              )
                            : const Icon(
                                Icons.grade,
                                size: 30,
                                color: Colors.brown,
                              ),
                      ),
                    );
                  },
                ),
              ),
              
              if (!_isGameActive)
                Padding(
                  padding: const EdgeInsets.all(24),
                  child: ElevatedButton.icon(
                    onPressed: _startGame,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
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
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              
              if (_isGameActive)
                const SizedBox(height: 80),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStat(String label, int value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.brown.withOpacity(0.3),
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
      ),
    );
  }
}

import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const NumberGuesserApp());
}

class NumberGuesserApp extends StatelessWidget {
  const NumberGuesserApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Number Guessing Game',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        brightness: Brightness.light,
      ),
      home: const NumberGuesserHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class NumberGuesserHome extends StatefulWidget {
  const NumberGuesserHome({super.key});

  @override
  State<NumberGuesserHome> createState() => _NumberGuesserHomeState();
}

class _NumberGuesserHomeState extends State<NumberGuesserHome> {
  final Random _random = Random();
  final TextEditingController _guessController = TextEditingController();
  
  late int _secretNumber;
  int _guessCount = 0;
  String _message = "I'm thinking of a number between 1 and 100!";
  Color _messageColor = Colors.black87;
  bool _gameOver = false;

  @override
  void initState() {
    super.initState();
    _startNewGame();
  }

  void _startNewGame() {
    setState(() {
      _secretNumber = _random.nextInt(100) + 1;
      _guessCount = 0;
      _message = "I'm thinking of a number between 1 and 100!";
      _messageColor = Colors.black87;
      _gameOver = false;
      _guessController.clear();
    });
  }

  void _submitGuess() {
    final guessText = _guessController.text.trim();
    final guess = int.tryParse(guessText);

    if (guess == null) {
      setState(() {
        _message = "Please enter a valid number!";
        _messageColor = Colors.red;
      });
      return;
    }

    if (guess < 1 || guess > 100) {
      setState(() {
        _message = "Please enter a number between 1 and 100!";
        _messageColor = Colors.red;
      });
      return;
    }

    if (_gameOver) {
      setState(() {
        _message = "Game over! Press 'New Game' to play again.";
        _messageColor = Colors.orange;
      });
      return;
    }

    setState(() {
      _guessCount++;
      
      if (guess == _secretNumber) {
        _message = "🎉 You got it! The number was $_secretNumber!\nYou found it in $_guessCount guesses!";
        _messageColor = Colors.green;
        _gameOver = true;
      } else if (guess < _secretNumber) {
        _message = "📈 Too Low! Try a higher number.";
        _messageColor = Colors.blue;
      } else {
        _message = "📉 Too High! Try a lower number.";
        _messageColor = Colors.blue;
      }
    });
    
    _guessController.clear();
    FocusScope.of(context).unfocus();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Number Guessing Game'),
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.purple[50]!, Colors.deepPurple[50]!],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                
                // Game title/icon
                const Icon(
                  Icons.question_answer,
                  size: 80,
                  color: Colors.purple,
                ),
                const SizedBox(height: 16),
              
                // Message
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.purple.withOpacity(0.15),
                        blurRadius: 15,
                        offset: const Offset(0, 5),
                      ),
                    ],
                  ),
                  child: Text(
                    _message,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: _guessCount >= 3 ? 18 : 22,
                      color: _messageColor,
                      height: 1.4,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
              
                // Guess counter
                Center(
                  child: Chip(
                    backgroundColor: Colors.purple[100],
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 8,
                    ),
                    label: Text(
                      'Guesses: $_guessCount',
                      style: const TextStyle(
                        color: Colors.purple,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
              
                // Input section
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _guessController,
                        keyboardType: TextInputType.number,
                        decoration: InputDecoration(
                          labelText: 'Your guess (1-100)',
                          border: const OutlineInputBorder(),
                          hintText: 'Type here...',
                        ),
                        onSubmitted: (value) => _submitGuess(),
                      ),
                    ),
                    const SizedBox(width: 8),
                    IconButton(
                      icon: const Icon(Icons.send, size: 30, color: Colors.purple),
                      onPressed: _submitGuess,
                    ),
                  ],
                ),
                const SizedBox(height: 16),
              
                // Submit button
                ElevatedButton(
                  onPressed: _submitGuess,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.purple,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    'Submit Guess',
                    style: TextStyle(fontSize: 18, color: Colors.white),
                  ),
                ),
                const SizedBox(height: 16),
              
                // New Game button
                if (_gameOver)
                  ElevatedButton.icon(
                    onPressed: _startNewGame,
                    icon: const Icon(Icons.refresh),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      'Play Again?',
                      style: TextStyle(fontSize: 18, color: Colors.white),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

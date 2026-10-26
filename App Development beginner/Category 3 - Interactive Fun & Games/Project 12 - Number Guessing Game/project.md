# Project 12 - Number Guessing Game (Flutter)

## 1. Project Title
**Number Guessing Game**

## 2. The Concept
This app thinks of a random number between 1 and 100, and you try to guess it. After each guess, the app tells you whether to go "Higher" or "Lower" — like a game of hot-and-cold. Behind the scenes, the app generates a secret random number (like writing a number on a piece of paper and hiding it), and each guess gets compared to that secret number using greater-than/less-than logic. It's like having a magic friend who knows a secret number and gives you hints until you crack the code!

## 3. What You Will Build/Do
You'll build an app with a number input field, a "Guess" button, and a result message area. Each guess gets feedback: "Too High!", "Too Low!", or "You Got It!". A guess counter shows how many attempts you took, and a reset button starts a new game. The final app looks like a clean, interactive puzzle game with satisfying feedback.

## 4. Core App Concept
**Input Validation and Comparison Logic** — The app reads a number from the user, compares it to a secret value, and gives feedback based on whether it's greater than, less than, or equal to that secret. Like a bouncer at an exclusive club door who checks your number against the secret guest list and points you in the right direction.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone

## 6. What You Will Learn
- Reading and parsing user input from text fields
- Generating and storing secret random values
- Implementing comparison logic with conditional feedback
- Managing game state (ongoing vs. finished)

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create number_guesser
cd number_guesser
```

### Step 2: Complete Source Code

```dart
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
      title: 'Number Guesser',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        useMaterial3: true,
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
  String _messageColor = '';
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
      _messageColor = '';
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
        _messageColor = 'error';
      });
      return;
    }

    if (guess < 1 || guess > 100) {
      setState(() {
        _message = "Please enter a number between 1 and 100!";
        _messageColor = 'error';
      });
      return;
    }

    if (_gameOver) {
      setState(() {
        _message = "Game over! Press 'New Game' to play again.";
        _messageColor = 'info';
      });
      return;
    }

    setState(() {
      _guessCount++;
      
      if (guess == _secretNumber) {
        _message = "🎉 You got it! The number was $_secretNumber!\nYou found it in $_guessCount guesses!";
        _messageColor = 'success';
        _gameOver = true;
      } else if (guess < _secretNumber) {
        _message = "📈 Too Low! Try a higher number.";
        _messageColor = 'hint';
      } else {
        _message = "📉 Too High! Try a lower number.";
        _messageColor = 'hint';
      }
    });
    
    _guessController.clear();
    FocusScope.of(context).unfocus();
  }

  Color _getMessageColor() {
    switch (_messageColor) {
      case 'success':
        return Colors.green;
      case 'error':
        return Colors.red;
      case 'hint':
        return Colors.blue;
      case 'info':
        return Colors.orange;
      default:
        return Colors.black87;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Number Guessing Game'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _startNewGame,
            tooltip: 'New Game',
          ),
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.purple[50]!, Colors.deepPurple[100]!],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
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
                      color: _getMessageColor(),
                      height: 1.5,
                    ),
                  ),
                ),
                const SizedBox(height: 24),
              
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
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.purple,
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
```

### Step 3: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Show a hint about how close the last guess was
- Add difficulty levels (1-100, 1-1000, etc.)
- Add a history of guesses made
- Add sound effects for correct/incorrect guesses
- Add a leaderboard tracking best scores

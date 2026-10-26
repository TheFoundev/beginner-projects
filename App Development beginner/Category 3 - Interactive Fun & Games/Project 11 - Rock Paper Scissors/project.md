# Project 11 - Rock Paper Scissors (Flutter)

## 1. Project Title
**Rock Paper Scissors**

## 2. The Concept
This app lets you play the classic hand game against your phone. You tap rock, paper, or scissors, and the phone picks one randomly too. Then it compares both choices — rock crushes scissors, paper covers rock, scissors cuts paper — and declares the winner. It's like having a friend to play with, except your opponent never gets bored! Behind the scenes, the app uses randomness to pick the computer's choice and simple if/else logic to determine who wins.

## 3. What You Will Build/Do
You'll build an app with three choice buttons (rock, paper, scissors emojis). Tap any button, and the screen shows both your choice and the phone's random choice, plus the winner. The final app looks like a friendly game board — bright, colorful, and ready for endless rounds of play.

## 4. Core App Concept
**Conditional Logic** — The app evaluates certain conditions (if this happens, do that; otherwise, do this). Like a decision tree in a "Choose Your Own Adventure" book — based on your choice and a random roll, the story (game) takes a specific path to one of three possible endings.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone

## 6. What You Will Learn
- Handling multiple button presses with different outcomes
- Using random number generators and enum-like choices
- Implementing game logic with if/else conditionals
- Building a responsive, game-like UI

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create rps_game
cd rps_game
```

### Step 2: Complete Source Code

```dart
import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const RPSGameApp());
}

class RPSGameApp extends StatelessWidget {
  const RPSGameApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rock Paper Scissors',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const RPSGameHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

enum Choice { rock, paper, scissors }

class RPSGameHome extends StatefulWidget {
  const RPSGameHome({super.key});

  @override
  State<RPSGameHome> createState() => _RPSGameHomeState();
}

class _RPSGameHomeState extends State<RPSGameHome> {
  final Random _random = Random();
  Choice? _playerChoice;
  Choice? _computerChoice;
  String _result = '';
  int _playerScore = 0;
  int _computerScore = 0;

  static const Map<Choice, String> choiceEmojis = {
    Choice.rock: '✊',
    Choice.paper: '✋',
    Choice.scissors: '✌️',
  };

  void _playGame(Choice playerChoice) {
    final computerChoice = _getRandomChoice();
    
    setState(() {
      _playerChoice = playerChoice;
      _computerChoice = computerChoice;
      _result = _determineWinner(playerChoice, computerChoice);
      
      // Update scores
      if (_result.contains('You Win')) {
        _playerScore++;
      } else if (_result.contains('Computer Wins')) {
        _computerScore++;
      }
    });
  }

  Choice _getRandomChoice() {
    final values = Choice.values;
    return values[_random.nextInt(values.length)];
  }

  String _determineWinner(Choice player, Choice computer) {
    // Rock beats Scissors, Scissors beats Paper, Paper beats Rock
    if (player == computer) {
      return "It's a Tie! 🤝";
    }
    
    if ((player == Choice.rock && computer == Choice.scissors) ||
        (player == Choice.paper && computer == Choice.rock) ||
        (player == Choice.scissors && computer == Choice.paper)) {
      return "You Win! 🎉";
    }
    
    return "Computer Wins! 💻";
  }

  String _getChoiceName(Choice choice) {
    switch (choice) {
      case Choice.rock:
        return 'Rock';
      case Choice.paper:
        return 'Paper';
      case Choice.scissors:
        return 'Scissors';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Rock Paper Scissors'),
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.blue[50]!, Colors.blue[100]!],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Scores display
              Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Column(
                      children: [
                        const Text('YOU', style: TextStyle(fontSize: 14)),
                        Text(
                          '$_playerScore',
                          style: const TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue,
                          ),
                        ),
                      ],
                    ),
                    Column(
                      children: [
                        const Text('COMPUTER', style: TextStyle(fontSize: 14)),
                        Text(
                          '$_computerScore',
                          style: const TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.red,
                          ),
                        ),
                      ],
                    ),
                  ],
                )),
              
              // Game area
              Expanded(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    // Player side
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text(
                            'Your Choice',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            _playerChoice != null
                                ? choiceEmojis[_playerChoice]!
                                : '❔',
                            style: const TextStyle(fontSize: 70),
                          ),
                          Text(
                            _playerChoice != null
                                ? _getChoiceName(_playerChoice!)
                                : 'Choose!',
                            style: const TextStyle(fontSize: 16),
                          ),
                        ],
                      ),
                    ),
                
                    const SizedBox(width: 16),
                
                    // vs label
                    const Text(
                      'VS',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.grey,
                      ),
                    ),
                
                    const SizedBox(width: 16),
                
                    // Computer side
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Text(
                            'Computer\'s Choice',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            _computerChoice != null
                                ? choiceEmojis[_computerChoice]!
                                : '❔',
                            style: const TextStyle(fontSize: 70),
                          ),
                          Text(
                            _computerChoice != null
                                ? _getChoiceName(_computerChoice!)
                                : '?',
                            style: const TextStyle(fontSize: 16),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            
              // Result
              if (_result.isNotEmpty)
                AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  padding: const EdgeInsets.all(20),
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: _result.contains('Win')
                        ? Colors.green[100]
                        : _result.contains('Tie')
                            ? Colors.orange[100]
                            : Colors.red[100],
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(
                    _result,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: _result.contains('Win')
                          ? Colors.green[700]
                          : _result.contains('Tie')
                              ? Colors.orange[700]
                              : Colors.red[700],
                    ),
                  ),
                ),
            
              // Choice buttons
              Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildChoiceButton(Choice.rock, '✊', Colors.brown),
                    _buildChoiceButton(Choice.paper, '✋', Colors.blue),
                    _buildChoiceButton(Choice.scissors, '✌️', Colors.red),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildChoiceButton(Choice choice, String emoji, Color color) {
    return GestureDetector(
      onTap: () => _playGame(choice),
      child: Container(
        width: 70,
        height: 70,
        decoration: BoxDecoration(
          color: color.withOpacity(0.2),
          shape: BoxShape.circle,
          border: Border.all(color: color, width: 3),
        ),
        child: Center(
          child: Text(
            emoji,
            style: const TextStyle(fontSize: 36),
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
- Add a best-of-5 game mode
- Add sound effects for win/lose/tie
- Show an animated countdown before the computer "chooses"
- Add a reset score button
- Add a history of past games

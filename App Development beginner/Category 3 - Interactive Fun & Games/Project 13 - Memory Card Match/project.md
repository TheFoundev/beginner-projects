# Project 13 - Memory Card Match (Flutter)

## 1. Project Title
**Memory Card Match**

## 2. The Concept
This app is a classic memory matching game. A grid of cards is face-down on the screen, and you tap two cards to flip them face-up. If they match, they stay revealed; if they don't, they flip back down. It's like the physical card game Concentration — you're trying to remember where you've seen each symbol before. Behind the scenes, the app tracks which cards are flipped, compares pairs, and uses a timer to control the flip-back animation, keeping everything in sync like a well-rehearsed card trick.

## 3. What You Will Build/Do
You'll create a 4x4 grid of cards with matching emoji pairs hidden face-down. Tap any card to flip it, tap a second card to see if they match. Matched pairs stay visible in green; unmatched pairs flip back after 1.5 seconds. Your move count is tracked at the top. The final app looks like a polished card game ready for hours of entertainment!

## 4. Core App Concept
**Grid Layout and State Tracking** — The app displays items in a grid structure (rows and columns), keeps track of which items are currently "flipped," and manages game state (first selection, second selection, match, no match). Like a chessboard that remembers where each piece is and updates the board after each move.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone

## 6. What You Will Learn
- Building responsive grid layouts
- Managing complex state (multiple selections, matches, flips)
- Using timers for delayed actions
- Building interactive card-flip animations

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create memory_game
cd memory_game
```

### Step 2: Complete Source Code

```dart
import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const MemoryGameApp());
}

class MemoryGameApp extends StatelessWidget {
  const MemoryGameApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Memory Card Match',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        useMaterial3: true,
      ),
      home: const MemoryGameHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// Individual card model
class CardItem {
  final String emoji;
  bool isFaceUp = false;
  bool isMatched = false;

  CardItem({required this.emoji});
}

class MemoryGameHome extends StatefulWidget {
  const MemoryGameHome({super.key});

  @override
  State<MemoryGameHome> createState() => _MemoryGameHomeState();
}

class _MemoryGameHomeState extends State<MemoryGameHome> {
  final Random _random = Random();
  List<CardItem> _cards = [];
  CardItem? _firstCard;
  CardItem? _secondCard;
  bool _isBusy = false;
  int _moves = 0;
  int _matches = 0;
  
  static const List<String> emojis = [
    '🐱', '🐶', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁',
  ];

  @override
  void initState() {
    super.initState();
    _initializeGame();
  }

  void _initializeGame() {
    // Create pairs of cards
    List<String> gameEmojis = [];
    for (int i = 0; i < 8; i++) {
      gameEmojis.add(emojis[i]);
      gameEmojis.add(emojis[i]); // Each emoji has a pair
    }
    
    // Shuffle the cards
    gameEmojis.shuffle(_random);
    
    setState(() {
      _cards = gameEmojis.map((emoji) => CardItem(emoji: emoji)).toList();
      _firstCard = null;
      _secondCard = null;
      _isBusy = false;
      _moves = 0;
      _matches = 0;
    });
  }

  void _handleCardTap(CardItem card) {
    if (_isBusy || card.isFaceUp || card.isMatched) return;

    setState(() {
      card.isFaceUp = true;
      
      if (_firstCard == null) {
        _firstCard = card;
      } else if (_secondCard == null) {
        _secondCard = card;
        _moves++;
        
        if (_firstCard!.emoji == _secondCard!.emoji) {
          // Match found!
          _firstCard!.isMatched = true;
          _secondCard!.isMatched = true;
          _matches++;
          _firstCard = null;
          _secondCard = null;
          
          if (_matches == 8) {
            // Game won! Show dialog after slight delay
            Future.delayed(const Duration(milliseconds: 300), () {
              _showGameWonDialog();
            });
          }
        } else {
          // No match - flip cards back
          _isBusy = true;
          Future.delayed(const Duration(milliseconds: 1000), () {
            setState(() {
              _firstCard!.isFaceUp = false;
              _secondCard!.isFaceUp = false;
              _firstCard = null;
              _secondCard = null;
              _isBusy = false;
            });
          });
        }
      }
    });
  }

  void _showGameWonDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.emoji_events, size: 60, color: Colors.amber),
              const SizedBox(height: 16),
              const Text(
                'Congratulations!',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
              ),
              Text(
                'You found all pairs in $_moves moves!',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                _initializeGame();
              },
              child: const Text(
                'Play Again',
                style: TextStyle(color: Colors.teal, fontSize: 16),
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
        title: const Text('Memory Card Match'),
        centerTitle: true,
        actions: [
          if (_matches < 8 && _cards.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.refresh),
              onPressed: _initializeGame,
              tooltip: 'Restart Game',
            ),
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.teal[50]!, Colors.blue[50]!],
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
                    _buildStatCard('Moves', _moves),
                    _buildStatCard('Matches', _matches),
                    _buildStatCard('Remaining', 16 - _matches * 2),
                  ],
                )),
              
              // Grid of cards
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: GridView.builder(
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 4,
                      crossAxisSpacing: 8,
                      mainAxisSpacing: 8,
                      childAspectRatio: 0.8,
                    ),
                    itemCount: _cards.length,
                    itemBuilder: (context, index) {
                      final card = _cards[index];
                      return GestureDetector(
                        onTap: () => _handleCardTap(card),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          decoration: BoxDecoration(
                            color: card.isFaceUp || card.isMatched
                                ? Colors.white
                                : Colors.teal,
                            borderRadius: BorderRadius.circular(12),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.15),
                                blurRadius: 8,
                                offset: const Offset(0, 4),
                              ),
                            ],
                            border: card.isFaceUp
                                ? Border.all(color: Colors.teal, width: 2)
                                : null,
                          ),
                          child: Center(
                            child: card.isFaceUp
                                ? Text(
                                    card.emoji,
                                    style: const TextStyle(fontSize: 36),
                                  )
                                : const Icon(
                                    Icons.question_mark,
                                    size: 30,
                                    color: Colors.white70,
                                  ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ),
              
              // Footer hint
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text(
                  _isBusy
                      ? '...'
                      : _firstCard != null
                          ? 'Find the matching ${_firstCard!.emoji}!'
                          : 'Flip two cards to start!',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.teal[700],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatCard(String label, int value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.teal.withOpacity(0.15),
            blurRadius: 8,
          ),
        ],
      ),
      child: Column(
        children: [
          Text(
            value.toString(),
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.teal,
            ),
          ),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey[600],
            ),
          ),
        ],
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
- Add difficulty levels (4x4, 6x6 grids)
- Add a timer to track completion time
- Add sound effects for matches and flips
- Add different themes (animals, food, flags)
- Save best scores locally

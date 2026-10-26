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
    List<String> gameEmojis = [];
    for (int i = 0; i < 8; i++) {
      gameEmojis.add(emojis[i]);
      gameEmojis.add(emojis[i]);
    }
    gameEmojis.shuffle(_random);

    setState(() {
      _cards = gameEmojis.map((emoji) => CardItem(emoji: emoji)).toList();
      _firstCard = null;
      _secondCard = null;
      _moves = 0;
      _matches = 0;
    });
  }

  void _handleCardTap(CardItem card) {
    if (_firstCard == null) {
      setState(() {
        card.isFaceUp = true;
        _firstCard = card;
      });
    } else if (_secondCard == null) {
      setState(() {
        card.isFaceUp = true;
        _secondCard = card;
        _moves++;
      });

      if (_firstCard!.emoji == _secondCard!.emoji) {
        setState(() {
          _firstCard!.isMatched = true;
          _secondCard!.isMatched = true;
          _matches++;
        });

        if (_matches == 8) {
          Future.delayed(const Duration(milliseconds: 300), () {
            _showGameWonDialog();
          });
        }
      } else {
        Future.delayed(const Duration(milliseconds: 1000), () {
          setState(() {
            _firstCard!.isFaceUp = false;
            _secondCard!.isFaceUp = false;
            _firstCard = null;
            _secondCard = null;
          });
        });
      }
    }
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
          backgroundColor: Colors.teal[50],
          title: const Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.emoji_events, size: 50, color: Colors.amber),
              SizedBox(height: 8),
              Text(
                'Congratulations!',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
              ),
            ],
          ),
          content: Text(
            'You found all 8 pairs in $_moves moves!',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 16),
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
                ),
              ),

              // Grid of cards
              Expanded(
                child: GridView.builder(
                  itemCount: _cards.length,
                  padding: const EdgeInsets.all(12),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 4,
                    crossAxisSpacing: 8,
                    mainAxisSpacing: 8,
                  ),
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
                              color: Colors.black.withOpacity(0.1),
                              blurRadius: 4,
                            ),
                          ],
                          border: Border.all(
                            color: card.isFaceUp
                                ? Colors.teal
                                : Colors.teal,
                            width: card.isFaceUp ? 2 : 0,
                          ),
                        ),
                        child: Center(
                          child: card.isFaceUp
                              ? Text(
                                  card.emoji,
                                  style: const TextStyle(fontSize: 32),
                                )
                              : const Icon(
                                  Icons.question_mark,
                                  size: 32,
                                  color: Colors.white70,
                                ),
                        ),
                      ),
                    );
                  },
                ),
              ),

              // Hint
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text(
                  _firstCard != null && _secondCard == null
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
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.teal.withOpacity(0.1),
            blurRadius: 4,
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

# Project 7 - Digital Dice Roller (Flutter)

## 1. Project Title
**Digital Dice Roller**

## 2. The Concept
This app replaces a physical dice with a virtual one on your screen. You tap a "Roll" button, and the app generates a random number between 1 and 6 — just like rolling a real dice. Behind the scenes, the app uses a random number generator (RNG), which is like a digital version of shaking a dice cup: the math picks a number from the hat without you knowing which one it'll pull out.

## 3. What You Will Build/Do
You'll create an app with a large dice graphic that changes to show one of six faces (1 through 6) each time you tap the Roll button. The final app looks like a single digital dice on a nice background — tap roll, and the dice animates to a new random face. You can use it for board games, homework, or just for fun!

## 4. Core App Concept
**Random Number Generation with UI Updates** — The app generates an unpredictable number behind the scenes and then instantly updates what you see on the screen based on that number. Like a lottery machine: the balls tumble randomly, and then the winning number is revealed in bright lights.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** (free) or **Android Studio** (free)
- **Android Studio Device Manager** (for emulator) or real Android/iOS phone

## 6. What You Will Learn
- Generating random numbers in Flutter
- Displaying different images or text based on state changes
- Building button-driven interactions with animations

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create dice_roller
cd dice_roller
```

### Step 2: Add Assets (Dice Images)
Create an `assets/images` folder and add dice face images (dice_1.png through dice_6.png). Alternatively, we'll use Unicode dice characters for simplicity (no assets needed). For a polished version with images, download free dice icons or create them.

### Step 3: Complete Source Code (Using Unicode characters - no assets needed)

```dart
import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(const DiceRollerApp());
}

class DiceRollerApp extends StatelessWidget {
  const DiceRollerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dice Roller',
      theme: ThemeData(
        primarySwatch: Colors.deepOrange,
        brightness: Brightness.light,
      ),
      home: const DiceRollerHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class DiceRollerHome extends StatefulWidget {
  const DiceRollerHome({super.key});

  @override
  State<DiceRollerHome> createState() => _DiceRollerHomeState();
}

class _DiceRollerHomeState extends State<DiceRollerHome>
    with SingleTickerProviderStateMixin {
  final Random _random = Random();
  int _diceValue = 1;
  int _totalRolls = 0;
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  // Unicode dice characters for each face (1-6)
  static const List<String> diceUnicode = [
    '⚀', // 1
    '⚁', // 2
    '⚂', // 3
    '⚃', // 4
    '⚄', // 5
    '⚅', // 6
  ];

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.3).animate(
      CurvedAnimation(parent: _controller, curve: Curves.elasticOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _rollDice() {
    setState(() {
      // Roll multiple times quickly for a realistic dice-rolling effect
      int tempValue = _diceValue;
      for (int i = 0; i < 10; i++) {
        tempValue = _random.nextInt(6) + 1;
      }
      _diceValue = tempValue;
      _totalRolls++;
    });
    _controller
      ..reset()
      ..forward();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Digital Dice Roller'),
        centerTitle: true,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Roll the Dice!',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.deepOrange,
                ),
              ),
              const SizedBox(height: 40),
              
              // Dice display with animation
              ScaleTransition(
                scale: _scaleAnimation,
                child: Container(
                  width: 150,
                  height: 150,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    border: Border.all(color: Colors.deepOrange, width: 4),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.deepOrange.withOpacity(0.3),
                        blurRadius: 15,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: Center(
                    child: AnimatedSwitcher(
                      duration: const Duration(milliseconds: 300),
                      transitionBuilder: (Widget child, Animation<double> animation) {
                        return ScaleTransition(scale: animation, child: child);
                      },
                      child: Text(
                        diceUnicode[_diceValue - 1],
                        key: ValueKey<int>(_diceValue),
                        style: const TextStyle(
                          fontSize: 80,
                          color: Colors.deepOrange,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              
              const SizedBox(height: 30),
              
              // Current value display
              Text(
                'Rolled: $_diceValue',
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                'Total Rolls: $_totalRolls',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _rollDice,
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
        icon: const Icon(Icons.casino, size: 30),
        label: const Text(
          'ROLL',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}

// ==================== ALTERNATIVE: Double Dice Version ====================
// NOTE: This is an optional extension. Use EITHER the single dice version above
// OR swap to this two-dice version. The DoubleDiceHome class is provided
// as a separate alternative — don't use both in the same main.dart.
class DoubleDiceHome extends StatefulWidget {
  const DoubleDiceHome({super.key});

  @override
  State<DoubleDiceHome> createState() => _DoubleDiceHomeState();
}

class _DoubleDiceHomeState extends State<DoubleDiceHome> {
  final Random _random = Random();
  int _dice1 = 1;
  int _dice2 = 1;

  static const List<String> diceUnicode = [
    '⚀', '⚁', '⚂', '⚃', '⚄', '⚅',
  ];

  void _rollBothDice() {
    setState(() {
      _dice1 = _random.nextInt(6) + 1;
      _dice2 = _random.nextInt(6) + 1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Double Dice')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildDice(_dice1),
                const SizedBox(width: 20),
                _buildDice(_dice2),
              ],
            ),
            const SizedBox(height: 20),
            Text(
              'Total: ${_dice1 + _dice2}',
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _rollBothDice,
        child: const Icon(Icons.casino),
      ),
    );
  }

  Widget _buildDice(int value) {
    return Container(
      width: 100,
      height: 100,
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: Colors.deepOrange, width: 3),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Center(
        child: Text(
          diceUnicode[value - 1],
          style: const TextStyle(fontSize: 50, color: Colors.deepOrange),
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
- Add a second dice for a board game experience
- Track statistics (how many times each number was rolled)
- Add realistic dice roll sound effects
- Add shake-to-roll using the accelerometer sensor
- Show a history of recent rolls

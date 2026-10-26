# Project 6 - Quick Tip Calculator (Flutter)

## 1. Project Title
**Quick Tip Calculator**

## 2. The Concept
This app calculates how much tip to leave at a restaurant. You enter your bill amount and pick a tip percentage (like 15% or 20%), and the app shows you exactly how much extra to pay and your total with tip. It works like a smart calculator — you give it numbers, and it does the math instantly. Behind the scenes, the app multiplies your bill by the percentage and adds it up, displaying the result on screen in real time.

## 3. What You Will Build/Do
You'll build a clean single-screen app with a bill input field, percentage buttons, and live-updating results. Enter "$50" and tap "20%" — the screen instantly shows "$10.00 tip" and "$60.00 total". The final app looks like a polished restaurant calculator you'd actually want to keep in your phone.

## 4. Core App Concept
**State Management (Flutter Stateful Widgets)** — The app keeps track of the current values (bill amount, selected tip) in its "memory," and when those values change, the screen automatically redraws itself with the new information. Like a calculator that updates its display as you type — the screen reacts instantly to your inputs.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** (free) or **Android Studio** (free)
- **Android Studio Device Manager** (for emulator) or a real Android/iOS phone
- Internet connection for `flutter pub get`

## 6. What You Will Learn
- Creating input fields and buttons with Flutter widgets
- Handling user input and updating state in real time
- Building responsive layouts with columns, rows, and padding

---

## Step-by-Step Instructions

### Step 1: Install Flutter
If you haven't installed Flutter yet:
1. Download from [flutter.dev](https://flutter.dev) and extract to `C:\src\flutter` (or your preferred location)
2. Add Flutter to your PATH
3. Run `flutter doctor` to verify installation

### Step 2: Create the Project
```bash
flutter create tip_calculator
cd tip_calculator
```

### Step 3: Replace lib/main.dart
Open `lib/main.dart` and replace its contents with the complete code below:

### Step 4: Complete Source Code

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const TipCalculatorApp());
}

class TipCalculatorApp extends StatelessWidget {
  const TipCalculatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tip Calculator',
      theme: ThemeData(
        primarySwatch: Colors.green,
        brightness: Brightness.light,
      ),
      home: const TipCalculatorHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class TipCalculatorHome extends StatefulWidget {
  const TipCalculatorHome({super.key});

  @override
  State<TipCalculatorHome> createState() => _TipCalculatorHomeState();
}

class _TipCalculatorHomeState extends State<TipCalculatorHome> {
  final TextEditingController _billController = TextEditingController();
  int _selectedTipIndex = 1; // Default to 15%
  
  static const List<int> tipPercents = [10, 15, 20, 25];

  double get billAmount {
    final value = double.tryParse(_billController.text) ?? 0.0;
    return value;
  }

  double get tipAmount {
    return (billAmount * tipPercents[_selectedTipIndex] / 100).roundToDouble();
  }

  double get totalAmount {
    return billAmount + tipAmount;
  }

  String get currency => "\$";

  FormatCurrency(double value) {
    return "$currency${value.toStringAsFixed(2)}";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Quick Tip Calculator'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Bill input section
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.grey[100],
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Bill Amount',
                    style: TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    controller: _billController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: 'Enter bill amount',
                      prefixText: currency,
                      border: const OutlineInputBorder(),
                      hintStyle: const TextStyle(fontSize: 18),
                    ),
                    style: const TextStyle(fontSize: 22),
                    onChanged: (value) {
                      setState(() {});
                    },
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 24),
            
            // Tip percentage buttons
            const Text(
              'Select Tip',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              alignment: WrapAlignment.center,
              children: List.generate(
                tipPercents.length,
                (index) {
                  final isSelected = index == _selectedTipIndex;
                  return ChoiceChip(
                    label: Text(
                      '${tipPercents[index]}%',
                      style: TextStyle(
                        fontSize: 18,
                        color: isSelected ? Colors.white : Colors.green,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                    ),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() {
                        _selectedTipIndex = index;
                      });
                    },
                    selectedColor: Colors.green,
                    backgroundColor: Colors.green[50],
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  );
                },
              ),
            ),
            
            const SizedBox(height: 32),
            
            // Results section
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.green[50],
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.green[200]!, width: 2),
              ),
              child: Column(
                children: [
                  const Text(
                    'Your Total',
                    style: TextStyle(fontSize: 18, color: Colors.grey),
                  ),
                  Text(
                    FormatCurrency(totalAmount),
                    style: const TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                      color: Colors.green,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Divider(color: Colors.green[200]),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Tip Amount:', style: TextStyle(fontSize: 16)),
                      Text(
                        FormatCurrency(tipAmount),
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.green,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Bill Total:', style: TextStyle(fontSize: 16)),
                      Text(
                        FormatCurrency(billAmount),
                        style: const TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 16),
            
            Text(
              'Based on ${tipPercents[_selectedTipIndex]}% tip',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 14, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Step 5: Run the App
```bash
# Install dependencies
flutter pub get

# Run on an emulator or connected device
flutter run
```

### How to Run on Your Phone:
1. Enable "Developer Options" on your Android phone
2. Enable "USB Debugging" and "Install via USB"
3. Connect your phone via USB
4. Run `flutter run` in the terminal
5. Select your device when prompted

## Extension Ideas
- Add a "Split Bill" feature to divide the total among friends
- Add a "Reset" button to clear the bill amount
- Store recent calculations in local storage
- Add custom tip percentage input

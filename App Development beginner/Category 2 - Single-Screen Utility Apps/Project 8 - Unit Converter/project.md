# Project 8 - Unit Converter (Flutter)

## 1. Project Title
**Unit Converter**

## 2. The Concept
This app converts measurements from one unit to another — like swapping currencies when you travel. Enter 100 kilometers and it instantly shows you 62.14 miles. It works behind the scenes using simple math formulas: the app multiplies your input by a fixed conversion rate (just like a currency exchange booth). The key insight is that each unit pair has a consistent ratio — 1 kilometer always equals 0.6214 miles, so the math never changes.

## 3. What You Will Build/Do
You'll create an app with a scrollable list of conversion categories (distance, weight, temperature). Tap on "Kilometers to Miles," enter a number, and see the converted result live as you type. The final app looks like a handy travel tool — perfect for homework, cooking, or international trips.

## 4. Core App Concept
**Reusable Components and Data Structures** — Instead of building each converter separately, the app stores all conversion formulas in a single "recipe book" (a list of data). Like a cookbook where one recipe card holds all the info (name, ingredients, steps) — each converter is one card with its own formula.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone

## 6. What You Will Learn
- Creating reusable components (widgets) that work with different data
- Using lists and maps to store structured data
- Building responsive layouts that adapt to different screen sizes

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create unit_converter
cd unit_converter
```

### Step 2: Complete Source Code

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const UnitConverterApp());
}

class UnitConverterApp extends StatelessWidget {
  const UnitConverterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Unit Converter',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const UnitConverterHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// Data model for a conversion unit
class ConversionUnit {
  final String name;
  final String fromUnit;
  final String toUnit;
  final double Function(double) convert;
  final String formula;

  ConversionUnit({
    required this.name,
    required this.fromUnit,
    required this.toUnit,
    required this.convert,
    required this.formula,
  });
}

// Define all conversion units
final List<ConversionUnit> conversionUnits = [
  ConversionUnit(
    name: 'Distance',
    fromUnit: 'Kilometers',
    toUnit: 'Miles',
    convert: (km) => km * 0.621371,
    formula: 'miles = km × 0.621371',
  ),
  ConversionUnit(
    name: 'Distance (Reverse)',
    fromUnit: 'Miles',
    toUnit: 'Kilometers',
    convert: (miles) => miles * 1.60934,
    formula: 'km = miles × 1.60934',
  ),
  ConversionUnit(
    name: 'Weight',
    fromUnit: 'Kilograms',
    toUnit: 'Pounds',
    convert: (kg) => kg * 2.20462,
    formula: 'lbs = kg × 2.20462',
  ),
  ConversionUnit(
    name: 'Weight (Reverse)',
    fromUnit: 'Pounds',
    toUnit: 'Kilograms',
    convert: (lbs) => lbs * 0.453592,
    formula: 'kg = lbs × 0.453592',
  ),
  ConversionUnit(
    name: 'Temperature',
    fromUnit: 'Celsius',
    toUnit: 'Fahrenheit',
    convert: (c) => (c * 9 / 5) + 32,
    formula: '°F = (°C × 9/5) + 32',
  ),
  ConversionUnit(
    name: 'Temperature (Reverse)',
    fromUnit: 'Fahrenheit',
    toUnit: 'Celsius',
    convert: (f) => (f - 32) * 5 / 9,
    formula: '°C = (°F - 32) × 5/9',
  ),
  ConversionUnit(
    name: 'Volume',
    fromUnit: 'Liters',
    toUnit: 'Gallons',
    convert: (l) => l * 0.264172,
    formula: 'gal = L × 0.264172',
  ),
  ConversionUnit(
    name: 'Time',
    fromUnit: 'Hours',
    toUnit: 'Minutes',
    convert: (h) => h * 60,
    formula: 'min = hr × 60',
  ),
];

class UnitConverterHome extends StatefulWidget {
  const UnitConverterHome({super.key});

  @override
  State<UnitConverterHome> createState() => _UnitConverterHomeState();
}

class _UnitConverterHomeState extends State<UnitConverterHome> {
  int _selectedIndex = 0;
  double _inputValue = 0.0;
  String _inputText = '';

  @override
  Widget build(BuildContext context) {
    final unit = conversionUnits[_selectedIndex];
    final result = unit.convert(_inputValue);
    final formattedResult = result.toStringAsFixed(4);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Unit Converter'),
        centerTitle: true,
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text(
            'Pick a category:',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 12),
          
          // Category selector buttons
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: List.generate(
              conversionUnits.length,
              (index) {
                final isSelected = index == _selectedIndex;
                return FilterChip(
                  label: Text(conversionUnits[index].name),
                  selected: isSelected,
                  onSelected: (selected) {
                    setState(() {
                      _selectedIndex = index;
                      _inputValue = 0.0;
                      _inputText = '';
                    });
                  },
                  backgroundColor: Colors.blue[50],
                  selectedColor: Colors.blue,
                  labelStyle: TextStyle(
                    color: isSelected ? Colors.white : Colors.blue,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                );
              },
            ),
          ),
          
          const SizedBox(height: 32),
          
          // Converter card
          Card(
            elevation: 4,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    '${unit.fromUnit} → ${unit.toUnit}',
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 24),
                  
                  // Input field
                  TextField(
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      labelText: 'Enter ${unit.fromUnit.toLowerCase()}',
                      border: const OutlineInputBorder(),
                      prefixIcon: const Icon(Icons.numbers),
                    ),
                    onChanged: (value) {
                      setState(() {
                        _inputText = value;
                        _inputValue = double.tryParse(value) ?? 0.0;
                      });
                    },
                  ),
                  
                  const SizedBox(height: 24),
                  
                  // Result display
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.blue[50],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      children: [
                        const Text(
                          'Result',
                          style: TextStyle(fontSize: 16, color: Colors.grey),
                        ),
                        Text(
                          formattedResult,
                          style: const TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue,
                          ),
                        ),
                        Text(
                          '${unit.toUnit}',
                          style: const TextStyle(
                            fontSize: 18,
                            color: Colors.blue,
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 16),
                  
                  // Formula
                  Text(
                    unit.formula,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[600],
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ),
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
- Add more conversion types (area, speed, energy)
- Add a "swap units" button to flip direction
- Add copy-to-clipboard for the result
- Add conversion history
- Add offline functionality badge

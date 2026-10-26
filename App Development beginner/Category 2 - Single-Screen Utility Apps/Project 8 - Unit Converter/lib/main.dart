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
        brightness: Brightness.light,
      ),
      home: const UnitConverterHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

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
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Pick a category:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              alignment: WrapAlignment.center,
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
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.blue[50],
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.blue[200]!, width: 2),
              ),
              child: Column(
                children: [
                  Text(
                    '$_inputValue ${unit.fromUnit} =',
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    formattedResult,
                    style: const TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue,
                    ),
                  ),
                  Text(
                    unit.toUnit,
                    style: const TextStyle(
                      fontSize: 18,
                      color: Colors.blue,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'Enter ${unit.fromUnit.toLowerCase()}',
                border: const OutlineInputBorder(),
                hintText: 'Type a number...',
              ),
              onChanged: (value) {
                setState(() {
                  _inputText = value;
                  _inputValue = double.tryParse(value) ?? 0.0;
                });
              },
            ),
            const SizedBox(height: 16),
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
    );
  }
}

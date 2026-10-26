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
  int _selectedTipIndex = 1;

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

  String FormatCurrency(double value) {
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
                    onChanged: (value) => setState(() {}),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
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

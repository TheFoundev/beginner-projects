# Project 15 - Simple Drawing Canvas (Flutter)

## 1. Project Title
**Simple Drawing Canvas**

## 2. The Concept
This app gives you a blank digital canvas where you can draw anything by dragging your finger across the screen. Think of it as a piece of digital paper — your finger acts like a paintbrush, and wherever you move it, color appears on the screen. Behind the scenes, the app tracks your finger's X and Y position (like a GPS tracking your movements), and draws a line connecting those positions as you move, creating a continuous path just like dragging a pen across paper.

## 3. What You Will Build/Do
You'll build an app with a white drawing canvas and a toolbar at the bottom with color buttons and a clear button. Drag your finger to draw in black, red, blue, or green. Tap the eraser or clear button to start fresh. The final app looks like a sketchpad — perfect for doodling, drawing mustaches on photos, or taking quick notes!

## 4. Core App Concept
**Touch/Gesture Tracking** — The app detects when your finger touches the screen (touch start), tracks where it moves (touch drag), and records the path. Like a GPS tracking a car's route on a map — every point gets recorded, and the app connects the dots to show your drawing path.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone (touch screen recommended)

## 6. What You Will Learn
- Handling touch/gesture input in Flutter
- Drawing on a canvas using custom painters
- Managing drawing paths and state
- Building a toolbar with interactive buttons

---

## Step-by-Step Instructions

### Step 1: Create the Project
```bash
flutter create drawing_canvas
cd drawing_canvas
```

### Step 2: Complete Source Code

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const DrawingCanvasApp());
}

class DrawingCanvasApp extends StatelessWidget {
  const DrawingCanvasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Drawing Canvas',
      theme: ThemeData(
        primarySwatch: Colors.deepOrange,
        useMaterial3: true,
      ),
      home: const DrawingCanvasHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class DrawingCanvasHome extends StatefulWidget {
  const DrawingCanvasHome({super.key});

  @override
  State<DrawingCanvasHome> createState() => _DrawingCanvasHomeState();
}

class _DrawingCanvasHomeState extends State<DrawingCanvasHome> {
  Color _selectedColor = Colors.black;
  double _strokeWidth = 5.0;
  final List<DrawingPoint> _points = [];
  
  static const List<Color> colors = [
    Colors.black,
    Colors.red,
    Colors.blue,
    Colors.green,
    Colors.orange,
    Colors.purple,
    Colors.pink,
    Colors.teal,
    Colors.yellow,
    Colors.white,
  ];

  void _clearCanvas() {
    setState(() {
      _points.clear();
    });
  }

  void _undoLast() {
    setState(() {
      if (_points.isNotEmpty) {
        _points.removeLast();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Drawing canvas
          Positioned.fill(
            child: GestureDetector(
              onPanStart: (details) {
                setState(() {
                  final RenderBox renderBox = context.findRenderObject() as RenderBox;
                  final localPosition = renderBox.localToGlobal(details.localPosition);
                  _points.add(DrawingPoint(
                    point: details.localPosition,
                    color: _selectedColor,
                    strokeWidth: _strokeWidth,
                  ));
                });
              },
              onPanUpdate: (details) {
                setState(() {
                  final RenderBox renderBox = context.findRenderObject() as RenderBox;
                  _points.add(DrawingPoint(
                    point: details.localPosition,
                    color: _selectedColor,
                    strokeWidth: _strokeWidth,
                  ));
                });
              },
              onPanEnd: (details) {
                _points.add(DrawingPoint());
              },
              child: CustomPaint(
                painter: DrawingPainter(points: _points),
                size: Size.infinite,
              ),
            ),
          ),
          
          // Toolbar at top
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              color: Colors.white.withOpacity(0.9),
              child: Row(
                children: [
                  // Undo button
                  IconButton(
                    icon: const Icon(Icons.undo, size: 22),
                    onPressed: _points.isEmpty ? null : _undoLast,
                    color: Colors.grey[700],
                  ),
                  const SizedBox(width: 4),
                  
                  // Clear button
                  IconButton(
                    icon: const Icon(Icons.clear, size: 22),
                    onPressed: _points.isEmpty ? null : _clearCanvas,
                    color: Colors.red,
                  ),
                  const SizedBox(width: 8),
                  
                  // Stroke width slider
                  Expanded(
                    child: SliderTheme(
                      data: SliderTheme.of(context).copyWith(
                        activeColor: _selectedColor,
                        inactiveColor: Colors.grey[300],
                        thumbColor: _selectedColor,
                      ),
                      child: Slider(
                        value: _strokeWidth,
                        min: 1.0,
                        max: 20.0,
                        divisions: 19,
                        label: _strokeWidth.round().toString(),
                        onChanged: (value) {
                          setState(() {
                            _strokeWidth = value;
                          });
                        },
                      ),
                    ),
                  ),
                  Text(
                    _strokeWidth.round().toString(),
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                  const SizedBox(width: 8),
                  
                  // Selected color indicator
                  Container(
                    width: 30,
                    height: 30,
                    decoration: BoxDecoration(
                      color: _selectedColor,
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.grey, width: 2),
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          // Color palette at bottom
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.all(12),
              color: Colors.white.withOpacity(0.95),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                alignment: WrapAlignment.center,
                children: List.generate(
                  colors.length,
                  (index) {
                    final color = colors[index];
                    final isSelected = color == _selectedColor;
                    return GestureDetector(
                      onTap: () {
                        setState(() {
                          _selectedColor = color;
                        });
                      },
                      child: Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          color: color,
                          shape: BoxShape.circle,
                          border: isSelected
                              ? Border.all(color: Colors.deepOrange, width: 3)
                              : Border.all(color: Colors.grey, width: 1),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _clearCanvas,
        backgroundColor: Colors.red,
        foregroundColor: Colors.white,
        icon: const Icon(Icons.delete_sweep),
        label: const Text('Clear All'),
      ),
    );
  }
}

// Data model for a single drawing point
class DrawingPoint {
  Offset? point;
  Color? color;
  double? strokeWidth;

  DrawingPoint({this.point, this.color, this.strokeWidth});
}

// Custom painter that draws all the points
class DrawingPainter extends CustomPainter {
  final List<DrawingPoint> points;

  DrawingPainter({required this.points});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..isAntiAlias = true
      ..strokeCap = StrokeCap.round;

    for (int i = 0; i < points.length - 1; i++) {
      final p1 = points[i];
      final p2 = points[i + 1];

      if (p1.point != null && p2.point != null) {
        paint.color = p1.color!;
        paint.strokeWidth = p1.strokeWidth!;
        canvas.drawLine(p1.point!, p2.point!, paint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}

// ==================== ALTERNATIVE: Simpler drawing implementation ====================
// NOTE: This is a simplified version for reference. Use EITHER the main app code above
// OR this alternative — they use different class names (SimpleDrawingHome vs DrawingCanvasHome)
// so you can keep both in separate files without conflicts.
class SimpleDrawingHome extends StatefulWidget {
  const SimpleDrawingHome({super.key});

  @override
  State<SimpleDrawingHome> createState() => _SimpleDrawingHomeState();
}

class _SimpleDrawingHomeState extends State<SimpleDrawingHome> {
  final List<Offset> _points = [];
  final List<Color> _colors = [];
  final List<double> _stops = [];
  Color _currentColor = Colors.black;
  double _currentStroke = 5.0;

  void _clearCanvas() {
    setState(() {
      _points.clear();
      _colors.clear();
      _stops.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Positioned.fill(
            child: GestureDetector(
              onPanStart: (details) {
                setState(() {
                  _points.add(details.localPosition);
                  _colors.add(_currentColor);
                  _stops.add(_currentStroke);
                });
              },
              onPanUpdate: (details) {
                setState(() {
                  _points.add(details.localPosition);
                  _colors.add(_currentColor);
                  _stops.add(_currentStroke);
                });
              },
              child: CustomPaint(
                painter: _SimpleDrawingPainter(
                  points: _points,
                  colors: _colors,
                  stops: _stops,
                ),
              ),
            ),
          ),
          
          // Toolbar
          Positioned(
            top: 50,
            child: Row(
              children: [
                _colorButton(Colors.black),
                _colorButton(Colors.red),
                _colorButton(Colors.blue),
                _colorButton(Colors.green),
                _colorButton(Colors.orange),
                IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: _clearCanvas,
                  color: Colors.red,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _colorButton(Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4),
      child: GestureDetector(
        onTap: () => setState(() => _currentColor = color),
        child: Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
            border: Border.all(
              color: _currentColor == color ? Colors.deepOrange : Colors.grey,
              width: 3,
            ),
          ),
        ),
      ),
    );
  }
}

class _SimpleDrawingPainter extends CustomPainter {
  final List<Offset> points;
  final List<Color> colors;
  final List<double> stops;

  _SimpleDrawingPainter({
    required this.points,
    required this.colors,
    required this.stops,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..isAntiAlias = true
      ..strokeCap = StrokeCap.round;

    for (int i = 0; i < points.length - 1; i++) {
      paint.color = colors[i];
      paint.strokeWidth = stops[i];
      canvas.drawLine(points[i], points[i + 1], paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}
```

### Step 3: Run the App
```bash
flutter pub get
flutter run
```

## Extension Ideas
- Add different brush types (spray, blur, texture)
- Add an eraser tool
- Add layers for advanced drawing
- Save drawings to the gallery
- Add a background template (grid, circle, etc.)

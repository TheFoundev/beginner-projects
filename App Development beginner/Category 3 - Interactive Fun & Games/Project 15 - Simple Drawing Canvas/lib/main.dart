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
        primarySwatch: Colors.orange,
        brightness: Brightness.light,
      ),
      home: const DrawingCanvasHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class DrawingPoint {
  Offset? point;
  Color? color;
  double? strokeWidth;

  DrawingPoint({this.point, this.color, this.strokeWidth});
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Drawing area
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
          
          // Top toolbar
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              color: Colors.white.withOpacity(0.9),
              child: Row(
                children: [
                  // Clear button
                  IconButton(
                    icon: const Icon(Icons.clear, size: 24, color: Colors.red),
                    onPressed: _points.isEmpty ? null : _clearCanvas,
                    tooltip: 'Clear Canvas',
                  ),
                  const SizedBox(width: 8),
                  
                  // Stroke width
                  Text(
                    '${_strokeWidth.round()}px',
                    style: TextStyle(color: Colors.grey[600], fontSize: 14),
                  ),
                  Expanded(
                    child: SliderTheme(
                      data: SliderTheme.of(context).copyWith(
                        activeColor: _selectedColor,
                        inactiveColor: Colors.grey[300],
                        thumbColor: _selectedColor,
                      ),
                      child: Slider(
                        value: _strokeWidth,
                        min: 2.0,
                        max: 20.0,
                        divisions: 18,
                        label: _strokeWidth.round().toString(),
                        onChanged: (value) {
                          setState(() {
                            _strokeWidth = value;
                          });
                        },
                      ),
                    ),
                  ),
                  
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
                spacing: 10,
                runSpacing: 10,
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
                          border: Border.all(
                            color: isSelected ? Colors.deepOrange : Colors.grey,
                            width: isSelected ? 3 : 1,
                          ),
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

# Project 10 - Basic To-Do List (Flutter)

## 1. Project Title
**Basic To-Do List**

## 2. The Concept
This app is a digital sticky note board for your tasks. You type in something to do (like "Buy milk"), tap "Add," and it appears as a checkbox on your list. When you complete a task, you check the box and it gets a line through it. Behind the scenes, the app stores each task in a list (like items on a physical checklist) and remembers them while the app stays open. It's like having a digital checklist that you can add to and mark off throughout the day.

## 3. What You Will Build/Do
You'll create a clean app with a text input at the top, an "Add Task" button, and a scrollable list of tasks below. Each task has a checkbox that you can tap to mark as complete. Completed tasks show with a strikethrough. The final app looks like a minimal, elegant task manager — simple but useful for daily planning.

## 4. Core App Concept
**Local State Management with Lists** — The app maintains a list of items (tasks) in its memory, and whenever that list changes (add, remove, check off), the screen updates automatically to show the current state. Like a whiteboard where you write tasks and erase them — the board always shows exactly what you've written, no more, no less.

## 5. Tools Needed
- **Flutter** (free, install from flutter.dev)
- **Visual Studio Code** or **Android Studio** (both free)
- Android emulator or real phone
- Optional: `shared_preferences` package for saving tasks between sessions

### Step 1: Create the Project
```bash
flutter create todo_list_app
cd todo_list_app
```

### Step 2: Add Dependencies (optional for persistence)
Add to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  shared_preferences: ^2.2.2
```

### Step 3: Complete Source Code

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const TodoListApp());
}

class TodoListApp extends StatelessWidget {
  const TodoListApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My To-Do List',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        useMaterial3: true,
      ),
      home: const TodoListHome(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// Task data model
class Task {
  final String id;
  final String title;
  bool isCompleted;

  Task({
    required this.id,
    required this.title,
    this.isCompleted = false,
  });
}

class TodoListHome extends StatefulWidget {
  const TodoListHome({super.key});

  @override
  State<TodoListHome> createState() => _TodoListHomeState();
}

class _TodoListHomeState extends State<TodoListHome> {
  final List<Task> _tasks = [];
  final TextEditingController _textController = TextEditingController();
  int _counter = 0;

  void _addTask() {
    final text = _textController.text.trim();
    if (text.isNotEmpty) {
      setState(() {
        _tasks.add(Task(
          id: (_counter++).toString(),
          title: text,
        ));
      });
      _textController.clear();
    }
  }

  void _toggleTask(String id) {
    setState(() {
      final task = _tasks.firstWhere((task) => task.id == id);
      task.isCompleted = !task.isCompleted;
    });
  }

  void _deleteTask(String id) {
    setState(() {
      _tasks.removeWhere((task) => task.id == id);
    });
  }

  int get _completedCount {
    return _tasks.where((task) => task.isCompleted).length;
  }

  int get _pendingCount {
    return _tasks.length - _completedCount;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My To-Do List'),
        centerTitle: true,
        actions: [
          if (_tasks.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Center(
                child: Text(
                  '$_pendingCount left',
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          // Input section
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: InputDecoration(
                      labelText: 'What needs to be done?',
                      border: const OutlineInputBorder(),
                      hintText: 'Enter a new task...',
                    ),
                    onSubmitted: (value) => _addTask(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.add, size: 30, color: Colors.teal),
                  onPressed: _addTask,
                ),
              ],
            ),
          ),
          
          // Stats row
          if (_tasks.isNotEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Chip(
                    backgroundColor: Colors.orange[100],
                    label: Text(
                      '$_pendingCount pending',
                      style: const TextStyle(color: Colors.orange),
                    ),
                  ),
                  Chip(
                    backgroundColor: Colors.green[100],
                    label: Text(
                      '$_completedCount done',
                      style: const TextStyle(color: Colors.green),
                    ),
                  ),
                ],
              ),
            ),
          const SizedBox(height: 8),
          
          // Task list
          Expanded(
            child: _tasks.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.check_circle_outline,
                          size: 80,
                          color: Colors.grey[400],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'No tasks yet! Add one above.',
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    itemCount: _tasks.length,
                    padding: const EdgeInsets.symmetric(horizontal: 8),
                    itemBuilder: (context, index) {
                      final task = _tasks[index];
                      return Dismissible(
                        key: Key(task.id),
                        direction: DismissDirection.endToStart,
                        background: Container(
                          alignment: Alignment.centerRight,
                          padding: const EdgeInsets.only(right: 20),
                          decoration: BoxDecoration(
                            color: Colors.red,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Icon(
                            Icons.delete,
                            color: Colors.white,
                          ),
                        ),
                        onDismissed: (direction) {
                          _deleteTask(task.id);
                        },
                        child: Card(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 4,
                          ),
                          child: ListTile(
                            leading: IconButton(
                              icon: Icon(
                                task.isCompleted
                                    ? Icons.check_box
                                    : Icons.check_box_outline_blank,
                                color: task.isCompleted
                                    ? Colors.teal
                                    : Colors.grey,
                              ),
                              onPressed: () => _toggleTask(task.id),
                            ),
                            title: Text(
                              task.title,
                              style: TextStyle(
                                decoration: task.isCompleted
                                    ? TextDecoration.lineThrough
                                    : null,
                                color: task.isCompleted
                                    ? Colors.grey
                                    : Colors.black87,
                              ),
                            ),
                            trailing: IconButton(
                              icon: const Icon(
                                Icons.delete,
                                color: Colors.red,
                              ),
                              onPressed: () => _deleteTask(task.id),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
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
- Add due dates for tasks
- Add task categories or labels
- Save tasks locally using shared_preferences
- Add task reordering by dragging
- Add a "clear completed" button

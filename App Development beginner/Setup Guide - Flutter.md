# Setup Guide - Flutter Development

## Getting Started with Flutter (Real App Development!)

### What is Flutter?
Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase. You write in Dart (a simple, readable language) and compile to native code for real performance.

### Prerequisites
- Windows 10 or later (this guide is Windows-focused)
- At least 4GB of free disk space
- Administrative access to install software

### Step 1: Download and Install Flutter
1. Go to [https://docs.flutter.dev/get-started/install](https://docs.flutter.dev/get-started/install)
2. Download the Flutter SDK for Windows
3. Extract the zip file to `C:\src\flutter` (or another location)
4. Add Flutter to your PATH:
   - Search for "Environment Variables" in Windows search
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables," find "Path" and click "Edit"
   - Add `C:\src\flutter\bin`
   - Click OK on all dialogs

### Step 2: Verify Installation
Open a **new** PowerShell/Command Prompt and type:
```powershell
flutter --version
```
You should see the Flutter version number.

### Step 3: Install Android Studio (for Emulator)
1. Download Android Studio from [developer.android.com/studio](https://developer.android.com/studio)
2. Install it with default settings
3. During first launch, choose "Do first time setup"
4. Install the Android SDK, Android SDK Platform, and Android Virtual Device
5. Create a virtual device:
   - Tools → Device Manager → Create Device
   - Choose "Pixel 5" (or any phone)
   - Select a system image (API 33 or higher recommended)
   - Finish

### Step 4: Install VS Code
1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Install these extensions:
   - **Flutter** (by Dart Team)
   - **Dart** (by Dart Team)

### Step 5: Verify Everything Works
Run Flutter Doctor:
```powershell
flutter doctor
```
This checks for:
- ✅ Flutter SDK
- ✅ Android toolchain (Android Studio)
- ✅ VS Code
- ✅ Connected device (emulator or phone)

You may need to accept some license agreements by typing `y` when prompted.

### Step 6: Enable Developer Mode (for testing on your phone)
If you want to test on your real phone:
1. Go to Settings → About phone
2. Tap "Build number" 7 times
3. Go back to Settings → Developer options
4. Enable "USB Debugging"
5. Connect your phone via USB
6. Run `flutter devices` to confirm it's recognized

### Creating Your First App
```powershell
# Create a new Flutter project
flutter create my_app
cd my_app

# Install dependencies
flutter pub get

# Run on connected device or emulator
flutter run
```

### Project Structure
```
my_app/
├── android/          # Android native code
├── ios/              # iOS native code
├── lib/
│   └── main.dart     # Your main Flutter code goes here
├── pubspec.yaml      # Project configuration and dependencies
└── test/             # Unit and widget tests
```

### Common Flutter Commands
```bash
flutter pub get           # Install dependencies
flutter run               # Run the app
flutter run -d chrome     # Run in Chrome browser
flutter build apk         # Build APK for Android
flutter build ios         # Build for iOS
flutter test              # Run tests
flutter doctor            # Check installation status
flutter devices           # List connected devices
flutter clean             # Clean build files
```

### Quick Hello World in Flutter
Replace `lib/main.dart` with this code:
```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hello Flutter',
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Hello Flutter')),
      body: const Center(
        child: Text(
          'Welcome to Flutter!',
          style: TextStyle(fontSize: 32),
        ),
      ),
    );
  }
}
```

Run with:
```bash
flutter run
```

### Troubleshooting
- **"No connected devices"**: Make sure your emulator is running or phone is connected via USB
- **Permission denied**: Try running as administrator or check your PATH setup
- **Build failed**: Run `flutter clean` then `flutter pub get` again
- **Port in use**: Run `flutter emulators --shutdown-all` then start your emulator again

### Recommended Next Steps After Setup
1. Complete the official [Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
2. Try building Project 6 (Tip Calculator) from this repository
3. Use hot reload (`r` in terminal) to see changes instantly

### Additional Resources
- [Flutter Documentation](https://docs.flutter.dev)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Flutter Widget Catalog](https://docs.flutter.dev/ui/widgets)
- [Flutter Cookbook](https://docs.flutter.dev/cookbook)

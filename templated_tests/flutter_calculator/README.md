# Flutter Calculator

A cross-platform calculator application built with Flutter that runs on mobile, web, and desktop.

## Prerequisites

Install Flutter:

```bash
# On macOS
brew install --cask flutter

# On Linux
snap install flutter

# On Windows
# Download from https://flutter.dev/docs/get-started/install/windows

# Verify installation
flutter doctor
```

## Installation and Setup

Get dependencies:

```bash
flutter pub get
```

## Running the Application

### Mobile (iOS/Android)

```bash
# Check connected devices
flutter devices

# Run on connected device/emulator
flutter run
```

### Web

```bash
# Enable web support (first time only)
flutter config --enable-web

# Run on web
flutter run -d chrome
```

### Desktop

```bash
# Enable desktop support (first time only)
flutter config --enable-macos-desktop  # macOS
flutter config --enable-linux-desktop  # Linux
flutter config --enable-windows-desktop  # Windows

# Run on desktop
flutter run -d macos    # macOS
flutter run -d linux    # Linux
flutter run -d windows  # Windows
```

## Testing

Run all tests:

```bash
flutter test
```

Run tests with coverage:

```bash
flutter test --coverage
```

Generate HTML coverage report:

```bash
genhtml coverage/lcov.info -o coverage/html
```

Open `coverage/html/index.html` to view the coverage report.

## Build

### Build for Mobile

```bash
# Android APK
flutter build apk

# Android App Bundle
flutter build appbundle

# iOS
flutter build ios
```

### Build for Web

```bash
flutter build web
```

### Build for Desktop

```bash
# macOS
flutter build macos

# Linux
flutter build linux

# Windows
flutter build windows
```

## Project Structure

```
flutter_calculator/
├── lib/
│   ├── main.dart              # App entry point
│   ├── calculator.dart        # Calculator logic
│   └── calculator_screen.dart # UI component
├── test/
│   ├── calculator_test.dart   # Unit tests
│   └── widget_test.dart       # Widget tests
├── pubspec.yaml              # Dependencies
└── README.md                 # This file
```

## Features Demonstrated

- Flutter framework
- Material Design UI
- State management with StatefulWidget
- Cross-platform development (mobile, web, desktop)
- Unit testing with flutter_test
- Widget testing
- Code coverage reporting
- Dart programming language
- Responsive layout
- Touch and mouse input handling
- Error handling

## Calculator Operations

- Basic arithmetic: addition, subtraction, multiplication, division
- Clear functionality
- Decimal number support
- Error handling for division by zero
- Visual feedback and Material Design styling

## Platform-Specific Features

- **Mobile**: Touch-optimized interface
- **Web**: Responsive web layout
- **Desktop**: Mouse and keyboard support

## Testing Coverage

- Unit tests for calculator logic
- Widget tests for UI components
- Integration tests for user workflows
- Coverage reporting for test analysis

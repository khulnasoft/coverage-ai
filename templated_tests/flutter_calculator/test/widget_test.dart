import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_calculator/main.dart';

void main() {
  testWidgets('Calculator smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the calculator screen is displayed
    expect(find.text('Flutter Calculator'), findsOneWidget);
    expect(find.text('0'), findsOneWidget);
    
    // Verify that number buttons are present
    expect(find.text('1'), findsOneWidget);
    expect(find.text('2'), findsOneWidget);
    expect(find.text('3'), findsOneWidget);
    expect(find.text('4'), findsOneWidget);
    expect(find.text('5'), findsOneWidget);
    expect(find.text('6'), findsOneWidget);
    expect(find.text('7'), findsOneWidget);
    expect(find.text('8'), findsOneWidget);
    expect(find.text('9'), findsOneWidget);
    expect(find.text('0'), findsOneWidget);
    
    // Verify that operation buttons are present
    expect(find.text('+'), findsOneWidget);
    expect(find.text('-'), findsOneWidget);
    expect(find.text('×'), findsOneWidget);
    expect(find.text('÷'), findsOneWidget);
    expect(find.text('='), findsOneWidget);
    expect(find.text('C'), findsOneWidget);
    expect(find.text('.'), findsOneWidget);
  });

  testWidgets('Calculator basic operation test', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    // Test simple addition: 2 + 3 = 5
    await tester.tap(find.text('2'));
    await tester.pump();
    expect(find.text('2'), findsOneWidget);

    await tester.tap(find.text('+'));
    await tester.pump();

    await tester.tap(find.text('3'));
    await tester.pump();
    expect(find.text('3'), findsOneWidget);

    await tester.tap(find.text('='));
    await tester.pump();
    expect(find.text('5'), findsOneWidget);
  });

  testWidgets('Calculator clear test', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    // Enter some numbers
    await tester.tap(find.text('1'));
    await tester.pump();
    await tester.tap(find.text('2'));
    await tester.pump();
    expect(find.text('12'), findsOneWidget);

    // Clear the calculator
    await tester.tap(find.text('C'));
    await tester.pump();
    expect(find.text('0'), findsOneWidget);
  });

  testWidgets('Calculator decimal input test', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    // Test decimal input
    await tester.tap(find.text('1'));
    await tester.pump();
    await tester.tap(find.text('.'));
    await tester.pump();
    await tester.tap(find.text('5'));
    await tester.pump();
    expect(find.text('1.5'), findsOneWidget);
  });
}

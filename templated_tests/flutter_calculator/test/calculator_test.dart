import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_calculator/calculator.dart';

void main() {
  group('Calculator Tests', () {
    late Calculator calculator;

    setUp(() {
      calculator = Calculator();
    });

    test('add should return correct sum', () {
      expect(calculator.add(2, 3), equals(5.0));
      expect(calculator.add(-1, 1), equals(0.0));
      expect(calculator.add(0, 0), equals(0.0));
    });

    test('subtract should return correct difference', () {
      expect(calculator.subtract(5, 3), equals(2.0));
      expect(calculator.subtract(1, 1), equals(0.0));
      expect(calculator.subtract(-2, -3), equals(1.0));
    });

    test('multiply should return correct product', () {
      expect(calculator.multiply(2, 3), equals(6.0));
      expect(calculator.multiply(-2, 3), equals(-6.0));
      expect(calculator.multiply(0, 5), equals(0.0));
    });

    test('divide should return correct quotient', () {
      expect(calculator.divide(6, 2), equals(3.0));
      expect(calculator.divide(-4, 2), equals(-2.0));
      expect(calculator.divide(5, 2), equals(2.5));
    });

    test('divide should throw error for division by zero', () {
      expect(() => calculator.divide(1, 0), throwsArgumentError);
    });

    test('calculate should perform addition', () {
      expect(calculator.calculate('+', 2, 3), equals(5.0));
    });

    test('calculate should perform subtraction', () {
      expect(calculator.calculate('-', 5, 3), equals(2.0));
    });

    test('calculate should perform multiplication', () {
      expect(calculator.calculate('*', 3, 4), equals(12.0));
    });

    test('calculate should perform division', () {
      expect(calculator.calculate('/', 12, 3), equals(4.0));
    });

    test('calculate should throw error for unknown operation', () {
      expect(() => calculator.calculate('%', 5, 3), throwsArgumentError);
    });

    test('calculate should throw error for division by zero', () {
      expect(() => calculator.calculate('/', 5, 0), throwsArgumentError);
    });
  });
}

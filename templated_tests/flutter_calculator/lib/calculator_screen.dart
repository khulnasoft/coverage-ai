import 'package:flutter/material.dart';
import 'package:flutter_calculator/calculator.dart';

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({super.key});

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  final Calculator _calculator = Calculator();
  String _display = '0';
  double? _previousValue;
  String? _currentOperation;
  bool _waitingForNewValue = false;

  void _inputNumber(String number) {
    setState(() {
      if (_waitingForNewValue) {
        _display = number;
        _waitingForNewValue = false;
      } else {
        _display = _display == '0' ? number : _display + number;
      }
    });
  }

  void _inputOperation(String operation) {
    final currentValue = double.tryParse(_display);
    if (currentValue == null) return;

    setState(() {
      if (_previousValue == null) {
        _previousValue = currentValue;
      } else if (_currentOperation != null) {
        _calculateResult();
        _previousValue = double.tryParse(_display);
      }
      _currentOperation = operation;
      _waitingForNewValue = true;
    });
  }

  void _calculateResult() {
    if (_previousValue == null || _currentOperation == null) return;

    final currentValue = double.tryParse(_display);
    if (currentValue == null) return;

    try {
      final result = _calculator.calculate(_currentOperation!, _previousValue!, currentValue);
      setState(() {
        _display = result.toStringAsFixed(result.truncateToDouble() == result ? 0 : 2);
        _previousValue = null;
        _currentOperation = null;
        _waitingForNewValue = true;
      });
    } catch (e) {
      setState(() {
        _display = 'Error';
        _previousValue = null;
        _currentOperation = null;
        _waitingForNewValue = true;
      });
    }
  }

  void _clear() {
    setState(() {
      _display = '0';
      _previousValue = null;
      _currentOperation = null;
      _waitingForNewValue = false;
    });
  }

  void _inputDecimal() {
    setState(() {
      if (_waitingForNewValue) {
        _display = '0.';
        _waitingForNewValue = false;
      } else if (!_display.contains('.')) {
        _display += '.';
      }
    });
  }

  Widget _buildButton({
    required String text,
    required VoidCallback onPressed,
    Color? backgroundColor,
    Color? textColor,
    bool flex = false,
  }) {
    return Expanded(
      flex: flex ? 2 : 1,
      child: Padding(
        padding: const EdgeInsets.all(4.0),
        child: ElevatedButton(
          onPressed: onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: backgroundColor ?? Colors.grey[300],
            foregroundColor: textColor ?? Colors.black,
            padding: const EdgeInsets.all(24),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          child: Text(
            text,
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Calculator'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Column(
        children: [
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(16),
              alignment: Alignment.bottomRight,
              child: Text(
                _display,
                style: const TextStyle(
                  fontSize: 48,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.right,
              ),
            ),
          ),
          Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Row(
                  children: [
                    _buildButton(
                      text: 'C',
                      onPressed: _clear,
                      backgroundColor: Colors.orange[300],
                    ),
                    _buildButton(
                      text: '±',
                      onPressed: () {}, // Not implemented
                    ),
                    _buildButton(
                      text: '%',
                      onPressed: () {}, // Not implemented
                    ),
                    _buildButton(
                      text: '÷',
                      onPressed: () => _inputOperation('/'),
                      backgroundColor: Colors.blue[300],
                    ),
                  ],
                ),
                Row(
                  children: [
                    _buildButton(
                      text: '7',
                      onPressed: () => _inputNumber('7'),
                    ),
                    _buildButton(
                      text: '8',
                      onPressed: () => _inputNumber('8'),
                    ),
                    _buildButton(
                      text: '9',
                      onPressed: () => _inputNumber('9'),
                    ),
                    _buildButton(
                      text: '×',
                      onPressed: () => _inputOperation('*'),
                      backgroundColor: Colors.blue[300],
                    ),
                  ],
                ),
                Row(
                  children: [
                    _buildButton(
                      text: '4',
                      onPressed: () => _inputNumber('4'),
                    ),
                    _buildButton(
                      text: '5',
                      onPressed: () => _inputNumber('5'),
                    ),
                    _buildButton(
                      text: '6',
                      onPressed: () => _inputNumber('6'),
                    ),
                    _buildButton(
                      text: '−',
                      onPressed: () => _inputOperation('-'),
                      backgroundColor: Colors.blue[300],
                    ),
                  ],
                ),
                Row(
                  children: [
                    _buildButton(
                      text: '1',
                      onPressed: () => _inputNumber('1'),
                    ),
                    _buildButton(
                      text: '2',
                      onPressed: () => _inputNumber('2'),
                    ),
                    _buildButton(
                      text: '3',
                      onPressed: () => _inputNumber('3'),
                    ),
                    _buildButton(
                      text: '+',
                      onPressed: () => _inputOperation('+'),
                      backgroundColor: Colors.blue[300],
                    ),
                  ],
                ),
                Row(
                  children: [
                    _buildButton(
                      text: '0',
                      onPressed: () => _inputNumber('0'),
                      flex: true,
                    ),
                    _buildButton(
                      text: '.',
                      onPressed: _inputDecimal,
                    ),
                    _buildButton(
                      text: '=',
                      onPressed: _calculateResult,
                      backgroundColor: Colors.green[300],
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

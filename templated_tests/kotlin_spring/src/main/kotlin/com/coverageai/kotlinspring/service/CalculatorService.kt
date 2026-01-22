package com.coverageai.kotlinspring.service

import org.springframework.stereotype.Service

@Service
class CalculatorService {

    fun calculate(operation: String, a: Double, b: Double): Double {
        return when (operation.lowercase()) {
            "add" -> add(a, b)
            "subtract" -> subtract(a, b)
            "multiply" -> multiply(a, b)
            "divide" -> divide(a, b)
            else -> throw IllegalArgumentException("Invalid operation: $operation. Use: add, subtract, multiply, divide")
        }
    }

    private fun add(a: Double, b: Double): Double = a + b
    private fun subtract(a: Double, b: Double): Double = a - b
    private fun multiply(a: Double, b: Double): Double = a * b
    private fun divide(a: Double, b: Double): Double {
        if (b == 0.0) {
            throw IllegalArgumentException("Division by zero")
        }
        return a / b
    }
}

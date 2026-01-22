package com.coverageai.kotlinspring.service

import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows

class CalculatorServiceTest {

    private val calculatorService = CalculatorService()

    @Test
    fun `add returns correct sum`() {
        val result = calculatorService.calculate("add", 5.0, 3.0)
        assertEquals(8.0, result)
    }

    @Test
    fun `subtract returns correct difference`() {
        val result = calculatorService.calculate("subtract", 10.0, 4.0)
        assertEquals(6.0, result)
    }

    @Test
    fun `multiply returns correct product`() {
        val result = calculatorService.calculate("multiply", 6.0, 7.0)
        assertEquals(42.0, result)
    }

    @Test
    fun `divide returns correct quotient`() {
        val result = calculatorService.calculate("divide", 20.0, 5.0)
        assertEquals(4.0, result)
    }

    @Test
    fun `divide by zero throws exception`() {
        val exception = assertThrows<IllegalArgumentException> {
            calculatorService.calculate("divide", 10.0, 0.0)
        }
        assertEquals("Division by zero", exception.message)
    }

    @Test
    fun `invalid operation throws exception`() {
        val exception = assertThrows<IllegalArgumentException> {
            calculatorService.calculate("invalid", 5.0, 3.0)
        }
        assertTrue(exception.message!!.contains("Invalid operation"))
    }

    @Test
    fun `case insensitive operation works`() {
        val result = calculatorService.calculate("ADD", 5.0, 3.0)
        assertEquals(8.0, result)
    }

    @Test
    fun `negative numbers work correctly`() {
        assertEquals(-2.0, calculatorService.calculate("add", -5.0, 3.0))
        assertEquals(-8.0, calculatorService.calculate("subtract", -5.0, 3.0))
        assertEquals(-15.0, calculatorService.calculate("multiply", -5.0, 3.0))
        assertEquals(-1.6666666666666667, calculatorService.calculate("divide", -5.0, 3.0))
    }
}

import { describe, it, expect } from 'vitest';
import { add, subtract, multiply, divide, calculate } from './calculator.js';

describe('Calculator Utils', () => {
	describe('add', () => {
		it('should add two positive numbers', () => {
			expect(add(2, 3)).toBe(5);
		});

		it('should add negative numbers', () => {
			expect(add(-2, -3)).toBe(-5);
		});

		it('should add positive and negative numbers', () => {
			expect(add(5, -3)).toBe(2);
		});
	});

	describe('subtract', () => {
		it('should subtract two positive numbers', () => {
			expect(subtract(5, 3)).toBe(2);
		});

		it('should subtract negative numbers', () => {
			expect(subtract(-2, -3)).toBe(1);
		});
	});

	describe('multiply', () => {
		it('should multiply two positive numbers', () => {
			expect(multiply(3, 4)).toBe(12);
		});

		it('should multiply by zero', () => {
			expect(multiply(5, 0)).toBe(0);
		});

		it('should multiply negative numbers', () => {
			expect(multiply(-2, 3)).toBe(-6);
		});
	});

	describe('divide', () => {
		it('should divide two positive numbers', () => {
			expect(divide(12, 3)).toBe(4);
		});

		it('should handle decimal results', () => {
			expect(divide(5, 2)).toBe(2.5);
		});

		it('should throw error for division by zero', () => {
			expect(() => divide(5, 0)).toThrow('Division by zero');
		});
	});

	describe('calculate', () => {
		it('should perform addition', () => {
			expect(calculate('+', 2, 3)).toBe(5);
		});

		it('should perform subtraction', () => {
			expect(calculate('-', 5, 3)).toBe(2);
		});

		it('should perform multiplication', () => {
			expect(calculate('*', 3, 4)).toBe(12);
		});

		it('should perform division', () => {
			expect(calculate('/', 12, 3)).toBe(4);
		});

		it('should throw error for unknown operation', () => {
			expect(() => calculate('%', 5, 3)).toThrow('Unknown operation: %');
		});
	});
});

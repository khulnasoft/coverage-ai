export function add(a, b) {
  return a + b
}

export function subtract(a, b) {
  return a - b
}

export function multiply(a, b) {
  return a * b
}

export function divide(a, b) {
  if (b === 0) {
    throw new Error('Division by zero')
  }
  return a / b
}

export function calculate(operation, a, b) {
  switch (operation) {
    case '+':
      return add(a, b)
    case '-':
      return subtract(a, b)
    case '*':
      return multiply(a, b)
    case '/':
      return divide(a, b)
    default:
      throw new Error(`Unknown operation: ${operation}`)
  }
}

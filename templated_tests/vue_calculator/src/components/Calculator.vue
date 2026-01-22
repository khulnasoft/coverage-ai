<template>
  <div class="calculator">
    <div class="display" :class="{ operation: currentOperation }">
      {{ display }}
    </div>
    
    <div class="buttons">
      <button class="function" @click="clear">C</button>
      <button class="function" disabled>±</button>
      <button class="function" disabled>%</button>
      <button class="operator" @click="setOperation('/')">÷</button>
      
      <button class="number" @click="inputNumber('7')">7</button>
      <button class="number" @click="inputNumber('8')">8</button>
      <button class="number" @click="inputNumber('9')">9</button>
      <button class="operator" @click="setOperation('*')">×</button>
      
      <button class="number" @click="inputNumber('4')">4</button>
      <button class="number" @click="inputNumber('5')">5</button>
      <button class="number" @click="inputNumber('6')">6</button>
      <button class="operator" @click="setOperation('-')">−</button>
      
      <button class="number" @click="inputNumber('1')">1</button>
      <button class="number" @click="inputNumber('2')">2</button>
      <button class="number" @click="inputNumber('3')">3</button>
      <button class="operator" @click="setOperation('+')">+</button>
      
      <button class="number zero" @click="inputNumber('0')">0</button>
      <button class="number" @click="inputDecimal">.</button>
      <button class="equals" @click="calculate">=</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Calculator',
  setup() {
    const display = ref('0')
    const previousValue = ref(null)
    const currentOperation = ref(null)
    const waitingForNewValue = ref(false)

    const add = (a, b) => a + b
    const subtract = (a, b) => a - b
    const multiply = (a, b) => a * b
    const divide = (a, b) => {
      if (b === 0) {
        return 'Error'
      }
      return a / b
    }

    const calculate = () => {
      if (previousValue.value === null || currentOperation.value === null) return

      const current = parseFloat(display.value)
      let result

      switch (currentOperation.value) {
        case '+':
          result = add(previousValue.value, current)
          break
        case '-':
          result = subtract(previousValue.value, current)
          break
        case '*':
          result = multiply(previousValue.value, current)
          break
        case '/':
          result = divide(previousValue.value, current)
          break
      }

      display.value = result.toString()
      previousValue.value = null
      currentOperation.value = null
      waitingForNewValue.value = true
    }

    const inputNumber = (num) => {
      if (waitingForNewValue.value) {
        display.value = num
        waitingForNewValue.value = false
      } else {
        display.value = display.value === '0' ? num : display.value + num
      }
    }

    const setOperation = (op) => {
      const current = parseFloat(display.value)

      if (previousValue.value === null) {
        previousValue.value = current
      } else if (currentOperation.value) {
        calculate()
        previousValue.value = parseFloat(display.value)
      }

      currentOperation.value = op
      waitingForNewValue.value = true
    }

    const clear = () => {
      display.value = '0'
      previousValue.value = null
      currentOperation.value = null
      waitingForNewValue.value = false
    }

    const inputDecimal = () => {
      if (waitingForNewValue.value) {
        display.value = '0.'
        waitingForNewValue.value = false
      } else if (!display.value.includes('.')) {
        display.value += '.'
      }
    }

    return {
      display,
      currentOperation,
      calculate,
      inputNumber,
      setOperation,
      clear,
      inputDecimal
    }
  }
}
</script>

<style scoped>
.calculator {
  max-width: 320px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.display {
  background: #333;
  color: white;
  font-size: 2.5em;
  padding: 20px;
  text-align: right;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.display.operation {
  background: #555;
}

.buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}

button {
  border: none;
  padding: 20px;
  font-size: 1.5em;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  opacity: 0.8;
}

button:active {
  opacity: 0.6;
}

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.number {
  background: #f0f0f0;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}

.number:nth-child(4n) {
  border-right: none;
}

.zero {
  grid-column: span 2;
}

.operator {
  background: #42b883;
  color: white;
  border-bottom: 1px solid #ccc;
}

.function {
  background: #d4d4d2;
  color: black;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}

.equals {
  background: #42b883;
  color: white;
  grid-row: span 2;
}
</style>

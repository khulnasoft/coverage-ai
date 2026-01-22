<script>
	let display = '0';
	let previousValue = null;
	let currentOperation = null;
	let waitingForNewValue = false;

	function add(a, b) {
		return a + b;
	}

	function subtract(a, b) {
		return a - b;
	}

	function multiply(a, b) {
		return a * b;
	}

	function divide(a, b) {
		if (b === 0) {
			return 'Error';
		}
		return a / b;
	}

	function calculate() {
		if (previousValue === null || currentOperation === null) return;

		const current = parseFloat(display);
		let result;

		switch (currentOperation) {
			case '+':
				result = add(previousValue, current);
				break;
			case '-':
				result = subtract(previousValue, current);
				break;
			case '*':
				result = multiply(previousValue, current);
				break;
			case '/':
				result = divide(previousValue, current);
				break;
		}

		display = result.toString();
		previousValue = null;
		currentOperation = null;
		waitingForNewValue = true;
	}

	function inputNumber(num) {
		if (waitingForNewValue) {
			display = num;
			waitingForNewValue = false;
		} else {
			display = display === '0' ? num : display + num;
		}
	}

	function inputOperation(op) {
		const current = parseFloat(display);

		if (previousValue === null) {
			previousValue = current;
		} else if (currentOperation) {
			calculate();
			previousValue = parseFloat(display);
		}

		currentOperation = op;
		waitingForNewValue = true;
	}

	function clear() {
		display = '0';
		previousValue = null;
		currentOperation = null;
		waitingForNewValue = false;
	}

	function inputDecimal() {
		if (waitingForNewValue) {
			display = '0.';
			waitingForNewValue = false;
		} else if (!display.includes('.')) {
			display += '.';
		}
	}
</script>

<div class="calculator">
	<div class="display" class:operation={currentOperation}>
		{display}
	</div>
	
	<div class="buttons">
		<button class="function" on:click={clear}>C</button>
		<button class="function" disabled>±</button>
		<button class="function" disabled>%</button>
		<button class="operator" on:click={() => inputOperation('/')}>÷</button>
		
		<button class="number" on:click={() => inputNumber('7')}>7</button>
		<button class="number" on:click={() => inputNumber('8')}>8</button>
		<button class="number" on:click={() => inputNumber('9')}>9</button>
		<button class="operator" on:click={() => inputOperation('*')}>×</button>
		
		<button class="number" on:click={() => inputNumber('4')}>4</button>
		<button class="number" on:click={() => inputNumber('5')}>5</button>
		<button class="number" on:click={() => inputNumber('6')}>6</button>
		<button class="operator" on:click={() => inputOperation('-')}>−</button>
		
		<button class="number" on:click={() => inputNumber('1')}>1</button>
		<button class="number" on:click={() => inputNumber('2')}>2</button>
		<button class="number" on:click={() => inputNumber('3')}>3</button>
		<button class="operator" on:click={() => inputOperation('+')}>+</button>
		
		<button class="number zero" on:click={() => inputNumber('0')}>0</button>
		<button class="number" on:click={inputDecimal}>.</button>
		<button class="equals" on:click={calculate}>=</button>
	</div>
</div>

<style>
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
		background: #ff9500;
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
		background: #ff9500;
		color: white;
		grid-row: span 2;
	}
</style>

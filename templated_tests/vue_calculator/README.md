# Vue Calculator

A modern calculator application built with Vue 3 and Vite.

## Prerequisites

Install Node.js (version 16 or higher):

```bash
# On macOS
brew install node

# On Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# Verify installation
node --version
npm --version
```

## Installation and Setup

Install dependencies:

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## Build

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Testing

Run tests:

```bash
npm test
```

Run tests with UI:

```bash
npm run test:ui
```

Run tests with coverage:

```bash
npm run test:coverage
```

Coverage reports will be generated in the `coverage/` directory.

## Project Structure

```
vue_calculator/
├── src/
│   ├── components/
│   │   └── Calculator.vue
│   ├── utils/
│   │   ├── calculator.js
│   │   └── calculator.test.js
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## Features Demonstrated

- Vue 3 Composition API
- Reactive data with `ref`
- Component-based architecture
- Event handling and methods
- Scoped CSS styling
- CSS Grid layout
- Unit testing with Vitest
- Code coverage reporting
- Modern JavaScript ES6+ features
- Vite build tool
- Single File Components (.vue)

## Calculator Operations

- Basic arithmetic: addition, subtraction, multiplication, division
- Clear functionality
- Decimal number support
- Error handling for division by zero
- Visual feedback for operations

# Svelte Calculator

A modern calculator application built with Svelte and SvelteKit.

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
svelte_calculator/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   └── Calculator.svelte
│   │   └── utils/
│   │       ├── calculator.js
│   │       └── calculator.test.js
│   ├── routes/
│   │   └── +page.svelte
│   └── app.html
├── package.json
├── svelte.config.js
├── vite.config.js
└── README.md
```

## Features Demonstrated

- Svelte reactive programming
- SvelteKit routing and app structure
- Component-based architecture
- Event handling and state management
- CSS Grid layout
- Unit testing with Vitest
- Code coverage reporting
- Modern JavaScript ES6+ features
- Responsive design

## Calculator Operations

- Basic arithmetic: addition, subtraction, multiplication, division
- Clear functionality
- Decimal number support
- Error handling for division by zero
- Visual feedback for operations

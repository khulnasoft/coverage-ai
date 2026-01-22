# Node.js Express Calculator API

A RESTful API built with Node.js and Express that provides calculator operations.

## Prerequisites

Install Node.js (version 14 or higher):

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

## Running the Application

Development mode with auto-reload:

```bash
npm run dev
```

Production mode:

```bash
npm start
```

The server will start on `http://localhost:3000`.

## API Endpoints

### Health Check
```
GET /health
```

Returns the health status of the service.

### Calculator Operations
```
POST /calculate
Content-Type: application/json

{
  "operation": "add|subtract|multiply|divide",
  "a": number,
  "b": number
}
```

Example requests:
```bash
# Addition
curl -X POST http://localhost:3000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 5, "b": 3}'

# Division
curl -X POST http://localhost:3000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 20, "b": 5}'
```

## Testing

Run tests:

```bash
npm test
```

Run tests with coverage:

```bash
npm run test:coverage
```

This will generate a coverage report in the `coverage/` directory and show coverage information in the terminal.

## Project Structure

```
node_express/
├── src/
│   └── app.js          # Main application file
├── tests/
│   └── app.test.js     # Test suite
├── package.json        # Dependencies and scripts
└── README.md          # This file
```

## Features Demonstrated

- Express.js web framework
- RESTful API design
- JSON request/response handling
- Error handling and validation
- Unit testing with Jest
- Code coverage reporting
- Environment-based configuration

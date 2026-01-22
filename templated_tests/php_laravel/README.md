# PHP Laravel Calculator API

A RESTful API built with Laravel that provides calculator operations.

## Prerequisites

Install PHP (version 8.1 or higher) and Composer:

```bash
# On macOS
brew install php composer

# On Ubuntu/Debian
sudo apt update
sudo apt install php8.1 php8.1-cli php8.1-xml php8.1-mbstring php8.1-curl composer

# Verify installation
php --version
composer --version
```

## Installation and Setup

1. Install dependencies:
```bash
composer install
```

2. Set up environment:
```bash
cp .env.example .env
php artisan key:generate
```

3. Start the development server:
```bash
php artisan serve
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
```
GET /api/health
```

Returns the health status of the service.

### Calculator Operations
```
POST /api/calculate
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
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 5, "b": 3}'

# Division
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 20, "b": 5}'
```

## Testing

Run the test suite:

```bash
# Run all tests
php artisan test

# Run with coverage
php artisan test --coverage
```

For detailed coverage reports, you can use Xdebug:

```bash
# Install Xdebug (if not already installed)
pecl install xdebug

# Run tests with Xdebug coverage
XDEBUG_MODE=coverage php artisan test --coverage
```

## Project Structure

```
php_laravel/
├── app/
│   └── Http/
│       └── Controllers/
│           └── CalculatorController.php
├── config/
│   └── app.php
├── routes/
│   └── api.php
├── tests/
│   └── Feature/
│       └── CalculatorTest.php
├── composer.json
├── .env.example
└── README.md
```

## Features Demonstrated

- Laravel framework
- RESTful API design
- Request validation
- Error handling
- Feature testing with PHPUnit
- Code coverage reporting
- Environment configuration
- Modern PHP 8.1 features (match expressions)

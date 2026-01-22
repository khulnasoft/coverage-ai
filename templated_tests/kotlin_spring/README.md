# Kotlin Spring Boot Calculator API

A RESTful API built with Kotlin and Spring Boot that provides calculator operations.

## Prerequisites

Install Java 17 or higher and Gradle:

```bash
# On macOS
brew install openjdk@17 gradle

# On Ubuntu/Debian
sudo apt update
sudo apt install openjdk-17-jdk gradle

# Verify installation
java --version
gradle --version
```

## Build and Run

Build the application:

```bash
./gradlew build
```

Run the application:

```bash
./gradlew bootRun
```

The API will be available at `http://localhost:8080`.

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
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 5, "b": 3}'

# Division
curl -X POST http://localhost:8080/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 20, "b": 5}'
```

## Testing

Run tests:

```bash
./gradlew test
```

Run tests with coverage:

```bash
./gradlew test jacocoTestReport
```

Coverage reports will be generated in `build/reports/jacoco/test/html/index.html`.

## Project Structure

```
kotlin_spring/
├── src/main/kotlin/com/coverageai/kotlinspring/
│   ├── controller/
│   │   └── CalculatorController.kt
│   ├── service/
│   │   └── CalculatorService.kt
│   ├── dto/
│   │   ├── CalculateRequest.kt
│   │   ├── CalculateResponse.kt
│   │   └── HealthResponse.kt
│   └── KotlinSpringApplication.kt
├── src/test/kotlin/com/coverageai/kotlinspring/
│   ├── controller/
│   │   └── CalculatorControllerTest.kt
│   └── service/
│       └── CalculatorServiceTest.kt
├── build.gradle.kts
└── README.md
```

## Features Demonstrated

- Kotlin programming language
- Spring Boot framework
- RESTful API design
- Bean validation
- Error handling
- Unit testing with JUnit 5
- MockMvc for controller testing
- JaCoCo coverage reporting
- Gradle build system
- Modern Kotlin features (data classes, extension functions)

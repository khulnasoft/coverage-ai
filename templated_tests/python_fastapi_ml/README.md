# Python FastAPI ML Calculator

A FastAPI application that demonstrates machine learning integration with a simple linear regression model.

## Prerequisites

Install Python 3.8 or higher:

```bash
# On macOS
brew install python3

# On Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

## Installation and Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
python app.py
```

Or use uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```
GET /health
```

Returns the health status and model information.

### Single Prediction
```
POST /predict
Content-Type: application/json

{
  "input_value": 5.0
}
```

### Batch Prediction
```
POST /predict/batch
Content-Type: application/json

{
  "input_values": [1.0, 2.0, 3.0, 4.0, 5.0]
}
```

## Testing

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

Coverage reports will be generated in the `htmlcov/` directory.

## Project Structure

```
python_fastapi_ml/
├── app.py              # Main FastAPI application
├── test_app.py         # Test suite
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Features Demonstrated

- FastAPI web framework
- Machine learning with scikit-learn
- Pydantic data validation
- Automatic API documentation
- Request/response models
- Error handling
- Unit testing with pytest
- Code coverage reporting
- NumPy for numerical operations
- Linear regression model
- Batch processing
- RESTful API design

## ML Model

The application includes a simple linear regression model trained on dummy data following the pattern `y = 2x + 1` with some noise. This demonstrates:

- Model initialization and training
- Feature scaling with StandardScaler
- Single and batch predictions
- Model state management

## Example Usage

```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"input_value": 5.0}'

# Batch prediction
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"input_values": [1.0, 2.0, 3.0]}'
```

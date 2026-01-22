import pytest
from fastapi.testclient import TestClient
from app import app, ml_model

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["model_trained"] == True
    assert data["model_type"] == "Linear Regression"

def test_single_prediction():
    request_data = {"input_value": 5.0}
    response = client.post("/predict", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["input_value"] == 5.0
    assert "prediction" in data
    assert "model_info" in data
    # The prediction should be close to 11 (2*5 + 1)
    assert abs(data["prediction"] - 11.0) < 2.0  # Allow some tolerance due to noise

def test_batch_prediction():
    request_data = {"input_values": [1.0, 2.0, 3.0]}
    response = client.post("/predict/batch", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 3
    assert len(data["predictions"]) == 3
    assert "model_info" in data
    
    # Check each prediction
    for i, pred in enumerate(data["predictions"]):
        expected_value = 2 * (i + 1) + 1  # 2*x + 1
        assert abs(pred["prediction"] - expected_value) < 2.0

def test_invalid_input():
    # Test with invalid input type
    request_data = {"input_value": "invalid"}
    response = client.post("/predict", json=request_data)
    assert response.status_code == 422  # Validation error

def test_empty_batch():
    request_data = {"input_values": []}
    response = client.post("/predict/batch", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 0
    assert len(data["predictions"]) == 0

def test_large_batch():
    # Test with a larger batch
    request_data = {"input_values": list(range(1, 101))}
    response = client.post("/predict/batch", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 100
    assert len(data["predictions"]) == 100

def test_model_functionality():
    # Test the ML model directly
    prediction = ml_model.predict(5.0)
    assert isinstance(prediction, float)
    assert abs(prediction - 11.0) < 2.0  # Should be close to 2*5 + 1

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert len(data["endpoints"]) == 3

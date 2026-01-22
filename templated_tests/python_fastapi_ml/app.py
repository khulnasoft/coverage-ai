from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

app = FastAPI(title="ML Calculator API", version="1.0.0")

# Simple ML model for demonstration
class MLModel:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self._train_dummy_model()
    
    def _train_dummy_model(self):
        """Train a simple model for demonstration"""
        # Create dummy data: y = 2x + 1 + noise
        X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
        y = np.array([3, 5, 7, 9, 11, 13, 15, 17, 19, 21]) + np.random.normal(0, 0.1, 10)
        
        # Fit the model
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict(self, x: float) -> float:
        if not self.is_trained:
            raise ValueError("Model is not trained")
        
        X = np.array([[x]])
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)
        return float(prediction[0])

# Initialize the ML model
ml_model = MLModel()

class PredictionRequest(BaseModel):
    input_value: float
    
class PredictionResponse(BaseModel):
    input_value: float
    prediction: float
    model_info: str

class BatchPredictionRequest(BaseModel):
    input_values: List[float]
    
class BatchPredictionResponse(BaseModel):
    predictions: List[dict]
    total_count: int
    model_info: str

class HealthResponse(BaseModel):
    status: str
    model_trained: bool
    model_type: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="OK",
        model_trained=ml_model.is_trained,
        model_type="Linear Regression"
    )

@app.post("/predict", response_model=PredictionResponse)
async def make_prediction(request: PredictionRequest):
    try:
        prediction = ml_model.predict(request.input_value)
        return PredictionResponse(
            input_value=request.input_value,
            prediction=prediction,
            model_info="Linear Regression: y ≈ 2x + 1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def make_batch_prediction(request: BatchPredictionRequest):
    try:
        predictions = []
        for value in request.input_values:
            prediction = ml_model.predict(value)
            predictions.append({
                "input_value": value,
                "prediction": prediction
            })
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_count=len(predictions),
            model_info="Linear Regression: y ≈ 2x + 1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "ML Calculator API",
        "endpoints": [
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/predict", "method": "POST", "description": "Single prediction"},
            {"path": "/predict/batch", "method": "POST", "description": "Batch prediction"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

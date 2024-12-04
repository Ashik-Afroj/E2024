# Import required libraries
from fastapi import FastAPI
import pandas as pd
import joblib

# Load the trained machine learning model
model = joblib.load('earthquake_model.pkl')  # Make sure this file is saved and accessible

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Earthquake Prediction API"}

@app.post("/predict/")
def predict(latitude: float, longitude: float, depth: float, year: int, month: int, day: int):
    # Create input features for prediction
    input_features = pd.DataFrame([{
        'latitude': latitude,
        'longitude': longitude,
        'depth': depth,
        'year': year,
        'month': month,
        'day': day
    }])
    
    # Make prediction
    prediction = model.predict(input_features)[0]
    return {"predicted_magnitude": prediction}

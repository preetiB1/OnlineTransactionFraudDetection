from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load the trained model
with open('fraud_detection_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

app = FastAPI()

# Define the data model for the input data. This ensures automatic validation.
class TransactionData(BaseModel):
    step: int
    type: int
    amount: float
    oldbalanceOrg: float
    oldbalanceDest: float

# Define the prediction endpoint
@app.post("/predict")
def predict_fraud(data: TransactionData):
    # Convert the input data to a numpy array for the model
    input_data = np.array([
        data.step,
        data.type,
        data.amount,
        data.oldbalanceOrg,
        data.oldbalanceDest
    ]).reshape(1, -1)

    # Make the prediction
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)[:, 1]

    # Return the prediction and probability
    return {
        "prediction": int(prediction[0]),
        "prediction_probability": float(prediction_proba[0]),
        "is_fraud": bool(prediction[0])
    }

# Root endpoint for basic health check
@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running!"}
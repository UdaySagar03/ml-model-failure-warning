from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_DIR / "models"

MODEL_PATH = MODEL_DIR / "failure_prediction_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"

# Load the trained model and preprocessor
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

# Create FastAPI application
app = FastAPI(
    title="ML Machine Failure Prediction API",
    description="Predict machine failure risk using machine operating readings.",
    version="1.0.0",
)

# Allow requests from the local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this before production deployment
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class MachineReading(BaseModel):
    machine_type: str = Field(pattern="^[LMH]$")
    air_temperature: float
    process_temperature: float
    rotational_speed: int = Field(gt=0)
    torque: float = Field(ge=0)
    tool_wear: int = Field(ge=0)


@app.get("/")
def home():
    return {
        "message": "Machine Failure Prediction API is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(reading: MachineReading):
    try:
        # Use the same feature names and order as model training
        input_data = pd.DataFrame(
            [{
                "Type": reading.machine_type,
                "Air temperature [K]": reading.air_temperature,
                "Process temperature [K]": reading.process_temperature,
                "Rotational speed [rpm]": reading.rotational_speed,
                "Torque [Nm]": reading.torque,
                "Tool wear [min]": reading.tool_wear,
            }]
        )

        # Transform input using the saved preprocessor
        processed_data = preprocessor.transform(input_data)

        # Calculate probability of failure
        failure_probability = float(
            model.predict_proba(processed_data)[0, 1]
        )

        # Use the experimental threshold from your project
        threshold = 0.25
        predicted_failure = int(failure_probability >= threshold)

        if failure_probability >= 0.50:
            risk_level = "High"
        elif failure_probability >= threshold:
            risk_level = "Elevated"
        else:
            risk_level = "Low"

        return {
            "predicted_failure": predicted_failure,
            "failure_probability": round(failure_probability, 4),
            "failure_probability_percent": round(
                failure_probability * 100, 2
            ),
            "risk_level": risk_level,
            "threshold": threshold,
            "message": (
                "Potential failure detected. Inspect the machine."
                if predicted_failure
                else "No failure predicted at the configured threshold."
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}",
        ) from exc
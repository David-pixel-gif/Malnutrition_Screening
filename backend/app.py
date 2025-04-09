import os
import logging
import traceback
import warnings
import pandas as pd
import joblib

from fastapi import FastAPI, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# 🔌 Database and Auth
from models import Base, engine
from auth import auth_router

# 🔧 Ensure log directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 📝 Logging configuration
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "errors.log"),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 🧠 Suppress sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# 🚀 FastAPI instance
app = FastAPI(
    title="Malnutrition Risk Detection API",
    description="API for predicting malnutrition risk using anthropometric data and authenticating users.",
    version="1.0.0"
)

# 🌐 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to trusted origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📥 Input Schema
class MalnutritionInput(BaseModel):
    Stunting: float
    Wasting: float
    Underweight: float
    Overweight: float
    U5_Pop_Thousands: float

# 🧠 Label meanings
label_description = {
    "Low": "Minimal malnutrition risk.",
    "Moderate": "Moderate risk. Consider intervention.",
    "High": "High risk. Urgent intervention advised.",
    "Very High": "Critical risk. Immediate intervention required."
}

# 🔍 Load Model and Scaler
MODEL_PATH = "malnutrition_risk_model.pkl"
SCALER_PATH = "feature_scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ ML model and scaler loaded.")
except Exception as e:
    logger.error("❌ Model or scaler failed to load", exc_info=True)
    raise RuntimeError(f"❌ Model or scaler load error: {e}")

# 🧱 Create tables
Base.metadata.create_all(bind=engine)

# 🔗 Register authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# 🏠 Root route
@app.get("/")
def read_root():
    return {"message": "🌐 Malnutrition Risk Prediction API is running!"}

# 📊 Predict POST endpoint
@app.post("/predict")
def predict(data: MalnutritionInput):
    try:
        df = pd.DataFrame([data.dict()])
        X_scaled = scaler.transform(df)
        prediction = model.predict(X_scaled)[0]

        return {
            "input": data.dict(),
            "predicted_risk_level": prediction,
            "description": label_description.get(prediction, "No description available.")
        }

    except Exception as e:
        logger.error("Prediction failed", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

# 🔍 Predict via GET (query string)
@app.get("/predict")
def predict_get(
    Stunting: float = Query(...),
    Wasting: float = Query(...),
    Underweight: float = Query(...),
    Overweight: float = Query(...),
    U5_Pop_Thousands: float = Query(...)
):
    return predict(MalnutritionInput(
        Stunting=Stunting,
        Wasting=Wasting,
        Underweight=Underweight,
        Overweight=Overweight,
        U5_Pop_Thousands=U5_Pop_Thousands
    ))

# 📂 Batch prediction
@app.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
        required_cols = ["Stunting", "Wasting", "Underweight", "Overweight", "U5_Pop_Thousands"]

        if not all(col in df.columns for col in required_cols):
            return JSONResponse(
                status_code=400,
                content={"error": f"Missing columns. Required: {required_cols}"}
            )

        clean_df = df[required_cols].dropna()
        predictions = model.predict(scaler.transform(clean_df))

        df_result = df.loc[clean_df.index].copy()
        df_result["Predicted Risk"] = predictions

        return {"predictions": df_result.to_dict(orient="records")}

    except Exception as e:
        logger.error("Batch prediction failed", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

# 🖨️ Print all registered routes on startup
@app.on_event("startup")
def log_routes():
    routes = [f"{route.path} ({', '.join(route.methods)})" for route in app.routes if hasattr(route, "methods")]
    print("\n📋 Registered Routes:")
    for r in routes:
        print("•", r)
    logger.info("📋 Registered Routes:\n" + "\n".join(routes))

# 🔁 Dev runner
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting server at http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

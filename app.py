"""
Fetal Health Prediction System - Main Application
A Flask web application for predicting fetal health conditions.
"""

from flask import Flask, request, render_template, jsonify
import joblib
import os
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fetal_health.pkl")

# Load the ML model
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Class labels mapping
CLASS_LABELS = {
    1.0: "NORMAL",
    2.0: "SUSPECT", 
    3.0: "PATHOLOGICAL"
}

# Feature names in correct order
FEATURE_NAMES = [
    'prolongued_decelerations',
    'abnormal_short_term_variability',
    'percentage_abnormal_long_term_variability',
    'histogram_variance',
    'histogram_median',
    'mean_long_term_variability',
    'histogram_mode',
    'accelerations'
]

# Feature validation ranges
FEATURE_RANGES = {
    'prolongued_decelerations': (0.0, 0.005),
    'abnormal_short_term_variability': (12.0, 87.0),
    'percentage_abnormal_long_term_variability': (0.0, 91.0),
    'histogram_variance': (0.0, 269.0),
    'histogram_median': (77.0, 186.0),
    'mean_long_term_variability': (0.0, 50.7),
    'histogram_mode': (60.0, 187.0),
    'accelerations': (0.0, 0.019)
}

def validate_input(data):
    """Validate input data for prediction."""
    errors = []
    
    # Check if all required features are present
    missing_features = [f for f in FEATURE_NAMES if f not in data]
    if missing_features:
        errors.append(f"Missing features: {', '.join(missing_features)}")
    
    # Validate data types and ranges
    for feature, value in data.items():
        if feature in FEATURE_RANGES:
            try:
                value = float(value)
                min_val, max_val = FEATURE_RANGES[feature]
                if not (min_val <= value <= max_val):
                    errors.append(f"{feature}: value {value} outside range [{min_val}, {max_val}]")
            except (ValueError, TypeError):
                errors.append(f"{feature}: invalid numeric value")
    
    return errors

def make_prediction(data):
    """Make prediction using the loaded model."""
    if model is None:
        return {
            "success": False,
            "error": "Model not loaded",
            "prediction": None,
            "confidence": None
        }
    
    # Validate input
    errors = validate_input(data)
    if errors:
        return {
            "success": False,
            "error": "; ".join(errors),
            "prediction": None,
            "confidence": None
        }
    
    try:
        # Prepare features in correct order
        features = [float(data[feature]) for feature in FEATURE_NAMES]
        X = np.array([features])
        
        # Make prediction
        prediction = model.predict(X)[0]
        result = CLASS_LABELS[prediction]
        
        # Get confidence scores
        confidence = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X)[0]
            confidence = {
                "NORMAL": float(probabilities[0]),
                "SUSPECT": float(probabilities[1]),
                "PATHOLOGICAL": float(probabilities[2])
            }
        
        return {
            "success": True,
            "prediction": result,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "input_data": data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Prediction error: {str(e)}",
            "prediction": None,
            "confidence": None
        }

@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")

@app.route("/form")
def form():
    """Prediction form page."""
    return render_template("form.html", features=FEATURE_NAMES, ranges=FEATURE_RANGES)

@app.route("/predict", methods=["POST"])
def predict():
    """Handle form submission and make prediction."""
    try:
        # Extract data from form
        data = {}
        for feature in FEATURE_NAMES:
            value = request.form.get(feature)
            if value:
                data[feature] = float(value)
        
        # Make prediction
        result = make_prediction(data)
        
        if result["success"]:
            return render_template("result.html", 
                                 prediction=result["prediction"],
                                 confidence=result["confidence"],
                                 input_data=result["input_data"])
        else:
            return render_template("error.html", error=result["error"])
            
    except Exception as e:
        return render_template("error.html", error=f"Processing error: {str(e)}")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """API endpoint for predictions."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        result = make_prediction(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/sample")
def api_sample():
    """Get sample input data."""
    sample_data = {
        'prolongued_decelerations': 0.002,
        'abnormal_short_term_variability': 50.0,
        'percentage_abnormal_long_term_variability': 45.0,
        'histogram_variance': 134.0,
        'histogram_median': 130.0,
        'mean_long_term_variability': 25.0,
        'histogram_mode': 120.0,
        'accelerations': 0.01
    }
    return jsonify(sample_data)

@app.route("/api/features")
def api_features():
    """Get feature information."""
    feature_info = {}
    for feature in FEATURE_NAMES:
        min_val, max_val = FEATURE_RANGES[feature]
        feature_info[feature] = {
            "range": [min_val, max_val],
            "description": feature.replace('_', ' ').title()
        }
    return jsonify(feature_info)

@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("error.html", error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template("error.html", error="Internal server error"), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
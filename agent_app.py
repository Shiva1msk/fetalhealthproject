"""
Fetal Health AI Agent Web Application
Flask web interface for the intelligent fetal health agent.
"""

from flask import Flask, request, render_template, jsonify
from agent import FetalHealthAgent
import json
import os

app = Flask(__name__)
agent = FetalHealthAgent()

@app.route("/")
def home():
    """Agent home page."""
    return render_template("agent_home.html")

@app.route("/agent")
def agent_interface():
    """Main agent chat interface."""
    return render_template("agent_interface.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat messages from the user."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Check if user provided prediction data
        prediction_data = data.get('data')
        
        response = agent.process_query(message, prediction_data)
        
        return jsonify({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/predict", methods=["POST"])
def predict():
    """Handle prediction requests."""
    try:
        data = request.get_json()
        result = agent.make_prediction(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/sample")
def get_sample():
    """Get sample data."""
    return jsonify(agent.get_sample_data())

@app.route("/api/features")
def get_features():
    """Get feature information."""
    return jsonify(agent.get_feature_info())

@app.route("/api/examples")
def get_examples():
    """Get example cases for each classification."""
    return jsonify(agent.get_example_cases())

@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "agent_ready": agent.model is not None,
        "timestamp": agent.get_sample_data()  # Reuse for timestamp
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
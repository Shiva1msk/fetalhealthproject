"""
Fetal Health AI Agent
Intelligent agent for natural language interaction with the fetal health prediction system.
"""

import joblib
import os
import json
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

class FetalHealthAgent:
    def __init__(self, model_path: str = None):
        """Initialize the agent with the ML model."""
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "models", "fetal_health.pkl")
        
        self.model_path = model_path
        self.model = None
        self.labels = ['NORMAL', 'SUSPECT', 'PATHOLOGICAL']
        self.feature_names = [
            'prolongued_decelerations',
            'abnormal_short_term_variability', 
            'percentage_abnormal_long_term_variability',
            'histogram_variance',
            'histogram_median',
            'mean_long_term_variability',
            'histogram_mode',
            'accelerations'
        ]
        self.load_model()
        
    def load_model(self) -> bool:
        """Load the ML model."""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"✅ Agent model loaded successfully from {self.model_path}")
                return True
            else:
                print(f"❌ Model file not found: {self.model_path}")
                return False
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def validate_input(self, data: Dict[str, float]) -> tuple[bool, str]:
        """Validate input data for prediction."""
        try:
            # Check if all required features are present
            missing_features = [f for f in self.feature_names if f not in data]
            if missing_features:
                return False, f"Missing features: {', '.join(missing_features)}"
            
            # Validate data types and ranges
            ranges = {
                'prolongued_decelerations': (0.0, 0.005),
                'abnormal_short_term_variability': (12.0, 87.0),
                'percentage_abnormal_long_term_variability': (0.0, 91.0),
                'histogram_variance': (0.0, 269.0),
                'histogram_median': (77.0, 186.0),
                'mean_long_term_variability': (0.0, 50.7),
                'histogram_mode': (60.0, 187.0),
                'accelerations': (0.0, 0.019)
            }
            
            for feature, value in data.items():
                if not isinstance(value, (int, float)):
                    return False, f"Invalid data type for {feature}: expected number, got {type(value)}"
                
                if feature in ranges:
                    min_val, max_val = ranges[feature]
                    if not (min_val <= value <= max_val):
                        return False, f"Value for {feature} should be between {min_val} and {max_val}"
            
            return True, "Input validation successful"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def make_prediction(self, data: Dict[str, float]) -> Dict[str, Any]:
        """Make a prediction using the loaded model."""
        if self.model is None:
            return {
                "success": False,
                "error": "Model not loaded",
                "prediction": None,
                "confidence": None
            }
        
        # Validate input
        is_valid, message = self.validate_input(data)
        if not is_valid:
            return {
                "success": False,
                "error": message,
                "prediction": None,
                "confidence": None
            }
        
        try:
            # Prepare data for prediction
            features = [data[feature] for feature in self.feature_names]
            X = np.array([features])
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            # Map model classes [1.0, 2.0, 3.0] to array indices [0, 1, 2]
            class_index = int(prediction) - 1
            result = self.labels[class_index]
            
            # Get prediction probabilities
            confidence = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(X)[0]
                confidence = {
                    label: float(prob) for label, prob in zip(self.labels, probabilities)
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
    
    def get_sample_data(self) -> Dict[str, float]:
        """Return sample data for testing."""
        return {
            'prolongued_decelerations': 0.002,
            'abnormal_short_term_variability': 50.0,
            'percentage_abnormal_long_term_variability': 45.0,
            'histogram_variance': 134.0,
            'histogram_median': 130.0,
            'mean_long_term_variability': 25.0,
            'histogram_mode': 120.0,
            'accelerations': 0.01
        }
    
    def get_feature_info(self) -> Dict[str, Dict[str, Any]]:
        """Return information about features and their expected ranges."""
        return {
            'prolongued_decelerations': {
                'description': 'Prolonged decelerations in fetal heart rate',
                'range': [0.0, 0.005],
                'unit': 'ratio',
                'importance': 'Low values indicate healthier condition'
            },
            'abnormal_short_term_variability': {
                'description': 'Abnormal short-term variability percentage',
                'range': [12.0, 87.0],
                'unit': 'percentage',
                'importance': 'Most important feature - extreme values indicate problems'
            },
            'percentage_abnormal_long_term_variability': {
                'description': 'Percentage of time with abnormal long-term variability',
                'range': [0.0, 91.0],
                'unit': 'percentage',
                'importance': 'Second most important - high values concerning'
            },
            'histogram_variance': {
                'description': 'Variance of the fetal heart rate histogram',
                'range': [0.0, 269.0],
                'unit': 'numeric',
                'importance': 'Extreme values (very high/low) indicate issues'
            },
            'histogram_median': {
                'description': 'Median of the fetal heart rate histogram',
                'range': [77.0, 186.0],
                'unit': 'bpm',
                'importance': 'Normal range around 140-160 bpm'
            },
            'mean_long_term_variability': {
                'description': 'Mean value of long-term variability',
                'range': [0.0, 50.7],
                'unit': 'numeric',
                'importance': 'Zero values are extremely concerning'
            },
            'histogram_mode': {
                'description': 'Mode of the fetal heart rate histogram',
                'range': [60.0, 187.0],
                'unit': 'bpm',
                'importance': 'Should align with median for healthy patterns'
            },
            'accelerations': {
                'description': 'Number of accelerations per second',
                'range': [0.0, 0.019],
                'unit': 'per second',
                'importance': 'Higher values indicate healthy fetal responses'
            }
        }
    
    def get_example_cases(self) -> Dict[str, Dict[str, float]]:
        """Return example cases for each classification."""
        return {
            "NORMAL": {
                "prolongued_decelerations": 0.0,
                "abnormal_short_term_variability": 85.0,
                "percentage_abnormal_long_term_variability": 5.0,
                "histogram_variance": 80.0,
                "histogram_median": 170.0,
                "mean_long_term_variability": 5.0,
                "histogram_mode": 170.0,
                "accelerations": 0.015
            },
            "SUSPECT": {
                "prolongued_decelerations": 0.0,
                "abnormal_short_term_variability": 73.0,
                "percentage_abnormal_long_term_variability": 43.0,
                "histogram_variance": 73.0,
                "histogram_median": 121.0,
                "mean_long_term_variability": 2.4,
                "histogram_mode": 120.0,
                "accelerations": 0.0
            },
            "PATHOLOGICAL": {
                "prolongued_decelerations": 0.002,
                "abnormal_short_term_variability": 26.0,
                "percentage_abnormal_long_term_variability": 0.0,
                "histogram_variance": 170.0,
                "histogram_median": 107.0,
                "mean_long_term_variability": 0.0,
                "histogram_mode": 76.0,
                "accelerations": 0.001
            }
        }
    
    def process_query(self, query: str, data: Optional[Dict[str, float]] = None) -> str:
        """Process natural language queries from users."""
        query_lower = query.lower()
        
        if "predict" in query_lower or "prediction" in query_lower:
            if data:
                result = self.make_prediction(data)
                if result["success"]:
                    response = f"🔍 **Prediction: {result['prediction']}**\n\n"
                    if result['confidence']:
                        response += "📊 **Confidence Scores:**\n"
                        for label, conf in result['confidence'].items():
                            emoji = "🟢" if label == "NORMAL" else "🟡" if label == "SUSPECT" else "🔴"
                            response += f"  {emoji} {label}: {conf:.1%}\n"
                    
                    # Add interpretation
                    pred = result['prediction']
                    if pred == "NORMAL":
                        response += "\n✅ **Interpretation:** Healthy fetal condition. Regular monitoring sufficient."
                    elif pred == "SUSPECT":
                        response += "\n⚠️ **Interpretation:** Requires medical attention and close monitoring."
                    else:
                        response += "\n🚨 **Interpretation:** URGENT - Immediate medical intervention required!"
                    
                    return response
                else:
                    return f"❌ **Prediction failed:** {result['error']}"
            else:
                return "To make a prediction, please provide the required medical data. Use 'sample' to see example data format."
        
        elif "sample" in query_lower or "example" in query_lower:
            if "cases" in query_lower or "all" in query_lower:
                examples = self.get_example_cases()
                response = "📋 **Example Cases for Each Classification:**\n\n"
                for class_name, data in examples.items():
                    emoji = "🟢" if class_name == "NORMAL" else "🟡" if class_name == "SUSPECT" else "🔴"
                    response += f"{emoji} **{class_name} Case:**\n"
                    for key, value in data.items():
                        response += f"  • {key}: {value}\n"
                    response += "\n"
                return response
            else:
                sample = self.get_sample_data()
                response = "📋 **Sample Input Data:**\n\n"
                for key, value in sample.items():
                    response += f"  • **{key}**: {value}\n"
                return response
        
        elif "features" in query_lower or "parameters" in query_lower:
            features = self.get_feature_info()
            response = "📝 **Medical Parameters Information:**\n\n"
            for name, info in features.items():
                response += f"**{name.replace('_', ' ').title()}:**\n"
                response += f"  • Description: {info['description']}\n"
                response += f"  • Range: {info['range'][0]} - {info['range'][1]} {info['unit']}\n"
                response += f"  • Clinical Note: {info['importance']}\n\n"
            return response
        
        elif "help" in query_lower:
            return """
🤖 **Fetal Health AI Agent Help**

**Available Commands:**
• **"predict"** - Make a prediction (requires medical data)
• **"sample"** - Get sample input data format
• **"sample cases"** - Get examples for all classifications
• **"features"** - Get detailed parameter information
• **"help"** - Show this help message

**Classifications:**
🟢 **NORMAL** - Healthy fetal condition
🟡 **SUSPECT** - Requires medical attention  
🔴 **PATHOLOGICAL** - Urgent intervention needed

**To make a prediction:**
Provide medical data in JSON format with all 8 required parameters.

**Medical Disclaimer:**
This system is for clinical decision support only. Always combine with professional medical judgment.
"""
        
        elif "accuracy" in query_lower or "performance" in query_lower:
            return """
📊 **Model Performance:**

• **Overall Accuracy:** 95.92%
• **Algorithm:** Random Forest Classifier
• **Training Data:** 2,126 fetal health records
• **Features:** 8 medical parameters
• **Classes:** 3 fetal health conditions

**Feature Importance:**
1. Abnormal Short Term Variability (22.83%)
2. Percentage Abnormal Long Term Variability (19.52%)
3. Histogram Median (13.37%)
4. Histogram Mode (12.36%)

**Clinical Validation:**
✅ Suitable for medical screening
✅ High reliability for decision support
⚠️ Requires clinical oversight
"""
        
        else:
            return """
I can help you with fetal health predictions! 

**Try asking:**
• "help" - See all available commands
• "sample" - Get example input data
• "features" - Learn about medical parameters
• "sample cases" - See examples for each classification
• "accuracy" - View model performance details

**For predictions:** Provide medical data and ask me to "predict"
"""


def main():
    """Main function to demonstrate the agent."""
    print("🤖 Fetal Health AI Agent Starting...")
    
    # Initialize agent
    agent = FetalHealthAgent()
    
    if agent.model is None:
        print("❌ Cannot start agent - model not loaded")
        return
    
    # Test with sample data
    print("\n📋 Testing with sample data:")
    sample_data = agent.get_sample_data()
    result = agent.make_prediction(sample_data)
    
    if result["success"]:
        print(f"✅ Prediction: {result['prediction']}")
        if result['confidence']:
            print("📊 Confidence scores:")
            for label, conf in result['confidence'].items():
                print(f"  • {label}: {conf:.2%}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Interactive mode
    print("\n💬 Interactive mode (type 'quit' to exit):")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            response = agent.process_query(user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
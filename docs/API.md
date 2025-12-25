# API Documentation

## Overview

The Fetal Health Prediction System provides RESTful API endpoints for making predictions and accessing system information.

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, no authentication is required. For production deployment, consider implementing API keys or OAuth.

## Endpoints

### Health Check

**GET** `/health`

Check if the system is running and the model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-22T15:30:00.000000"
}
```

### Get Sample Data

**GET** `/api/sample`

Returns sample input data for testing predictions.

**Response:**
```json
{
  "prolongued_decelerations": 0.002,
  "abnormal_short_term_variability": 50.0,
  "percentage_abnormal_long_term_variability": 45.0,
  "histogram_variance": 134.0,
  "histogram_median": 130.0,
  "mean_long_term_variability": 25.0,
  "histogram_mode": 120.0,
  "accelerations": 0.01
}
```

### Get Feature Information

**GET** `/api/features`

Returns information about all input features including ranges and descriptions.

**Response:**
```json
{
  "prolongued_decelerations": {
    "range": [0.0, 0.005],
    "description": "Prolongued Decelerations"
  },
  "abnormal_short_term_variability": {
    "range": [12.0, 87.0],
    "description": "Abnormal Short Term Variability"
  }
  // ... other features
}
```

### Make Prediction

**POST** `/api/predict`

Make a fetal health prediction based on medical parameters.

**Request Body:**
```json
{
  "prolongued_decelerations": 0.002,
  "abnormal_short_term_variability": 50.0,
  "percentage_abnormal_long_term_variability": 45.0,
  "histogram_variance": 134.0,
  "histogram_median": 130.0,
  "mean_long_term_variability": 25.0,
  "histogram_mode": 120.0,
  "accelerations": 0.01
}
```

**Success Response:**
```json
{
  "success": true,
  "prediction": "NORMAL",
  "confidence": {
    "NORMAL": 0.79,
    "SUSPECT": 0.16,
    "PATHOLOGICAL": 0.05
  },
  "timestamp": "2025-12-22T15:30:00.000000",
  "input_data": {
    // Original input data
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Missing features: histogram_variance, histogram_median",
  "prediction": null,
  "confidence": null
}
```

## Agent API Endpoints

### Chat with Agent

**POST** `/api/chat`

Send a message to the AI agent for natural language interaction.

**Request Body:**
```json
{
  "message": "help",
  "data": {
    // Optional: medical data for predictions
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "🤖 Fetal Health AI Agent Help:\n\nAvailable commands:\n• \"predict\" - Make a prediction..."
}
```

### Get Example Cases

**GET** `/api/examples`

Returns example cases for each classification type.

**Response:**
```json
{
  "NORMAL": {
    "prolongued_decelerations": 0.0,
    "abnormal_short_term_variability": 85.0,
    // ... other parameters
  },
  "SUSPECT": {
    // ... suspect case parameters
  },
  "PATHOLOGICAL": {
    // ... pathological case parameters
  }
}
```

## Error Codes

- **200**: Success
- **400**: Bad Request (invalid input data)
- **500**: Internal Server Error (model error, system error)

## Rate Limiting

Currently no rate limiting is implemented. For production, consider implementing rate limiting based on your requirements.

## Data Validation

All input data is validated for:
- Required fields presence
- Data type correctness
- Value range compliance
- Medical parameter constraints

## Security Considerations

For production deployment:
- Implement HTTPS
- Add API authentication
- Implement rate limiting
- Add input sanitization
- Log all API requests
- Monitor for unusual patterns

## Integration Examples

### Python
```python
import requests

# Make prediction
data = {
    "prolongued_decelerations": 0.002,
    "abnormal_short_term_variability": 50.0,
    # ... other parameters
}

response = requests.post('http://localhost:5000/api/predict', json=data)
result = response.json()

if result['success']:
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}")
```

### JavaScript
```javascript
// Make prediction
const data = {
    prolongued_decelerations: 0.002,
    abnormal_short_term_variability: 50.0,
    // ... other parameters
};

fetch('/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        console.log('Prediction:', result.prediction);
        console.log('Confidence:', result.confidence);
    }
});
```

### cURL
```bash
# Make prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "prolongued_decelerations": 0.002,
    "abnormal_short_term_variability": 50.0,
    "percentage_abnormal_long_term_variability": 45.0,
    "histogram_variance": 134.0,
    "histogram_median": 130.0,
    "mean_long_term_variability": 25.0,
    "histogram_mode": 120.0,
    "accelerations": 0.01
  }'
```
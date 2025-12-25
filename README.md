# 🏥 Fetal Health Prediction System

A comprehensive AI-powered system for predicting fetal health conditions using machine learning with 95.92% accuracy.

## 🎯 Features

- **High Accuracy**: 95.92% prediction accuracy using Random Forest
- **Three Classifications**: NORMAL, SUSPECT, PATHOLOGICAL
- **Confidence Scores**: Probability estimates for each prediction
- **Web Interface**: User-friendly form-based interface
- **AI Agent**: Intelligent chat-based interaction
- **REST API**: Complete API for integration
- **Docker Ready**: Containerized deployment
- **Cloud Deploy**: Multiple platform configurations
- https://fetalhealthproject.onrender.com

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Main web interface
python app.py

# AI Agent interface  
python agent_app.py

# Docker deployment
docker-compose up
```

### 3. Access Applications
- **Main App**: http://localhost:5000
- **Agent App**: http://localhost:5001
- **API Docs**: See API section below

## 📊 Model Performance

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 95.92%
- **Features**: 8 medical parameters
- **Classes**: 3 fetal health conditions
- **Confidence**: Probability scores included

## 🏗️ Project Structure

```
fetal-health-system/
├── app.py                 # Main Flask application
├── agent_app.py          # AI agent interface
├── agent.py              # Core agent logic
├── models/
│   └── fetal_health.pkl  # Trained ML model
├── data/
│   └── fetal_health.csv  # Training dataset
├── templates/            # HTML templates
├── static/              # CSS and assets
├── tests/               # Test files
├── deployment/          # Deployment configs
└── docs/               # Documentation
```

## 🔬 Medical Parameters

The system analyzes 8 key fetal health indicators:

1. **Prolonged Decelerations** (0.0 - 0.005)
2. **Abnormal Short Term Variability** (12.0 - 87.0)
3. **Percentage Abnormal Long Term Variability** (0.0 - 91.0)
4. **Histogram Variance** (0.0 - 269.0)
5. **Histogram Median** (77.0 - 186.0)
6. **Mean Long Term Variability** (0.0 - 50.7)
7. **Histogram Mode** (60.0 - 187.0)
8. **Accelerations** (0.0 - 0.019)

## 📈 Prediction Classes

### 🟢 NORMAL
- Healthy fetal condition
- Regular monitoring sufficient
- No immediate concerns

### 🟡 SUSPECT  
- Requires medical attention
- Close monitoring needed
- Clinical evaluation recommended

### 🔴 PATHOLOGICAL
- Urgent intervention required
- High-risk situation
- Emergency obstetric care needed

## 🛠️ API Reference

### Prediction Endpoint
```bash
POST /api/predict
Content-Type: application/json

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

### Response
```json
{
  "success": true,
  "prediction": "NORMAL",
  "confidence": {
    "NORMAL": 0.79,
    "SUSPECT": 0.16,
    "PATHOLOGICAL": 0.05
  },
  "timestamp": "2025-12-22T09:30:06.137261"
}
```

## 🚀 Deployment

### Docker
```bash
docker build -t fetal-health-app .
docker run -p 8000:7860 fetal-health-app
```

### Cloud Platforms
- **Render**: Uses `render.yaml`
- **Railway**: Uses `railway.json`
- **Vercel**: Uses `vercel.json`
- **Heroku**: Uses `Procfile`
- **Google Cloud**: Uses `app.yaml`

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Test specific component
python test_agent.py
python test_model.py
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Model Documentation](docs/model.md)
- [Agent Guide](docs/agent.md)

## ⚠️ Medical Disclaimer

This system is designed for **clinical decision support only**. It should:
- Be used alongside professional medical judgment
- Not replace clinical evaluation
- Be validated with current medical protocols
- Include human oversight for all decisions

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📞 Support

For technical support or medical integration questions, please refer to the documentation or create an issue.

---

**Built with ❤️ for better fetal health outcomes**

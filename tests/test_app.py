"""
Test suite for the main Flask application
"""

import pytest
import json
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Fetal Health Prediction System' in response.data

def test_form_page(client):
    """Test form page loads correctly."""
    response = client.get('/form')
    assert response.status_code == 200
    assert b'Prediction Form' in response.data

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_api_sample(client):
    """Test sample data API endpoint."""
    response = client.get('/api/sample')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prolongued_decelerations' in data
    assert len(data) == 8

def test_api_features(client):
    """Test features API endpoint."""
    response = client.get('/api/features')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prolongued_decelerations' in data

def test_api_predict_valid_data(client):
    """Test prediction API with valid data."""
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
    
    response = client.post('/api/predict',
                          data=json.dumps(sample_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'prediction' in data
    assert data['prediction'] in ['NORMAL', 'SUSPECT', 'PATHOLOGICAL']

def test_api_predict_invalid_data(client):
    """Test prediction API with invalid data."""
    invalid_data = {
        'prolongued_decelerations': 999,  # Out of range
        'abnormal_short_term_variability': 50.0
        # Missing other required fields
    }
    
    response = client.post('/api/predict',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'error' in data

def test_form_submission(client):
    """Test form submission with valid data."""
    form_data = {
        'prolongued_decelerations': '0.002',
        'abnormal_short_term_variability': '50.0',
        'percentage_abnormal_long_term_variability': '45.0',
        'histogram_variance': '134.0',
        'histogram_median': '130.0',
        'mean_long_term_variability': '25.0',
        'histogram_mode': '120.0',
        'accelerations': '0.01'
    }
    
    response = client.post('/predict', data=form_data)
    assert response.status_code == 200
    assert b'Prediction Result' in response.data

if __name__ == '__main__':
    pytest.main([__file__])
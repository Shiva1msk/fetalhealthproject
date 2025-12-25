"""
Test suite for the AI agent
"""

import pytest
import sys
import os

# Add parent directory to path to import agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import FetalHealthAgent

@pytest.fixture
def agent():
    """Create agent instance for testing."""
    return FetalHealthAgent()

def test_agent_initialization(agent):
    """Test agent initializes correctly."""
    assert agent is not None
    assert len(agent.feature_names) == 8
    assert len(agent.labels) == 3

def test_sample_data(agent):
    """Test sample data generation."""
    sample = agent.get_sample_data()
    assert len(sample) == 8
    assert 'prolongued_decelerations' in sample
    assert isinstance(sample['prolongued_decelerations'], float)

def test_feature_info(agent):
    """Test feature information."""
    features = agent.get_feature_info()
    assert len(features) == 8
    assert 'prolongued_decelerations' in features
    assert 'range' in features['prolongued_decelerations']

def test_example_cases(agent):
    """Test example cases."""
    examples = agent.get_example_cases()
    assert 'NORMAL' in examples
    assert 'SUSPECT' in examples
    assert 'PATHOLOGICAL' in examples
    
    for case in examples.values():
        assert len(case) == 8

def test_input_validation_valid(agent):
    """Test input validation with valid data."""
    valid_data = agent.get_sample_data()
    is_valid, message = agent.validate_input(valid_data)
    assert is_valid == True
    assert "successful" in message

def test_input_validation_invalid_range(agent):
    """Test input validation with out-of-range data."""
    invalid_data = agent.get_sample_data()
    invalid_data['prolongued_decelerations'] = 999  # Out of range
    
    is_valid, message = agent.validate_input(invalid_data)
    assert is_valid == False
    assert "between" in message

def test_input_validation_missing_features(agent):
    """Test input validation with missing features."""
    incomplete_data = {
        'prolongued_decelerations': 0.002,
        'abnormal_short_term_variability': 50.0
        # Missing other features
    }
    
    is_valid, message = agent.validate_input(incomplete_data)
    assert is_valid == False
    assert "Missing features" in message

def test_prediction_valid_data(agent):
    """Test prediction with valid data."""
    if agent.model is None:
        pytest.skip("Model not loaded")
    
    sample_data = agent.get_sample_data()
    result = agent.make_prediction(sample_data)
    
    assert result['success'] == True
    assert result['prediction'] in ['NORMAL', 'SUSPECT', 'PATHOLOGICAL']
    assert 'confidence' in result
    assert 'timestamp' in result

def test_prediction_invalid_data(agent):
    """Test prediction with invalid data."""
    invalid_data = {'invalid': 'data'}
    result = agent.make_prediction(invalid_data)
    
    assert result['success'] == False
    assert 'error' in result

def test_query_processing_help(agent):
    """Test query processing for help command."""
    response = agent.process_query("help")
    assert "Fetal Health AI Agent Help" in response
    assert "Available Commands" in response

def test_query_processing_sample(agent):
    """Test query processing for sample command."""
    response = agent.process_query("sample")
    assert "Sample Input Data" in response
    assert "prolongued_decelerations" in response

def test_query_processing_features(agent):
    """Test query processing for features command."""
    response = agent.process_query("features")
    assert "Medical Parameters Information" in response
    assert "Description:" in response

def test_query_processing_accuracy(agent):
    """Test query processing for accuracy command."""
    response = agent.process_query("accuracy")
    assert "Model Performance" in response
    assert "95.92%" in response

def test_query_processing_unknown(agent):
    """Test query processing for unknown command."""
    response = agent.process_query("unknown command")
    assert "help" in response.lower()

if __name__ == '__main__':
    pytest.main([__file__])
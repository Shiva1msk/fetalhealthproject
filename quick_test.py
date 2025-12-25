#!/usr/bin/env python3
"""
Quick Test Script for Fetal Health Prediction System
Tests all major components to ensure everything works correctly.
"""

import sys
import os
import json
import time
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask")
        
        import numpy
        print("✅ NumPy")
        
        import pandas
        print("✅ Pandas")
        
        import sklearn
        print("✅ scikit-learn")
        
        import joblib
        print("✅ joblib")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_model_loading():
    """Test if the ML model can be loaded."""
    print("\n🔍 Testing model loading...")
    
    model_path = Path('models/fetal_health.pkl')
    
    if not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        return False
    
    try:
        import joblib
        model = joblib.load(model_path)
        print(f"✅ Model loaded successfully")
        print(f"   Type: {type(model).__name__}")
        print(f"   Features: {getattr(model, 'n_features_in_', 'Unknown')}")
        print(f"   Classes: {getattr(model, 'classes_', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_agent():
    """Test the AI agent functionality."""
    print("\n🔍 Testing AI agent...")
    
    try:
        from agent import FetalHealthAgent
        
        agent = FetalHealthAgent()
        print("✅ Agent initialized")
        
        # Test sample data
        sample = agent.get_sample_data()
        print(f"✅ Sample data: {len(sample)} features")
        
        # Test feature info
        features = agent.get_feature_info()
        print(f"✅ Feature info: {len(features)} features")
        
        # Test query processing
        response = agent.process_query("help")
        print("✅ Query processing works")
        
        # Test prediction if model is loaded
        if agent.model is not None:
            result = agent.make_prediction(sample)
            if result['success']:
                print(f"✅ Prediction: {result['prediction']}")
                print(f"   Confidence: {max(result['confidence'].values()):.1%}")
            else:
                print(f"❌ Prediction failed: {result['error']}")
                return False
        else:
            print("⚠️ Model not loaded, skipping prediction test")
        
        return True
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        return False

def test_flask_app():
    """Test Flask application components."""
    print("\n🔍 Testing Flask application...")
    
    try:
        # Import app without running it
        sys.path.insert(0, '.')
        from app import app, make_prediction, validate_input, FEATURE_NAMES
        
        print("✅ Flask app imported")
        print(f"✅ Feature names: {len(FEATURE_NAMES)} features")
        
        # Test validation function
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
        
        errors = validate_input(sample_data)
        if not errors:
            print("✅ Input validation works")
        else:
            print(f"❌ Validation errors: {errors}")
            return False
        
        # Test prediction function
        result = make_prediction(sample_data)
        if result['success']:
            print(f"✅ Flask prediction: {result['prediction']}")
        else:
            print(f"❌ Flask prediction failed: {result['error']}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Flask app test error: {e}")
        return False

def test_templates():
    """Test if all template files exist."""
    print("\n🔍 Testing templates...")
    
    required_templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/form.html',
        'templates/result.html',
        'templates/error.html',
        'templates/agent_home.html',
        'templates/agent_interface.html'
    ]
    
    all_exist = True
    for template in required_templates:
        if Path(template).exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - MISSING")
            all_exist = False
    
    return all_exist

def test_static_files():
    """Test if static files exist."""
    print("\n🔍 Testing static files...")
    
    static_files = [
        'static/style.css'
    ]
    
    all_exist = True
    for static_file in static_files:
        if Path(static_file).exists():
            print(f"✅ {static_file}")
        else:
            print(f"❌ {static_file} - MISSING")
            all_exist = False
    
    return all_exist

def test_deployment_configs():
    """Test if deployment configuration files exist."""
    print("\n🔍 Testing deployment configs...")
    
    config_files = [
        'Dockerfile',
        'docker-compose.yml',
        'requirements.txt',
        'Procfile',
        'render.yaml',
        '.gitignore'
    ]
    
    all_exist = True
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file}")
        else:
            print(f"❌ {config_file} - MISSING")
            all_exist = False
    
    return all_exist

def test_documentation():
    """Test if documentation files exist."""
    print("\n🔍 Testing documentation...")
    
    doc_files = [
        'README.md',
        'CHANGELOG.md',
        'docs/API.md',
        'docs/DEPLOYMENT.md'
    ]
    
    all_exist = True
    for doc_file in doc_files:
        if Path(doc_file).exists():
            print(f"✅ {doc_file}")
        else:
            print(f"❌ {doc_file} - MISSING")
            all_exist = False
    
    return all_exist

def run_all_tests():
    """Run all tests and provide summary."""
    print("🧪 FETAL HEALTH PREDICTION SYSTEM - COMPREHENSIVE TEST")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Model Loading", test_model_loading),
        ("AI Agent", test_agent),
        ("Flask App", test_flask_app),
        ("Templates", test_templates),
        ("Static Files", test_static_files),
        ("Deployment Configs", test_deployment_configs),
        ("Documentation", test_documentation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your Fetal Health Prediction System is ready to use!")
        print("\nQuick start commands:")
        print("  python run.py --setup     # First-time setup")
        print("  python run.py --both      # Run both applications")
        print("  python run.py --test      # Run unit tests")
        print("\nAccess URLs:")
        print("  Main App: http://localhost:5000")
        print("  Agent App: http://localhost:5001")
    else:
        print(f"\n⚠️ {total - passed} tests failed!")
        print("Please check the errors above and fix any issues.")
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
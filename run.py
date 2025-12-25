#!/usr/bin/env python3
"""
Fetal Health Prediction System - Application Runner
Convenient script to run the application in different modes.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_main_app(port=5000, debug=False):
    """Run the main Flask application."""
    print(f"🚀 Starting main application on port {port}")
    os.environ['PORT'] = str(port)
    os.environ['DEBUG'] = str(debug).lower()
    
    if debug:
        # Development mode
        subprocess.run([sys.executable, 'app.py'])
    else:
        # Production mode with Gunicorn
        subprocess.run([
            'gunicorn', 
            '--bind', f'0.0.0.0:{port}',
            '--workers', '2',
            '--timeout', '120',
            'app:app'
        ])

def run_agent_app(port=5001, debug=False):
    """Run the AI agent application."""
    print(f"🤖 Starting AI agent on port {port}")
    os.environ['PORT'] = str(port)
    os.environ['DEBUG'] = str(debug).lower()
    
    if debug:
        # Development mode
        subprocess.run([sys.executable, 'agent_app.py'])
    else:
        # Production mode with Gunicorn
        subprocess.run([
            'gunicorn', 
            '--bind', f'0.0.0.0:{port}',
            '--workers', '2',
            '--timeout', '120',
            'agent_app:app'
        ])

def run_both_apps(debug=False):
    """Run both applications simultaneously."""
    print("🚀 Starting both applications...")
    
    import threading
    import time
    
    # Start main app in thread
    main_thread = threading.Thread(
        target=run_main_app, 
        args=(5000, debug)
    )
    main_thread.daemon = True
    main_thread.start()
    
    # Wait a moment then start agent
    time.sleep(2)
    
    agent_thread = threading.Thread(
        target=run_agent_app, 
        args=(5001, debug)
    )
    agent_thread.daemon = True
    agent_thread.start()
    
    print("✅ Both applications started!")
    print("📊 Main App: http://localhost:5000")
    print("🤖 Agent App: http://localhost:5001")
    print("Press Ctrl+C to stop both applications")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down applications...")

def run_tests():
    """Run the test suite."""
    print("🧪 Running test suite...")
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("❌ pytest not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest'])
    
    # Run tests
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 
        'tests/', 
        '-v',
        '--tb=short'
    ])
    
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return result.returncode

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'numpy', 'pandas', 'scikit-learn', 
        'joblib', 'gunicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install'
        ] + missing_packages)
    else:
        print("\n✅ All dependencies are installed!")

def check_model():
    """Check if the ML model file exists and is loadable."""
    print("🔍 Checking ML model...")
    
    model_path = Path('models/fetal_health.pkl')
    
    if not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        print("Please ensure the model file is in the correct location.")
        return False
    
    try:
        import joblib
        model = joblib.load(model_path)
        print(f"✅ Model loaded successfully")
        print(f"   Type: {type(model).__name__}")
        print(f"   Features: {getattr(model, 'n_features_in_', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def setup_project():
    """Set up the project for first-time use."""
    print("🛠️ Setting up Fetal Health Prediction System...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Install dependencies
    check_dependencies()
    
    # Check model
    model_ok = check_model()
    
    # Create necessary directories
    directories = ['logs', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    if model_ok:
        print("\n🎉 Setup complete! You can now run the application.")
        print("\nQuick start commands:")
        print("  python run.py --main          # Run main app only")
        print("  python run.py --agent         # Run agent only") 
        print("  python run.py --both          # Run both apps")
        print("  python run.py --test          # Run tests")
    else:
        print("\n⚠️ Setup incomplete - model file issues detected")
    
    return model_ok

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fetal Health Prediction System Runner'
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--main', action='store_true', 
                           help='Run main application only')
    mode_group.add_argument('--agent', action='store_true',
                           help='Run AI agent only')
    mode_group.add_argument('--both', action='store_true',
                           help='Run both applications')
    mode_group.add_argument('--test', action='store_true',
                           help='Run test suite')
    mode_group.add_argument('--setup', action='store_true',
                           help='Set up project for first use')
    mode_group.add_argument('--check', action='store_true',
                           help='Check dependencies and model')
    
    # Options
    parser.add_argument('--port', type=int, default=5000,
                       help='Port for main application (default: 5000)')
    parser.add_argument('--agent-port', type=int, default=5001,
                       help='Port for agent application (default: 5001)')
    parser.add_argument('--debug', action='store_true',
                       help='Run in debug mode')
    parser.add_argument('--production', action='store_true',
                       help='Run in production mode with Gunicorn')
    
    args = parser.parse_args()
    
    # Set debug mode (opposite of production)
    debug_mode = args.debug and not args.production
    
    try:
        if args.setup:
            setup_project()
        elif args.check:
            check_dependencies()
            check_model()
        elif args.test:
            sys.exit(run_tests())
        elif args.main:
            run_main_app(args.port, debug_mode)
        elif args.agent:
            run_agent_app(args.agent_port, debug_mode)
        elif args.both:
            run_both_apps(debug_mode)
            
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
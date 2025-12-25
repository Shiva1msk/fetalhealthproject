#!/usr/bin/env python3
"""
GitHub Setup Script for Fetal Health Prediction System
Automates the process of setting up and uploading the project to GitHub.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_git_installed():
    """Check if Git is installed."""
    success, _, _ = run_command("git --version", check=False)
    return success

def check_github_cli():
    """Check if GitHub CLI is installed."""
    success, _, _ = run_command("gh --version", check=False)
    return success

def initialize_git_repo():
    """Initialize Git repository."""
    print("🔧 Initializing Git repository...")
    
    # Initialize git repo
    success, stdout, stderr = run_command("git init")
    if not success:
        print(f"❌ Failed to initialize Git repo: {stderr}")
        return False
    
    # Add all files
    success, _, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return False
    
    # Initial commit
    success, _, stderr = run_command('git commit -m "Initial commit: Fetal Health Prediction System v1.0.0"')
    if not success:
        print(f"❌ Failed to create initial commit: {stderr}")
        return False
    
    print("✅ Git repository initialized successfully")
    return True

def create_github_repo(repo_name, description, private=False):
    """Create GitHub repository using GitHub CLI."""
    print(f"🚀 Creating GitHub repository: {repo_name}")
    
    visibility = "--private" if private else "--public"
    command = f'gh repo create {repo_name} {visibility} --description "{description}" --source=.'
    
    success, stdout, stderr = run_command(command, check=False)
    if not success:
        print(f"❌ Failed to create GitHub repo: {stderr}")
        return False
    
    print("✅ GitHub repository created successfully")
    return True

def push_to_github():
    """Push code to GitHub."""
    print("📤 Pushing code to GitHub...")
    
    # Push to main branch
    success, _, stderr = run_command("git push -u origin main", check=False)
    if not success:
        # Try master branch if main fails
        success, _, stderr = run_command("git push -u origin master", check=False)
        if not success:
            print(f"❌ Failed to push to GitHub: {stderr}")
            return False
    
    print("✅ Code pushed to GitHub successfully")
    return True

def setup_git_config():
    """Setup Git configuration if not already configured."""
    print("🔧 Checking Git configuration...")
    
    # Check if user name is configured
    success, stdout, _ = run_command("git config --global user.name", check=False)
    if not success or not stdout.strip():
        name = input("Enter your Git username: ")
        run_command(f'git config --global user.name "{name}"')
    
    # Check if user email is configured
    success, stdout, _ = run_command("git config --global user.email", check=False)
    if not success or not stdout.strip():
        email = input("Enter your Git email: ")
        run_command(f'git config --global user.email "{email}"')
    
    print("✅ Git configuration complete")

def create_github_workflows():
    """Create GitHub Actions workflows."""
    print("🔧 Creating GitHub Actions workflows...")
    
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    # CI/CD workflow
    ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=.
    
    - name: Test application startup
      run: |
        python quick_test.py

  docker:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t fetal-health-app .
    
    - name: Test Docker container
      run: |
        docker run -d -p 5000:5000 --name test-container fetal-health-app
        sleep 10
        curl -f http://localhost:5000/health || exit 1
        docker stop test-container

  deploy:
    runs-on: ubuntu-latest
    needs: [test, docker]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Add your deployment steps here"
        # Example: Deploy to cloud platform
"""
    
    with open(workflows_dir / "ci-cd.yml", "w") as f:
        f.write(ci_workflow)
    
    print("✅ GitHub Actions workflows created")

def create_issue_templates():
    """Create GitHub issue templates."""
    print("🔧 Creating GitHub issue templates...")
    
    templates_dir = Path(".github/ISSUE_TEMPLATE")
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Bug report template
    bug_template = """---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment (please complete the following information):**
 - OS: [e.g. Windows 10, Ubuntu 20.04]
 - Python Version: [e.g. 3.10.0]
 - Browser: [e.g. chrome, safari]
 - Version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.

**Medical Context (if applicable)**
- Are you using this for clinical purposes?
- What type of medical data are you working with?
- Any specific medical requirements or constraints?
"""
    
    with open(templates_dir / "bug_report.md", "w") as f:
        f.write(bug_template)
    
    # Feature request template
    feature_template = """---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Medical/Clinical Context**
- Is this feature for clinical use?
- What medical standards or regulations should be considered?
- How would this improve patient care or medical decision-making?

**Additional context**
Add any other context or screenshots about the feature request here.
"""
    
    with open(templates_dir / "feature_request.md", "w") as f:
        f.write(feature_template)
    
    print("✅ GitHub issue templates created")

def create_pull_request_template():
    """Create pull request template."""
    print("🔧 Creating pull request template...")
    
    github_dir = Path(".github")
    github_dir.mkdir(exist_ok=True)
    
    pr_template = """## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed
- [ ] Medical accuracy verified (if applicable)

## Medical/Clinical Considerations
- [ ] No impact on medical predictions
- [ ] Medical accuracy maintained
- [ ] Clinical validation performed (if applicable)
- [ ] Regulatory compliance considered

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information that reviewers should know.
"""
    
    with open(github_dir / "pull_request_template.md", "w") as f:
        f.write(pr_template)
    
    print("✅ Pull request template created")

def main():
    """Main function to set up GitHub repository."""
    print("🚀 FETAL HEALTH PREDICTION SYSTEM - GITHUB SETUP")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Please run this script from the fetal-health-system directory")
        sys.exit(1)
    
    # Check prerequisites
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first.")
        print("   Download from: https://git-scm.com/downloads")
        sys.exit(1)
    
    print("✅ Git is installed")
    
    # Setup Git configuration
    setup_git_config()
    
    # Create GitHub-specific files
    create_github_workflows()
    create_issue_templates()
    create_pull_request_template()
    
    # Initialize Git repository
    if not initialize_git_repo():
        sys.exit(1)
    
    # Check if GitHub CLI is available
    if check_github_cli():
        print("✅ GitHub CLI is available")
        
        # Get repository details
        repo_name = input("Enter repository name (default: fetal-health-prediction): ").strip()
        if not repo_name:
            repo_name = "fetal-health-prediction"
        
        description = "AI-powered fetal health prediction system with 95.92% accuracy using machine learning"
        
        private = input("Make repository private? (y/N): ").strip().lower() == 'y'
        
        # Create GitHub repository
        if create_github_repo(repo_name, description, private):
            # Push to GitHub
            if push_to_github():
                print("\n🎉 SUCCESS! Your project is now on GitHub!")
                print(f"📍 Repository URL: https://github.com/{os.environ.get('USER', 'your-username')}/{repo_name}")
                print("\n📋 Next steps:")
                print("1. Visit your repository on GitHub")
                print("2. Add a detailed description")
                print("3. Add topics/tags for discoverability")
                print("4. Set up branch protection rules")
                print("5. Configure deployment settings")
            else:
                print("❌ Failed to push to GitHub")
        else:
            print("❌ Failed to create GitHub repository")
    else:
        print("⚠️ GitHub CLI not found. Manual setup required:")
        print("\n📋 Manual GitHub Setup Steps:")
        print("1. Go to https://github.com/new")
        print("2. Create a new repository named 'fetal-health-prediction'")
        print("3. Don't initialize with README (we already have files)")
        print("4. Copy the repository URL")
        print("5. Run these commands:")
        print(f"   git remote add origin <your-repo-url>")
        print(f"   git branch -M main")
        print(f"   git push -u origin main")
        
        print("\n💡 To install GitHub CLI:")
        print("   Windows: winget install --id GitHub.cli")
        print("   macOS: brew install gh")
        print("   Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md")

if __name__ == "__main__":
    main()
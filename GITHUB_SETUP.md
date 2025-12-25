# GitHub Setup Guide

## Quick Setup (Automated)

Run the automated setup script:

```bash
cd fetal-health-system
python setup_github.py
```

This script will:
- ✅ Check Git installation
- ✅ Configure Git settings
- ✅ Create GitHub workflows
- ✅ Initialize Git repository
- ✅ Create GitHub repository (if GitHub CLI is installed)
- ✅ Push code to GitHub

## Manual Setup (Step by Step)

### Prerequisites

1. **Install Git**
   - Windows: Download from [git-scm.com](https://git-scm.com/downloads)
   - macOS: `brew install git` or download from website
   - Linux: `sudo apt install git` (Ubuntu/Debian) or equivalent

2. **Create GitHub Account**
   - Go to [github.com](https://github.com) and sign up
   - Verify your email address

3. **Install GitHub CLI (Optional but Recommended)**
   - Windows: `winget install --id GitHub.cli`
   - macOS: `brew install gh`
   - Linux: Follow [installation guide](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

### Step 1: Configure Git

```bash
# Set your name and email (use your GitHub email)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

### Step 2: Initialize Git Repository

```bash
# Navigate to project directory
cd fetal-health-system

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Fetal Health Prediction System v1.0.0"
```

### Step 3: Create GitHub Repository

#### Option A: Using GitHub CLI (Recommended)

```bash
# Login to GitHub
gh auth login

# Create repository (public)
gh repo create fetal-health-prediction --public --description "AI-powered fetal health prediction system with 95.92% accuracy" --source=.

# Push code
git push -u origin main
```

#### Option B: Using GitHub Website

1. **Go to GitHub**
   - Visit [github.com/new](https://github.com/new)

2. **Create Repository**
   - Repository name: `fetal-health-prediction`
   - Description: `AI-powered fetal health prediction system with 95.92% accuracy using machine learning`
   - Choose Public or Private
   - **Don't** initialize with README, .gitignore, or license (we already have these)
   - Click "Create repository"

3. **Connect Local Repository**
   ```bash
   # Add remote origin (replace YOUR_USERNAME)
   git remote add origin https://github.com/YOUR_USERNAME/fetal-health-prediction.git
   
   # Set main branch
   git branch -M main
   
   # Push code
   git push -u origin main
   ```

### Step 4: Configure Repository Settings

1. **Go to Repository Settings**
   - Navigate to your repository on GitHub
   - Click "Settings" tab

2. **Add Topics/Tags**
   - Click "⚙️" next to "About"
   - Add topics: `machine-learning`, `healthcare`, `flask`, `python`, `ai`, `medical`, `prediction`, `fetal-health`

3. **Set Up Branch Protection**
   - Go to Settings → Branches
   - Add rule for `main` branch
   - Enable "Require pull request reviews before merging"
   - Enable "Require status checks to pass before merging"

4. **Configure Pages (Optional)**
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: main / docs (if you want to host documentation)

### Step 5: Set Up GitHub Actions

The automated script creates workflows, but you can also create them manually:

1. **Create `.github/workflows/ci-cd.yml`**
   - Automated testing on push/PR
   - Docker build testing
   - Deployment pipeline

2. **Enable Actions**
   - Go to Actions tab in your repository
   - Enable GitHub Actions if prompted

### Step 6: Add Collaborators (Optional)

1. **Go to Settings → Manage access**
2. **Click "Invite a collaborator"**
3. **Add team members or reviewers**

## Repository Structure

Your GitHub repository will have this structure:

```
fetal-health-prediction/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── docs/
│   ├── API.md
│   └── DEPLOYMENT.md
├── models/
│   └── fetal_health.pkl
├── static/
│   └── style.css
├── templates/
│   ├── *.html files
├── tests/
│   ├── test_app.py
│   └── test_agent.py
├── app.py
├── agent.py
├── agent_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── .gitignore
```

## Post-Setup Tasks

### 1. Update README Badges

Add these badges to your README.md:

```markdown
![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build](https://github.com/YOUR_USERNAME/fetal-health-prediction/workflows/CI%2FCD%20Pipeline/badge.svg)
```

### 2. Create Releases

```bash
# Tag your first release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 3. Set Up Deployment

Configure deployment to your preferred platform:
- **Render**: Connect GitHub repository
- **Railway**: Import from GitHub
- **Heroku**: Connect GitHub for auto-deploy
- **Vercel**: Import GitHub repository

### 4. Monitor Repository

- **Watch** for issues and pull requests
- **Enable notifications** for repository activity
- **Set up security alerts** for dependencies

## Security Considerations

### 1. Secrets Management

Never commit sensitive data:
- API keys
- Database passwords
- Secret keys
- Personal medical data

Use GitHub Secrets for sensitive environment variables:
- Go to Settings → Secrets and variables → Actions
- Add repository secrets

### 2. Dependency Security

- Enable **Dependabot alerts**
- Review **security advisories**
- Keep **dependencies updated**

### 3. Code Scanning

- Enable **CodeQL analysis**
- Set up **security scanning**
- Review **vulnerability reports**

## Collaboration Workflow

### 1. Development Process

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature

# Create pull request on GitHub
```

### 2. Code Review Process

1. **Create pull request**
2. **Request reviews** from team members
3. **Address feedback**
4. **Merge after approval**

### 3. Release Process

1. **Update version numbers**
2. **Update CHANGELOG.md**
3. **Create release branch**
4. **Test thoroughly**
5. **Merge to main**
6. **Tag release**
7. **Deploy to production**

## Troubleshooting

### Common Issues

**Authentication Error:**
```bash
# Use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/fetal-health-prediction.git
```

**Large File Error:**
```bash
# Use Git LFS for large model files
git lfs track "*.pkl"
git add .gitattributes
```

**Permission Denied:**
```bash
# Check SSH key setup
ssh -T git@github.com

# Or use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/fetal-health-prediction.git
```

## Next Steps

After successful GitHub setup:

1. **Share your repository** with the community
2. **Add comprehensive documentation**
3. **Set up continuous deployment**
4. **Monitor usage and feedback**
5. **Plan future enhancements**

Your Fetal Health Prediction System is now ready for collaborative development and deployment! 🎉
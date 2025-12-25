@echo off
echo ========================================
echo Uploading Fetal Health System to GitHub
echo Repository: https://github.com/Shiva1msk/fetalhealthproject.git
echo ========================================

REM Initialize Git repository
echo Initializing Git repository...
git init

REM Add all files
echo Adding all files...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: Complete Fetal Health Prediction System v1.0.0

- AI-powered fetal health prediction with 95.92% accuracy
- Web interface with form-based input
- AI agent with natural language processing
- RESTful API endpoints
- Docker containerization support
- Comprehensive test suite
- Multi-platform deployment configurations
- Complete documentation and guides"

REM Add remote repository
echo Adding remote repository...
git remote add origin https://github.com/Shiva1msk/fetalhealthproject.git

REM Set main branch
echo Setting main branch...
git branch -M main

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Project uploaded to GitHub!
    echo ========================================
    echo.
    echo Repository URL: https://github.com/Shiva1msk/fetalhealthproject
    echo.
    echo Next steps:
    echo 1. Visit your repository on GitHub
    echo 2. Add repository description and topics
    echo 3. Enable GitHub Actions for CI/CD
    echo 4. Set up deployment to your preferred platform
    echo.
) else (
    echo.
    echo ========================================
    echo Upload failed!
    echo ========================================
    echo.
    echo Possible solutions:
    echo 1. Make sure you have Git installed
    echo 2. Check your GitHub credentials
    echo 3. Ensure repository exists and you have access
    echo 4. Try running: git push -f origin main
    echo.
)

pause
#!/bin/bash

# FraudAGENT - GitHub Repository Initialization Script

echo "=================================="
echo "FraudAGENT - GitHub Setup"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'GITIGNORE'
__pycache__/
*.pyc
.env
venv/
uploaded_data/
*.log
data_schema_summary.json
GITIGNORE
    echo "✓ .gitignore created"
fi

# Copy GitHub README
if [ -f "README_GITHUB.md" ]; then
    cp README_GITHUB.md README.md
    echo "✓ README.md updated for GitHub"
fi

# Add all files
echo ""
echo "Adding files to git..."
git add .
echo "✓ Files added"

# Create initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: FraudAGENT - Insurance Claims AI Agent with Excel Upload"
echo "✓ Initial commit created"

echo ""
echo "=================================="
echo "Next Steps:"
echo "=================================="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Run these commands to push your code:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/fraudagent.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to your preferred platform:"
echo "   - Hugging Face Spaces: See README_HF.md"
echo "   - Railway: See DEPLOY_RAILWAY.md"
echo "   - Render: See DEPLOY_RENDER.md"
echo ""
echo "=================================="

# KumoRFM Insurance Claims AI Agent - PowerShell Launcher
# Automates environment setup and application launch

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  KumoRFM Insurance Claims AI Agent - FraudAGENT Launcher" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = $null

# Try different Python commands
$pythonCommands = @("python", "python3", "py")
foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python 3\.(9|1[0-3])") {
            $pythonCmd = $cmd
            Write-Host "      Found: $version" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host "      ERROR: Python 3.9+ not found!" -ForegroundColor Red
    Write-Host "      Please install Python 3.9 or higher from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check/Create virtual environment
Write-Host "[2/6] Setting up virtual environment..." -ForegroundColor Yellow
$venvPath = "venv"

if (-not (Test-Path $venvPath)) {
    Write-Host "      Creating new virtual environment..." -ForegroundColor Cyan
    & $pythonCmd -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      ERROR: Failed to create virtual environment!" -ForegroundColor Red
        exit 1
    }
    Write-Host "      Virtual environment created successfully" -ForegroundColor Green
} else {
    Write-Host "      Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "      Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "      ERROR: Activation script not found!" -ForegroundColor Red
    exit 1
}

# Install/Update dependencies
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Yellow
Write-Host "      This may take a few minutes on first run..." -ForegroundColor Cyan

& python -m pip install --upgrade pip --quiet
& pip install -r requirements.txt --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Failed to install dependencies!" -ForegroundColor Red
    Write-Host "      Try running manually: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host "      Dependencies installed successfully" -ForegroundColor Green

# Check/Create .env file
Write-Host "[5/6] Checking environment configuration..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Write-Host "      .env file not found, creating from template..." -ForegroundColor Cyan
    Copy-Item ".env.template" ".env"
    Write-Host "" -ForegroundColor Yellow
    Write-Host "      ============================================================" -ForegroundColor Red
    Write-Host "      ACTION REQUIRED: Please edit .env file with your API keys!" -ForegroundColor Red
    Write-Host "      ============================================================" -ForegroundColor Red
    Write-Host "" -ForegroundColor Yellow
    Write-Host "      1. Open .env file in a text editor" -ForegroundColor Yellow
    Write-Host "      2. Replace 'your-kumo-api-key-here' with your actual Kumo API key" -ForegroundColor Yellow
    Write-Host "      3. Replace 'your-openai-api-key-here' with your actual OpenAI API key" -ForegroundColor Yellow
    Write-Host "      4. Save the file and run this script again" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Yellow
    Write-Host "      Get API keys from:" -ForegroundColor Cyan
    Write-Host "        Kumo:   https://kumorfm.ai/api-keys" -ForegroundColor Cyan
    Write-Host "        OpenAI: https://platform.openai.com/api-keys" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor Yellow
    
    # Open .env file in default editor
    Start-Process notepad.exe ".env"
    
    Read-Host "Press Enter after you've updated the .env file to continue"
} else {
    Write-Host "      .env file found" -ForegroundColor Green
}

# Verify API keys are set
$envContent = Get-Content ".env" -Raw
if ($envContent -match "your-kumo-api-key-here" -or $envContent -match "your-openai-api-key-here") {
    Write-Host "" -ForegroundColor Red
    Write-Host "      WARNING: API keys not configured in .env file!" -ForegroundColor Red
    Write-Host "      The application will fail to start without valid API keys." -ForegroundColor Red
    Write-Host "" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "      Exiting. Please configure .env and run again." -ForegroundColor Yellow
        exit 0
    }
}

# Check data file
Write-Host "[6/6] Checking data file..." -ForegroundColor Yellow
$dataPath = "data/insurance_claims_data.parquet"

if (-not (Test-Path $dataPath)) {
    Write-Host "      WARNING: Data file not found at $dataPath" -ForegroundColor Yellow
    Write-Host "      Please ensure your insurance claims data is in the data/ directory" -ForegroundColor Yellow
    Write-Host "      The application may fail to start without data." -ForegroundColor Yellow
} else {
    $dataSize = (Get-Item $dataPath).Length / 1MB
    Write-Host "      Data file found: $dataPath ($([math]::Round($dataSize, 2)) MB)" -ForegroundColor Green
}

# Launch application
Write-Host "" -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  Launching KumoRFM Insurance Claims AI Agent..." -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White

& python main.py

# Handle exit
if ($LASTEXITCODE -ne 0) {
    Write-Host "" -ForegroundColor Red
    Write-Host "Application exited with error code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "" -ForegroundColor Yellow
    Write-Host "Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "  1. Check that API keys are correctly set in .env" -ForegroundColor White
    Write-Host "  2. Verify data file exists in data/ directory" -ForegroundColor White
    Write-Host "  3. Check console output above for specific error messages" -ForegroundColor White
    Write-Host "  4. Try running: python main.py directly for detailed errors" -ForegroundColor White
    Write-Host "" -ForegroundColor White
}

Write-Host "" -ForegroundColor White
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

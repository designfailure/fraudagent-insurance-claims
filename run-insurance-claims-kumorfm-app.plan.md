# KumoRFM Insurance Claims AI Agent - Run Plan & Checklist

This document provides a concise runbook and checklist for setting up and running the **FraudAGENT** application. It includes commands for both PowerShell (Windows) and Bash (Linux/macOS).

---

## 🚀 RUN Checklist

Follow these steps to get the application running:

1.  **Prerequisites**:
    -   [ ] **Python 3.9+** installed and available in your PATH.
    -   [ ] **Git** installed (for cloning the repository).
    -   [ ] **KumoRFM API Key**: Get from [kumorfm.ai/api-keys](https://kumorfm.ai/api-keys).
    -   [ ] **OpenAI API Key**: Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

2.  **Clone Repository**:
    -   [ ] Clone the project repository to your local machine.

3.  **Data Setup**:
    -   [ ] Place your Parquet dataset (`insurance_claims_data.parquet`) into the `data/` directory.

4.  **Environment Configuration**:
    -   [ ] Copy `.env.template` to a new file named `.env`.
    -   [ ] Edit the `.env` file and add your `KUMO_API_KEY` and `OPENAI_API_KEY`.

5.  **Install Dependencies**:
    -   [ ] Run the setup script (`launch.ps1` or `launch.sh`) to create a virtual environment and install all required packages from `requirements.txt`.

6.  **Launch Application**:
    -   [ ] Run the main application using the launch script or by directly calling `python main.py`.

7.  **Access UI**:
    -   [ ] Open your web browser and navigate to the URL provided in the console (default: `http://0.0.0.0:7860`).

---

## ⚙️ Setup & Launch Commands

Choose the appropriate set of commands for your operating system.

### Option 1: Using the Launcher Script (Recommended)

The easiest way to get started is to use the provided launcher script, which automates all setup steps.

**Windows (PowerShell)**

```powershell
# Open PowerShell, navigate to the project directory, and run:
.\launch.ps1
```

**Linux / macOS (Bash)**

*First, create a `launch.sh` script (or run commands manually below):*

```bash
#!/bin/bash
# launch.sh - KumoRFM Insurance Claims AI Agent Launcher

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️ .env file not found. Please copy .env.template to .env and add your API keys."
    exit 1
fi

# Run application
python main.py
```

*Then, make it executable and run:*

```bash
chmod +x launch.sh
./launch.sh
```

### Option 2: Manual Setup

If you prefer to set up the environment manually, follow these steps.

**Windows (PowerShell)**

```powershell
# 1. Navigate to the project directory
cd path\to\insurance-claims-kumo-agent

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
Copy-Item .env.template .env
# --> Now, edit the .env file with your API keys

# 5. Run the application
python main.py
```

**Linux / macOS (Bash)**

```bash
# 1. Navigate to the project directory
cd path/to/insurance-claims-kumo-agent

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.template .env
# --> Now, edit the .env file with your API keys (e.g., using nano or vim)
nano .env

# 5. Run the application
python main.py
```

---

## 🧪 Use-Case Scenarios & Test Cases

Once the application is running, you can test it with the following scenarios in the Gradio UI.

### Scenario 1: Fraud Prediction for a Specific Claim

-   **User Query**: `Is claim 98765 fraudulent?`
-   **Expected PQL**: `PREDICT claims.fraud_flag FOR claims.claim_id=98765`
-   **Expected Result**: A DataFrame with a single row showing the prediction for `fraud_flag` (True/False) and the associated probability.

### Scenario 2: Temporal Claim Count Prediction

-   **User Query**: `How many claims will customer 123 file in the next 60 days?`
-   **Expected PQL**: `PREDICT COUNT(claims.*, 0, 60, days) FOR customers.customer_id=123`
-   **Expected Result**: A DataFrame showing the predicted count of claims for customer 123.

### Scenario 3: Bulk Fraud Prediction

-   **User Query**: `Predict fraud for all pending claims`
-   **Expected PQL**: `PREDICT claims.fraud_flag FOR EACH claims.claim_id WHERE claims.status='Pending'`
-   **Expected Result**: A multi-row DataFrame with fraud predictions for all claims where the status is 'Pending'.

### Scenario 4: High-Risk Customer Identification

-   **User Query**: `Which customers will have a total claim amount over $5000 in the next 90 days?`
-   **Expected PQL**: `PREDICT SUM(claims.claim_amount, 0, 90, days) > 5000 FOR EACH customers.customer_id`
-   **Expected Result**: A DataFrame listing customers predicted to exceed the specified claim amount threshold.

### Smoke Tests

1.  **Load Validation**: Check the console output on startup to ensure the data file is loaded and profiled without errors.
2.  **Translator Dry-Run**: Use the example queries in the Gradio UI to verify that PQL is generated correctly.
3.  **Prediction Smoke Test**: Execute a simple query like `PREDICT claims.fraud_flag FOR EACH claims.claim_id` and verify that a DataFrame with results is returned.
4.  **UI Smoke Test**: Navigate through all tabs in the Gradio interface (Chat Agent, Data Explorer, Direct PQL, etc.) to ensure they load and function correctly.

# KumoRFM Insurance Claims AI Agent (FraudAGENT)

**FraudAGENT** is a production-ready Python application that provides a conversational AI interface for insurance claims fraud detection and predictive analysis. It integrates the **KumoRFM (Relational Foundation Model)** for powerful predictions on structured data and uses **OpenAI** to translate natural language questions into KumoRFM's Predictive Query Language (PQL).

This allows analysts, investigators, and business users to interact with complex insurance data using plain English, democratizing access to powerful predictive insights.

![Gradio UI Screenshot](https://raw.githubusercontent.com/path/to/screenshot.png)  <!-- Placeholder for a UI screenshot -->

---

## ✨ Features

-   **Conversational AI**: Ask questions in natural language (e.g., "Is this claim fraudulent?" or "Which customers are high-risk?").
-   **NL-to-PQL Translation**: Uses OpenAI's `gpt-4o-mini` or `gpt-4o` to automatically convert user questions into executable PQL queries.
-   **KumoRFM Integration**: Leverages the KumoRFM SDK to perform complex predictions, including:
    -   Fraud detection
    -   Claim amount forecasting
    -   Claim frequency prediction
    -   Customer risk assessment
-   **Interactive Web UI**: A multi-tab Gradio interface for chat, data exploration, direct PQL execution, and performance monitoring.
-   **Reproducible & Extensible**: Built with a modular structure, environment variable management, and clear dependency definitions for easy setup and customization.
-   **Automated Setup**: Includes a PowerShell launcher (`launch.ps1`) to automate environment creation and dependency installation.

---

## 🚀 Quick Start

Follow these steps to get the application up and running in minutes.

### Prerequisites

-   **Python 3.9+**
-   **Git**
-   **KumoRFM API Key**: [Get one here](https://kumorfm.ai/api-keys)
-   **OpenAI API Key**: [Get one here](https://platform.openai.com/api-keys)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd insurance-claims-kumo-agent
```

### 2. Prepare Your Data

Place your insurance claims dataset in Parquet format into the `data/` directory. The application expects a file named `insurance_claims_data.parquet` by default. This can be a single file or a directory of Parquet files.

### 3. Configure Your Environment

Copy the environment template file and add your API keys:

```bash
# For Linux/macOS
cp .env.template .env

# For Windows
copy .env.template .env
```

Now, open the `.env` file in a text editor and replace the placeholder values with your actual **KumoRFM** and **OpenAI** API keys.

```ini
# .env
KUMO_API_KEY=your-kumo-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Launch the Application

The easiest way to start is with the provided PowerShell script.

**On Windows (PowerShell):**

```powershell
.\launch.ps1
```

This script will automatically:
1.  Create a Python virtual environment (`venv`).
2.  Install all required dependencies from `requirements.txt`.
3.  Check for the `.env` file and prompt you to create it if missing.
4.  Launch the main application.

**On Linux/macOS (Bash):**

Run these commands manually:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 5. Access the UI

Once the application is running, open your web browser and navigate to:

**[http://127.0.0.1:7860](http://127.0.0.1:7860)** (or the URL shown in your console).

---

## 💡 Example Queries

Here are some examples of questions you can ask the agent:

-   `Is claim 12345 fraudulent?`
-   `Predict fraud probability for all pending claims.`
-   `How many claims will customer 100 file in the next 30 days?`
-   `What is the expected total claim amount for customer 200 in the next quarter?`
-   `Which customers are likely to have a claim amount over $10,000 in the next 60 days?`
-   `Will claim 500 be approved?`
-   `Show me the top 5 most common claim types for customer 500.`

---

## 🔧 Troubleshooting

-   **`KUMO_API_KEY` or `OPENAI_API_KEY` not set**: Ensure your `.env` file is correctly named and contains your valid API keys. The application will fail to start without them.
-   **`FileNotFoundError` for data file**: Make sure your Parquet data file is located in the `data/` directory and that the `INSURANCE_DATA_PATH` in your `.env` file points to the correct location.
-   **SDK Import Errors**: If you see errors related to `kumoai` or `kumorfm`, it may indicate an issue with the installed SDK version. The `kumo_setup.py` module attempts to handle common import patterns, but you can ensure compatibility by installing the version specified in `requirements.txt`.
-   **PQL Execution Errors**: If a query fails to execute, check the console for detailed error messages from the KumoRFM SDK. Common issues include incorrect entity IDs, non-existent columns, or improperly configured graph relationships.

---

## 📂 Project Structure

```
insurance-claims-kumo-agent/
├── data/
│   └── insurance_claims_data.parquet   # Your dataset goes here
├── notebooks/                          # Reference notebooks
├── src/                                # Source code
│   ├── __init__.py
│   ├── data_loader.py                # Loads and profiles data
│   ├── kumo_setup.py                 # Handles KumoRFM client and graph setup
│   ├── text_to_pql.py                # NL -> PQL translation with OpenAI
│   └── kumo_agent.py                 # Gradio UI and conversational agent logic
├── main.py                             # Main application entry point
├── requirements.txt                    # Python dependencies
├── .env.template                       # Environment variable template
├── .env                                # Your environment configuration (not committed)
├── launch.ps1                          # PowerShell launcher for Windows
├── run-insurance-claims-kumorfm-app.plan.md # Runbook and checklist
└── README.md                           # This file
```

---

## ⚖️ License

This project is licensed under the MIT License. See the `LICENSE` file for details.

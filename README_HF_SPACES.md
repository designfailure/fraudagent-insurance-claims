---
title: FraudAGENT - Insurance Claims AI
emoji: 🛡️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🛡️ FraudAGENT - KumoRFM Insurance Claims AI Agent

**AI-powered fraud detection and predictive analytics for insurance claims using KumoRFM and OpenAI**

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

FraudAGENT is an intelligent insurance claims analysis platform that combines:

- **🤖 Natural Language Interface** - Ask questions in plain English
- **📊 KumoRFM Integration** - Predictive analytics and graph-based ML
- **🧠 OpenAI GPT** - Natural language to PQL (Predictive Query Language) translation
- **📤 Data Upload** - Bring your own insurance data (Excel → Parquet)
- **🔍 Fraud Detection** - Predict fraudulent claims with confidence scores
- **📈 Risk Assessment** - Identify high-risk customers and patterns

---

## ✨ Features

### 💬 Conversational AI Agent
Ask natural language questions like:
- "Is claim CLM12345 fraudulent?"
- "How many claims will customer CUST1000 file in the next 30 days?"
- "Which customers are high risk?"
- "Predict fraud probability for all open claims"

### 📤 Data Upload & Processing
- Upload Excel files with multiple sheets
- Automatic schema detection (primary keys, foreign keys, temporal columns)
- Relationship inference between tables
- Convert to optimized Parquet format

### ⚡ Direct PQL Query
- Execute PQL queries manually for advanced users
- Syntax highlighting and validation
- Real-time results

### 📊 Data Explorer
- View graph schema
- Inspect table relationships
- Sample data preview

---

## 🚀 Quick Start

### 1. Set Up Secrets

In your Hugging Face Space settings, add these secrets:

```
KUMO_API_KEY=your-kumo-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Deploy

Click "Deploy" and the application will automatically start!

### 3. Use the Application

1. **Upload Data** (optional) - Upload your own insurance claims Excel file
2. **Chat Agent** - Ask questions in natural language
3. **View Results** - See generated PQL queries and predictions

---

## 📊 Sample Data

The application comes with sample insurance data:
- **12 tables** with 151,563 rows
- **Claims, Customers, Policies, Vehicles, Agents**
- **Fraud flags, Risk scores, Temporal data**

You can also upload your own data in the "Data Upload" tab.

---

## 🛠️ Technology Stack

- **Frontend**: Gradio 4.0+ (multi-tab interface)
- **Backend**: Python 3.11
- **AI**: OpenAI GPT-4 (natural language understanding)
- **ML**: KumoRFM SDK (predictive analytics)
- **Data**: Pandas, Parquet (efficient data processing)

---

## 📖 How It Works

1. **User asks a question** in natural language
2. **OpenAI GPT** translates it to PQL (Predictive Query Language)
3. **KumoRFM** executes the query on the graph-based ML model
4. **Results** are returned with confidence scores and explanations

---

## 🔒 Privacy & Security

- All data processing happens in your Hugging Face Space
- API keys are stored securely as Hugging Face Secrets
- No data is sent to third parties except OpenAI and KumoRFM APIs

---

## 📝 Example Queries

### Fraud Detection
```
"Is claim CLM40000 fraudulent?"
"Predict fraud for all claims filed in the last 30 days"
"Show me the top 10 most suspicious claims"
```

### Customer Risk
```
"Which customers are high risk in the next 60 days?"
"What is the risk score for customer CUST5000?"
"Find customers with risk score above 0.8"
```

### Claim Forecasting
```
"How many claims will customer CUST1234 file next month?"
"What is the expected claim amount for policy POL50000?"
"Predict total claims for next quarter"
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **KumoRFM** - Graph-based machine learning platform
- **OpenAI** - Natural language processing
- **Gradio** - Interactive web interface
- **Hugging Face** - Hosting and deployment

---

## 📧 Support

For issues or questions, please open an issue on GitHub or contact the maintainers.

---

**Built with ❤️ for the insurance industry**

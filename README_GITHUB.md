# 🏥 FraudAGENT - Insurance Claims AI Agent

> **AI-powered fraud detection and predictive analytics for insurance claims using KumoRFM and OpenAI**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/gradio-4.0+-orange.svg)](https://gradio.app/)

## 🎯 Features

- **📤 Excel Data Upload** - Bring your own insurance data (.xlsx) with automatic conversion to Parquet
- **🤖 Natural Language Queries** - Ask questions in plain English, powered by OpenAI GPT-4
- **⚡ Automatic PQL Generation** - Converts natural language to Predictive Query Language (PQL)
- **🔍 Fraud Detection** - Predict fraud probability for claims using KumoRFM
- **📊 Predictive Analytics** - Forecast claim volumes, amounts, and customer behavior
- **🎨 Interactive UI** - Multi-tab Gradio interface with chat, data explorer, and settings
- **🔗 Relationship Inference** - Automatically detects table relationships from your data

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fraudagent.git
cd fraudagent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env and add your API keys

# Run the application
python3 app.py
```

Open http://localhost:7860 in your browser.

### One-Click Deploy

Deploy to your preferred platform:

[![Deploy to Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-lg.svg)](https://huggingface.co/new-space?template=YOUR_USERNAME/fraudagent)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/fraudagent)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/fraudagent)

## 📊 How It Works

1. **Upload Your Data** - Upload an Excel file with your insurance claims data
2. **Automatic Conversion** - System converts all sheets to Parquet and infers relationships
3. **Ask Questions** - Use natural language to query your data
4. **Get Predictions** - Receive fraud predictions, forecasts, and insights

### Example Queries

```
"Is claim CLM12345 fraudulent?"
"How many claims will customer CUST001 file in the next 30 days?"
"What is the total claim amount for high-risk customers?"
"Predict fraud probability for all pending claims"
```

## 🏗️ Architecture

```
FraudAGENT
├── Excel Upload → Parquet Conversion
├── Schema Detection → Relationship Inference
├── KumoRFM Graph → Knowledge Graph Creation
├── Natural Language → PQL Translation (OpenAI)
├── PQL Execution → Predictions & Insights
└── Gradio UI → Interactive Interface
```

## 📁 Project Structure

```
fraudagent/
├── app.py                    # Main application entry point
├── main_with_upload.py       # Application logic with upload feature
├── requirements.txt          # Python dependencies
├── .env.template            # Environment variables template
├── src/
│   ├── data_loader.py       # Data loading and profiling
│   ├── excel_converter.py   # Excel to Parquet conversion
│   ├── kumo_setup.py        # KumoRFM SDK initialization
│   ├── text_to_pql.py       # Natural language to PQL translation
│   ├── kumo_agent.py        # Conversational agent logic
│   └── upload_ui.py         # Gradio upload interface
├── data/                     # Sample data
└── docs/                     # Documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```ini
# Required
KUMO_API_KEY=your-kumo-api-key
OPENAI_API_KEY=your-openai-api-key

# Optional
INSURANCE_DATA_PATH=data/
OPENAI_MODEL=gpt-4o-mini
APP_HOST=0.0.0.0
APP_PORT=7860
```

### Excel File Requirements

Your Excel file should:
- Use `.xlsx` format
- Have clear column headers in the first row
- Use consistent naming for ID columns (e.g., `customer_ID`, `claim_ID`)
- Format dates as datetime in Excel
- Avoid merged cells and subtotals

## 📚 Documentation

- [Upload Feature Guide](UPLOAD_FEATURE_GUIDE.md) - Detailed guide for Excel upload
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Deploy to Hugging Face](README_HF.md) - Hugging Face Spaces deployment
- [Deploy to Railway](DEPLOY_RAILWAY.md) - Railway.app deployment
- [Deploy to Render](DEPLOY_RENDER.md) - Render.com deployment
- [AWS Deployment](DEPLOY_AWS.md) - AWS deployment options
- [Azure Deployment](DEPLOY_AZURE.md) - Azure deployment options
- [GCP Deployment](DEPLOY_GCP.md) - Google Cloud deployment options

## 🎨 Screenshots

### Chat Agent
Ask questions in natural language and get AI-powered predictions.

### Data Upload
Upload Excel files and automatically convert to Parquet with schema detection.

### Data Explorer
View your data schema and relationships in an interactive interface.

## 🧪 Testing

```bash
# Run module tests
python3 test_modules.py

# Test with sample data
python3 -c "from src.data_loader import InsuranceDataLoader; loader = InsuranceDataLoader('data'); loader.load_data()"
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **KumoRFM** - Predictive analytics platform
- **OpenAI** - Natural language processing
- **Gradio** - Interactive UI framework
- **Pandas** - Data manipulation
- **PyArrow** - Parquet file format

## 📞 Support

- **Issues**: https://github.com/YOUR_USERNAME/fraudagent/issues
- **Discussions**: https://github.com/YOUR_USERNAME/fraudagent/discussions
- **Email**: your-email@example.com

## 🗺️ Roadmap

- [ ] Support for additional file formats (CSV, JSON)
- [ ] Advanced fraud detection models
- [ ] Multi-user authentication
- [ ] Dashboard with analytics
- [ ] API endpoints for programmatic access
- [ ] Integration with insurance platforms

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Built with ❤️ for the insurance industry**

# FraudAGENT - KumoRFM Insurance Claims AI Agent

## Project Summary

**FraudAGENT** is a production-ready, agentic AI application that revolutionizes insurance claims fraud detection and predictive analytics by combining the power of **KumoRFM (Relational Foundation Model)** with **OpenAI's GPT models** through an intuitive **Gradio-based conversational interface**.

This application enables insurance analysts, investigators, and business users to interact with complex relational data using natural language, democratizing access to advanced predictive insights without requiring technical expertise in machine learning or query languages.

---

## 🎯 Key Features

### 1. Natural Language Query Interface
-   **Plain English Queries**: Ask questions like "Is claim 12345 fraudulent?" or "Which customers will file claims over $10,000 in the next 60 days?"
-   **Intelligent Translation**: Automatically converts natural language to KumoRFM's Predictive Query Language (PQL) using OpenAI GPT-4o-mini or GPT-4o
-   **Context-Aware Clarification**: Detects ambiguous queries and asks follow-up questions

### 2. Powerful Predictive Analytics
-   **Fraud Detection**: Predict fraud probability for individual claims or bulk analysis
-   **Claim Forecasting**: Estimate future claim amounts, frequencies, and patterns
-   **Risk Assessment**: Identify high-risk customers and policies
-   **Approval Prediction**: Forecast claim approval likelihood
-   **Temporal Analysis**: Time-based predictions with configurable windows (days, months, years)

### 3. Multi-Tab Gradio Interface
-   **💬 Chat Agent**: Conversational interface with query history
-   **📊 Data Explorer**: Schema visualization and sample data inspection
-   **⚡ Direct PQL Query**: Advanced mode for manual PQL execution
-   **📈 Performance**: Query execution history and metrics
-   **⚙️ Settings**: Configuration and system information

### 4. Production-Ready Architecture
-   **Modular Design**: Clean separation of concerns (data loading, KumoRFM setup, translation, UI)
-   **Environment-Based Configuration**: Secure API key management via `.env` files
-   **Comprehensive Error Handling**: Graceful fallbacks and user-friendly error messages
-   **Automated Setup**: PowerShell launcher for one-click deployment
-   **Extensive Documentation**: README, deployment guide, runbook, and inline code comments

---

## 📂 Project Structure

```
insurance-claims-kumo-agent/
├── src/                                # Source code modules
│   ├── __init__.py                    # Package initialization
│   ├── data_loader.py                 # Data ingestion and profiling
│   ├── kumo_setup.py                  # KumoRFM client and graph setup
│   ├── text_to_pql.py                 # OpenAI-powered NL → PQL translation
│   └── kumo_agent.py                  # Gradio UI and conversational agent
├── data/                               # Data directory
│   ├── customers.parquet              # Sample customer data
│   └── claims.parquet                 # Sample claims data
├── notebooks/                          # Reference notebooks (optional)
├── main.py                             # Application entry point
├── requirements.txt                    # Python dependencies
├── .env.template                       # Environment variable template
├── launch.ps1                          # PowerShell launcher (Windows)
├── test_modules.py                     # Module testing script
├── README.md                           # Quick start guide
├── DEPLOYMENT_GUIDE.md                 # Comprehensive deployment instructions
├── run-insurance-claims-kumorfm-app.plan.md  # Runbook and checklist
└── PROJECT_SUMMARY.md                  # This file
```

---

## 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Foundation Model** | KumoRFM (kumoai SDK) | Relational predictions on structured data |
| **NL Understanding** | OpenAI GPT-4o-mini/GPT-4o | Natural language to PQL translation |
| **Web Interface** | Gradio 4.0+ | Interactive multi-tab UI |
| **Data Processing** | Pandas, PyArrow | Parquet data handling and profiling |
| **Configuration** | python-dotenv | Environment variable management |
| **Visualization** | Matplotlib, Plotly | Result visualization (optional) |

---

## 🚀 Quick Start

### Prerequisites
-   Python 3.9+
-   KumoRFM API Key ([Get one here](https://kumorfm.ai/api-keys))
-   OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Installation (3 Steps)

1.  **Clone and Navigate**:
    ```bash
    git clone <repository-url>
    cd insurance-claims-kumo-agent
    ```

2.  **Configure Environment**:
    ```bash
    cp .env.template .env
    # Edit .env and add your API keys
    ```

3.  **Launch Application**:
    ```powershell
    # Windows
    .\launch.ps1
    ```
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python main.py
    ```

4.  **Access UI**: Open browser to `http://127.0.0.1:7860`

---

## 💡 Example Use Cases

### Use Case 1: Fraud Detection
**Query**: `"Is claim 98765 fraudulent?"`

**Generated PQL**:
```sql
PREDICT claims.fraud_flag FOR claims.claim_id=98765
```

**Result**: Fraud probability and classification for the specific claim.

---

### Use Case 2: Customer Risk Assessment
**Query**: `"Which customers will have total claims over $5000 in the next 90 days?"`

**Generated PQL**:
```sql
PREDICT SUM(claims.claim_amount, 0, 90, days) > 5000 FOR EACH customers.customer_id
```

**Result**: List of high-risk customers with predicted claim amounts.

---

### Use Case 3: Claim Frequency Forecasting
**Query**: `"How many claims will customer 123 file in the next 60 days?"`

**Generated PQL**:
```sql
PREDICT COUNT(claims.*, 0, 60, days) FOR customers.customer_id=123
```

**Result**: Predicted claim count for the customer.

---

## 🧪 Testing & Validation

The project includes comprehensive testing:

### Module Tests
Run `test_modules.py` to validate all core modules:
```bash
python test_modules.py
```

**Test Coverage**:
-   ✅ Data Loader: Parquet ingestion, profiling, validation
-   ✅ KumoRFM Setup: SDK import, client initialization
-   ✅ Text-to-PQL Translator: OpenAI integration, PQL validation
-   ✅ Gradio Agent: UI components, conversation orchestration
-   ✅ Main Application: End-to-end integration

### Sample Data
The project includes synthetic sample data for testing:
-   **customers.parquet**: 100 customer records
-   **claims.parquet**: 500 claim records with fraud flags

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **README.md** | Quick start guide and overview |
| **DEPLOYMENT_GUIDE.md** | Production deployment, security, monitoring |
| **run-insurance-claims-kumorfm-app.plan.md** | Step-by-step runbook and use-case scenarios |
| **PROJECT_SUMMARY.md** | This comprehensive summary |
| **Inline Code Comments** | Detailed explanations in all source files |

---

## 🔐 Security & Best Practices

### API Key Management
-   ✅ Never commit `.env` to version control (included in `.gitignore`)
-   ✅ Use environment-specific keys for dev/staging/prod
-   ✅ Rotate keys regularly (every 90 days recommended)

### Error Handling
-   ✅ Graceful fallbacks for SDK method variations
-   ✅ Clear error messages with troubleshooting hints
-   ✅ Validation of PQL queries before execution

### Code Quality
-   ✅ Modular architecture with single-responsibility modules
-   ✅ Type hints for improved code clarity
-   ✅ Comprehensive docstrings and comments
-   ✅ Try/except blocks with specific error handling

---

## 🛠️ Customization & Extension

### Adding New Prediction Types
1.  Update `_build_pql_knowledge_base()` in `text_to_pql.py` with new examples
2.  Add domain-specific patterns to the system prompt
3.  Test with sample queries

### Integrating Additional Data Sources
1.  Add new Parquet files to `data/` directory
2.  Update `kumo_setup.py` to define relationships
3.  Modify `create_graph()` to include new tables

### Custom UI Components
1.  Edit `create_gradio_interface()` in `kumo_agent.py`
2.  Add new tabs or modify existing layouts
3.  Implement custom visualization functions

---

## 📊 Performance Considerations

### Optimization Strategies
-   **Caching**: Implement LRU cache for frequently used queries
-   **Async Processing**: Use asyncio for concurrent API calls
-   **Batch Predictions**: Execute bulk predictions for efficiency
-   **Database Backend**: Store query history and results in a database for large-scale deployments

### Scalability
-   **Horizontal Scaling**: Deploy multiple instances behind a load balancer
-   **API Rate Limiting**: Implement rate limits to prevent abuse
-   **Monitoring**: Track API latency, error rates, and resource usage

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Module not found** | Activate virtual environment and reinstall dependencies |
| **API key errors** | Verify `.env` file exists and contains valid keys |
| **Data loading fails** | Check `INSURANCE_DATA_PATH` and verify Parquet file validity |
| **Port already in use** | Change `APP_PORT` in `.env` or kill process using the port |
| **PQL execution errors** | Validate entity IDs exist and columns match schema |

See **DEPLOYMENT_GUIDE.md** for detailed troubleshooting.

---

## 🌟 Future Enhancements

### Planned Features
-   **Multi-User Authentication**: User login and role-based access control
-   **Query Templates**: Pre-built query templates for common use cases
-   **Export Functionality**: Download results as CSV, Excel, or PDF
-   **Advanced Visualizations**: Interactive charts and dashboards
-   **Model Performance Metrics**: Track prediction accuracy and confidence
-   **Integration with BI Tools**: Connect to Tableau, Power BI, etc.

### Roadmap
-   **Q1 2025**: User authentication and session management
-   **Q2 2025**: Advanced analytics dashboard
-   **Q3 2025**: Integration with enterprise data warehouses
-   **Q4 2025**: Mobile-responsive UI and API endpoints

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

---

## 📞 Support

For questions, issues, or feature requests:
-   **Documentation**: Refer to README.md and DEPLOYMENT_GUIDE.md
-   **KumoRFM Support**: [https://kumo.ai/support](https://kumo.ai/support)
-   **OpenAI Support**: [https://help.openai.com](https://help.openai.com)

---

## 🙏 Acknowledgments

-   **KumoRFM Team**: For the powerful Relational Foundation Model
-   **OpenAI**: For GPT models enabling natural language understanding
-   **Gradio Team**: For the excellent UI framework
-   **Open Source Community**: For the amazing Python ecosystem

---

**Built with ❤️ by the Autonomous Developer Agent**

*Empowering insurance professionals with AI-driven insights*

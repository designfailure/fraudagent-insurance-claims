#!/usr/bin/env python3
"""
KumoRFM Insurance Claims AI Agent - Main Application with Upload Feature
Entry point for the FraudAGENT application with Excel upload capability.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data_loader import InsuranceDataLoader
from src.kumo_setup import KumoSetup
from src.text_to_pql import TextToPQLTranslator
from src.kumo_agent import KumoConversationAgent
from src.upload_ui import DataUploadUI
import gradio as gr


def validate_environment() -> bool:
    """
    Validate required environment variables and dependencies.
    
    Returns:
        True if validation passes, False otherwise
    """
    print("\n" + "="*80)
    print("ENVIRONMENT VALIDATION")
    print("="*80)
    
    errors = []
    warnings = []
    
    # Check API keys
    if not os.getenv("KUMO_API_KEY"):
        errors.append("KUMO_API_KEY environment variable not set")
    else:
        print("✓ KUMO_API_KEY is set")
    
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY environment variable not set")
    else:
        print("✓ OPENAI_API_KEY is set")
    
    # Check data path - now optional since users can upload
    data_path = os.getenv("INSURANCE_DATA_PATH", "data/insurance_claims_data.parquet")
    if not os.path.exists(data_path) and not os.path.exists("uploaded_data"):
        warnings.append(f"No data found at {data_path} or uploaded_data/")
        warnings.append("Please upload data using the Data Upload tab")
        print(f"⚠ No data found - upload required")
    else:
        if os.path.exists(data_path):
            print(f"✓ Default data file found: {data_path}")
        if os.path.exists("uploaded_data"):
            print(f"✓ Uploaded data found: uploaded_data/")
    
    # Print errors
    if errors:
        print("\n❌ VALIDATION FAILED:")
        for error in errors:
            print(f"  • {error}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        print("See .env.template for reference.")
        return False
    
    # Print warnings
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
    
    print("\n✅ Environment validation passed!")
    return True


def determine_data_source() -> str:
    """
    Determine which data source to use.
    
    Returns:
        Path to data directory
    """
    # Priority: uploaded_data > INSURANCE_DATA_PATH > data/
    if os.path.exists("uploaded_data") and len(os.listdir("uploaded_data")) > 0:
        print("\n📊 Using uploaded data as primary source: uploaded_data/")
        return "uploaded_data"
    
    data_path = os.getenv("INSURANCE_DATA_PATH", "data")
    if os.path.exists(data_path):
        print(f"\n📊 Using default data source: {data_path}")
        return data_path
    
    print("\n⚠️  No data source available. Please upload data using the Data Upload tab.")
    return None


def create_integrated_interface(agent, graph_schema, upload_ui):
    """
    Create integrated Gradio interface with upload tab.
    
    Args:
        agent: KumoConversationAgent instance
        graph_schema: Graph schema dictionary
        upload_ui: DataUploadUI instance
        
    Returns:
        Gradio Blocks interface
    """
    with gr.Blocks(
        title="FraudAGENT - Insurance Claims AI Agent",
        theme=gr.themes.Soft()
    ) as app:
        gr.Markdown("""
        # 🏥 FraudAGENT - KumoRFM Insurance Claims AI Agent
        
        **Fraud detection and predictive analytics using KumoRFM and OpenAI**
        """)
        
        with gr.Tabs():
            # Data Upload Tab (First tab)
            upload_ui.create_upload_tab()
            
            # Chat Agent Tab
            with gr.Tab("💬 Chat Agent"):
                gr.Markdown("""
                Ask questions in natural language about insurance claims, fraud detection, and predictions.
                The AI will translate your question into a KumoRFM query and execute it.
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(
                            label="Conversation",
                            height=500
                        )
                        
                        with gr.Row():
                            user_input = gr.Textbox(
                                label="Your Question",
                                placeholder="e.g., Is claim 12345 fraudulent?",
                                scale=4
                            )
                            submit_btn = gr.Button("Ask", variant="primary", scale=1)
                        
                        clear_btn = gr.Button("Clear Chat")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### 💡 Example Queries")
                        examples = gr.Examples(
                            examples=[
                                "Is claim CLM40000 fraudulent?",
                                "How many claims will customer CUST17989 file in the next 30 days?",
                                "What is the total claim amount for policy POL40718?",
                                "Predict fraud probability for all open claims",
                                "Which customers are high risk in the next 60 days?"
                            ],
                            inputs=user_input
                        )
                        
                        pql_output = gr.Textbox(
                            label="Generated PQL Query",
                            lines=3,
                            interactive=False
                        )
                        
                        execute_btn = gr.Button("Execute Query", variant="secondary")
                        
                        result_output = gr.Dataframe(
                            label="Query Results",
                            wrap=True
                        )
                
                # Event handlers
                def chat_response(message, history):
                    response = agent.process_query(message)
                    history = history or []
                    history.append((message, response['response']))
                    return history, response.get('pql_query', '')
                
                def execute_query(pql):
                    if not pql:
                        return None
                    result = agent.execute_pql_query(pql)
                    return result.get('dataframe')
                
                submit_btn.click(
                    fn=chat_response,
                    inputs=[user_input, chatbot],
                    outputs=[chatbot, pql_output]
                ).then(
                    fn=lambda: "",
                    outputs=user_input
                )
                
                execute_btn.click(
                    fn=execute_query,
                    inputs=pql_output,
                    outputs=result_output
                )
                
                clear_btn.click(
                    fn=lambda: ([], "", None),
                    outputs=[chatbot, pql_output, result_output]
                )
            
            # Data Explorer Tab
            with gr.Tab("📊 Data Explorer"):
                gr.Markdown("### Graph Schema")
                
                if graph_schema:
                    schema_md = "## Tables\n\n"
                    for table_name, table_info in graph_schema.get('tables', {}).items():
                        schema_md += f"### `{table_name}`\n"
                        schema_md += f"- **Primary Key:** `{table_info.get('primary_key', 'N/A')}`\n"
                        schema_md += f"- **Columns:** {len(table_info.get('columns', {}))}\n\n"
                    
                    gr.Markdown(schema_md)
                else:
                    gr.Markdown("⚠️ No schema available. Please upload data first.")
            
            # Direct PQL Query Tab
            with gr.Tab("⚡ Direct PQL Query"):
                gr.Markdown("""
                ### Execute PQL Queries Directly
                
                For advanced users: write and execute PQL queries manually.
                """)
                
                pql_input = gr.Textbox(
                    label="PQL Query",
                    placeholder="PREDICT claims.fraud_flag FOR claims.claim_id=12345",
                    lines=5
                )
                
                pql_execute_btn = gr.Button("Execute", variant="primary")
                
                pql_result = gr.Dataframe(label="Results")
                
                pql_execute_btn.click(
                    fn=execute_query,
                    inputs=pql_input,
                    outputs=pql_result
                )
            
            # Settings Tab
            with gr.Tab("⚙️ Settings"):
                gr.Markdown("""
                ### System Information
                
                **Data Source:** {}
                
                **OpenAI Model:** {}
                
                **KumoRFM Status:** Connected
                """.format(
                    determine_data_source() or "No data loaded",
                    os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                ))
    
    return app


def main():
    """
    Main application entry point.
    """
    print("="*80)
    print("🏥 KUMORFM INSURANCE CLAIMS AI AGENT - FRAUDAGENT (WITH UPLOAD)")
    print("="*80)
    print("Fraud detection and predictive analytics using KumoRFM and OpenAI")
    print("="*80)
    
    # Load environment variables
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✓ Loaded environment from: {env_file}")
    else:
        print(f"⚠ No .env file found at: {env_file}")
        print("  Using system environment variables")
    
    # Validate environment
    if not validate_environment():
        print("\n❌ Application startup failed due to environment validation errors.")
        print("\nQuick fix:")
        print("  1. Copy .env.template to .env")
        print("  2. Edit .env and add your API keys")
        print("  3. Run the application again")
        sys.exit(1)
    
    # Get configuration
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "7860"))
    share_ui = os.getenv("GRADIO_SHARE", "false").lower() == "true"
    
    try:
        # Determine data source
        data_path = determine_data_source()
        
        if data_path:
            # ===== PHASE 1: Load and Profile Data =====
            print("\n" + "="*80)
            print("PHASE 1: DATA LOADING AND PROFILING")
            print("="*80)
            
            loader = InsuranceDataLoader(data_path)
            tables = loader.load_data()
            schema_info = loader.profile_data()
            loader.validate_temporal_columns()
            loader.check_duplicates()
            
            print("\n✅ Phase 1 complete: Data loaded and profiled")
            
            # ===== PHASE 2: Initialize KumoRFM =====
            print("\n" + "="*80)
            print("PHASE 2: KUMORFM INITIALIZATION")
            print("="*80)
            
            kumo = KumoSetup()
            kumo.authenticate()
            
            # Import dataset
            local_tables = kumo.import_dataset(tables, auto_infer_metadata=True)
            
            # Create graph
            graph = kumo.create_graph(local_tables, auto_infer_links=True)
            
            # Materialize graph
            model = kumo.materialize_graph()
            
            # Get graph schema
            graph_schema = kumo.get_graph_schema()
            
            print("\n✅ Phase 2 complete: KumoRFM initialized and graph materialized")
            
            # ===== PHASE 3: Initialize NL to PQL Translator =====
            print("\n" + "="*80)
            print("PHASE 3: NL TO PQL TRANSLATOR INITIALIZATION")
            print("="*80)
            
            openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            translator = TextToPQLTranslator(graph_schema, model=openai_model)
            
            print(f"\n✅ Phase 3 complete: Translator initialized with model {openai_model}")
            
            # ===== PHASE 4: Create Conversational Agent =====
            print("\n" + "="*80)
            print("PHASE 4: CONVERSATIONAL AGENT CREATION")
            print("="*80)
            
            agent = KumoConversationAgent(kumo, translator, graph_schema)
            
            print("\n✅ Phase 4 complete: Conversational agent created")
        else:
            # No data yet - create minimal components
            graph_schema = None
            agent = None
            print("\n⚠️  Starting in upload-only mode. Please upload data to enable predictions.")
        
        # ===== PHASE 5: Create Upload UI =====
        print("\n" + "="*80)
        print("PHASE 5: CREATING UPLOAD UI")
        print("="*80)
        
        upload_ui = DataUploadUI()
        
        print("\n✅ Phase 5 complete: Upload UI created")
        
        # ===== PHASE 6: Launch Gradio Interface =====
        print("\n" + "="*80)
        print("PHASE 6: LAUNCHING GRADIO INTERFACE")
        print("="*80)
        
        if agent:
            app = create_integrated_interface(agent, graph_schema, upload_ui)
        else:
            # Upload-only interface
            with gr.Blocks(title="FraudAGENT - Data Upload") as app:
                gr.Markdown("# 🏥 FraudAGENT - Upload Data to Begin")
                upload_ui.create_upload_tab()
                gr.Markdown("""
                ### ⚠️ Next Steps
                1. Upload your Excel file using the form above
                2. Restart the application to load the uploaded data
                3. The full interface will be available after restart
                """)
        
        print(f"\n🚀 Launching Gradio UI at http://{app_host}:{app_port}")
        print(f"   Share mode: {'Enabled' if share_ui else 'Disabled'}")
        print("\n" + "="*80)
        print("APPLICATION READY!")
        print("="*80)
        print("\n💡 Features:")
        print("  • Upload Excel files and convert to Parquet")
        print("  • Ask questions in natural language")
        print("  • Automatic PQL query generation")
        print("  • Fraud detection and predictions")
        print("\n" + "="*80)
        
        # Launch Gradio
        app.launch(
            server_name=app_host,
            server_port=app_port,
            share=share_ui,
            show_error=True
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n\n❌ APPLICATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

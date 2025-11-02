#!/usr/bin/env python3
"""
FraudAGENT Launcher - Fixed version without __file__ dependency
"""

import os
import sys

# Set up environment
os.environ.setdefault('KUMO_API_KEY', 'demo-kumo-key')
os.environ.setdefault('APP_HOST', '0.0.0.0')
os.environ.setdefault('APP_PORT', '7865')

# Add current directory to path
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

# Install mock kumoai
try:
    import kumoai
except ImportError:
    import mock_kumoai
    sys.modules['kumoai'] = mock_kumoai
    sys.modules['kumoai.experimental'] = mock_kumoai
    sys.modules['kumoai.experimental.rfm'] = mock_kumoai

# Now import and run the application
from dotenv import load_dotenv
load_dotenv()

from src.data_loader import InsuranceDataLoader
from src.kumo_setup import KumoSetup
from src.text_to_pql import TextToPQLTranslator
from src.kumo_agent import KumoConversationAgent
from src.upload_ui import DataUploadUI
import gradio as gr


def determine_data_source():
    """Determine which data source to use based on priority."""
    # Priority 1: uploaded_data directory
    if os.path.exists("uploaded_data") and os.listdir("uploaded_data"):
        return "uploaded_data"
    
    # Priority 2: Environment variable
    env_path = os.getenv("INSURANCE_DATA_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
    
    # Priority 3: Default data directory
    if os.path.exists("data"):
        return "data"
    
    return None


def main():
    """Main application entry point."""
    
    print("\n" + "="*80)
    print("🏥 KUMORFM INSURANCE CLAIMS AI AGENT - FRAUDAGENT")
    print("="*80)
    print("Fraud detection and predictive analytics using KumoRFM and OpenAI")
    print("="*80)
    
    # Determine data source
    data_source = determine_data_source()
    
    if not data_source:
        print("\n⚠️  No data source found. Starting in upload-only mode.")
        print("Please upload an Excel file to get started.\n")
        
        # Create upload-only interface
        upload_ui = DataUploadUI()
        upload_interface = upload_ui.create_upload_interface()
        
        upload_interface.launch(
            server_name=os.getenv("APP_HOST", "0.0.0.0"),
            server_port=int(os.getenv("APP_PORT", 7865)),
            share=os.getenv("GRADIO_SHARE", "false").lower() == "true"
        )
        return
    
    print(f"\n📊 Using data source: {data_source}\n")
    
    # Phase 1: Load Data
    print("="*80)
    print("PHASE 1: DATA LOADING AND PROFILING")
    print("="*80)
    
    loader = InsuranceDataLoader(data_source)
    tables = loader.load_data()
    schema_info = loader.profile_data()
    loader.validate_temporal_columns()
    loader.check_duplicates()
    
    print("\n✅ Phase 1 complete: Data loaded and profiled")
    
    # Phase 2: Initialize KumoRFM
    print("\n" + "="*80)
    print("PHASE 2: KUMORFM INITIALIZATION")
    print("="*80)
    
    kumo = KumoSetup()
    kumo.import_dataset(tables, schema_info)
    graph_obj = kumo.create_graph(tables)
    kumo.materialize_graph()
    
    print("\n✅ Phase 2 complete: KumoRFM initialized and graph materialized")
    
    # Phase 3: Initialize Translator
    print("\n" + "="*80)
    print("PHASE 3: NL TO PQL TRANSLATOR INITIALIZATION")
    print("="*80)
    
    # Create a JSON-serializable schema dictionary
    # Convert schema_info to JSON-serializable format (convert Timestamps to strings)
    import json
    import pandas as pd
    
    def make_json_serializable(obj):
        """Recursively convert non-JSON-serializable objects to strings."""
        if isinstance(obj, (pd.Timestamp, pd.Timedelta)):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(make_json_serializable(item) for item in obj)
        else:
            return obj
    
    # Convert schema_info to JSON-serializable format
    serializable_schema = make_json_serializable(schema_info)
    
    graph_schema = {
        "tables": list(tables.keys()),
        "schema_info": serializable_schema
    }
    
    translator = TextToPQLTranslator(
        graph_schema=graph_schema,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    
    print("\n✅ Phase 3 complete: Translator initialized with model", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    
    # Phase 4: Create Agent
    print("\n" + "="*80)
    print("PHASE 4: CONVERSATIONAL AGENT CREATION")
    print("="*80)
    
    agent = KumoConversationAgent(
        kumo_client=kumo,
        translator=translator,
        graph_schema=graph_schema
    )
    
    print("\n✅ Phase 4 complete: Conversational agent created")
    
    # Phase 5: Create Upload UI
    print("\n" + "="*80)
    print("PHASE 5: CREATING UPLOAD UI")
    print("="*80)
    
    upload_ui = DataUploadUI()
    
    print("\n✅ Phase 5 complete: Upload UI created")
    
    # Phase 6: Create Gradio Interface
    print("\n" + "="*80)
    print("PHASE 6: LAUNCHING GRADIO INTERFACE")
    print("="*80)
    
    with gr.Blocks(title="FraudAGENT - Insurance Claims AI", theme=gr.themes.Soft()) as app:
        
        gr.Markdown("""
        # 🏥 FraudAGENT - Insurance Claims AI Agent
        
        **AI-powered fraud detection and predictive analytics using KumoRFM and OpenAI**
        
        Upload your own data or use the sample dataset to ask questions and get predictions.
        """)
        
        with gr.Tabs():
            
            # Tab 1: Data Upload
            with gr.Tab("📤 Data Upload"):
                upload_ui.create_upload_tab()
            
            # Tab 2: Chat Agent
            with gr.Tab("💬 Chat Agent"):
                gr.Markdown("### Ask questions about insurance claims and fraud detection")
                
                chatbot = gr.Chatbot(label="Conversation", height=400)
                
                with gr.Row():
                    user_input = gr.Textbox(
                        label="Your Question",
                        placeholder="e.g., Is claim CLM12345 fraudulent?",
                        lines=2,
                        scale=4
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                gr.Markdown("### Generated PQL Query")
                pql_output = gr.Code(label="PQL Query", language="sql", lines=5)
                
                execute_btn = gr.Button("Execute Query", variant="secondary")
                
                result_output = gr.Dataframe(label="Query Results", wrap=True)
                
                # Event handlers
                def chat_response(message, history):
                    try:
                        response = agent.process_query(message)
                        history = history or []
                        history.append((message, response['response']))
                        return history, response.get('pql_query', '')
                    except Exception as e:
                        import traceback
                        error_trace = traceback.format_exc()
                        print(f"ERROR in chat_response: {error_trace}")
                        history = history or []
                        history.append((message, f"😕 I encountered an error. Could you rephrase your query?\n\nError details: {str(e)}"))
                        return history, ''
                
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
            
            # Tab 3: Settings
            with gr.Tab("⚙️ Settings"):
                gr.Markdown("### System Information")
                
                settings_info = f"""
                **Data Source**: `{data_source}`  
                **OpenAI Model**: `{os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}`  
                **KumoRFM Status**: Connected (demo mode)  
                **Tables Loaded**: {len(tables)}  
                **Total Rows**: {sum(len(df) for df in tables.values()):,}
                """
                
                gr.Markdown(settings_info)
    
    print(f"\n📊 Using data source: {data_source}")
    print(f"🚀 Launching Gradio UI at http://{os.getenv('APP_HOST', '0.0.0.0')}:{os.getenv('APP_PORT', 7865)}")
    print(f"   Share mode: {'Enabled' if os.getenv('GRADIO_SHARE', 'false').lower() == 'true' else 'Disabled'}")
    
    print("\n" + "="*80)
    print("APPLICATION READY!")
    print("="*80)
    print("💡 Features:")
    print("  • Upload Excel files and convert to Parquet")
    print("  • Ask questions in natural language")
    print("  • Automatic PQL query generation")
    print("  • Fraud detection and predictions")
    print("="*80)
    
    app.launch(
        server_name=os.getenv("APP_HOST", "0.0.0.0"),
        server_port=int(os.getenv("APP_PORT", 7865)),
        share=os.getenv("GRADIO_SHARE", "false").lower() == "true"
    )


if __name__ == "__main__":
    main()

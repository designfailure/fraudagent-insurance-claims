#!/usr/bin/env python3
"""
KumoRFM Insurance Claims AI Agent - Main Application
Entry point for the FraudAGENT application.
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
from src.kumo_agent import KumoConversationAgent, create_gradio_interface


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
    
    # Check data path
    data_path = os.getenv("INSURANCE_DATA_PATH", "data/insurance_claims_data.parquet")
    if not os.path.exists(data_path):
        warnings.append(f"Data file not found: {data_path}")
        print(f"⚠ Data file not found: {data_path}")
    else:
        print(f"✓ Data file found: {data_path}")
    
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


def main():
    """
    Main application entry point.
    """
    print("="*80)
    print("🏥 KUMORFM INSURANCE CLAIMS AI AGENT - FRAUDAGENT")
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
    data_path = os.getenv("INSURANCE_DATA_PATH", "data/insurance_claims_data.parquet")
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "7860"))
    share_ui = os.getenv("GRADIO_SHARE", "false").lower() == "true"
    
    try:
        # ===== PHASE 1: Load and Profile Data =====
        print("\n" + "="*80)
        print("PHASE 1: DATA LOADING AND PROFILING")
        print("="*80)
        
        loader = InsuranceDataLoader(data_path)
        tables = loader.load_data()
        schema_info = loader.profile_data()
        loader.validate_temporal_columns()
        loader.check_duplicates()
        loader.export_schema_summary("data_schema_summary.json")
        
        print("\n✅ Phase 1 complete: Data loaded and profiled")
        
        # ===== PHASE 2: Initialize KumoRFM =====
        print("\n" + "="*80)
        print("PHASE 2: KUMORFM INITIALIZATION")
        print("="*80)
        
        kumo = KumoSetup()
        kumo.authenticate()
        
        # Import dataset
        local_tables = kumo.import_dataset(tables, auto_infer_metadata=True)
        
        # Create graph with auto-inferred links
        # Note: Manual links can be added if auto-inference doesn't work
        # Example manual links:
        # manual_links = [
        #     {"src_table": "claims", "fkey": "customer_id", "dst_table": "customers"},
        #     {"src_table": "claims", "fkey": "policy_id", "dst_table": "policies"}
        # ]
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
        
        # ===== PHASE 5: Launch Gradio Interface =====
        print("\n" + "="*80)
        print("PHASE 5: LAUNCHING GRADIO INTERFACE")
        print("="*80)
        
        app = create_gradio_interface(agent, graph_schema)
        
        print(f"\n🚀 Launching Gradio UI at http://{app_host}:{app_port}")
        print(f"   Share mode: {'Enabled' if share_ui else 'Disabled'}")
        print("\n" + "="*80)
        print("APPLICATION READY!")
        print("="*80)
        print("\n💡 Example queries to try:")
        print("  • Is claim 12345 fraudulent?")
        print("  • How many claims will customer 100 file in the next 30 days?")
        print("  • What is the total claim amount for customer 200?")
        print("  • Predict fraud probability for all claims")
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

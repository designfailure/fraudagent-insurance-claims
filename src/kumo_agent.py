"""
KumoRFM Conversational Agent Module
Gradio-based UI for natural language queries to KumoRFM predictions.
"""

import os
import json
import pandas as pd
import gradio as gr
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime


class KumoConversationAgent:
    """
    Conversational AI agent for KumoRFM insurance claims analysis.
    Orchestrates NL → PQL translation and query execution.
    """
    
    def __init__(self, kumo_client, translator, graph_schema: Dict[str, Any]):
        """
        Initialize conversation agent.
        
        Args:
            kumo_client: KumoSetup instance with materialized model
            translator: TextToPQLTranslator instance
            graph_schema: Graph schema dictionary
        """
        self.kumo_client = kumo_client
        self.translator = translator
        self.graph_schema = graph_schema
        self.query_history = []
        self.current_pql = None
        self.current_result = None
    
    def process_message(
        self, 
        user_message: str, 
        chat_history: List[Tuple[str, str]]
    ) -> Tuple[List[Tuple[str, str]], str, Optional[pd.DataFrame], str]:
        """
        Process user message and generate response.
        
        Args:
            user_message: User's natural language query
            chat_history: Conversation history
        
        Returns:
            Tuple of (updated_chat_history, pql_code, result_dataframe, plot_json)
        """
        if not user_message.strip():
            return chat_history, "", None, ""
        
        # Add user message to history
        chat_history.append((user_message, None))
        
        # Translate to PQL
        translation_result = self.translator.translate(user_message)
        
        # Check if clarification needed
        if translation_result.get("requires_clarification"):
            clarification = translation_result.get("clarification_question", "Could you please clarify?")
            chat_history[-1] = (user_message, f"🤔 {clarification}")
            return chat_history, "", None, ""
        
        # Get PQL query
        pql_query = translation_result.get("pql_query")
        confidence = translation_result.get("confidence", 0)
        explanation = translation_result.get("explanation", "")
        
        if not pql_query:
            chat_history[-1] = (user_message, "❌ Could not generate PQL query. Please try rephrasing.")
            return chat_history, "", None, ""
        
        # Store current PQL
        self.current_pql = pql_query
        
        # Validate PQL
        is_valid, validation_msg = self.translator.validate_pql(pql_query)
        
        # Generate response
        response = f"**Generated PQL Query** (confidence: {confidence:.0%}):\n```\n{pql_query}\n```\n\n"
        response += f"**Explanation**: {explanation}\n\n"
        
        if not is_valid:
            response += f"⚠️ **Validation Warning**: {validation_msg}\n\n"
        
        response += "Click **Execute Query** to run this prediction."
        
        chat_history[-1] = (user_message, response)
        
        return chat_history, pql_query, None, ""
    
    def execute_query(
        self, 
        pql_query: str,
        anchor_time_str: Optional[str] = None
    ) -> Tuple[Optional[pd.DataFrame], str, str]:
        """
        Execute PQL query via KumoRFM.
        
        Args:
            pql_query: PQL query string
            anchor_time_str: Optional anchor time string (YYYY-MM-DD)
        
        Returns:
            Tuple of (result_dataframe, status_message, plot_json)
        """
        if not pql_query or not pql_query.strip():
            return None, "❌ No PQL query to execute", ""
        
        try:
            # Parse anchor time if provided
            anchor_time = None
            if anchor_time_str and anchor_time_str.strip():
                try:
                    anchor_time = pd.Timestamp(anchor_time_str)
                except Exception as e:
                    return None, f"❌ Invalid anchor time format: {e}", ""
            
            # Execute query
            print(f"\n🚀 Executing PQL: {pql_query}")
            result_df = self.kumo_client.execute_pql(pql_query, anchor_time=anchor_time)
            
            # Store result
            self.current_result = result_df
            
            # Add to history
            self.query_history.append({
                "timestamp": datetime.now().isoformat(),
                "pql_query": pql_query,
                "anchor_time": str(anchor_time) if anchor_time else None,
                "num_results": len(result_df)
            })
            
            # Generate status message
            status = f"✅ Query executed successfully!\n"
            status += f"📊 Returned {len(result_df)} row(s), {len(result_df.columns)} column(s)\n"
            status += f"⏱️ Executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Generate simple plot data (if applicable)
            plot_json = self._generate_plot(result_df)
            
            return result_df, status, plot_json
            
        except Exception as e:
            error_msg = f"❌ Query execution failed:\n{str(e)}\n\n"
            error_msg += "**Troubleshooting**:\n"
            error_msg += "- Check that entity IDs exist in the data\n"
            error_msg += "- Verify column names match the schema\n"
            error_msg += "- Ensure temporal columns are properly configured"
            return None, error_msg, ""
    
    def _generate_plot(self, df: pd.DataFrame) -> str:
        """
        Generate plot data from result DataFrame.
        
        Args:
            df: Result DataFrame
        
        Returns:
            JSON string for plotting (empty if not applicable)
        """
        # Simple heuristic: if result has probability columns, create bar chart
        if df is None or len(df) == 0:
            return ""
        
        # Check for common result patterns
        prob_cols = [col for col in df.columns if 'PROB' in col.upper()]
        
        if prob_cols and len(df) <= 20:
            # Create simple bar chart data
            plot_data = {
                "type": "bar",
                "x": df.iloc[:, 0].astype(str).tolist(),  # First column as x-axis
                "y": df[prob_cols[0]].tolist(),  # First probability column
                "title": f"Prediction Results: {prob_cols[0]}"
            }
            return json.dumps(plot_data)
        
        return ""
    
    def get_query_history(self) -> pd.DataFrame:
        """
        Get query execution history.
        
        Returns:
            DataFrame with query history
        """
        if not self.query_history:
            return pd.DataFrame(columns=["timestamp", "pql_query", "anchor_time", "num_results"])
        
        return pd.DataFrame(self.query_history)
    
    def process_query(self, user_message: str) -> Dict[str, Any]:
        """
        Process user query and return response with PQL.
        Simplified interface for main_with_upload.py compatibility.
        
        Args:
            user_message: User's natural language query
        
        Returns:
            Dictionary with 'response' and 'pql_query' keys
        """
        print(f"\n[DEBUG] process_query called with: {user_message}")
        
        if not user_message.strip():
            return {"response": "Please enter a question.", "pql_query": ""}
        
        print("[DEBUG] About to call translator.translate()")
        try:
            # Translate to PQL
            translation_result = self.translator.translate(user_message)
            print(f"[DEBUG] Translation result: {translation_result}")
        except Exception as e:
            print(f"[DEBUG] Error in translator.translate(): {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # Check if clarification needed
        if translation_result.get("requires_clarification"):
            clarification = translation_result.get("clarification_question", "Could you please clarify?")
            return {"response": f"🤔 {clarification}", "pql_query": ""}
        
        # Get PQL query
        pql_query = translation_result.get("pql_query")
        confidence = translation_result.get("confidence", 0)
        explanation = translation_result.get("explanation", "")
        
        if not pql_query:
            return {
                "response": "❌ Could not generate PQL query. Please try rephrasing.",
                "pql_query": ""
            }
        
        # Store current PQL
        self.current_pql = pql_query
        
        # Validate PQL
        is_valid, validation_msg = self.translator.validate_pql(pql_query)
        
        # Generate response
        response = f"**Generated PQL Query** (confidence: {confidence:.0%}):\n```\n{pql_query}\n```\n\n"
        response += f"**Explanation**: {explanation}\n\n"
        
        if not is_valid:
            response += f"⚠️ **Validation Warning**: {validation_msg}\n\n"
        
        response += "Click **Execute Query** to run this prediction."
        
        return {
            "response": response,
            "pql_query": pql_query
        }
    
    def execute_pql_query(self, pql_query: str, anchor_time_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute PQL query and return results.
        Simplified interface for main_with_upload.py compatibility.
        
        Args:
            pql_query: PQL query string
            anchor_time_str: Optional anchor time string (YYYY-MM-DD)
        
        Returns:
            Dictionary with 'dataframe', 'status', and 'plot' keys
        """
        result_df, status, plot_json = self.execute_query(pql_query, anchor_time_str)
        
        return {
            "dataframe": result_df,
            "status": status,
            "plot": plot_json
        }


def create_gradio_interface(agent: KumoConversationAgent, graph_schema: Dict[str, Any]) -> gr.Blocks:
    """
    Create Gradio interface for KumoRFM agent.
    
    Args:
        agent: KumoConversationAgent instance
        graph_schema: Graph schema dictionary
    
    Returns:
        Gradio Blocks interface
    """
    
    with gr.Blocks(title="KumoRFM Insurance Claims AI Agent", theme=gr.themes.Soft()) as app:
        
        gr.Markdown("""
        # 🏥 KumoRFM Insurance Claims AI Agent
        
        **FraudAGENT**: Natural language interface for insurance claims fraud detection and analysis.
        
        Ask questions in plain English, and the AI will translate them to PQL queries and execute predictions.
        """)
        
        with gr.Tabs():
            
            # ===== TAB 1: Chat Agent =====
            with gr.Tab("💬 Chat Agent"):
                gr.Markdown("### Ask questions about insurance claims, fraud detection, and predictions")
                
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=400,
                    show_label=True
                )
                
                with gr.Row():
                    user_input = gr.Textbox(
                        label="Your Question",
                        placeholder="e.g., Is claim 12345 fraudulent? or How many claims will customer 100 file in next 30 days?",
                        lines=2,
                        scale=4
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)
                
                gr.Markdown("### Generated PQL Query")
                pql_code = gr.Code(
                    label="PQL Query",
                    language="sql",
                    lines=5,
                    interactive=True
                )
                
                with gr.Row():
                    anchor_time_input = gr.Textbox(
                        label="Anchor Time (optional)",
                        placeholder="YYYY-MM-DD, e.g., 2024-09-01",
                        scale=3
                    )
                    execute_btn = gr.Button("▶️ Execute Query", variant="primary", scale=1)
                
                execution_status = gr.Markdown("Status: Ready")
                
                gr.Markdown("### Query Results")
                result_table = gr.Dataframe(
                    label="Prediction Results",
                    interactive=False,
                    wrap=True
                )
                
                # Example queries
                gr.Markdown("### 💡 Example Queries")
                gr.Examples(
                    examples=[
                        ["Is claim 12345 fraudulent?"],
                        ["How many claims will customer 100 file in the next 30 days?"],
                        ["What is the total claim amount for customer 200 in next 90 days?"],
                        ["Will claim 500 be approved?"],
                        ["Predict fraud probability for all claims"],
                        ["Which customers are high risk in the next 60 days?"],
                    ],
                    inputs=user_input
                )
                
                # Event handlers
                def send_message(message, history):
                    new_history, pql, result, plot = agent.process_message(message, history)
                    return new_history, pql, None, "Status: PQL generated. Click Execute to run."
                
                def execute_pql(pql, anchor_time):
                    result, status, plot = agent.execute_query(pql, anchor_time)
                    return result, status
                
                send_btn.click(
                    fn=send_message,
                    inputs=[user_input, chatbot],
                    outputs=[chatbot, pql_code, result_table, execution_status]
                ).then(
                    lambda: "",
                    outputs=user_input
                )
                
                user_input.submit(
                    fn=send_message,
                    inputs=[user_input, chatbot],
                    outputs=[chatbot, pql_code, result_table, execution_status]
                ).then(
                    lambda: "",
                    outputs=user_input
                )
                
                execute_btn.click(
                    fn=execute_pql,
                    inputs=[pql_code, anchor_time_input],
                    outputs=[result_table, execution_status]
                )
            
            # ===== TAB 2: Data Explorer =====
            with gr.Tab("📊 Data Explorer"):
                gr.Markdown("### Graph Schema and Sample Data")
                
                # Display schema
                schema_json = gr.JSON(
                    label="Graph Schema",
                    value=graph_schema
                )
                
                gr.Markdown("### Sample Data")
                gr.Markdown("*Sample data would be displayed here from loaded tables*")
            
            # ===== TAB 3: Direct PQL Query =====
            with gr.Tab("⚡ Direct PQL Query"):
                gr.Markdown("### Execute PQL Queries Directly")
                gr.Markdown("For advanced users: write and execute PQL queries manually.")
                
                direct_pql_input = gr.Code(
                    label="PQL Query",
                    language="sql",
                    lines=10,
                    value="PREDICT claims.fraud_flag FOR EACH claims.claim_id"
                )
                
                with gr.Row():
                    validate_btn = gr.Button("✓ Validate", scale=1)
                    direct_execute_btn = gr.Button("▶️ Execute", variant="primary", scale=1)
                
                direct_status = gr.Markdown("Status: Ready")
                direct_result = gr.Dataframe(label="Results")
                
                def validate_pql(pql):
                    is_valid, msg = agent.translator.validate_pql(pql)
                    if is_valid:
                        return f"✅ **Valid PQL**: {msg}"
                    else:
                        return f"❌ **Invalid PQL**: {msg}"
                
                def execute_direct_pql(pql):
                    result, status, _ = agent.execute_query(pql)
                    return result, status
                
                validate_btn.click(
                    fn=validate_pql,
                    inputs=direct_pql_input,
                    outputs=direct_status
                )
                
                direct_execute_btn.click(
                    fn=execute_direct_pql,
                    inputs=direct_pql_input,
                    outputs=[direct_result, direct_status]
                )
                
                # PQL Reference
                gr.Markdown("""
                ### PQL Quick Reference
                
                **Basic Syntax**:
                - `PREDICT <target> FOR <entity>`
                - `PREDICT COUNT(table.*, start, end, unit) FOR EACH <entity>`
                - `PREDICT SUM/AVG/MIN/MAX(table.column, start, end, unit) FOR <entity>`
                
                **Examples**:
                - `PREDICT claims.fraud_flag FOR claims.claim_id=12345`
                - `PREDICT COUNT(claims.*, 0, 30, days) FOR customers.customer_id=100`
                - `PREDICT SUM(claims.claim_amount, 0, 90, days) FOR EACH customers.customer_id`
                """)
            
            # ===== TAB 4: Performance =====
            with gr.Tab("📈 Performance"):
                gr.Markdown("### Query Execution History")
                
                refresh_btn = gr.Button("🔄 Refresh History")
                history_table = gr.Dataframe(
                    label="Query History",
                    interactive=False
                )
                
                def refresh_history():
                    return agent.get_query_history()
                
                refresh_btn.click(
                    fn=refresh_history,
                    outputs=history_table
                )
            
            # ===== TAB 5: Settings =====
            with gr.Tab("⚙️ Settings"):
                gr.Markdown("### Application Settings")
                
                gr.Markdown(f"""
                **Environment Variables**:
                - `KUMO_API_KEY`: {'✅ Set' if os.getenv('KUMO_API_KEY') else '❌ Not Set'}
                - `OPENAI_API_KEY`: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not Set'}
                
                **Model Configuration**:
                - OpenAI Model: {agent.translator.model}
                - KumoRFM SDK: {agent.kumo_client.sdk_import_method}
                
                **Graph Statistics**:
                - Number of Tables: {len(graph_schema.get('tables', {}))}
                - Number of Relationships: {len(graph_schema.get('relationships', []))}
                """)
                
                gr.Markdown("""
                ### About
                
                **FraudAGENT** - KumoRFM Insurance Claims AI Agent
                
                This application combines:
                - **KumoRFM**: Relational Foundation Model for predictive analytics
                - **OpenAI GPT**: Natural language understanding and PQL translation
                - **Gradio**: Interactive web interface
                
                Built for insurance claims fraud detection, risk assessment, and predictive analytics.
                """)
        
        return app


def main():
    """
    Standalone test mode for Gradio interface.
    """
    print("KumoRFM Agent - Gradio Interface Test Mode")
    print("="*80)
    
    # Mock components for testing
    class MockKumoClient:
        sdk_import_method = "import kumoai.experimental.rfm as rfm"
        def execute_pql(self, query, anchor_time=None):
            return pd.DataFrame({
                "ENTITY": [1, 2, 3],
                "TARGET_PRED": [0.8, 0.3, 0.6],
                "CONFIDENCE": [0.9, 0.85, 0.88]
            })
    
    class MockTranslator:
        model = "gpt-4o-mini"
        def translate(self, query, context=None):
            return {
                "pql_query": "PREDICT claims.fraud_flag FOR claims.claim_id=12345",
                "query_type": "classification",
                "confidence": 0.9,
                "explanation": "Mock translation",
                "requires_clarification": False,
                "clarification_question": None,
                "suggested_entities": []
            }
        def validate_pql(self, query):
            return True, "Mock validation passed"
    
    mock_schema = {
        "tables": {
            "claims": {"name": "claims", "primary_key": "claim_id", "columns": {}},
            "customers": {"name": "customers", "primary_key": "customer_id", "columns": {}}
        },
        "relationships": []
    }
    
    agent = KumoConversationAgent(MockKumoClient(), MockTranslator(), mock_schema)
    app = create_gradio_interface(agent, mock_schema)
    
    print("\n✅ Gradio interface created successfully!")
    print("Launching in test mode...")
    
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == "__main__":
    main()

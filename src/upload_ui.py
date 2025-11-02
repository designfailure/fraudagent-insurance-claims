"""
Gradio Upload UI Component
Provides a user interface for uploading Excel files and converting them to Parquet.
"""

import gradio as gr
import pandas as pd
import os
from typing import Tuple, Dict, List
from .excel_converter import ExcelToParquetConverter


class DataUploadUI:
    """
    Gradio UI component for data upload and conversion.
    """
    
    def __init__(self):
        """Initialize the upload UI."""
        self.converter = None
        self.current_metadata = None
    
    def process_upload(self, excel_file) -> Tuple[str, str, str]:
        """
        Process uploaded Excel file.
        
        Args:
            excel_file: Uploaded file object from Gradio
            
        Returns:
            Tuple of (status_message, schema_display, relationship_display)
        """
        if excel_file is None:
            return "❌ No file uploaded", "", ""
        
        try:
            # Create converter
            self.converter = ExcelToParquetConverter(output_dir="uploaded_data")
            
            # Convert Excel to Parquet
            tables = self.converter.convert_excel_to_parquet(excel_file.name)
            
            # Analyze schema
            schema_info = self.converter.analyze_schema()
            
            # Infer relationships
            relationships = self.converter.infer_relationships()
            
            # Export metadata
            self.converter.export_metadata()
            
            # Validate conversion
            is_valid = self.converter.validate_conversion()
            
            if not is_valid:
                return "⚠️ Conversion completed with warnings", "", ""
            
            # Get summary
            summary = self.converter.get_conversion_summary()
            
            # Format status message
            status_msg = f"""✅ **Conversion Successful!**

**Summary:**
- **Tables Converted:** {summary['num_tables']}
- **Total Rows:** {summary['total_rows']:,}
- **Total Columns:** {summary['total_columns']}
- **Relationships Inferred:** {summary['num_relationships']}
- **Output Directory:** `{summary['output_directory']}`

**Tables:** {', '.join(summary['table_names'])}
"""
            
            # Format schema display
            schema_display = self._format_schema_display(schema_info)
            
            # Format relationship display
            relationship_display = self._format_relationship_display(relationships)
            
            return status_msg, schema_display, relationship_display
            
        except Exception as e:
            return f"❌ **Error during conversion:** {str(e)}", "", ""
    
    def _format_schema_display(self, schema_info: Dict) -> str:
        """Format schema information for display."""
        output = "## 📊 Schema Information\n\n"
        
        for table_name, schema in schema_info.items():
            output += f"### Table: `{table_name}`\n\n"
            output += f"- **Rows:** {schema['row_count']:,}\n"
            output += f"- **Columns:** {schema['column_count']}\n"
            
            if schema['primary_key']:
                output += f"- **Primary Key:** `{schema['primary_key']}`\n"
            
            if schema['foreign_keys']:
                output += f"- **Foreign Keys:** {', '.join(f'`{fk}`' for fk in schema['foreign_keys'])}\n"
            
            if schema['temporal_columns']:
                output += f"- **Temporal Columns:** {', '.join(f'`{tc}`' for tc in schema['temporal_columns'])}\n"
            
            output += "\n**Columns:**\n\n"
            output += "| Column | Type | Nulls | Unique |\n"
            output += "|--------|------|-------|--------|\n"
            
            for col_name, col_info in schema['columns'].items():
                null_pct = f"{col_info['null_percentage']:.1f}%"
                unique_pct = f"{col_info['unique_percentage']:.1f}%"
                output += f"| `{col_name}` | {col_info['dtype']} | {null_pct} | {unique_pct} |\n"
            
            output += "\n---\n\n"
        
        return output
    
    def _format_relationship_display(self, relationships: List[Dict]) -> str:
        """Format relationship information for display."""
        if not relationships:
            return "## 🔗 Relationships\n\n⚠️ No relationships automatically inferred.\n\nYou may need to manually define relationships in the configuration."
        
        output = "## 🔗 Inferred Relationships\n\n"
        output += "| Source Table | Foreign Key | Target Table | Target Key |\n"
        output += "|--------------|-------------|--------------|------------|\n"
        
        for rel in relationships:
            output += f"| `{rel['src_table']}` | `{rel['fkey']}` | `{rel['dst_table']}` | `{rel['dst_key']}` |\n"
        
        return output
    
    def create_upload_tab(self) -> gr.Tab:
        """
        Create the Gradio upload tab.
        
        Returns:
            Gradio Tab component
        """
        with gr.Tab("📤 Data Upload") as tab:
            gr.Markdown("""
            # 📤 Upload Your Insurance Data
            
            Upload an Excel file (.xlsx) containing your insurance claims data. The system will:
            1. Convert all sheets to Parquet format
            2. Analyze the schema and detect primary/foreign keys
            3. Infer relationships between tables
            4. Prepare the data for KumoRFM graph creation
            
            **Supported Format:** Excel (.xlsx) with multiple sheets
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    file_upload = gr.File(
                        label="Upload Excel File",
                        file_types=[".xlsx"],
                        type="filepath"
                    )
                    
                    upload_btn = gr.Button("🚀 Convert to Parquet", variant="primary", size="lg")
                    
                    status_output = gr.Markdown(label="Status")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 💡 Tips")
                    gr.Markdown("""
                    - Ensure your Excel file has clear column headers
                    - Include ID columns for primary and foreign keys
                    - Date columns should be in datetime format
                    - Each sheet will become a separate table
                    """)
            
            gr.Markdown("---")
            
            with gr.Row():
                with gr.Column():
                    schema_output = gr.Markdown(label="Schema Information")
                
                with gr.Column():
                    relationship_output = gr.Markdown(label="Relationships")
            
            # Connect upload button
            upload_btn.click(
                fn=self.process_upload,
                inputs=[file_upload],
                outputs=[status_output, schema_output, relationship_output]
            )
        
        return tab
    
    def get_uploaded_data_path(self) -> str:
        """
        Get the path to the uploaded data directory.
        
        Returns:
            Path to uploaded_data directory
        """
        return "uploaded_data" if os.path.exists("uploaded_data") else None
    
    def has_uploaded_data(self) -> bool:
        """
        Check if data has been uploaded.
        
        Returns:
            True if uploaded data exists
        """
        return os.path.exists("uploaded_data") and len(os.listdir("uploaded_data")) > 0


def create_upload_interface() -> gr.Blocks:
    """
    Create standalone upload interface for testing.
    
    Returns:
        Gradio Blocks interface
    """
    upload_ui = DataUploadUI()
    
    with gr.Blocks(title="Data Upload - FraudAGENT") as interface:
        gr.Markdown("# 🏥 FraudAGENT - Data Upload")
        upload_ui.create_upload_tab()
    
    return interface


if __name__ == "__main__":
    # Test the upload UI
    interface = create_upload_interface()
    interface.launch(server_name="0.0.0.0", server_port=7861)

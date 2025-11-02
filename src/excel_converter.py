"""
Excel to Parquet Converter Module
Converts Excel (.xlsx) files with multiple sheets to Parquet format
and prepares them for KumoRFM graph inference.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime


class ExcelToParquetConverter:
    """
    Converts Excel files to Parquet format with automatic schema detection
    and relationship inference for KumoRFM.
    """
    
    def __init__(self, output_dir: str = "uploaded_data"):
        """
        Initialize the converter.
        
        Args:
            output_dir: Directory to save converted Parquet files
        """
        self.output_dir = output_dir
        self.tables = {}
        self.schema_info = {}
        self.relationships = []
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def convert_excel_to_parquet(self, excel_file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Convert all sheets in an Excel file to Parquet format.
        
        Args:
            excel_file_path: Path to the Excel file
            
        Returns:
            Dictionary mapping table names to DataFrames
        """
        print("\n" + "="*80)
        print("EXCEL TO PARQUET CONVERSION")
        print("="*80)
        print(f"Source file: {excel_file_path}")
        
        # Load Excel file and get all sheet names
        excel_file = pd.ExcelFile(excel_file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"Found {len(sheet_names)} sheets: {sheet_names}")
        print()
        
        # Convert each sheet
        for sheet_name in sheet_names:
            print(f"Processing sheet: {sheet_name}")
            
            # Read sheet into DataFrame
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Clean table name (remove _fact suffix if present, make lowercase)
            table_name = sheet_name.replace('_fact', '').lower()
            
            # Store DataFrame
            self.tables[table_name] = df
            
            # Save as Parquet
            parquet_path = os.path.join(self.output_dir, f"{table_name}.parquet")
            df.to_parquet(parquet_path, index=False)
            
            print(f"  ✓ Converted to: {parquet_path}")
            print(f"  ✓ Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        print(f"\n✅ Successfully converted {len(self.tables)} sheets to Parquet")
        return self.tables
    
    def analyze_schema(self) -> Dict:
        """
        Analyze schema of all tables and detect primary keys, foreign keys,
        and temporal columns.
        
        Returns:
            Schema information dictionary
        """
        print("\n" + "="*80)
        print("SCHEMA ANALYSIS")
        print("="*80)
        
        for table_name, df in self.tables.items():
            print(f"\n📊 Table: {table_name}")
            print("-" * 80)
            
            schema = {
                'name': table_name,
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': {},
                'primary_key': None,
                'foreign_keys': [],
                'temporal_columns': []
            }
            
            # Analyze each column
            for col in df.columns:
                col_info = {
                    'dtype': str(df[col].dtype),
                    'null_count': int(df[col].isnull().sum()),
                    'null_percentage': float(df[col].isnull().sum() / len(df) * 100),
                    'unique_count': int(df[col].nunique()),
                    'unique_percentage': float(df[col].nunique() / len(df) * 100)
                }
                
                # Detect primary key (unique identifier)
                if col_info['unique_count'] == len(df) and col_info['null_count'] == 0:
                    if 'id' in col.lower() or 'number' in col.lower():
                        schema['primary_key'] = col
                        col_info['is_primary_key'] = True
                        print(f"  🔑 Primary Key detected: {col}")
                
                # Detect foreign keys (references to other tables)
                if 'id' in col.lower() and col != schema['primary_key']:
                    # Check if this might reference another table
                    potential_ref_table = col.replace('_ID', '').replace('_id', '').lower()
                    if potential_ref_table in self.tables or potential_ref_table.replace('customer', 'customers') in self.tables:
                        schema['foreign_keys'].append(col)
                        col_info['is_foreign_key'] = True
                        print(f"  🔗 Foreign Key detected: {col}")
                
                # Detect temporal columns
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    schema['temporal_columns'].append(col)
                    col_info['is_temporal'] = True
                    print(f"  📅 Temporal column detected: {col}")
                
                schema['columns'][col] = col_info
            
            # If no primary key detected, try to infer one
            if not schema['primary_key']:
                for col in df.columns:
                    if df[col].nunique() == len(df) and df[col].notnull().all():
                        schema['primary_key'] = col
                        print(f"  🔑 Inferred Primary Key: {col}")
                        break
            
            self.schema_info[table_name] = schema
        
        print("\n✅ Schema analysis complete")
        return self.schema_info
    
    def infer_relationships(self) -> List[Dict]:
        """
        Infer relationships between tables based on foreign keys.
        
        Returns:
            List of relationship dictionaries
        """
        print("\n" + "="*80)
        print("RELATIONSHIP INFERENCE")
        print("="*80)
        
        self.relationships = []
        
        for table_name, schema in self.schema_info.items():
            for fkey in schema['foreign_keys']:
                # Infer target table from foreign key name
                # e.g., customer_ID -> customer, policy_ID -> policy
                target_table = fkey.replace('_ID', '').replace('_id', '').lower()
                
                # Handle plural forms
                if target_table + 's' in self.schema_info:
                    target_table = target_table + 's'
                elif target_table.endswith('y'):
                    # e.g., policy -> policies
                    plural = target_table[:-1] + 'ies'
                    if plural in self.schema_info:
                        target_table = plural
                
                # Check if target table exists
                if target_table in self.schema_info:
                    relationship = {
                        'src_table': table_name,
                        'fkey': fkey,
                        'dst_table': target_table,
                        'dst_key': self.schema_info[target_table]['primary_key']
                    }
                    self.relationships.append(relationship)
                    print(f"  🔗 {table_name}.{fkey} → {target_table}.{relationship['dst_key']}")
        
        if not self.relationships:
            print("  ⚠️  No relationships automatically inferred")
            print("  💡 You may need to manually define relationships in the UI")
        else:
            print(f"\n✅ Inferred {len(self.relationships)} relationships")
        
        return self.relationships
    
    def export_metadata(self, output_file: str = "upload_metadata.json") -> str:
        """
        Export schema and relationship metadata to JSON.
        
        Args:
            output_file: Output JSON file path
            
        Returns:
            Path to the exported file
        """
        metadata = {
            'conversion_timestamp': datetime.now().isoformat(),
            'tables': self.schema_info,
            'relationships': self.relationships,
            'output_directory': self.output_dir
        }
        
        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        print(f"\n✅ Metadata exported to: {output_path}")
        return output_path
    
    def get_conversion_summary(self) -> Dict:
        """
        Get a summary of the conversion process.
        
        Returns:
            Summary dictionary
        """
        summary = {
            'num_tables': len(self.tables),
            'table_names': list(self.tables.keys()),
            'total_rows': sum(len(df) for df in self.tables.values()),
            'total_columns': sum(len(df.columns) for df in self.tables.values()),
            'num_relationships': len(self.relationships),
            'output_directory': self.output_dir
        }
        
        return summary
    
    def validate_conversion(self) -> bool:
        """
        Validate that all tables were converted successfully.
        
        Returns:
            True if validation passes, False otherwise
        """
        print("\n" + "="*80)
        print("VALIDATION")
        print("="*80)
        
        all_valid = True
        
        for table_name, df in self.tables.items():
            parquet_path = os.path.join(self.output_dir, f"{table_name}.parquet")
            
            if not os.path.exists(parquet_path):
                print(f"  ❌ Missing Parquet file: {parquet_path}")
                all_valid = False
                continue
            
            # Try to read back the Parquet file
            try:
                df_check = pd.read_parquet(parquet_path)
                if len(df_check) == len(df) and len(df_check.columns) == len(df.columns):
                    print(f"  ✓ {table_name}: Valid ({len(df)} rows, {len(df.columns)} columns)")
                else:
                    print(f"  ❌ {table_name}: Shape mismatch")
                    all_valid = False
            except Exception as e:
                print(f"  ❌ {table_name}: Error reading Parquet - {e}")
                all_valid = False
        
        if all_valid:
            print("\n✅ All tables validated successfully")
        else:
            print("\n❌ Validation failed for some tables")
        
        return all_valid


def main():
    """
    Main function for testing the converter.
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python excel_converter.py <excel_file_path>")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    if not os.path.exists(excel_file):
        print(f"Error: File not found: {excel_file}")
        sys.exit(1)
    
    # Create converter
    converter = ExcelToParquetConverter(output_dir="uploaded_data")
    
    # Convert Excel to Parquet
    tables = converter.convert_excel_to_parquet(excel_file)
    
    # Analyze schema
    schema_info = converter.analyze_schema()
    
    # Infer relationships
    relationships = converter.infer_relationships()
    
    # Export metadata
    converter.export_metadata()
    
    # Validate conversion
    converter.validate_conversion()
    
    # Print summary
    summary = converter.get_conversion_summary()
    print("\n" + "="*80)
    print("CONVERSION SUMMARY")
    print("="*80)
    print(f"Tables converted: {summary['num_tables']}")
    print(f"Table names: {', '.join(summary['table_names'])}")
    print(f"Total rows: {summary['total_rows']:,}")
    print(f"Total columns: {summary['total_columns']}")
    print(f"Relationships inferred: {summary['num_relationships']}")
    print(f"Output directory: {summary['output_directory']}")
    print("="*80)


if __name__ == "__main__":
    main()

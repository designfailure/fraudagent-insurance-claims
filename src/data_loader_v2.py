"""
Insurance Data Loader Module (Version 2 - with Upload Support)
Loads and profiles insurance claims data from Parquet files or uploaded directory.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List
import json


class InsuranceDataLoader:
    """
    Loads and profiles insurance data from Parquet files.
    Supports both single file and multi-file directory structures.
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to Parquet file or directory containing Parquet files
        """
        self.data_path = data_path
        self.tables = {}
        self.schema_info = {}
        
        # Determine if path is file or directory
        if os.path.isfile(data_path):
            self.mode = "single_file"
        elif os.path.isdir(data_path):
            self.mode = "directory"
        else:
            raise ValueError(f"Invalid data path: {data_path}")
    
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load data from Parquet file(s).
        
        Returns:
            Dictionary mapping table names to DataFrames
        """
        print(f"\nLoading data from: {self.data_path}")
        print(f"Mode: {self.mode}")
        
        if self.mode == "single_file":
            # Load single Parquet file
            df = pd.read_parquet(self.data_path)
            table_name = Path(self.data_path).stem
            self.tables[table_name] = df
            print(f"✓ Loaded table '{table_name}': {df.shape[0]} rows × {df.shape[1]} columns")
        
        elif self.mode == "directory":
            # Load all Parquet files from directory
            parquet_files = list(Path(self.data_path).glob("*.parquet"))
            
            if not parquet_files:
                raise ValueError(f"No Parquet files found in: {self.data_path}")
            
            print(f"Found {len(parquet_files)} Parquet files")
            
            for file_path in sorted(parquet_files):
                table_name = file_path.stem
                df = pd.read_parquet(file_path)
                self.tables[table_name] = df
                print(f"✓ Loaded table '{table_name}': {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Check for metadata file
            metadata_path = Path(self.data_path) / "upload_metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    print(f"✓ Found metadata file with {len(metadata.get('relationships', []))} relationships")
                    self.metadata = metadata
        
        print(f"\n✅ Loaded {len(self.tables)} table(s)")
        return self.tables
    
    def profile_data(self) -> Dict:
        """
        Profile the loaded data and generate schema information.
        
        Returns:
            Dictionary containing schema information for all tables
        """
        print("\n" + "="*80)
        print("DATA PROFILING")
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
                'temporal_columns': []
            }
            
            # Analyze columns
            for col in df.columns:
                col_info = {
                    'dtype': str(df[col].dtype),
                    'null_count': int(df[col].isnull().sum()),
                    'unique_count': int(df[col].nunique()),
                    'sample_values': df[col].dropna().head(3).tolist()
                }
                
                # Detect primary key
                if df[col].nunique() == len(df) and df[col].notnull().all():
                    if 'id' in col.lower() or 'number' in col.lower():
                        schema['primary_key'] = col
                
                # Detect temporal columns
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    schema['temporal_columns'].append(col)
                
                schema['columns'][col] = col_info
            
            print(f"  Rows: {schema['row_count']:,}")
            print(f"  Columns: {schema['column_count']}")
            if schema['primary_key']:
                print(f"  Primary Key: {schema['primary_key']}")
            if schema['temporal_columns']:
                print(f"  Temporal Columns: {', '.join(schema['temporal_columns'])}")
            
            self.schema_info[table_name] = schema
        
        print("\n✅ Data profiling complete")
        return self.schema_info
    
    def validate_temporal_columns(self):
        """Validate temporal columns in the dataset."""
        print("\n" + "="*80)
        print("TEMPORAL VALIDATION")
        print("="*80)
        
        for table_name, schema in self.schema_info.items():
            if schema['temporal_columns']:
                print(f"\n📅 Table: {table_name}")
                for col in schema['temporal_columns']:
                    df = self.tables[table_name]
                    min_date = df[col].min()
                    max_date = df[col].max()
                    print(f"  {col}: {min_date} to {max_date}")
    
    def check_duplicates(self):
        """Check for duplicate records in tables."""
        print("\n" + "="*80)
        print("DUPLICATE CHECK")
        print("="*80)
        
        for table_name, df in self.tables.items():
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                print(f"⚠️  {table_name}: {duplicates} duplicate rows found")
            else:
                print(f"✓ {table_name}: No duplicates")
    
    def get_table_names(self) -> List[str]:
        """Get list of loaded table names."""
        return list(self.tables.keys())
    
    def get_table(self, table_name: str) -> pd.DataFrame:
        """Get a specific table by name."""
        return self.tables.get(table_name)
    
    def export_schema(self, output_file: str = "data_schema_summary.json"):
        """Export schema information to JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.schema_info, f, indent=2, default=str)
        print(f"\n✅ Schema exported to: {output_file}")

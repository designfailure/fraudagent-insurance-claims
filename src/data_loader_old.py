"""
Data Loader Module
Loads and profiles insurance claims data from Parquet files.
"""

import os
import json
import pandas as pd
from typing import Dict, List, Tuple, Any
from pathlib import Path


class InsuranceDataLoader:
    """
    Loads insurance claims data from Parquet format and performs profiling.
    Supports multi-sheet/multi-table parquet files.
    """
    
    def __init__(self, data_path: str):
        """
        Initialize data loader.
        
        Args:
            data_path: Path to parquet file or directory containing parquet files
        """
        self.data_path = Path(data_path)
        self.tables: Dict[str, pd.DataFrame] = {}
        self.schema_info: Dict[str, Any] = {}
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load data from parquet file(s).
        
        Returns:
            Dictionary mapping table names to DataFrames
        """
        print(f"Loading data from: {self.data_path}")
        
        if self.data_path.is_file():
            # Single parquet file
            table_name = self.data_path.stem
            df = pd.read_parquet(self.data_path)
            self.tables[table_name] = df
            print(f"✓ Loaded table '{table_name}': {df.shape[0]} rows, {df.shape[1]} columns")
            
        elif self.data_path.is_dir():
            # Directory containing multiple parquet files
            parquet_files = list(self.data_path.glob("*.parquet")) + list(self.data_path.glob("*.pq"))
            
            if not parquet_files:
                raise FileNotFoundError(f"No parquet files found in {self.data_path}")
            
            for file_path in parquet_files:
                table_name = file_path.stem
                df = pd.read_parquet(file_path)
                self.tables[table_name] = df
                print(f"✓ Loaded table '{table_name}': {df.shape[0]} rows, {df.shape[1]} columns")
        else:
            raise FileNotFoundError(f"Data path not found: {self.data_path}")
        
        return self.tables
    
    def profile_data(self) -> Dict[str, Any]:
        """
        Profile loaded data: schema, dtypes, nulls, unique values, likely PKs, datetime columns.
        
        Returns:
            Dictionary containing profiling information
        """
        if not self.tables:
            raise ValueError("No data loaded. Call load_data() first.")
        
        print("\n" + "="*80)
        print("DATA PROFILING SUMMARY")
        print("="*80)
        
        self.schema_info = {
            "num_tables": len(self.tables),
            "tables": {}
        }
        
        for table_name, df in self.tables.items():
            print(f"\n📊 Table: {table_name}")
            print("-" * 80)
            
            # Basic info
            num_rows, num_cols = df.shape
            print(f"Shape: {num_rows} rows × {num_cols} columns")
            
            # Column analysis
            column_info = {}
            likely_pks = []
            likely_datetime_cols = []
            
            for col in df.columns:
                dtype = str(df[col].dtype)
                null_count = df[col].isnull().sum()
                null_pct = (null_count / num_rows) * 100 if num_rows > 0 else 0
                unique_count = df[col].nunique()
                unique_pct = (unique_count / num_rows) * 100 if num_rows > 0 else 0
                
                column_info[col] = {
                    "dtype": dtype,
                    "null_count": int(null_count),
                    "null_percentage": round(null_pct, 2),
                    "unique_count": int(unique_count),
                    "unique_percentage": round(unique_pct, 2)
                }
                
                # Detect likely primary keys (high uniqueness, low nulls)
                if unique_pct > 95 and null_pct < 5:
                    likely_pks.append(col)
                
                # Detect datetime columns
                if 'date' in col.lower() or 'time' in col.lower() or dtype.startswith('datetime'):
                    likely_datetime_cols.append(col)
            
            # Print column details
            print(f"\nColumns ({num_cols}):")
            for col, info in column_info.items():
                marker = ""
                if col in likely_pks:
                    marker += " [LIKELY PK]"
                if col in likely_datetime_cols:
                    marker += " [DATETIME]"
                print(f"  • {col}: {info['dtype']} | Nulls: {info['null_count']} ({info['null_percentage']}%) | "
                      f"Unique: {info['unique_count']} ({info['unique_percentage']}%){marker}")
            
            # Sample rows
            print(f"\nSample rows (first 3):")
            print(df.head(3).to_string())
            
            # Store schema info
            self.schema_info["tables"][table_name] = {
                "num_rows": num_rows,
                "num_columns": num_cols,
                "columns": column_info,
                "likely_primary_keys": likely_pks,
                "likely_datetime_columns": likely_datetime_cols
            }
        
        print("\n" + "="*80)
        return self.schema_info
    
    def validate_temporal_columns(self) -> None:
        """
        Validate and parse datetime columns.
        """
        print("\n" + "="*80)
        print("TEMPORAL COLUMN VALIDATION")
        print("="*80)
        
        for table_name, df in self.tables.items():
            table_schema = self.schema_info["tables"][table_name]
            datetime_cols = table_schema.get("likely_datetime_columns", [])
            
            if not datetime_cols:
                print(f"\n⚠ Table '{table_name}': No datetime columns detected")
                continue
            
            print(f"\n📅 Table: {table_name}")
            for col in datetime_cols:
                try:
                    # Try to parse as datetime
                    if not pd.api.types.is_datetime64_any_dtype(df[col]):
                        self.tables[table_name][col] = pd.to_datetime(df[col], errors='coerce')
                    
                    min_date = df[col].min()
                    max_date = df[col].max()
                    print(f"  ✓ {col}: {min_date} to {max_date}")
                except Exception as e:
                    print(f"  ✗ {col}: Failed to parse - {e}")
    
    def check_duplicates(self) -> None:
        """
        Check for duplicate rows based on likely primary keys.
        """
        print("\n" + "="*80)
        print("DUPLICATE CHECK")
        print("="*80)
        
        for table_name, df in self.tables.items():
            table_schema = self.schema_info["tables"][table_name]
            likely_pks = table_schema.get("likely_primary_keys", [])
            
            if not likely_pks:
                print(f"\n⚠ Table '{table_name}': No likely primary key detected, checking full row duplicates")
                dup_count = df.duplicated().sum()
            else:
                pk = likely_pks[0]  # Use first likely PK
                print(f"\n🔑 Table '{table_name}': Checking duplicates on '{pk}'")
                dup_count = df.duplicated(subset=[pk]).sum()
            
            if dup_count > 0:
                print(f"  ⚠ Found {dup_count} duplicate(s)")
            else:
                print(f"  ✓ No duplicates found")
    
    def export_schema_summary(self, output_path: str = "data_schema_summary.json") -> str:
        """
        Export schema summary to JSON file.
        
        Args:
            output_path: Path to output JSON file
            
        Returns:
            Path to exported file
        """
        if not self.schema_info:
            raise ValueError("No schema info available. Call profile_data() first.")
        
        output_file = Path(output_path)
        with open(output_file, 'w') as f:
            json.dump(self.schema_info, f, indent=2, default=str)
        
        print(f"\n✓ Schema summary exported to: {output_file}")
        return str(output_file)
    
    def get_dataframes(self) -> Dict[str, pd.DataFrame]:
        """
        Get loaded DataFrames.
        
        Returns:
            Dictionary mapping table names to DataFrames
        """
        return self.tables
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Get schema information.
        
        Returns:
            Schema information dictionary
        """
        return self.schema_info


def main():
    """
    Example usage and testing.
    """
    # Example: Load from environment variable or default path
    data_path = os.getenv("INSURANCE_DATA_PATH", "data/insurance_claims_data.parquet")
    
    if not os.path.exists(data_path):
        print(f"⚠ Data file not found: {data_path}")
        print("Please set INSURANCE_DATA_PATH environment variable or place data in data/ directory")
        return
    
    loader = InsuranceDataLoader(data_path)
    
    # Load data
    tables = loader.load_data()
    
    # Profile data
    schema_info = loader.profile_data()
    
    # Validate temporal columns
    loader.validate_temporal_columns()
    
    # Check duplicates
    loader.check_duplicates()
    
    # Export schema
    loader.export_schema_summary()
    
    print("\n✅ Data loading and profiling complete!")


if __name__ == "__main__":
    main()

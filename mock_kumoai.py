"""
Mock KumoRFM Module for Demonstration
Simulates KumoRFM SDK functionality without requiring actual API access.
"""

import pandas as pd
import random
from typing import Dict, Any, Optional


class MockLocalTable:
    """Mock LocalTable class."""
    
    def __init__(self, df: pd.DataFrame, name: str, primary_key: str = None, time_column: str = None):
        self.df = df
        self.name = name
        self.primary_key = primary_key
        self.time_column = time_column
        self.edges = []
        
    def infer_metadata(self):
        """Auto-infer metadata."""
        # Infer primary key
        for col in self.df.columns:
            if 'id' in col.lower() and self.df[col].nunique() == len(self.df):
                self.primary_key = col
                print(f"Detected primary key '{col}' in table '{self.name}'")
                break
        
        # Infer time column
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.time_column = col
                print(f"Detected time column '{col}' in table '{self.name}'")
                break
        
        return self
    
    def __getitem__(self, col_name):
        """Get column object."""
        return MockColumn(col_name)
    
    def print_metadata(self):
        """Print table metadata."""
        print(f"Table: {self.name}")
        print(f"  Primary Key: {self.primary_key}")
        print(f"  Time Column: {self.time_column}")
        print(f"  Columns: {list(self.df.columns)}")


class MockColumn:
    """Mock column object."""
    
    def __init__(self, name: str):
        self.name = name
        self.stype = "unknown"


class MockLocalGraph:
    """Mock LocalGraph class."""
    
    def __init__(self, tables: list):
        self.tables = tables
        self.edges = []
    
    def link(self, src_table: str, fkey: str, dst_table: str):
        """Add link between tables."""
        self.edges.append({
            'src_table': src_table,
            'fkey': fkey,
            'dst_table': dst_table
        })
    
    def print_metadata(self):
        """Print graph metadata."""
        print(f"Graph with {len(self.tables)} tables")
    
    def print_links(self):
        """Print graph links."""
        print(f"Links: {len(self.edges)}")
        for edge in self.edges:
            print(f"  {edge['src_table']}.{edge['fkey']} → {edge['dst_table']}")


class MockKumoRFM:
    """Mock KumoRFM model class."""
    
    def __init__(self, graph: MockLocalGraph):
        self.graph = graph
    
    def predict(self, query: str, anchor_time: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        """Mock prediction - returns simulated results."""
        
        # Parse query to determine result type
        if "fraud_flag" in query.lower():
            # Fraud prediction
            if "FOR EACH" in query.upper():
                # Multiple entities
                num_results = 10
                return pd.DataFrame({
                    'ENTITY': range(1, num_results + 1),
                    'ANCHOR_TIMESTAMP': [pd.Timestamp.now()] * num_results,
                    'TARGET_PRED': [random.choice([True, False]) for _ in range(num_results)],
                    'False_PROB': [random.uniform(0.3, 0.7) for _ in range(num_results)],
                    'True_PROB': [random.uniform(0.3, 0.7) for _ in range(num_results)]
                })
            else:
                # Single entity
                return pd.DataFrame({
                    'ENTITY': [1],
                    'ANCHOR_TIMESTAMP': [pd.Timestamp.now()],
                    'TARGET_PRED': [random.choice([True, False])],
                    'False_PROB': [random.uniform(0.3, 0.7)],
                    'True_PROB': [random.uniform(0.3, 0.7)]
                })
        
        elif "COUNT" in query.upper():
            # Count prediction
            if "FOR EACH" in query.upper():
                num_results = 10
                return pd.DataFrame({
                    'ENTITY': range(1, num_results + 1),
                    'ANCHOR_TIMESTAMP': [pd.Timestamp.now()] * num_results,
                    'TARGET_PRED': [random.randint(0, 10) for _ in range(num_results)]
                })
            else:
                return pd.DataFrame({
                    'ENTITY': [1],
                    'ANCHOR_TIMESTAMP': [pd.Timestamp.now()],
                    'TARGET_PRED': [random.randint(0, 10)]
                })
        
        elif "SUM" in query.upper() or "AVG" in query.upper():
            # Aggregation prediction
            if "FOR EACH" in query.upper():
                num_results = 10
                return pd.DataFrame({
                    'ENTITY': range(1, num_results + 1),
                    'ANCHOR_TIMESTAMP': [pd.Timestamp.now()] * num_results,
                    'TARGET_PRED': [random.uniform(1000, 50000) for _ in range(num_results)]
                })
            else:
                return pd.DataFrame({
                    'ENTITY': [1],
                    'ANCHOR_TIMESTAMP': [pd.Timestamp.now()],
                    'TARGET_PRED': [random.uniform(1000, 50000)]
                })
        
        else:
            # Generic prediction
            return pd.DataFrame({
                'ENTITY': [1],
                'ANCHOR_TIMESTAMP': [pd.Timestamp.now()],
                'TARGET_PRED': [random.uniform(0, 1)]
            })


def init(api_key: str):
    """Mock init function."""
    print(f"✓ Mock KumoRFM initialized (demo mode)")


# Create mock module structure
class experimental:
    class rfm:
        LocalTable = MockLocalTable
        LocalGraph = MockLocalGraph
        KumoRFM = MockKumoRFM
        init = staticmethod(init)


# Make it available as kumoai.experimental.rfm
import sys
sys.modules['kumoai'] = sys.modules[__name__]
sys.modules['kumoai.experimental'] = experimental
sys.modules['kumoai.experimental.rfm'] = experimental.rfm

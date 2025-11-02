"""
KumoRFM Setup Module
Handles KumoRFM client initialization, dataset import, and graph creation.
"""

import os
import sys
import pandas as pd
from typing import Dict, List, Optional, Any
from pathlib import Path


class KumoSetup:
    """
    Manages KumoRFM client setup, data import, and graph materialization.
    Attempts multiple SDK import patterns for compatibility.
    """
    
    def __init__(self):
        """Initialize KumoRFM setup manager."""
        self.rfm = None
        self.graph = None
        self.model = None
        self.sdk_import_method = None
        self._import_sdk()
    
    def _import_sdk(self):
        """
        Attempt to import KumoRFM SDK using various patterns.
        Tries common import variations and documents which succeeded.
        """
        import_attempts = [
            ("kumoai.experimental.rfm", "import kumoai.experimental.rfm as rfm"),
            ("kumo_rfm", "import kumo_rfm as rfm"),
            ("kumorfm", "import kumorfm as rfm"),
            ("kumoai.rfm", "from kumoai import rfm"),
        ]
        
        for module_name, import_statement in import_attempts:
            try:
                if module_name == "kumoai.experimental.rfm":
                    import kumoai.experimental.rfm as rfm
                elif module_name == "kumo_rfm":
                    import kumo_rfm as rfm
                elif module_name == "kumorfm":
                    import kumorfm as rfm
                elif module_name == "kumoai.rfm":
                    from kumoai import rfm
                
                self.rfm = rfm
                self.sdk_import_method = import_statement
                print(f"✓ Successfully imported KumoRFM SDK: {import_statement}")
                return
            except ImportError:
                continue
        
        # If all attempts fail
        raise ImportError(
            "Failed to import KumoRFM SDK. Tried the following:\n" +
            "\n".join([f"  - {stmt}" for _, stmt in import_attempts]) +
            "\n\nPlease install: pip install kumoai"
        )
    
    def authenticate(self) -> None:
        """
        Authenticate with KumoRFM using API key from environment variable.
        
        Raises:
            ValueError: If KUMO_API_KEY environment variable is not set
        """
        api_key = os.getenv("KUMO_API_KEY")
        
        if not api_key:
            raise ValueError(
                "KUMO_API_KEY environment variable not set.\n"
                "Please set it in your .env file or environment:\n"
                "  export KUMO_API_KEY='your-api-key-here'\n"
                "Get your API key at: https://kumorfm.ai/api-keys"
            )
        
        try:
            # Initialize client with API key
            self.rfm.init(api_key=api_key)
            print("✓ KumoRFM client authenticated successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with KumoRFM: {e}")
    
    def import_dataset(
        self, 
        tables: Dict[str, pd.DataFrame],
        auto_infer_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Import pandas DataFrames into KumoRFM as LocalTables.
        
        Args:
            tables: Dictionary mapping table names to pandas DataFrames
            auto_infer_metadata: Whether to automatically infer metadata (PKs, time columns, types)
        
        Returns:
            Dictionary mapping table names to LocalTable objects
        """
        print("\n" + "="*80)
        print("IMPORTING DATA TO KUMORFM")
        print("="*80)
        
        local_tables = {}
        
        for table_name, df in tables.items():
            print(f"\n📥 Importing table: {table_name}")
            
            try:
                # Create LocalTable
                # SDK method: rfm.LocalTable(df, name=table_name)
                local_table = self.rfm.LocalTable(df, name=table_name)
                
                if auto_infer_metadata:
                    # Auto-infer metadata (primary keys, time columns, semantic types)
                    local_table = local_table.infer_metadata()
                    print(f"  ✓ Metadata inferred for '{table_name}'")
                
                local_tables[table_name] = local_table
                print(f"  ✓ Table '{table_name}' imported successfully")
                
            except Exception as e:
                print(f"  ✗ Failed to import '{table_name}': {e}")
                raise
        
        print("\n✓ All tables imported to KumoRFM")
        return local_tables
    
    def create_graph(
        self,
        local_tables: Dict[str, Any],
        auto_infer_links: bool = True,
        manual_links: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """
        Create a LocalGraph from LocalTables and establish relationships.
        
        Args:
            local_tables: Dictionary of LocalTable objects
            auto_infer_links: Whether to automatically infer foreign key relationships
            manual_links: List of manual link specifications, each dict with keys:
                         'src_table', 'fkey', 'dst_table'
        
        Returns:
            LocalGraph object
        """
        print("\n" + "="*80)
        print("CREATING KUMORFM GRAPH")
        print("="*80)
        
        try:
            # Create graph from tables
            # SDK method: rfm.LocalGraph(tables=[...])
            table_list = list(local_tables.values())
            self.graph = self.rfm.LocalGraph(tables=table_list)
            print(f"✓ Graph created with {len(table_list)} tables")
            
            # Auto-infer links if requested
            if auto_infer_links:
                print("\n🔗 Auto-inferring relationships...")
                # The SDK may have an auto-link method; if not, we'll need manual linking
                # Attempt: graph.infer_links() or similar
                try:
                    if hasattr(self.graph, 'infer_links'):
                        self.graph.infer_links()
                        print("  ✓ Relationships auto-inferred")
                    else:
                        print("  ⚠ Auto-inference not available, use manual links")
                except Exception as e:
                    print(f"  ⚠ Auto-inference failed: {e}")
            
            # Add manual links
            if manual_links:
                print("\n🔗 Adding manual relationships...")
                for link in manual_links:
                    src_table = link['src_table']
                    fkey = link['fkey']
                    dst_table = link['dst_table']
                    
                    try:
                        # SDK method: graph.link(src_table=..., fkey=..., dst_table=...)
                        self.graph.link(src_table=src_table, fkey=fkey, dst_table=dst_table)
                        print(f"  ✓ Linked: {src_table}.{fkey} → {dst_table}")
                    except Exception as e:
                        print(f"  ✗ Failed to link {src_table}.{fkey} → {dst_table}: {e}")
            
            # Print graph metadata
            print("\n📊 Graph Metadata:")
            if hasattr(self.graph, 'print_metadata'):
                self.graph.print_metadata()
            
            if hasattr(self.graph, 'print_links'):
                print("\n🔗 Graph Links:")
                self.graph.print_links()
            
            return self.graph
            
        except Exception as e:
            raise RuntimeError(f"Failed to create graph: {e}")
    
    def materialize_graph(self) -> Any:
        """
        Materialize the graph and create KumoRFM model ready for predictions.
        
        Returns:
            KumoRFM model object
        """
        if self.graph is None:
            raise ValueError("Graph not created. Call create_graph() first.")
        
        print("\n" + "="*80)
        print("MATERIALIZING GRAPH")
        print("="*80)
        
        try:
            # SDK method: rfm.KumoRFM(graph)
            self.model = self.rfm.KumoRFM(self.graph)
            print("✓ Graph materialized, KumoRFM model ready for predictions")
            return self.model
            
        except Exception as e:
            raise RuntimeError(f"Failed to materialize graph: {e}")
    
    def get_graph_schema(self) -> Dict[str, Any]:
        """
        Extract graph schema information for PQL translation.
        
        Returns:
            Dictionary containing graph schema details (tables, columns, relationships)
        """
        if self.graph is None:
            raise ValueError("Graph not created. Call create_graph() first.")
        
        schema = {
            "tables": {},
            "relationships": []
        }
        
        # Extract table information
        for table in self.graph.tables:
            table_name = table.name
            schema["tables"][table_name] = {
                "name": table_name,
                "primary_key": getattr(table, 'primary_key', None),
                "time_column": getattr(table, 'time_column', None),
                "columns": {}
            }
            
            # Extract column information
            for col_name in table.df.columns:
                col_obj = table[col_name] if hasattr(table, '__getitem__') else None
                stype = getattr(col_obj, 'stype', 'unknown') if col_obj else 'unknown'
                
                schema["tables"][table_name]["columns"][col_name] = {
                    "name": col_name,
                    "dtype": str(table.df[col_name].dtype),
                    "stype": stype
                }
        
        # Extract relationships
        if hasattr(self.graph, 'edges'):
            for edge in self.graph.edges:
                schema["relationships"].append({
                    "src_table": edge.src_table,
                    "fkey": edge.fkey,
                    "dst_table": edge.dst_table
                })
        
        return schema
    
    def execute_pql(self, pql_query: str, anchor_time: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        """
        Execute a PQL query and return results.
        
        Args:
            pql_query: PQL query string
            anchor_time: Optional anchor timestamp for prediction
        
        Returns:
            DataFrame with prediction results
        """
        if self.model is None:
            raise ValueError("Model not materialized. Call materialize_graph() first.")
        
        try:
            # SDK method: model.predict(query, anchor_time=...)
            if anchor_time:
                result = self.model.predict(pql_query, anchor_time=anchor_time)
            else:
                result = self.model.predict(pql_query)
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to execute PQL query: {e}\nQuery: {pql_query}")


def main():
    """
    Example usage and testing.
    """
    print("KumoRFM Setup Module - Test Mode")
    print("="*80)
    
    # Initialize
    kumo = KumoSetup()
    
    # Authenticate
    try:
        kumo.authenticate()
    except ValueError as e:
        print(f"\n❌ {e}")
        return
    
    print("\n✅ KumoRFM setup module initialized successfully!")
    print(f"SDK imported via: {kumo.sdk_import_method}")


if __name__ == "__main__":
    main()

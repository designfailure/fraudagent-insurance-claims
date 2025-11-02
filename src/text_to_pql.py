"""
Text to PQL Translation Module
Converts natural language queries to KumoRFM PQL using OpenAI.
"""

import os
import json
import re
from typing import Dict, List, Optional, Any
from openai import OpenAI


class TextToPQLTranslator:
    """
    Translates natural language queries to KumoRFM Predictive Query Language (PQL).
    Uses OpenAI GPT models for intelligent translation.
    """
    
    def __init__(self, graph_schema: Dict[str, Any], model: str = "gpt-4o-mini"):
        """
        Initialize translator with graph schema.
        
        Args:
            graph_schema: Dictionary containing graph structure (tables, columns, relationships)
            model: OpenAI model to use (default: gpt-4o-mini, can also use gpt-4o)
        """
        self.graph_schema = graph_schema
        self.model = model
        self.client = None
        self.pql_knowledge_base = self._build_pql_knowledge_base()
        self._initialize_openai()
    
    def _initialize_openai(self):
        """
        Initialize OpenAI client using API key from environment.
        
        Raises:
            ValueError: If OPENAI_API_KEY environment variable is not set
        """
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set.\n"
                "Please set it in your .env file or environment:\n"
                "  export OPENAI_API_KEY='your-api-key-here'\n"
                "Get your API key at: https://platform.openai.com/api-keys"
            )
        
        self.client = OpenAI(api_key=api_key)
        print("✓ OpenAI client initialized successfully")
    
    def _build_pql_knowledge_base(self) -> str:
        """
        Build PQL knowledge base with insurance-specific examples.
        
        Returns:
            String containing PQL patterns and examples
        """
        knowledge_base = """
# PQL (Predictive Query Language) Knowledge Base

## Core PQL Syntax Patterns

1. **Basic Prediction**
   PREDICT <target> FOR <entity.primary_key>
   Example: PREDICT claims.fraud_flag FOR claims.claim_id=12345

2. **Temporal Count**
   PREDICT COUNT(table.*, start, end, unit) FOR EACH <entity.primary_key>
   Example: PREDICT COUNT(claims.*, 0, 30, days) FOR EACH customers.customer_id

3. **Temporal Aggregation**
   PREDICT AGG(table.column, start, end, unit) FOR <entity>
   AGG can be: SUM, AVG, MIN, MAX, COUNT
   Example: PREDICT SUM(claims.claim_amount, 0, 90, days) FOR customers.customer_id=100

4. **Classification/Binary Prediction**
   PREDICT COUNT(table.*, start, end, unit)=0 FOR <entity>
   Example: PREDICT COUNT(claims.*, 0, 180, days)=0 FOR customers.customer_id IN (1,2,3)

5. **Recommendation/Ranking**
   PREDICT LIST_DISTINCT(table.column, start, end, unit) RANK TOP N FOR <entity>
   Example: PREDICT LIST_DISTINCT(claims.claim_type, 0, 30, days) RANK TOP 5 FOR customers.customer_id=200

6. **Attribute Inference**
   PREDICT table.column FOR <entity>
   Example: PREDICT customers.age FOR customers.customer_id=50

## Time Units
- days
- hours
- months
- years

## Insurance Domain Examples

### Fraud Detection
1. "Is claim 12345 fraudulent?"
   → PREDICT claims.fraud_flag FOR claims.claim_id=12345

2. "Which claims are likely fraud?"
   → PREDICT claims.fraud_flag FOR EACH claims.claim_id

3. "Predict fraud probability for customer 100"
   → PREDICT COUNT(claims.fraud_flag=1, 0, 90, days) FOR customers.customer_id=100

### Claim Amount Prediction
4. "What is the expected claim amount for claim 500?"
   → PREDICT claims.claim_amount FOR claims.claim_id=500

5. "Total claim amount for customer 200 in next 30 days"
   → PREDICT SUM(claims.claim_amount, 0, 30, days) FOR customers.customer_id=200

6. "Average claim amount for policy 300 in next quarter"
   → PREDICT AVG(claims.claim_amount, 0, 90, days) FOR policies.policy_id=300

### Claim Frequency
7. "How many claims will customer 150 file in next 60 days?"
   → PREDICT COUNT(claims.*, 0, 60, days) FOR customers.customer_id=150

8. "Will customer 250 file zero claims in next 6 months?"
   → PREDICT COUNT(claims.*, 0, 180, days)=0 FOR customers.customer_id=250

### Approval Prediction
9. "Will claim 700 be approved?"
   → PREDICT claims.approval_status FOR claims.claim_id=700

10. "Approval probability for pending claims"
    → PREDICT claims.approval_status FOR EACH claims.claim_id WHERE claims.status='Pending'

### Customer Churn/Retention
11. "Will customer 400 renew policy in next 30 days?"
    → PREDICT COUNT(policies.*, 0, 30, days) > 0 FOR customers.customer_id=400

12. "Customers likely to cancel in next quarter"
    → PREDICT COUNT(policies.canceled_flag=1, 0, 90, days) FOR EACH customers.customer_id

### Risk Assessment
13. "Risk score for policy 600"
    → PREDICT policies.risk_score FOR policies.policy_id=600

14. "High-risk customers in next 60 days"
    → PREDICT SUM(claims.claim_amount, 0, 60, days) > 10000 FOR EACH customers.customer_id

### Recommendations
15. "Top 5 claim types for customer 500"
    → PREDICT LIST_DISTINCT(claims.claim_type, 0, 90, days) RANK TOP 5 FOR customers.customer_id=500

## Important Notes
- Entity must have a primary key defined in the graph
- Time columns enable temporal predictions
- Foreign keys establish relationships between tables
- Aggregations work on temporal windows (start, end, unit)
"""
        return knowledge_base
    
    def _create_system_prompt(self) -> str:
        """
        Create system prompt for OpenAI with strict JSON output instructions.
        
        Returns:
            System prompt string
        """
        schema_summary = json.dumps(self.graph_schema, indent=2)
        
        system_prompt = f"""You are an expert PQL (Predictive Query Language) translator for KumoRFM insurance claims analysis.

Your task is to convert natural language queries into valid PQL queries based on the provided graph schema.

## Graph Schema
{schema_summary}

## PQL Knowledge Base
{self.pql_knowledge_base}

## Output Format
You MUST return ONLY a valid JSON object with the following structure:
{{
  "pql_query": "the generated PQL query string",
  "query_type": "classification|regression|recommendation|temporal_aggregation|attribute_inference",
  "confidence": 0.0-1.0,
  "explanation": "brief explanation of the query logic",
  "requires_clarification": true|false,
  "clarification_question": "question to ask user if clarification needed, otherwise null",
  "suggested_entities": ["list of entity IDs if applicable, otherwise empty"]
}}

## Rules
1. Return ONLY parseable JSON, no markdown, no code blocks, no extra text
2. Use exact table and column names from the schema
3. Ensure entity has a primary key defined
4. Use appropriate time units (days, hours, months, years)
5. If query is ambiguous, set requires_clarification=true and provide clarification_question
6. Validate that referenced columns exist in the schema
7. For fraud detection, use fraud_flag or similar fraud indicator columns
8. For temporal queries, use COUNT, SUM, AVG, MIN, MAX with time windows
9. Confidence should reflect certainty of translation (0.0 = uncertain, 1.0 = certain)

## Examples of Valid JSON Responses

Example 1 - Clear query:
{{
  "pql_query": "PREDICT claims.fraud_flag FOR claims.claim_id=12345",
  "query_type": "classification",
  "confidence": 0.95,
  "explanation": "Predicting fraud flag for specific claim ID 12345",
  "requires_clarification": false,
  "clarification_question": null,
  "suggested_entities": ["12345"]
}}

Example 2 - Needs clarification:
{{
  "pql_query": null,
  "query_type": "unknown",
  "confidence": 0.3,
  "explanation": "Query is ambiguous - unclear which entity to predict for",
  "requires_clarification": true,
  "clarification_question": "Which customer ID or claim ID would you like to analyze?",
  "suggested_entities": []
}}

Now translate user queries following these rules strictly.
"""
        return system_prompt
    
    def translate(
        self, 
        user_query: str, 
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Translate natural language query to PQL.
        
        Args:
            user_query: Natural language query from user
            conversation_context: Optional conversation history for context
        
        Returns:
            Dictionary with PQL query and metadata
        """
        print(f"\n🔄 Translating query: '{user_query}'")
        
        # Build messages
        messages = [
            {"role": "system", "content": self._create_system_prompt()}
        ]
        
        # Add conversation context if provided
        if conversation_context:
            messages.extend(conversation_context)
        
        # Add user query
        messages.append({"role": "user", "content": user_query})
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for more deterministic output
                max_tokens=500
            )
            
            # Extract response
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks if present
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    # Fallback: return error
                    result = {
                        "pql_query": None,
                        "query_type": "error",
                        "confidence": 0.0,
                        "explanation": f"Failed to parse response as JSON: {response_text[:200]}",
                        "requires_clarification": true,
                        "clarification_question": "I couldn't process that query. Could you rephrase it?",
                        "suggested_entities": []
                    }
            
            # Validate PQL if generated
            if result.get("pql_query"):
                is_valid, validation_msg = self.validate_pql(result["pql_query"])
                if not is_valid:
                    result["confidence"] *= 0.5  # Reduce confidence
                    result["explanation"] += f" (Validation warning: {validation_msg})"
            
            print(f"✓ Translation complete (confidence: {result.get('confidence', 0):.2f})")
            return result
            
        except Exception as e:
            print(f"✗ Translation failed: {e}")
            return {
                "pql_query": None,
                "query_type": "error",
                "confidence": 0.0,
                "explanation": f"Translation error: {str(e)}",
                "requires_clarification": True,
                "clarification_question": "I encountered an error. Could you rephrase your query?",
                "suggested_entities": []
            }
    
    def validate_pql(self, pql_query: str) -> tuple[bool, str]:
        """
        Perform basic syntactic validation of PQL query.
        
        Args:
            pql_query: PQL query string to validate
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not pql_query or not isinstance(pql_query, str):
            return False, "PQL query is empty or invalid type"
        
        # Check for PREDICT keyword
        if not pql_query.strip().upper().startswith("PREDICT"):
            return False, "PQL query must start with PREDICT"
        
        # Check for FOR keyword (required for entity specification)
        if " FOR " not in pql_query.upper():
            return False, "PQL query must contain FOR clause"
        
        # Check balanced parentheses
        if pql_query.count("(") != pql_query.count(")"):
            return False, "Unbalanced parentheses in PQL query"
        
        # Check for valid aggregation functions
        valid_aggs = ["COUNT", "SUM", "AVG", "MIN", "MAX", "LIST_DISTINCT"]
        has_agg = any(agg in pql_query.upper() for agg in valid_aggs)
        
        # Check for valid time units if temporal query
        valid_time_units = ["days", "hours", "months", "years"]
        has_time_unit = any(unit in pql_query.lower() for unit in valid_time_units)
        
        # If has aggregation, should have time unit (for temporal queries)
        if has_agg and "LIST_DISTINCT" not in pql_query.upper():
            if not has_time_unit:
                return False, "Temporal aggregation query should specify time unit (days/hours/months/years)"
        
        return True, "PQL query appears valid"
    
    def explain_pql(self, pql_query: str) -> str:
        """
        Generate human-readable explanation of a PQL query.
        
        Args:
            pql_query: PQL query to explain
        
        Returns:
            Human-readable explanation
        """
        try:
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that explains PQL queries in simple terms."
                },
                {
                    "role": "user",
                    "content": f"Explain this PQL query in simple terms:\n{pql_query}"
                }
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Could not generate explanation: {e}"


def main():
    """
    Example usage and testing.
    """
    print("Text-to-PQL Translator - Test Mode")
    print("="*80)
    
    # Mock graph schema for testing
    mock_schema = {
        "tables": {
            "customers": {
                "name": "customers",
                "primary_key": "customer_id",
                "columns": {"customer_id": {"stype": "ID"}, "age": {"stype": "numerical"}}
            },
            "claims": {
                "name": "claims",
                "primary_key": "claim_id",
                "time_column": "claim_date",
                "columns": {
                    "claim_id": {"stype": "ID"},
                    "customer_id": {"stype": "ID"},
                    "claim_amount": {"stype": "numerical"},
                    "fraud_flag": {"stype": "categorical"}
                }
            }
        },
        "relationships": [
            {"src_table": "claims", "fkey": "customer_id", "dst_table": "customers"}
        ]
    }
    
    # Initialize translator
    try:
        translator = TextToPQLTranslator(mock_schema)
    except ValueError as e:
        print(f"\n❌ {e}")
        return
    
    # Test translations
    test_queries = [
        "Is claim 12345 fraudulent?",
        "How many claims will customer 100 file in the next 30 days?",
        "What is the total claim amount for customer 200?"
    ]
    
    print("\n" + "="*80)
    print("TEST TRANSLATIONS")
    print("="*80)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = translator.translate(query)
        print(f"PQL: {result.get('pql_query')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Explanation: {result.get('explanation')}")
    
    print("\n✅ Text-to-PQL translator test complete!")


if __name__ == "__main__":
    main()

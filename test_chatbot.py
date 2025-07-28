"""
Quick test script for the Secure Local SQL Chatbot
"""

import requests
import json

def test_chatbot():
    base_url = "http://localhost:5000"
    
    print("Testing Secure Local SQL Chatbot...")
    print("="*50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        health_data = response.json()
        print(f"Health Status: {health_data.get('status', 'Unknown')}")
        print(f"Groq Connected: {health_data.get('groq_connected', False)}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    print()
    
    # Test 2: Schema endpoint
    try:
        response = requests.get(f"{base_url}/schema")
        schema_data = response.json()
        if schema_data.get('success'):
            tables = list(schema_data['schema'].keys())
            print(f"Database Tables: {', '.join(tables)}")
        else:
            print(f"Schema error: {schema_data.get('error')}")
    except Exception as e:
        print(f"Schema test failed: {e}")
    
    print()
    
    # Test 3: Sample query
    test_queries = [
        "Show all customers",
        "Count total orders",
        "List products in Electronics category"
    ]
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{base_url}/chat",
                json={'message': query},
                headers={'Content-Type': 'application/json'}
            )
            
            data = response.json()
            if data.get('success'):
                print(f"Query: '{query}' - SUCCESS")
                print(f"  Results: {data.get('result_count', 0)} rows")
                print(f"  SQL: {data.get('generated_sql', 'N/A')[:50]}...")
            else:
                print(f"Query: '{query}' - ERROR")
                print(f"  Error: {data.get('error')}")
            
        except Exception as e:
            print(f"Query test failed: {e}")
        
        print()
    
    print("="*50)
    print("Test completed! Check the results above.")
    print("Open http://localhost:5000 in your browser to use the chat interface.")

if __name__ == "__main__":
    test_chatbot()

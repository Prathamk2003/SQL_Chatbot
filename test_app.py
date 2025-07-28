#!/usr/bin/env python3
"""
Quick test of the application's database and fallback functionality
"""

import sys
import os

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our application components
from app import SecureLocalChatbot

def test_chatbot():
    print("=== Testing Secure Local SQL Chatbot ===")
    
    try:
        # Initialize chatbot
        chatbot = SecureLocalChatbot()
        print("✅ Chatbot initialized successfully")
        
        # Test database connection
        schema = chatbot.get_database_schema()
        print(f"✅ Database schema loaded: {len(schema)} tables")
        
        # Test basic query
        test_queries = [
            "Show all customers",
            "Count customers", 
            "List products"
        ]
        
        for query in test_queries:
            print(f"\n--- Testing: {query} ---")
            sql = chatbot.generate_sql_from_natural_language(query)
            
            if sql:
                print(f"Generated SQL: {sql}")
                success, results = chatbot.execute_query(sql)
                if success:
                    print(f"✅ Query executed successfully: {len(results)} results")
                else:
                    print(f"❌ Query failed: {results}")
            else:
                print("❌ Failed to generate SQL")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot()

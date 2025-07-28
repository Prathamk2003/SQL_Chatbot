#!/usr/bin/env python3
"""
Quick test to verify Groq API connection
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=== Groq API Test ===")
print(f"API Key loaded: {'Yes' if os.getenv('GROQ_API_KEY') else 'No'}")

api_key = os.getenv('GROQ_API_KEY')
if api_key:
    print(f"API Key preview: {api_key[:10]}...{api_key[-4:]}")
else:
    print("ERROR: No API key found!")
    exit(1)

try:
    from groq import Groq
    print("Groq package imported successfully")
    
    client = Groq(api_key=api_key)
    print("Groq client created successfully")
    
    # Simple test
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user", 
            "content": "Convert this to SQL: Show all customers. Just respond with: SELECT * FROM customers;"
        }],
        temperature=0.1,
        max_tokens=100
    )
    
    print("✅ Groq API call successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

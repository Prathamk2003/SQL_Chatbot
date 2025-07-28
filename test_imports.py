"""
Simple Groq API test without complex imports
"""

import sys
import subprocess

def test_imports():
    try:
        print("=== Testing Package Imports ===")
        
        # Test dotenv
        try:
            import dotenv
            print("✅ python-dotenv imported successfully")
        except ImportError:
            print("❌ python-dotenv not found")
        
        # Test groq
        try:
            import groq
            print("✅ groq package imported successfully")
        except ImportError:
            print("❌ groq package not found")
        
        # Test environment loading
        try:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:]}")
            else:
                print("❌ API Key not found in environment")
                
        except Exception as e:
            print(f"❌ Environment test failed: {e}")
            
    except Exception as e:
        print(f"❌ Import test failed: {e}")

if __name__ == "__main__":
    test_imports()

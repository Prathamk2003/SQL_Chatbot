"""
Secure Local SQL Chatbot - Main Application
A professional Flask web application for natural language SQL queries
"""

import os
import sqlite3
import logging
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secure-chatbot-key-2025')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/chatbot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Database configuration
DATABASE_PATH = 'database/chatbot.db'

class SecureChatbot:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with sample tables"""
        os.makedirs('database', exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                city TEXT,
                country TEXT,
                registration_date DATE,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2),
                order_date DATE,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                price DECIMAL(10,2),
                stock_quantity INTEGER,
                description TEXT,
                created_date DATE
            )
        ''')
        
        # Insert sample data if tables are empty
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] == 0:
            self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def insert_sample_data(self, cursor):
        """Insert sample data for testing"""
        # Sample customers
        customers_data = [
            ('John Smith', 'john.smith@email.com', '+1-555-0101', 'New York', 'USA', '2024-01-15', 'active'),
            ('Sarah Johnson', 'sarah.j@email.com', '+1-555-0102', 'Los Angeles', 'USA', '2024-02-20', 'active'),
            ('Michael Brown', 'mike.brown@email.com', '+1-555-0103', 'Chicago', 'USA', '2024-03-10', 'inactive'),
            ('Emily Davis', 'emily.davis@email.com', '+1-555-0104', 'Houston', 'USA', '2024-04-05', 'active'),
            ('David Wilson', 'david.w@email.com', '+1-555-0105', 'Phoenix', 'USA', '2024-05-12', 'active'),
        ]
        
        cursor.executemany(
            'INSERT INTO customers (name, email, phone, city, country, registration_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            customers_data
        )
        
        # Sample products
        products_data = [
            ('Laptop Pro', 'Electronics', 1299.99, 50, 'High-performance laptop', '2024-01-01'),
            ('Wireless Mouse', 'Electronics', 29.99, 200, 'Ergonomic wireless mouse', '2024-01-01'),
            ('Office Chair', 'Furniture', 299.99, 25, 'Comfortable office chair', '2024-01-01'),
            ('Smartphone', 'Electronics', 699.99, 100, 'Latest smartphone model', '2024-01-01'),
            ('Coffee Mug', 'Kitchen', 12.99, 500, 'Ceramic coffee mug', '2024-01-01'),
        ]
        
        cursor.executemany(
            'INSERT INTO products (name, category, price, stock_quantity, description, created_date) VALUES (?, ?, ?, ?, ?, ?)',
            products_data
        )
        
        # Sample orders
        orders_data = [
            (1, 'Laptop Pro', 1, 1299.99, '2024-06-01', 'completed'),
            (2, 'Wireless Mouse', 2, 29.99, '2024-06-05', 'completed'),
            (1, 'Office Chair', 1, 299.99, '2024-06-10', 'pending'),
            (4, 'Smartphone', 1, 699.99, '2024-06-15', 'shipped'),
            (5, 'Coffee Mug', 3, 12.99, '2024-06-20', 'completed'),
        ]
        
        cursor.executemany(
            'INSERT INTO orders (customer_id, product_name, quantity, price, order_date, status) VALUES (?, ?, ?, ?, ?, ?)',
            orders_data
        )
        
        logger.info("Sample data inserted successfully")
    
    def get_database_schema(self):
        """Get database schema information"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        schema_info = {}
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema_info[table_name] = {
                'columns': [
                    {
                        'name': col[1],
                        'type': col[2],
                        'not_null': bool(col[3]),
                        'primary_key': bool(col[5])
                    }
                    for col in columns
                ]
            }
        
        conn.close()
        return schema_info
    
    def validate_sql_query(self, query):
        """Validate SQL query for security"""
        query = query.strip().upper()
        
        # Only allow SELECT statements
        if not query.startswith('SELECT'):
            return False, "Only SELECT queries are allowed for security reasons"
        
        # Check for dangerous keywords
        dangerous_keywords = [
            'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE',
            'EXEC', 'EXECUTE', 'TRUNCATE', 'REPLACE', 'MERGE'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in query:
                return False, f"Query contains forbidden keyword: {keyword}"
        
        return True, "Query is valid"
    
    def execute_query(self, sql_query):
        """Execute SQL query safely"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            data = [dict(row) for row in results]
            
            conn.close()
            return True, data
        
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            return False, f"Database error: {str(e)}"
    
    def generate_sql_from_natural_language(self, user_question):
        """Generate SQL query from natural language using Groq"""
        try:
            schema_info = self.get_database_schema()
            schema_text = self.format_schema_for_prompt(schema_info)
            
            prompt = f"""
You are a SQL expert. Convert the following natural language question to a SQL SELECT query.

Database Schema:
{schema_text}

Important Rules:
1. ONLY generate SELECT statements
2. Use proper SQL syntax for SQLite
3. Return ONLY the SQL query, no explanations
4. Use appropriate JOINs when needed
5. Handle aggregations correctly

User Question: {user_question}

SQL Query:"""

            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the response
            sql_query = re.sub(r'^```sql\n?', '', sql_query)
            sql_query = re.sub(r'\n?```$', '', sql_query)
            sql_query = sql_query.strip()
            
            return sql_query
        
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return None
    
    def format_schema_for_prompt(self, schema_info):
        """Format schema information for AI prompt"""
        schema_text = ""
        for table_name, table_info in schema_info.items():
            schema_text += f"\nTable: {table_name}\n"
            for column in table_info['columns']:
                constraints = []
                if column['primary_key']:
                    constraints.append('PRIMARY KEY')
                if column['not_null']:
                    constraints.append('NOT NULL')
                
                constraint_text = f" ({', '.join(constraints)})" if constraints else ""
                schema_text += f"  - {column['name']}: {column['type']}{constraint_text}\n"
        
        return schema_text

# Initialize chatbot
chatbot = SecureChatbot()

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/schema')
def get_schema():
    """API endpoint to get database schema"""
    try:
        schema = chatbot.get_database_schema()
        return jsonify({
            'success': True,
            'schema': schema
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Process chat messages and return responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Generate SQL query from natural language
        sql_query = chatbot.generate_sql_from_natural_language(user_message)
        
        if not sql_query:
            return jsonify({
                'success': False,
                'error': 'Failed to generate SQL query. Please try rephrasing your question.'
            })
        
        # Validate SQL query
        is_valid, validation_message = chatbot.validate_sql_query(sql_query)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': validation_message,
                'generated_sql': sql_query
            })
        
        # Execute query
        success, results = chatbot.execute_query(sql_query)
        
        if not success:
            return jsonify({
                'success': False,
                'error': results,
                'generated_sql': sql_query
            })
        
        # Format response
        response_data = {
            'success': True,
            'message': f"Found {len(results)} result(s)",
            'generated_sql': sql_query,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Query executed successfully: {sql_query}")
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logger.info("Starting Secure SQL Chatbot application")
    app.run(debug=True, host='0.0.0.0', port=5000)

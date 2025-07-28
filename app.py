"""
🔐 Secure Local SQL Chatbot - Professional Implementation
A Flask web application for natural language SQL queries with enterprise-grade security
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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secure-chatbot-2025')

# Configure professional logging
import sys
import codecs

# Set UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/chatbot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('SecureChatbot')

# Initialize Groq client
try:
    groq_api_key = os.getenv('GROQ_API_KEY')
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
        logger.info("Groq client initialized successfully")
    else:
        logger.error("GROQ_API_KEY not found in environment variables")
        groq_client = None
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    groq_client = None

# Database configuration
DATABASE_PATH = 'database/secure_chatbot.db'

class SecureLocalChatbot:
    """Professional SQL Chatbot with enterprise security features"""
    
    def __init__(self):
        self.init_database()
        logger.info("SecureLocalChatbot initialized successfully")
    
    def init_database(self):
        """Initialize SQLite database with professional schema"""
        os.makedirs('database', exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # 📊 CUSTOMERS TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                city TEXT,
                country TEXT,
                registration_date DATE NOT NULL,
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 🛒 ORDERS TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
                total_amount DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
                order_date DATE NOT NULL,
                status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # 🏢 PRODUCTS TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL CHECK (price > 0),
                stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
                description TEXT,
                supplier TEXT,
                created_date DATE NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 👥 EMPLOYEES TABLE (New)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                salary DECIMAL(10,2),
                hire_date DATE NOT NULL,
                manager_id INTEGER,
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'terminated')),
                FOREIGN KEY (manager_id) REFERENCES employees (id)
            )
        ''')
        
        # Check if data exists and insert samples
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] == 0:
            self.insert_comprehensive_sample_data(cursor)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def insert_comprehensive_sample_data(self, cursor):
        """Insert comprehensive sample data for testing"""
        logger.info("📊 Inserting sample data...")
        
        # 👤 SAMPLE CUSTOMERS
        customers_data = [
            ('John Smith', 'john.smith@techcorp.com', '+1-555-0101', 'New York', 'USA', '2023-01-15', 'active'),
            ('Sarah Johnson', 'sarah.j@innovate.com', '+1-555-0102', 'Los Angeles', 'USA', '2023-02-20', 'active'),
            ('Michael Brown', 'mike.brown@startup.io', '+1-555-0103', 'Chicago', 'USA', '2023-03-10', 'active'),
            ('Emily Davis', 'emily.davis@enterprise.org', '+1-555-0104', 'Houston', 'USA', '2023-04-05', 'inactive'),
            ('David Wilson', 'david.w@solutions.net', '+1-555-0105', 'Phoenix', 'USA', '2023-05-12', 'active'),
            ('Lisa Anderson', 'lisa.a@global.com', '+1-555-0106', 'Philadelphia', 'USA', '2023-06-18', 'active'),
            ('Robert Martinez', 'robert.m@tech.dev', '+1-555-0107', 'San Antonio', 'USA', '2023-07-22', 'active'),
            ('Jennifer Garcia', 'jen.garcia@digital.biz', '+1-555-0108', 'San Diego', 'USA', '2023-08-14', 'suspended'),
        ]
        
        cursor.executemany(
            'INSERT INTO customers (name, email, phone, city, country, registration_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            customers_data
        )
        
        # 📦 SAMPLE PRODUCTS
        products_data = [
            ('MacBook Pro 16"', 'Electronics', 2499.99, 45, 'High-performance laptop for professionals', 'Apple Inc.', '2024-01-01'),
            ('Dell XPS 15', 'Electronics', 1899.99, 32, 'Premium Windows laptop', 'Dell Technologies', '2024-01-01'),
            ('Wireless Mouse Pro', 'Electronics', 79.99, 150, 'Ergonomic wireless mouse with precision tracking', 'Logitech', '2024-01-01'),
            ('Office Chair Executive', 'Furniture', 599.99, 28, 'Leather executive office chair', 'Herman Miller', '2024-01-01'),
            ('iPhone 15 Pro', 'Electronics', 999.99, 85, 'Latest flagship smartphone', 'Apple Inc.', '2024-01-01'),
            ('Samsung Galaxy S24', 'Electronics', 899.99, 67, 'Android flagship smartphone', 'Samsung', '2024-01-01'),
            ('Coffee Machine Deluxe', 'Kitchen', 299.99, 42, 'Premium coffee brewing system', 'Breville', '2024-01-01'),
            ('Monitor 4K 27"', 'Electronics', 449.99, 38, 'Ultra HD 4K professional monitor', 'LG Electronics', '2024-01-01'),
            ('Mechanical Keyboard', 'Electronics', 159.99, 95, 'RGB mechanical gaming keyboard', 'Corsair', '2024-01-01'),
            ('Desk Lamp LED', 'Furniture', 89.99, 73, 'Adjustable LED desk lamp', 'Philips', '2024-01-01'),
        ]
        
        cursor.executemany(
            'INSERT INTO products (name, category, price, stock_quantity, description, supplier, created_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
            products_data
        )
        
        # 🛍️ SAMPLE ORDERS
        orders_data = [
            (1, 'MacBook Pro 16"', 'Electronics', 1, 2499.99, '2024-06-01', 'delivered'),
            (2, 'Wireless Mouse Pro', 'Electronics', 2, 79.99, '2024-06-02', 'delivered'),
            (1, 'Office Chair Executive', 'Furniture', 1, 599.99, '2024-06-05', 'shipped'),
            (4, 'iPhone 15 Pro', 'Electronics', 1, 999.99, '2024-06-08', 'processing'),
            (5, 'Coffee Machine Deluxe', 'Kitchen', 1, 299.99, '2024-06-10', 'pending'),
            (3, 'Monitor 4K 27"', 'Electronics', 2, 449.99, '2024-06-12', 'delivered'),
            (6, 'Dell XPS 15', 'Electronics', 1, 1899.99, '2024-06-15', 'shipped'),
            (7, 'Mechanical Keyboard', 'Electronics', 1, 159.99, '2024-06-18', 'delivered'),
            (2, 'Desk Lamp LED', 'Furniture', 3, 89.99, '2024-06-20', 'processing'),
            (1, 'Samsung Galaxy S24', 'Electronics', 1, 899.99, '2024-06-22', 'cancelled'),
        ]
        
        cursor.executemany(
            'INSERT INTO orders (customer_id, product_name, category, quantity, unit_price, order_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            orders_data
        )
        
        # 👥 SAMPLE EMPLOYEES
        employees_data = [
            ('Alice Johnson', 'alice.j@company.com', 'Engineering', 'Senior Developer', 95000.00, '2022-01-15', None, 'active'),
            ('Bob Smith', 'bob.s@company.com', 'Engineering', 'Team Lead', 110000.00, '2021-03-10', 1, 'active'),
            ('Carol Davis', 'carol.d@company.com', 'Marketing', 'Marketing Manager', 75000.00, '2022-05-20', None, 'active'),
            ('David Brown', 'david.b@company.com', 'Sales', 'Sales Representative', 65000.00, '2023-02-14', None, 'active'),
            ('Eve Wilson', 'eve.w@company.com', 'HR', 'HR Specialist', 60000.00, '2023-07-08', None, 'inactive'),
            ('Frank Miller', 'frank.m@company.com', 'Engineering', 'Junior Developer', 70000.00, '2024-01-10', 2, 'active'),
        ]
        
        cursor.executemany(
            'INSERT INTO employees (name, email, department, position, salary, hire_date, manager_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            employees_data
        )
        
        logger.info("Comprehensive sample data inserted successfully")
    
    def get_database_schema(self):
        """Get detailed database schema with relationships"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        schema_info = {}
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # Get foreign key information
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            foreign_keys = cursor.fetchall()
            
            schema_info[table_name] = {
                'columns': [
                    {
                        'name': col[1],
                        'type': col[2],
                        'not_null': bool(col[3]),
                        'primary_key': bool(col[5]),
                        'default_value': col[4]
                    }
                    for col in columns
                ],
                'foreign_keys': [
                    {
                        'column': fk[3],
                        'references_table': fk[2],
                        'references_column': fk[4]
                    }
                    for fk in foreign_keys
                ]
            }
        
        conn.close()
        return schema_info
    
    def validate_sql_query(self, query):
        """Enhanced SQL validation with detailed security checks"""
        if not query or not query.strip():
            return False, "Query cannot be empty"
        
        query_upper = query.strip().upper()
        
        # Only allow SELECT statements
        if not query_upper.startswith('SELECT'):
            return False, "Security: Only SELECT queries are allowed"
        
        # Enhanced dangerous keyword detection
        dangerous_keywords = [
            'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'TRUNCATE',
            'EXEC', 'EXECUTE', 'REPLACE', 'MERGE', 'PRAGMA', 'ATTACH', 'DETACH'
        ]
        
        for keyword in dangerous_keywords:
            if f' {keyword} ' in f' {query_upper} ' or query_upper.startswith(f'{keyword} '):
                return False, f"Forbidden keyword detected: {keyword}"
        
        # Check for potential SQL injection patterns
        injection_patterns = [
            r';\s*(DROP|DELETE|INSERT|UPDATE)',
            r'--',
            r'/\*.*\*/',
            r'UNION.*SELECT',
            r'OR.*1\s*=\s*1',
            r'AND.*1\s*=\s*1'
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, query_upper):
                return False, "Potential SQL injection detected"
        
        return True, "Query passed security validation"
    
    def execute_query(self, sql_query):
        """Execute SQL query with enhanced error handling"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            # Convert to list of dictionaries with proper formatting
            data = []
            for row in results:
                row_dict = dict(row)
                # Format decimal values
                for key, value in row_dict.items():
                    if isinstance(value, float) and '.' in str(value):
                        row_dict[key] = round(value, 2)
                data.append(row_dict)
            
            conn.close()
            return True, data
        
        except sqlite3.Error as e:
            logger.error(f"Database error: {str(e)}")
            return False, f"Database error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
    
    def generate_sql_from_natural_language(self, user_question):
        """Generate SQL using Groq with enhanced prompting"""
        if not groq_client:
            logger.error("Groq client not initialized")
            return self.generate_fallback_sql(user_question)
        
        try:
            schema_info = self.get_database_schema()
            schema_text = self.format_schema_for_ai(schema_info)
            
            enhanced_prompt = f"""You are an expert SQL analyst for a business database. Convert natural language questions to precise SQLite SELECT queries.

DATABASE SCHEMA:
{schema_text}

QUERY GUIDELINES:
1. Generate ONLY SELECT statements (security requirement)
2. Use proper SQLite syntax with correct JOINs
3. Apply appropriate WHERE clauses for filtering
4. Use aggregate functions (COUNT, SUM, AVG, MAX, MIN) when needed
5. Include proper GROUP BY and ORDER BY clauses
6. Handle date comparisons correctly
7. Return ONLY the SQL query without explanations

USER QUESTION: {user_question}

SQL QUERY:"""

            logger.info(f"Sending request to Groq for: {user_question}")
            
            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": enhanced_prompt}],
                temperature=0.1,
                max_tokens=600
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up response formatting
            sql_query = re.sub(r'^```sql\n?', '', sql_query)
            sql_query = re.sub(r'\n?```$', '', sql_query)
            sql_query = sql_query.strip()
            
            logger.info(f"Generated SQL: {sql_query}")
            return sql_query
        
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return self.generate_fallback_sql(user_question)
    
    def generate_fallback_sql(self, user_question):
        """Generate basic SQL for common queries when Groq is unavailable"""
        question_lower = user_question.lower()
        
        # Simple pattern matching for basic queries
        if any(keyword in question_lower for keyword in ['all customers', 'show customers', 'list customers']):
            if 'active' in question_lower:
                return "SELECT * FROM customers WHERE status = 'active'"
            return "SELECT * FROM customers"
        
        elif any(keyword in question_lower for keyword in ['count customers', 'how many customers']):
            return "SELECT COUNT(*) as customer_count FROM customers"
        
        elif any(keyword in question_lower for keyword in ['all orders', 'show orders', 'list orders']):
            return "SELECT * FROM orders ORDER BY order_date DESC"
        
        elif any(keyword in question_lower for keyword in ['count orders', 'how many orders']):
            return "SELECT COUNT(*) as order_count FROM orders"
        
        elif any(keyword in question_lower for keyword in ['all products', 'show products', 'list products']):
            if 'electronics' in question_lower:
                return "SELECT * FROM products WHERE category = 'Electronics'"
            return "SELECT * FROM products"
        
        elif any(keyword in question_lower for keyword in ['all employees', 'show employees', 'list employees']):
            return "SELECT * FROM employees WHERE status = 'active'"
        
        elif 'revenue' in question_lower and 'electronics' in question_lower:
            return "SELECT SUM(total_amount) as total_revenue FROM orders WHERE category = 'Electronics'"
        
        elif 'top' in question_lower and 'customers' in question_lower:
            return "SELECT c.name, c.email, SUM(o.total_amount) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name, c.email ORDER BY total_spent DESC LIMIT 5"
        
        # Default fallback
        logger.warning(f"No fallback SQL pattern matched for: {user_question}")
        return None
    
    def format_schema_for_ai(self, schema_info):
        """Format schema for AI with relationships and business context"""
        schema_text = ""
        
        for table_name, table_info in schema_info.items():
            schema_text += f"\n📋 Table: {table_name.upper()}\n"
            
            for column in table_info['columns']:
                constraints = []
                if column['primary_key']:
                    constraints.append('PRIMARY KEY')
                if column['not_null']:
                    constraints.append('NOT NULL')
                
                constraint_text = f" [{', '.join(constraints)}]" if constraints else ""
                schema_text += f"   • {column['name']}: {column['type']}{constraint_text}\n"
            
            # Add foreign key relationships
            if table_info['foreign_keys']:
                schema_text += "   🔗 Foreign Keys:\n"
                for fk in table_info['foreign_keys']:
                    schema_text += f"      - {fk['column']} → {fk['references_table']}.{fk['references_column']}\n"
            
            schema_text += "\n"
        
        return schema_text

# Initialize the secure chatbot
chatbot = SecureLocalChatbot()

# 🌐 FLASK ROUTES
@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/schema')
def get_schema():
    """API endpoint for database schema information"""
    try:
        schema = chatbot.get_database_schema()
        return jsonify({
            'success': True,
            'schema': schema,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Schema endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'groq_connected': groq_client is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced chat endpoint with comprehensive error handling"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        logger.info(f"Processing query: {user_message}")
        
        # Generate SQL from natural language
        sql_query = chatbot.generate_sql_from_natural_language(user_message)
        
        if not sql_query:
            error_message = "Failed to generate SQL query."
            if not groq_client:
                error_message += " Groq client is not initialized - please check your API key."
            else:
                error_message += " Please try rephrasing your question."
            
            return jsonify({
                'success': False,
                'error': error_message,
                'suggestion': 'Try asking: "Show all customers" or "How many orders were placed?"'
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
        
        # Format successful response
        response_data = {
            'success': True,
            'message': f"Found {len(results)} result(s)",
            'generated_sql': sql_query,
            'results': results,
            'result_count': len(results),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Query executed successfully: {sql_query} | Results: {len(results)}")
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    logger.info("Starting Secure Local SQL Chatbot")
    logger.info("="*60)
    logger.info("Security Features: SQL Injection Protection, SELECT-only queries")
    logger.info("Database: SQLite with 4 tables (customers, orders, products, employees)")
    logger.info("AI: Groq LLM (llama3-70b-8192)")
    logger.info("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

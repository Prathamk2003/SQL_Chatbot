# 🔐 Secure Local SQL Chatbot

A professional Flask web application that converts natural language queries into secure SQL SELECT statements using Groq's LLM API. Built with enterprise-grade security features and a modern, responsive interface.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![SQLite](https://img.shields.io/badge/SQLite-Local-orange)
![Groq](https://img.shields.io/badge/Groq-LLM-purple)
![Security](https://img.shields.io/badge/Security-SQL%20Injection%20Protected-red)

## 🌟 Features

### 🔒 Security First
- **SQL Injection Protection**: Advanced pattern detection and keyword filtering
- **SELECT-Only Queries**: Prevents any data modification operations
- **Local Database**: No cloud dependencies, complete data privacy
- **Input Validation**: Comprehensive query validation before execution

### 🧠 AI-Powered
- **Natural Language Processing**: Convert everyday questions to SQL
- **Groq LLM Integration**: Using llama3-70b-8192 for accurate query generation
- **Context-Aware**: Understands database schema and relationships
- **Smart Query Optimization**: Generates efficient SQL with proper JOINs

### 💼 Professional Interface
- **Modern Chat UI**: Clean, responsive design with real-time messaging
- **Interactive Results**: Tables with proper formatting and pagination
- **SQL Query Display**: Shows generated SQL alongside results
- **Database Schema Viewer**: Comprehensive table and relationship overview
- **Mobile Responsive**: Works perfectly on all device sizes

### 📊 Rich Database
- **4 Interconnected Tables**: Customers, Orders, Products, Employees
- **Sample Data Included**: Ready-to-use test data for demonstrations
- **Foreign Key Relationships**: Proper relational database design
- **Business Context**: Real-world scenarios for meaningful queries

## 🚀 Quick Start

### 1. Clone & Setup
```bash
# Clone the project
cd chat_bot

# Run automated setup
python setup.py
```

### 2. Configure Environment
Update `.env` file with your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from [Groq Console](https://console.groq.com/)

### 3. Start Application
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Start the application
python app.py
```

### 4. Access Application
Open your browser and navigate to: **http://localhost:5000**

## 📋 Database Schema

### 👥 Customers Table
```sql
- id (PRIMARY KEY)
- name, email, phone
- city, country
- registration_date, status
```

### 🛒 Orders Table
```sql
- id (PRIMARY KEY)
- customer_id (FK → customers.id)
- product_name, category
- quantity, unit_price, total_amount
- order_date, status
```

### 📦 Products Table
```sql
- id (PRIMARY KEY)
- name, category, price
- stock_quantity, description
- supplier, created_date
```

### 👔 Employees Table
```sql
- id (PRIMARY KEY)
- name, email, department
- position, salary, hire_date
- manager_id (FK → employees.id)
```

## 💬 Sample Queries

Try these natural language questions:

### Basic Queries
- "Show all active customers"
- "List products in Electronics category"
- "How many orders were placed this month?"

### Advanced Analytics
- "Top 5 customers by total order value"
- "Average order value by product category"
- "Monthly revenue trends for 2024"
- "Employees in Engineering department with salary > 80000"

### Business Intelligence
- "Which products are running low on stock?"
- "Customers who haven't placed orders recently"
- "Order status distribution"
- "Employee hierarchy with manager relationships"

## 🛡️ Security Features

### SQL Injection Prevention
```python
# Blocked patterns
- DROP, DELETE, INSERT, UPDATE operations
- Comment injections (-- and /* */)
- Union-based attacks
- Boolean-based blind injections
```

### Query Validation
```python
# Security checks
- SELECT-only statement verification
- Dangerous keyword detection
- Injection pattern recognition
- Input sanitization
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │   SQLite DB     │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • Route Handling│◄──►│ • Local Storage │
│ • Bootstrap UI  │    │ • Query Proc.   │    │ • 4 Tables      │
│ • Real-time     │    │ • Security Val. │    │ • Sample Data   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   Groq LLM      │
         └──────────────►│                 │
                        │ • llama3-70b    │
                        │ • NL → SQL      │
                        └─────────────────┘
```

## 📁 Project Structure

```
chat_bot/
├── app.py                 # Main Flask application
├── setup.py              # Automated setup script
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
├── README.md            # This documentation
├── static/
│   ├── css/
│   │   └── style.css    # Professional styling
│   └── js/
│       └── chat.js      # Interactive frontend
├── templates/
│   └── index.html       # Main chat interface
├── database/
│   └── secure_chatbot.db # SQLite database
├── logs/
│   └── chatbot.log      # Application logs
└── venv/                # Virtual environment
```

## ⚙️ Configuration Options

### Environment Variables
```env
GROQ_API_KEY=your_groq_api_key      # Required: Groq API key
SECRET_KEY=your_secret_key          # Flask secret key
DEBUG=True                          # Debug mode
DATABASE_PATH=database/chatbot.db   # Database location
LOG_LEVEL=INFO                      # Logging level
```

### Application Settings
```python
# In app.py, customize:
- Port number (default: 5000)
- Host binding (default: 0.0.0.0)
- Database location
- Logging configuration
```

## 🧪 Testing

### Manual Testing
1. **Basic Functionality**
   - Send simple queries like "Show all customers"
   - Verify results display correctly

2. **Security Testing**
   - Try malicious queries (should be blocked)
   - Test with various injection patterns

3. **UI Testing**
   - Test on different screen sizes
   - Verify all buttons and features work

### Sample Test Queries
```sql
-- These should work:
"Show all customers from New York"
"Count orders by status"
"Average salary by department"

-- These should be blocked:
"DROP TABLE customers"
"INSERT INTO customers ..."
"DELETE FROM orders WHERE ..."
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Groq API Key Error
**Error**: `Failed to generate SQL query`
**Solution**: Ensure your Groq API key is correctly set in `.env`

#### 2. Database Connection Error
**Error**: `Database error: no such table`
**Solution**: Delete `database/secure_chatbot.db` and restart the app

#### 3. Port Already in Use
**Error**: `Address already in use`
**Solution**: Change port in `app.py` or stop existing Flask processes

#### 4. Virtual Environment Issues
**Error**: Package import errors
**Solution**: Recreate virtual environment: `python setup.py`

### Debug Mode
Enable detailed logging by setting in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 🔄 Updates & Maintenance

### Regular Updates
1. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Database Maintenance**
   - Monitor log files for errors
   - Backup database regularly
   - Clear logs when they get large

3. **Security Updates**
   - Update Flask and dependencies regularly
   - Review security patterns quarterly
   - Test with new query patterns

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for all functions
- Include error handling
- Write tests for new features

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🆘 Support

### Getting Help
- Check troubleshooting section first
- Review application logs in `logs/chatbot.log`
- Create detailed issue with error messages
- Include system information and steps to reproduce

### Feature Requests
- Open issue with detailed description
- Explain business use case
- Provide example queries or scenarios

---

## 🏆 Achievements

✅ **Enterprise Security**: SQL injection protected  
✅ **Modern UI**: Professional chat interface  
✅ **AI-Powered**: Natural language query processing  
✅ **Local First**: No cloud dependencies  
✅ **Production Ready**: Comprehensive logging and error handling  
✅ **Well Documented**: Complete setup and usage guide  

---

**Built with ❤️ for secure, local SQL querying**

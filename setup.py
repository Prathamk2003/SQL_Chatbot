"""
🚀 Secure Local SQL Chatbot - Setup Script
Automated setup and configuration for the chatbot application
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

class ChatbotSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.venv_path = self.base_dir / 'venv'
        self.requirements_file = self.base_dir / 'requirements.txt'
        
    def print_banner(self):
        print("=" * 60)
        print("🔐 SECURE LOCAL SQL CHATBOT - SETUP")
        print("=" * 60)
        print("🚀 Setting up your professional chatbot application...")
        print()
    
    def check_python_version(self):
        print("🔍 Checking Python version...")
        if sys.version_info < (3, 8):
            print("❌ Python 3.8 or higher is required!")
            print(f"   Current version: {sys.version}")
            return False
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        return True
    
    def create_virtual_environment(self):
        print("\n🔧 Creating virtual environment...")
        try:
            if self.venv_path.exists():
                print("   Virtual environment already exists")
                return True
                
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], check=True)
            print("✅ Virtual environment created successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def get_pip_path(self):
        if os.name == 'nt':  # Windows
            return self.venv_path / 'Scripts' / 'pip.exe'
        else:  # Unix/Linux/macOS
            return self.venv_path / 'bin' / 'pip'
    
    def install_requirements(self):
        print("\n📦 Installing required packages...")
        pip_path = self.get_pip_path()
        
        try:
            # Upgrade pip first
            subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True)
            
            # Install requirements
            if self.requirements_file.exists():
                subprocess.run([str(pip_path), 'install', '-r', str(self.requirements_file)], check=True)
                print("✅ All packages installed successfully")
            else:
                print("❌ requirements.txt not found!")
                return False
                
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False
    
    def setup_directories(self):
        print("\n📁 Creating project directories...")
        
        directories = [
            'logs',
            'database',
            'static/css',
            'static/js',
            'templates'
        ]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {dir_path}")
        
        print("✅ All directories created")
        return True
    
    def validate_env_file(self):
        print("\n🔐 Checking environment configuration...")
        env_file = self.base_dir / '.env'
        
        if not env_file.exists():
            print("❌ .env file not found!")
            self.create_sample_env()
            return False
        
        # Check if GROQ_API_KEY is set
        with open(env_file, 'r') as f:
            content = f.read()
            if 'your_groq_api_key_here' in content:
                print("⚠️  Please update your GROQ_API_KEY in .env file")
                print("   Get your API key from: https://console.groq.com/")
                return False
        
        print("✅ Environment configuration looks good")
        return True
    
    def create_sample_env(self):
        print("📝 Creating sample .env file...")
        env_content = """# Secure Local SQL Chatbot - Environment Configuration
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=secure-chatbot-2025-key
DEBUG=True
DATABASE_PATH=database/chatbot.db
LOG_LEVEL=INFO"""
        
        with open(self.base_dir / '.env', 'w') as f:
            f.write(env_content)
        print("✅ Sample .env file created")
    
    def test_database_connection(self):
        print("\n🗄️  Testing database setup...")
        try:
            db_path = self.base_dir / 'database' / 'secure_chatbot.db'
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            print("✅ Database connection successful")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def display_next_steps(self):
        print("\n" + "=" * 60)
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("📋 NEXT STEPS:")
        print()
        print("1. 🔑 Update your Groq API key in .env file:")
        print("   GROQ_API_KEY=your_actual_api_key_here")
        print()
        print("2. 🚀 Start the application:")
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # Unix/Linux/macOS
            print("   source venv/bin/activate")
        print("   python app.py")
        print()
        print("3. 🌐 Open your browser and go to:")
        print("   http://localhost:5000")
        print()
        print("4. 💬 Try these sample queries:")
        print("   • Show all customers")
        print("   • How many orders were placed?")
        print("   • Top 5 products by sales")
        print("   • Average order value by month")
        print()
        print("🔐 Security Features Enabled:")
        print("   ✅ SQL injection protection")
        print("   ✅ SELECT-only query restrictions")
        print("   ✅ Local database (no cloud dependencies)")
        print("   ✅ Comprehensive logging")
        print()
        print("=" * 60)
    
    def run_setup(self):
        self.print_banner()
        
        # Check prerequisites
        if not self.check_python_version():
            return False
        
        # Setup steps
        steps = [
            ("Creating directories", self.setup_directories),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Installing packages", self.install_requirements),
            ("Validating configuration", self.validate_env_file),
            ("Testing database", self.test_database_connection)
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                print("   Please fix the errors above and run setup again.")
                return False
        
        self.display_next_steps()
        return True

if __name__ == '__main__':
    setup = ChatbotSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)

#!/usr/bin/env python
"""
Development startup script for AlzCarePlus
This script starts both the backend and frontend development servers.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def run_backend():
    """Run the Django backend server"""
    print("Starting Django backend server...")
    backend_dir = Path("backend")
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        python_path = venv_path / "Scripts" / "python.exe"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:  # Unix/Linux/Mac
        python_path = venv_path / "bin" / "python"
        pip_path = venv_path / "bin" / "pip"
    
    # Install dependencies
    print("Installing backend dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    
    # Run Django server
    print("Starting Django server on http://localhost:8000")
    subprocess.run([str(python_path), "manage.py", "runserver"], check=True)

def run_frontend():
    """Run the React frontend server"""
    print("Starting React frontend server...")
    frontend_dir = Path("frontend")
    os.chdir(frontend_dir)
    
    # Install dependencies
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], check=True)
    
    # Start React development server
    print("Starting React server on http://localhost:3000")
    subprocess.run(["npm", "start"], check=True)

def setup_database():
    """Setup the database if needed"""
    print("Setting up database...")
    backend_dir = Path("backend")
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if venv_path.exists():
        if os.name == 'nt':  # Windows
            python_path = venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux/Mac
            python_path = venv_path / "bin" / "python"
        
        # Run database setup
        try:
            subprocess.run([str(python_path), "setup_db.py"], check=True)
            print("Database setup completed!")
        except subprocess.CalledProcessError:
            print("Database setup failed. You may need to run it manually.")
    else:
        print("Virtual environment not found. Please run the backend setup first.")

def main():
    """Main function"""
    print("=== AlzCarePlus Development Startup ===")
    print()
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("Error: Please run this script from the AlzCarePlus root directory.")
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    print("\nStarting development servers...")
    print("Press Ctrl+C to stop all servers")
    print()
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in main thread
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)

if __name__ == '__main__':
    main() 
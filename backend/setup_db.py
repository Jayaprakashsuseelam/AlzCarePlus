#!/usr/bin/env python
"""
Setup script for AlzCarePlus backend
This script initializes the database, runs migrations, and creates a superuser.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def setup_database():
    """Initialize the database and run migrations"""
    print("Setting up database...")
    
    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Database setup complete!")

def create_superuser():
    """Create a superuser for testing"""
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists!")
        return
    
    print("Creating superuser...")
    print("Please enter the following information:")
    
    email = input("Email: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    password = input("Password: ")
    
    try:
        user = User.objects.create_superuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        print(f"Superuser created successfully: {user.email}")
    except Exception as e:
        print(f"Error creating superuser: {e}")

def create_test_patient():
    """Create a test patient account"""
    User = get_user_model()
    
    # Check if test patient already exists
    if User.objects.filter(email='test@patient.com').exists():
        print("Test patient already exists!")
        return
    
    print("Creating test patient...")
    
    try:
        user = User.objects.create_user(
            email='test@patient.com',
            first_name='John',
            last_name='Doe',
            password='testpass123',
            phone='1234567890',
            date_of_birth='1980-01-01',
            gender='male'
        )
        print(f"Test patient created successfully: {user.email}")
        print("Login credentials: test@patient.com / testpass123")
    except Exception as e:
        print(f"Error creating test patient: {e}")

def main():
    """Main setup function"""
    print("=== AlzCarePlus Backend Setup ===")
    
    # Setup database
    setup_database()
    
    # Create superuser
    create_superuser()
    
    # Create test patient
    create_test_patient()
    
    print("\n=== Setup Complete ===")
    print("You can now run the development server with:")
    print("python manage.py runserver")

if __name__ == '__main__':
    main() 
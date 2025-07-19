#!/usr/bin/env python
"""
Test script for patient authentication functionality
This script tests the patient registration and login endpoints.
"""

import os
import sys
import django
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# API base URL
API_BASE_URL = 'http://localhost:8000/api'

def test_patient_registration():
    """Test patient registration endpoint"""
    print("Testing patient registration...")
    
    registration_data = {
        'first_name': 'Test',
        'last_name': 'Patient',
        'email': 'testpatient@example.com',
        'phone': '1234567890',
        'date_of_birth': '1985-06-15',
        'gender': 'male',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/register/',
            json=registration_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"   Patient ID: {data['patient']['id']}")
            print(f"   Email: {data['patient']['email']}")
            print(f"   Token: {data['token'][:20]}...")
            return data['token']
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Django server is running.")
        return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_patient_login():
    """Test patient login endpoint"""
    print("\nTesting patient login...")
    
    login_data = {
        'email': 'testpatient@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   Patient ID: {data['patient']['id']}")
            print(f"   Email: {data['patient']['email']}")
            print(f"   Token: {data['token'][:20]}...")
            return data['token']
        else:
            print(f"❌ Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Django server is running.")
        return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_patient_profile(token):
    """Test patient profile endpoint"""
    print("\nTesting patient profile...")
    
    try:
        response = requests.get(
            f'{API_BASE_URL}/profile/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Profile retrieval successful!")
            print(f"   Name: {data['first_name']} {data['last_name']}")
            print(f"   Email: {data['email']}")
            print(f"   Phone: {data['phone']}")
            return True
        else:
            print(f"❌ Profile retrieval failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return False

def test_patient_dashboard(token):
    """Test patient dashboard endpoint"""
    print("\nTesting patient dashboard...")
    
    try:
        response = requests.get(
            f'{API_BASE_URL}/dashboard/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard retrieval successful!")
            print(f"   Patient: {data['patient']['first_name']} {data['patient']['last_name']}")
            print(f"   Statistics: {len(data['statistics'])} metrics available")
            return True
        else:
            print(f"❌ Dashboard retrieval failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        return False

def test_patient_logout(token):
    """Test patient logout endpoint"""
    print("\nTesting patient logout...")
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/auth/logout/',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 200:
            print("✅ Logout successful!")
            return True
        else:
            print(f"❌ Logout failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return False

def main():
    """Main test function"""
    print("=== Patient Authentication Test Suite ===")
    print("Make sure the Django server is running on http://localhost:8000")
    print()
    
    # Test registration
    token = test_patient_registration()
    
    if token:
        # Test login
        login_token = test_patient_login()
        
        if login_token:
            # Test profile
            test_patient_profile(login_token)
            
            # Test dashboard
            test_patient_dashboard(login_token)
            
            # Test logout
            test_patient_logout(login_token)
    
    print("\n=== Test Suite Complete ===")
    print("If all tests passed, the patient authentication system is working correctly!")

if __name__ == '__main__':
    main() 
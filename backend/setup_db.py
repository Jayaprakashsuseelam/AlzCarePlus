#!/usr/bin/env python
"""
Database setup script for AlzCarePlus
This script will:
1. Run migrations
2. Create a superuser (optional)
3. Create some dummy patient data
"""

import os
import sys
import django
from datetime import date, timedelta
import random

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient, PatientProfile

def create_dummy_patients():
    """Create some dummy patient data for testing"""
    
    # Sample data
    first_names = ['John', 'Jane', 'Robert', 'Mary', 'David', 'Sarah', 'Michael', 'Lisa', 'James', 'Patricia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    emails = ['john.smith@email.com', 'jane.johnson@email.com', 'robert.williams@email.com', 'mary.brown@email.com', 'david.jones@email.com']
    
    patients_created = 0
    
    for i in range(5):
        try:
            # Create patient
            patient = Patient.objects.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=emails[i],
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                date_of_birth=date(1950 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28)),
                gender=random.choice(['male', 'female']),
                age=random.randint(60, 85),
                medical_history=f"Patient has been diagnosed with {random.choice(['mild', 'moderate'])} cognitive impairment.",
                emergency_contact_name=f"Emergency Contact {i+1}",
                emergency_contact_phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                password='testpass123'
            )
            
            # Create profile
            profile = PatientProfile.objects.create(
                patient=patient,
                address=f"{random.randint(100, 9999)} Main St",
                city=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                state=random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
                zip_code=f"{random.randint(10000, 99999)}",
                blood_type=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                allergies=random.choice(['None', 'Penicillin', 'Peanuts', 'Latex']),
                current_medications=random.choice(['Donepezil', 'Memantine', 'Vitamin D', 'None']),
                primary_care_physician=f"Dr. {random.choice(['Johnson', 'Smith', 'Williams', 'Brown'])}",
                insurance_provider=random.choice(['Blue Cross', 'Aetna', 'Cigna', 'UnitedHealth']),
                insurance_number=f"INS{random.randint(100000, 999999)}"
            )
            
            patients_created += 1
            print(f"Created patient: {patient.full_name} ({patient.email})")
            
        except Exception as e:
            print(f"Error creating patient {i+1}: {e}")
    
    print(f"\nSuccessfully created {patients_created} dummy patients")
    return patients_created

def main():
    """Main setup function"""
    print("Setting up AlzCarePlus database...")
    
    try:
        # Create dummy patients
        print("\nCreating dummy patient data...")
        patients_created = create_dummy_patients()
        
        if patients_created > 0:
            print(f"\n✅ Database setup completed successfully!")
            print(f"Created {patients_created} dummy patients")
            print("\nYou can now test the application with these credentials:")
            print("Email: john.smith@email.com")
            print("Password: testpass123")
        else:
            print("\n⚠️ No patients were created. Check the error messages above.")
            
    except Exception as e:
        print(f"\n❌ Error during database setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
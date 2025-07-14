# backend/ml/patient_similarity.py
"""
The module will:
Scale and normalize the features
Use cosine similarity to find the most similar patients
Provide similarity scores and explanations
Handle missing values automatically
Generate synthetic patient data for testing and development
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import random
from datetime import datetime, timedelta

class PatientSimilarity:
    def __init__(self, n_neighbors: int = 5):
        """
        Initialize the PatientSimilarity class.
        
        Args:
            n_neighbors (int): Number of nearest neighbors to find
        """
        self.n_neighbors = n_neighbors
        self.model = NearestNeighbors(
            n_neighbors=n_neighbors,
            metric='cosine',
            algorithm='brute'
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False

    def generate_synthetic_data(
        self,
        num_patients: int = 100,
        age_range: Tuple[int, int] = (60, 90),
        cognitive_score_range: Tuple[float, float] = (10.0, 30.0),
        mood_score_range: Tuple[float, float] = (1.0, 10.0),
        sleep_hours_range: Tuple[float, float] = (4.0, 10.0),
        medication_adherence_range: Tuple[float, float] = (0.5, 1.0),
        social_interaction_range: Tuple[float, float] = (1.0, 10.0),
        include_demographics: bool = True,
        include_medical_history: bool = True,
        include_behavioral_data: bool = True,
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate synthetic patient data for testing and development.
        
        Args:
            num_patients (int): Number of patients to generate
            age_range (Tuple[int, int]): Range for patient ages
            cognitive_score_range (Tuple[float, float]): Range for cognitive scores (MMSE)
            mood_score_range (Tuple[float, float]): Range for mood scores (1-10 scale)
            sleep_hours_range (Tuple[float, float]): Range for average sleep hours
            medication_adherence_range (Tuple[float, float]): Range for medication adherence (0-1)
            social_interaction_range (Tuple[float, float]): Range for social interaction scores (1-10)
            include_demographics (bool): Whether to include demographic information
            include_medical_history (bool): Whether to include medical history
            include_behavioral_data (bool): Whether to include behavioral data
            seed (Optional[int]): Random seed for reproducibility
            
        Returns:
            List[Dict[str, Any]]: List of synthetic patient data dictionaries
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        patients_data = []
        
        for i in range(num_patients):
            patient = {
                'id': i + 1,
                'age': random.randint(age_range[0], age_range[1]),
                'cognitive_score': round(random.uniform(cognitive_score_range[0], cognitive_score_range[1]), 1),
                'mood_score': round(random.uniform(mood_score_range[0], mood_score_range[1]), 1),
                'sleep_hours': round(random.uniform(sleep_hours_range[0], sleep_hours_range[1]), 1),
                'medication_adherence': round(random.uniform(medication_adherence_range[0], medication_adherence_range[1]), 2),
                'social_interaction_score': round(random.uniform(social_interaction_range[0], social_interaction_range[1]), 1)
            }
            
            # Add demographic information
            if include_demographics:
                patient.update(self._generate_demographics())
            
            # Add medical history
            if include_medical_history:
                patient.update(self._generate_medical_history())
            
            # Add behavioral data
            if include_behavioral_data:
                patient.update(self._generate_behavioral_data())
            
            patients_data.append(patient)
        
        return patients_data

    def _generate_demographics(self) -> Dict[str, Any]:
        """Generate demographic information for a patient."""
        genders = ['Male', 'Female']
        education_levels = ['Primary', 'Secondary', 'Bachelor', 'Master', 'PhD']
        marital_statuses = ['Single', 'Married', 'Divorced', 'Widowed']
        
        return {
            'gender': random.choice(genders),
            'education_level': random.choice(education_levels),
            'marital_status': random.choice(marital_statuses),
            'living_situation': random.choice(['Independent', 'With Family', 'Assisted Living', 'Nursing Home']),
            'income_level': random.choice(['Low', 'Medium', 'High']),
            'location_type': random.choice(['Urban', 'Suburban', 'Rural'])
        }

    def _generate_medical_history(self) -> Dict[str, Any]:
        """Generate medical history for a patient."""
        # Common conditions in elderly population
        conditions = [
            'Hypertension', 'Diabetes', 'Heart Disease', 'Arthritis', 
            'Osteoporosis', 'Depression', 'Anxiety', 'Sleep Apnea',
            'Chronic Pain', 'Vision Problems', 'Hearing Loss'
        ]
        
        # Generate random number of conditions (0-4)
        num_conditions = random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.25, 0.15, 0.1])[0]
        selected_conditions = random.sample(conditions, num_conditions) if num_conditions > 0 else []
        
        # Generate medication list
        medications = [
            'Donepezil', 'Memantine', 'Rivastigmine', 'Galantamine',
            'Sertraline', 'Escitalopram', 'Bupropion', 'Mirtazapine',
            'Lorazepam', 'Zolpidem', 'Melatonin', 'Vitamin D',
            'Calcium', 'Omega-3', 'B12', 'Folic Acid'
        ]
        
        num_medications = random.choices([0, 1, 2, 3, 4, 5], weights=[0.1, 0.2, 0.25, 0.2, 0.15, 0.1])[0]
        selected_medications = random.sample(medications, num_medications) if num_medications > 0 else []
        
        return {
            'medical_conditions': selected_conditions,
            'medications': selected_medications,
            'years_since_diagnosis': random.randint(0, 15),
            'family_history_alzheimer': random.choice([True, False]),
            'smoking_history': random.choice(['Never', 'Former', 'Current']),
            'alcohol_consumption': random.choice(['None', 'Occasional', 'Moderate', 'Heavy']),
            'exercise_frequency': random.choice(['Never', 'Rarely', 'Sometimes', 'Regularly', 'Daily']),
            'bmi': round(random.uniform(18.5, 35.0), 1),
            'blood_pressure_systolic': random.randint(90, 180),
            'blood_pressure_diastolic': random.randint(60, 100),
            'cholesterol_total': random.randint(150, 300),
            'blood_sugar_fasting': random.randint(70, 200)
        }

    def _generate_behavioral_data(self) -> Dict[str, Any]:
        """Generate behavioral and lifestyle data for a patient."""
        # Generate daily activity patterns
        activities = {
            'reading': random.randint(0, 120),  # minutes per day
            'walking': random.randint(0, 60),
            'social_media': random.randint(0, 90),
            'tv_watching': random.randint(0, 240),
            'puzzle_solving': random.randint(0, 60),
            'cooking': random.randint(0, 90),
            'gardening': random.randint(0, 120),
            'music_listening': random.randint(0, 120)
        }
        
        # Generate weekly patterns
        weekly_patterns = {
            'doctor_visits_per_month': random.randint(0, 4),
            'family_visits_per_week': random.randint(0, 7),
            'social_events_per_month': random.randint(0, 8),
            'hobby_activities_per_week': random.randint(0, 5)
        }
        
        # Generate cognitive assessment scores
        cognitive_scores = {
            'memory_test_score': round(random.uniform(5.0, 25.0), 1),
            'attention_test_score': round(random.uniform(10.0, 30.0), 1),
            'language_test_score': round(random.uniform(15.0, 30.0), 1),
            'visuospatial_test_score': round(random.uniform(8.0, 25.0), 1),
            'executive_function_score': round(random.uniform(10.0, 30.0), 1)
        }
        
        # Generate quality of life indicators
        quality_of_life = {
            'life_satisfaction': random.randint(1, 10),
            'independence_level': random.randint(1, 10),
            'social_support': random.randint(1, 10),
            'financial_security': random.randint(1, 10),
            'access_to_care': random.randint(1, 10)
        }
        
        return {
            **activities,
            **weekly_patterns,
            **cognitive_scores,
            **quality_of_life,
            'technology_comfort': random.randint(1, 10),
            'caregiver_support': random.choice([True, False]),
            'emergency_contacts': random.randint(0, 5),
            'last_fall_incident': random.choice([None, '1_month_ago', '3_months_ago', '6_months_ago', '1_year_ago']),
            'wandering_incidents': random.randint(0, 10),
            'agitation_episodes': random.randint(0, 20),
            'sleep_quality': random.randint(1, 10),
            'appetite_level': random.randint(1, 10),
            'energy_level': random.randint(1, 10)
        }

    def generate_clinical_scenarios(
        self,
        scenario_type: str = 'mixed',
        num_patients: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Generate specific clinical scenarios for testing.
        
        Args:
            scenario_type (str): Type of scenario ('mild_cognitive_impairment', 'early_alzheimer', 'moderate_alzheimer', 'mixed')
            num_patients (int): Number of patients to generate
            
        Returns:
            List[Dict[str, Any]]: List of patient data for the specified scenario
        """
        if scenario_type == 'mild_cognitive_impairment':
            return self.generate_synthetic_data(
                num_patients=num_patients,
                cognitive_score_range=(20.0, 26.0),
                mood_score_range=(6.0, 9.0),
                sleep_hours_range=(6.0, 8.0),
                medication_adherence_range=(0.7, 0.9),
                social_interaction_range=(6.0, 9.0)
            )
        elif scenario_type == 'early_alzheimer':
            return self.generate_synthetic_data(
                num_patients=num_patients,
                cognitive_score_range=(15.0, 23.0),
                mood_score_range=(4.0, 7.0),
                sleep_hours_range=(5.0, 7.5),
                medication_adherence_range=(0.6, 0.8),
                social_interaction_range=(4.0, 7.0)
            )
        elif scenario_type == 'moderate_alzheimer':
            return self.generate_synthetic_data(
                num_patients=num_patients,
                cognitive_score_range=(10.0, 20.0),
                mood_score_range=(3.0, 6.0),
                sleep_hours_range=(4.0, 7.0),
                medication_adherence_range=(0.5, 0.7),
                social_interaction_range=(2.0, 6.0)
            )
        else:  # mixed
            return self.generate_synthetic_data(num_patients=num_patients)

    def generate_temporal_data(
        self,
        patient_id: int,
        num_visits: int = 12,
        months_between_visits: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate temporal data for a single patient over multiple visits.
        
        Args:
            patient_id (int): Patient ID
            num_visits (int): Number of visits to generate
            months_between_visits (int): Months between each visit
            
        Returns:
            List[Dict[str, Any]]: List of visit data over time
        """
        temporal_data = []
        base_date = datetime.now() - timedelta(days=months_between_visits * 30 * num_visits)
        
        # Generate baseline values
        baseline_cognitive = random.uniform(15.0, 25.0)
        baseline_mood = random.uniform(5.0, 8.0)
        
        for visit in range(num_visits):
            visit_date = base_date + timedelta(days=visit * months_between_visits * 30)
            
            # Simulate disease progression (gradual decline)
            progression_factor = visit / (num_visits - 1) if num_visits > 1 else 0
            
            # Add some random variation
            cognitive_variation = random.uniform(-2.0, 2.0)
            mood_variation = random.uniform(-1.0, 1.0)
            
            visit_data = {
                'patient_id': patient_id,
                'visit_date': visit_date.strftime('%Y-%m-%d'),
                'visit_number': visit + 1,
                'cognitive_score': max(5.0, baseline_cognitive - (progression_factor * 5) + cognitive_variation),
                'mood_score': max(1.0, baseline_mood - (progression_factor * 2) + mood_variation),
                'sleep_hours': random.uniform(5.0, 8.0),
                'medication_adherence': random.uniform(0.6, 0.9),
                'social_interaction_score': random.uniform(3.0, 8.0),
                'weight': random.uniform(50.0, 90.0),
                'blood_pressure_systolic': random.randint(110, 160),
                'blood_pressure_diastolic': random.randint(70, 90),
                'notes': f"Visit {visit + 1} - Patient showing {'stable' if random.random() > 0.3 else 'some decline'} in cognitive function."
            }
            
            temporal_data.append(visit_data)
        
        return temporal_data

    def export_generated_data(
        self,
        data: List[Dict[str, Any]],
        filename: str = 'generated_patient_data.csv',
        format: str = 'csv'
    ) -> str:
        """
        Export generated data to a file.
        
        Args:
            data (List[Dict[str, Any]]): Data to export
            filename (str): Output filename
            format (str): Export format ('csv', 'json', 'excel')
            
        Returns:
            str: Path to the exported file
        """
        df = pd.DataFrame(data)
        
        if format.lower() == 'csv':
            df.to_csv(filename, index=False)
        elif format.lower() == 'json':
            df.to_json(filename, orient='records', indent=2)
        elif format.lower() == 'excel':
            df.to_excel(filename, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filename

    def _prepare_features(self, patients_data: List[Dict[str, Any]]) -> np.ndarray:
        """
        Prepare patient features for similarity analysis.
        
        Args:
            patients_data (List[Dict]): List of patient data dictionaries
            
        Returns:
            np.ndarray: Prepared feature matrix
        """
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(patients_data)
        
        # Select relevant features for similarity
        features = [
            'age',
            'cognitive_score',
            'mood_score',
            'sleep_hours',
            'medication_adherence',
            'social_interaction_score'
        ]
        
        # Store feature names
        self.feature_names = features
        
        # Extract features and handle missing values
        X = df[features].fillna(df[features].mean())
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled

    def fit(self, patients_data: List[Dict[str, Any]]) -> None:
        """
        Fit the KNN model on patient data.
        
        Args:
            patients_data (List[Dict]): List of patient data dictionaries
        """
        X = self._prepare_features(patients_data)
        self.model.fit(X)
        self.is_fitted = True

    def find_similar_patients(
        self,
        patient_data: Dict[str, Any],
        patients_data: List[Dict[str, Any]]
    ) -> List[Tuple[int, float]]:
        """
        Find similar patients using KNN with cosine similarity.
        
        Args:
            patient_data (Dict): Data of the target patient
            patients_data (List[Dict]): List of all patients' data
            
        Returns:
            List[Tuple[int, float]]: List of (patient_index, similarity_score) tuples
        """
        if not self.is_fitted:
            self.fit(patients_data)
        
        # Prepare single patient data
        X = self._prepare_features([patient_data])
        
        # Find nearest neighbors
        distances, indices = self.model.kneighbors(X)
        
        # Convert distances to similarity scores (1 - normalized distance)
        similarities = 1 - (distances[0] / distances[0].max())
        
        # Return list of (index, similarity) tuples
        return list(zip(indices[0], similarities))

    def get_similarity_explanation(
        self,
        patient_data: Dict[str, Any],
        similar_patient_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Generate explanation of why two patients are similar.
        
        Args:
            patient_data (Dict): Data of the target patient
            similar_patient_data (Dict): Data of the similar patient
            
        Returns:
            Dict[str, float]: Dictionary of feature similarities
        """
        feature_similarities = {}
        
        for feature in self.feature_names:
            val1 = patient_data.get(feature, 0)
            val2 = similar_patient_data.get(feature, 0)
            
            # Calculate similarity for this feature
            similarity = 1 - abs(val1 - val2) / max(abs(val1), abs(val2), 1)
            feature_similarities[feature] = similarity
            
        return feature_similarities 
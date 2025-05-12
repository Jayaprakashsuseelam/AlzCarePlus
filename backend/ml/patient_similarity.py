import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Tuple
import pandas as pd

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
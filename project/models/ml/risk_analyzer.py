import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.preprocessing import StandardScaler

class RiskAnalyzer:
    def __init__(self):
        self.isolation_forest = IsolationForest(random_state=42)
        self.elliptic_envelope = EllipticEnvelope(random_state=42)
        self.scaler = StandardScaler()
        
    def analyze_risks(self, data):
        features = self.prepare_features(data)
        
        # Anomaly detection for risk scoring
        if_scores = self.isolation_forest.fit_predict(features)
        ee_scores = self.elliptic_envelope.fit_predict(features)
        
        # Convert to risk scores (0-1 range)
        if_risks = self.normalize_risks(if_scores)
        ee_risks = self.normalize_risks(ee_scores)
        
        # Environmental risk based on CO2 and Energy metrics
        env_risks = self.calculate_environmental_risks(data)
        
        # Financial risk based on investment and returns
        fin_risks = self.calculate_financial_risks(data)
        
        return {
            'risk_score': np.mean([if_risks, ee_risks], axis=0),
            'env_risk': env_risks,
            'fin_risk': fin_risks
        }
    
    def prepare_features(self, data):
        features = data[[
            'CO2 Reduction', 'Energy Savings', 
            'Investment (M)', 'Social Impact', 
            'Governance Score'
        ]]
        return self.scaler.fit_transform(features)
    
    def normalize_risks(self, scores):
        # Convert -1/1 predictions to 0-1 risk scores
        return (scores.max() - scores) / (scores.max() - scores.min())
    
    def calculate_environmental_risks(self, data):
        co2_impact = self.scaler.fit_transform(data[['CO2 Reduction']])
        energy_impact = self.scaler.fit_transform(data[['Energy Savings']])
        return 1 - np.mean([co2_impact, energy_impact], axis=0).flatten()
    
    def calculate_financial_risks(self, data):
        investment = self.scaler.fit_transform(data[['Investment (M)']])
        governance = self.scaler.fit_transform(data[['Governance Score']])
        return 1 - np.mean([investment, governance], axis=0).flatten()
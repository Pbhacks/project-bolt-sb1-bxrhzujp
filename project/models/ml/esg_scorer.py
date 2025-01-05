import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

class ESGScorer:
    def __init__(self):
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.nn_model = MLPRegressor(hidden_layer_sizes=(100, 50), random_state=42)
        self.scaler = StandardScaler()
        
    def prepare_features(self, data):
        features = data[[
            'CO2 Reduction', 'Energy Savings', 
            'Social Impact', 'Governance Score',
            'Job Creation', 'Investment (M)'
        ]]
        return self.scaler.fit_transform(features)
        
    def train_models(self, X, y):
        self.rf_model.fit(X, y)
        self.gb_model.fit(X, y)
        self.nn_model.fit(X, y)
        
    def predict_ensemble(self, X):
        rf_pred = self.rf_model.predict(X)
        gb_pred = self.gb_model.predict(X)
        nn_pred = self.nn_model.predict(X)
        return np.mean([rf_pred, gb_pred, nn_pred], axis=0)
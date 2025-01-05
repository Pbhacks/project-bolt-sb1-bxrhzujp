import numpy as np
from scipy.optimize import minimize
from sklearn.preprocessing import StandardScaler

class PortfolioOptimizer:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def optimize(self, data, risk_tolerance=0.5):
        returns = self.calculate_expected_returns(data)
        risks = self.calculate_risks(data)
        n_assets = len(returns)
        
        # Optimization constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # weights sum to 1
            {'type': 'ineq', 'fun': lambda x: risk_tolerance - self.portfolio_risk(x, risks)}  # risk constraint
        ]
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial weights
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Optimize for maximum ESG impact and returns
        result = minimize(
            lambda x: -self.objective_function(x, returns, risks, risk_tolerance),
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def calculate_expected_returns(self, data):
        # Combine ESG metrics for return estimation
        metrics = data[[
            'CO2 Reduction', 'Energy Savings',
            'Social Impact', 'Governance Score'
        ]]
        normalized = self.scaler.fit_transform(metrics)
        return np.mean(normalized, axis=1)
    
    def calculate_risks(self, data):
        investment_size = self.scaler.fit_transform(data[['Investment (M)']])
        governance_score = self.scaler.fit_transform(data[['Governance Score']])
        return 1 - np.mean([investment_size, governance_score], axis=0).flatten()
    
    def portfolio_risk(self, weights, risks):
        return np.sum(weights * risks)
    
    def objective_function(self, weights, returns, risks, risk_tolerance):
        portfolio_return = np.sum(weights * returns)
        risk_penalty = self.portfolio_risk(weights, risks) / risk_tolerance
        return portfolio_return - risk_penalty
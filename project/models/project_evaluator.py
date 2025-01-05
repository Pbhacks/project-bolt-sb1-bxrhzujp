import pandas as pd
import numpy as np
from .ml.esg_scorer import ESGScorer
from .ml.risk_analyzer import RiskAnalyzer
from .ml.portfolio_optimizer import PortfolioOptimizer
from .data.esg_data_fetcher import ESGDataFetcher

class ProjectEvaluator:
    def __init__(self):
        self.data = None
        self.esg_scorer = ESGScorer()
        self.risk_analyzer = RiskAnalyzer()
        self.portfolio_optimizer = PortfolioOptimizer()
        self.data_fetcher = ESGDataFetcher()

    def load_sample_data(self):
        self.data = self.data_fetcher.fetch_real_data()

    def has_data(self):
        return self.data is not None

    def get_projects(self):
        return self.data

    def evaluate_projects(self):
        if self.data is None:
            return None

        # Prepare features and train models
        X = self.esg_scorer.prepare_features(self.data)
        y = np.random.random(len(self.data))  # Sample target for training
        self.esg_scorer.train_models(X, y)
        
        # Get ensemble predictions
        return self.esg_scorer.predict_ensemble(X)

    def optimize_portfolio(self):
        if self.data is None:
            return None
            
        return self.portfolio_optimizer.optimize(self.data)

    def get_expected_returns(self):
        if self.data is None:
            return None
        return self.portfolio_optimizer.calculate_expected_returns(self.data)

    def get_risks(self):
        if self.data is None:
            return None
        return self.portfolio_optimizer.calculate_risks(self.data)

    def analyze_risks(self):
        if self.data is None:
            return None

        risk_metrics = self.risk_analyzer.analyze_risks(self.data)
        return {
            'project': self.data['Project Name'],
            'risk_score': risk_metrics['risk_score'],
            'env_risk': risk_metrics['env_risk'],
            'fin_risk': risk_metrics['fin_risk']
        }
import pandas as pd
import numpy as np
import json
from pandas import json_normalize
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

    def get_data(self):
        """Returns the data stored in the evaluator."""
        return self.data

    def save_data_to_csv(self, file_path):
        """Saves the data to a CSV file."""
        if self.data is not None:
            self.data.to_csv(file_path, index=False)
            return f"Data saved to {file_path}"
        else:
            return "No data available to save."

    def set_data_from_json(self, file_path):
        """Sets the data from a JSON file."""
        try:
            # Load data from JSON file
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            
            # Log the raw JSON data for inspection
            print("Raw JSON data loaded:", json_data)

            # Handle cases where JSON is a list of dictionaries
            if isinstance(json_data, list) and isinstance(json_data[0], dict):
                # Convert JSON data to DataFrame
                self.data = pd.DataFrame(json_data)
                return f"Data loaded from {file_path}"

            # Handle nested JSON (try flattening it)
            print("Attempting to normalize JSON structure...")
            normalized_data = json_normalize(json_data)
            self.data = normalized_data
            return f"Data loaded and normalized from {file_path}"

        except Exception as e:
            return f"Error loading data from JSON: {str(e)}"

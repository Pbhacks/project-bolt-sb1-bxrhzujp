"""Constants for ESG data processing"""

# API Endpoints
ESG_ENDPOINTS = {
    'environmental': 'https://api.esgdata.org/environmental',
    'social': 'https://api.esgdata.org/social',
    'governance': 'https://api.esgdata.org/governance'
}

# Scoring weights
ESG_WEIGHTS = {
    'CO2 Reduction': 0.3,
    'Energy Savings': 0.2,
    'Job Creation': 0.15,
    'Social Impact': 0.15,
    'Governance Score': 0.2
}

# Default values
DEFAULT_PROJECT_COUNT = 10
DEFAULT_RISK_TOLERANCE = 0.5

# Data ranges
DATA_RANGES = {
    'CO2 Reduction': (100, 1000),
    'Energy Savings': (10, 50),
    'Job Creation': (10, 100),
    'Social Impact': (1, 10),
    'Governance Score': (5, 10),
    'Investment': (1, 10)
}
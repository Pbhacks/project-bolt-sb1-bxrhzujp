import numpy as np
import pandas as pd

def normalize_data(data, columns):
    """Normalize specified columns to 0-1 range"""
    result = data.copy()
    for col in columns:
        min_val = data[col].min()
        max_val = data[col].max()
        result[col] = (data[col] - min_val) / (max_val - min_val)
    return result

def calculate_weighted_score(data, weights):
    """Calculate weighted score based on multiple metrics"""
    score = 0
    for col, weight in weights.items():
        score += data[col] * weight
    return score

def generate_project_names(n):
    """Generate sequential project names"""
    return [f'Project {i+1}' for i in range(n)]
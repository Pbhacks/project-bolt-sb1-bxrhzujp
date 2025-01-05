from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
    QTabWidget, QPushButton, QLabel, QFileDialog)
from .tabs.project_scoring_tab import ProjectScoringTab
from .tabs.portfolio_optimization_tab import PortfolioOptimizationTab
from .tabs.risk_analysis_tab import RiskAnalysisTab
from models.project_evaluator import ProjectEvaluator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Green Finance AI Platform")
        self.setGeometry(100, 100, 1200, 800)
        self.project_evaluator = ProjectEvaluator()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        tab_widget = QTabWidget()
        
        # Add tabs
        self.project_scoring_tab = ProjectScoringTab(self.project_evaluator)
        self.portfolio_tab = PortfolioOptimizationTab(self.project_evaluator)
        self.risk_tab = RiskAnalysisTab(self.project_evaluator)

        tab_widget.addTab(self.project_scoring_tab, "Project Scoring")
        tab_widget.addTab(self.portfolio_tab, "Portfolio Optimization")
        tab_widget.addTab(self.risk_tab, "Risk Analysis")

        layout.addWidget(tab_widget)
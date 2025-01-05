from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RiskAnalysisTab(QWidget):
    def __init__(self, project_evaluator):
        super().__init__()
        self.project_evaluator = project_evaluator
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Risk analysis controls
        self.analyze_btn = QPushButton("Analyze Risks")
        self.analyze_btn.clicked.connect(self.analyze_risks)
        layout.addWidget(self.analyze_btn)

        # Matplotlib figure for risk visualization
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Risk metrics table
        self.table = QTableWidget()
        layout.addWidget(self.table)

    def analyze_risks(self):
        if self.project_evaluator.has_data():
            risk_metrics = self.project_evaluator.analyze_risks()
            self.update_visualization(risk_metrics)
            self.update_table(risk_metrics)

    def update_visualization(self, risk_metrics):
        self.ax.clear()
        # Create risk heatmap
        projects = self.project_evaluator.get_projects()
        risks = risk_metrics['risk_score']
        self.ax.bar(range(len(risks)), risks)
        self.ax.set_xlabel('Projects')
        self.ax.set_ylabel('Risk Score')
        self.ax.set_title('Project Risk Analysis')
        plt.xticks(range(len(risks)), projects['Project Name'], rotation=45)
        self.canvas.draw()

    def update_table(self, risk_metrics):
        self.table.setRowCount(len(risk_metrics))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Project", "Risk Score", "Environmental Risk", "Financial Risk"
        ])

        for i in range(len(risk_metrics)):
            self.table.setItem(i, 0, QTableWidgetItem(risk_metrics['project'][i]))
            self.table.setItem(i, 1, QTableWidgetItem(f"{risk_metrics['risk_score'][i]:.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{risk_metrics['env_risk'][i]:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{risk_metrics['fin_risk'][i]:.2f}"))
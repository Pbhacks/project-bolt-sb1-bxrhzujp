from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PortfolioOptimizationTab(QWidget):
    def __init__(self, project_evaluator):
        super().__init__()
        self.project_evaluator = project_evaluator
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Optimization controls
        self.optimize_btn = QPushButton("Optimize Portfolio")
        self.optimize_btn.clicked.connect(self.optimize_portfolio)
        layout.addWidget(self.optimize_btn)

        # Matplotlib figure for efficient frontier
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Results table
        self.table = QTableWidget()
        layout.addWidget(self.table)

    def optimize_portfolio(self):
        if self.project_evaluator.has_data():
            weights = self.project_evaluator.optimize_portfolio()
            self.update_visualization(weights)
            self.update_table(weights)

    def update_visualization(self, weights):
        self.ax.clear()
        # Plot efficient frontier
        returns = self.project_evaluator.get_expected_returns()
        risks = self.project_evaluator.get_risks()
        self.ax.scatter(risks, returns)
        self.ax.set_xlabel('Risk')
        self.ax.set_ylabel('Expected Return')
        self.ax.set_title('Portfolio Optimization Results')
        self.canvas.draw()

    def update_table(self, weights):
        data = self.project_evaluator.get_projects()
        if data is None:
            return

        self.table.setRowCount(len(data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Project", "Weight", "Allocation"])

        for i in range(len(data)):
            self.table.setItem(i, 0, QTableWidgetItem(data.iloc[i]["Project Name"]))
            self.table.setItem(i, 1, QTableWidgetItem(f"{weights[i]:.2%}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"${weights[i] * 1000000:,.2f}"))
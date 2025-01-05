from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
import pandas as pd

class ProjectScoringTab(QWidget):
    def __init__(self, project_evaluator):
        super().__init__()
        self.project_evaluator = project_evaluator
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Controls
        controls_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Projects")
        self.load_btn.clicked.connect(self.load_projects)
        self.evaluate_btn = QPushButton("Evaluate Projects")
        self.evaluate_btn.clicked.connect(self.evaluate_projects)
        controls_layout.addWidget(self.load_btn)
        controls_layout.addWidget(self.evaluate_btn)
        layout.addLayout(controls_layout)

        # Results table
        self.table = QTableWidget()
        layout.addWidget(self.table)

    def load_projects(self):
        # In a real application, this would load actual project data
        self.project_evaluator.load_sample_data()
        self.update_table()

    def evaluate_projects(self):
        scores = self.project_evaluator.evaluate_projects()
        self.update_table(scores)

    def update_table(self, scores=None):
        data = self.project_evaluator.get_projects()
        if data is None:
            return

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns)

        for i in range(len(data)):
            for j in range(len(data.columns)):
                item = QTableWidgetItem(str(data.iloc[i, j]))
                self.table.setItem(i, j, item)

        if scores is not None:
            self.table.setColumnCount(len(data.columns) + 1)
            headers = list(data.columns) + ["ESG Score"]
            self.table.setHorizontalHeaderLabels(headers)
            for i, score in enumerate(scores):
                item = QTableWidgetItem(f"{score:.2f}")
                self.table.setItem(i, len(data.columns), item)
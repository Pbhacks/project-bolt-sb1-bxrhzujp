from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QPushButton, QLabel, QFileDialog,
    QStatusBar, QToolBar, QMenu, QMenuBar, QMessageBox,
    QSplitter, QFrame, QProgressBar, QDialog, QFormLayout,
    QSpinBox, QComboBox, QCheckBox, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer, QSettings, QSize
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont
import json
import pandas as pd
from pathlib import Path
from .tabs.project_scoring_tab import ProjectScoringTab
from .tabs.portfolio_optimization_tab import PortfolioOptimizationTab
from .tabs.risk_analysis_tab import RiskAnalysisTab
from models.project_evaluator import ProjectEvaluator

class ThemeManager:
   @staticmethod
   def get_dark_theme():
    return """
        QMainWindow, QDialog, QWidget {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        QTabWidget::pane {
            border: 1px solid #404040;
            background: #1a1a1a;
        }
        QWidget {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        QTabBar::tab {
            padding: 8px 16px;
            background: #2d2d2d;
            border: 1px solid #404040;
            color: #ffffff;
        }
        QTabBar::tab:selected {
            background: #404040;
            border-bottom: 2px solid #0d47a1;
        }
        QPushButton {
            background-color: #0d47a1;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1565c0;
        }
        QPushButton:pressed {
            background-color: #0a3d87;
        }
        QPushButton:disabled {
            background-color: #263238;
            color: #808080;
        }
        QFrame, QLabel, QToolTip {
            background: #1a1a1a;
            color: #ffffff;
            border: 1px solid #404040;
        }
        QMenuBar {
            background-color: #1a1a1a;
            color: #ffffff;
            border-bottom: 1px solid #404040;
        }
        QMenuBar::item {
            background-color: transparent;
        }
        QMenuBar::item:selected {
            background-color: #404040;
        }
        QMenu {
            background-color: #1a1a1a;
            color: #ffffff;
            border: 1px solid #404040;
        }
        QMenu::item:selected {
            background-color: #404040;
        }
        QStatusBar {
            background-color: #1a1a1a;
            color: #ffffff;
            border-top: 1px solid #404040;
        }
        QToolBar {
            background-color: #1a1a1a;
            border-bottom: 1px solid #404040;
        }
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #404040;
            padding: 5px;
            border-radius: 4px;
        }
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 1px solid #0d47a1;
        }
        QComboBox::drop-down {
            border: none;
            background: #404040;
        }
        QComboBox::down-arrow {
            background: #404040;
        }
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: #ffffff;
            selection-background-color: #404040;
        }
        QProgressBar {
            border: 1px solid #404040;
            background-color: #2d2d2d;
            text-align: center;
            color: #ffffff;
        }
        QProgressBar::chunk {
            background-color: #0d47a1;
        }
        QScrollBar:vertical {
            border: none;
            background-color: #1a1a1a;
            width: 12px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background-color: #404040;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #4a4a4a;
        }
        QScrollBar:horizontal {
            border: none;
            background-color: #1a1a1a;
            height: 12px;
            margin: 0;
        }
        QScrollBar::handle:horizontal {
            background-color: #404040;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #4a4a4a;
        }
        QHeaderView::section {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 5px;
            border: 1px solid #404040;
        }
        QTableView {
            background-color: #1a1a1a;
            color: #ffffff;
            gridline-color: #404040;
            selection-background-color: #404040;
            selection-color: #ffffff;
        }
        QTableView QTableCornerButton::section {
            background-color: #2d2d2d;
            border: 1px solid #404040;
        }
    """

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = QSettings('GreenFinanceAI', 'Platform')
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        current_theme = self.settings.value('theme', 'Light')
        self.theme_combo.setCurrentText(current_theme)
        layout.addRow("Theme:", self.theme_combo)

        # Auto-save settings
        self.autosave_check = QCheckBox()
        self.autosave_check.setChecked(self.settings.value('autosave', True, type=bool))
        layout.addRow("Auto-save:", self.autosave_check)

        # Auto-save interval
        self.autosave_interval = QSpinBox()
        self.autosave_interval.setRange(1, 60)
        self.autosave_interval.setValue(self.settings.value('autosave_interval', 5, type=int))
        layout.addRow("Auto-save interval (minutes):", self.autosave_interval)

        # API Settings
        self.api_key = QLineEdit()
        self.api_key.setText(self.settings.value('api_key', ''))
        layout.addRow("API Key:", self.api_key)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addRow(save_btn)

    def save_settings(self):
        self.settings.setValue('theme', self.theme_combo.currentText())
        self.settings.setValue('autosave', self.autosave_check.isChecked())
        self.settings.setValue('autosave_interval', self.autosave_interval.value())
        self.settings.setValue('api_key', self.api_key.text())
        
        # Apply theme
        self.parent.apply_theme(self.theme_combo.currentText())
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Green Finance AI Platform")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize settings
        self.settings = QSettings('GreenFinanceAI', 'Platform')
        self.project_evaluator = ProjectEvaluator()
        self.current_project_file = None
        self.unsaved_changes = False
        
        # Initialize UI components
        self.status_bar = None
        self.progress_bar = None
        self.tab_widget = None
        
        # Setup UI components - correct order is important
        self.setup_ui()
        self.setup_menubar()
        self.setup_toolbar()
        self.setup_statusbar()
        self.setup_autosave()
        
        # Apply saved theme
        self.apply_theme(self.settings.value('theme', 'Light'))
        
        # Show welcome message
        self.show_welcome_message()

    def setup_ui(self):
        """Setup the main UI components"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Initialize tab widget
        self.tab_widget = QTabWidget()
        self.project_scoring_tab = ProjectScoringTab(self.project_evaluator)
        self.portfolio_tab = PortfolioOptimizationTab(self.project_evaluator)
        self.risk_tab = RiskAnalysisTab(self.project_evaluator)

        self.tab_widget.addTab(self.project_scoring_tab, "Project Scoring")
        self.tab_widget.addTab(self.portfolio_tab, "Portfolio Optimization")
        self.tab_widget.addTab(self.risk_tab, "Risk Analysis")

        main_layout.addWidget(self.tab_widget)

    def apply_theme(self, theme_name):
        """Apply selected theme"""
        if theme_name == "Dark":
            self.setStyleSheet(ThemeManager.get_dark_theme())
        else:
            self.setStyleSheet(ThemeManager.get_light_theme())

    def setup_menubar(self):
        """Setup the menu bar"""
        # Create menubar if it doesn't exist
        if self.menuBar().isNativeMenuBar():
            menubar = QMenuBar(self)
            self.setMenuBar(menubar)
        else:
            menubar = self.menuBar()
        
        # Clear existing menus if any
        menubar.clear()
        
        # File menu
        file_menu = menubar.addMenu("File")
        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction("Open Project", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        import_action = QAction("Import Data", self)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        export_action = QAction("Export Results", self)
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        documentation_action = QAction("Documentation", self)
        documentation_action.triggered.connect(self.show_documentation)
        help_menu.addAction(documentation_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_toolbar(self):
        """Setup the toolbar"""
        # Remove existing toolbars if any
        for toolbar in self.findChildren(QToolBar):
            self.removeToolBar(toolbar)
            
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Add actions with icons
        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)

        open_action = QAction("Open Project", self)
        open_action.triggered.connect(self.open_project)
        toolbar.addAction(open_action)

        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)

    def setup_statusbar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximumSize(QSize(200, 20))
        self.status_bar.addPermanentWidget(self.progress_bar)

    def setup_autosave(self):
        """Setup auto-save timer"""
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.auto_save)
        
        if self.settings.value('autosave', True, type=bool):
            interval = self.settings.value('autosave_interval', 5, type=int)
            self.autosave_timer.start(interval * 60 * 1000)  # Convert minutes to milliseconds

    def auto_save(self):
        """Auto-save current project"""
        if self.current_project_file and self.unsaved_changes:
            self.save_project(self.current_project_file)
            self.status_bar.showMessage("Project auto-saved", 3000)
    def apply_theme(self, theme_name):
        """Apply selected theme"""
        if theme_name == "Dark":
            self.setStyleSheet(ThemeManager.get_dark_theme())
       

    def new_project(self):
        """Create new project"""
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                'Do you want to save your changes before creating a new project?',
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel)
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        self.current_project_file = None
        
        
        self.unsaved_changes = False
        self.status_bar.showMessage("New project created")

    def open_project(self):
        """Open existing project"""
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Unsaved Changes',
                'Do you want to save your changes before opening another project?',
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel)
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Project Files (*.json *.csv)"
        )
        if file_name:
            try:
                self.load_project(file_name)
                self.current_project_file = file_name
                self.unsaved_changes = False
                self.status_bar.showMessage(f"Opened project: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")

    def save_project(self, file_name=None):
        """Save current project"""
        if not file_name and not self.current_project_file:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Project", "", "Project Files (*.json)"
            )
        
        if file_name or self.current_project_file:
            try:
                save_path = file_name or self.current_project_file
                self.export_project_data(save_path)
                self.current_project_file = save_path
                self.unsaved_changes = False
                self.status_bar.showMessage(f"Project saved to: {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")

    def import_data(self):
        """Import data from external file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import Data", "", "Data Files (*.csv *.xlsx)"
        )
        if file_name:
            try:
                if file_name.endswith('.csv'):
                    data = pd.read_csv(file_name)
                else:
                    data = pd.read_excel(file_name)
                
                self.project_evaluator.set_data(data)
                self.update_ui_with_data()
                self.unsaved_changes = True
                self.status_bar.showMessage(f"Data imported from: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")

    def export_results(self):
        """Export analysis results"""
        file_name, file_type = QFileDialog.getSaveFileName(
            self, "Export Results", "", 
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        if file_name:
            try:
                results = self.project_evaluator.get_results()
                if file_name.endswith('.csv'):
                    results.to_csv(file_name, index=False)
                else:
                    results.to_excel(file_name, index=False)
                self.status_bar.showMessage(f"Results exported to: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export results: {str(e)}")

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()

    def show_help(self):
        """Show help documentation"""
        help_text = """
        Green Finance AI Platform Help
        
        1. Project Management:
           - Create new projects
           - Open existing projects
           - Save projects
           
        2. Data Management:
           - Import data from CSV/Excel
           - Export results
           
        3. Analysis Features:
           - Project Scoring
           - Portfolio Optimization
           - Risk Analysis
           
        For more information, visit our documentation.
        """
        QMessageBox.information(self, "Help", help_text)

    def show_documentation(self):
        """Show detailed documentation"""
        # Here you would typically open a more comprehensive help system
        # For now, we'll just show a message
        QMessageBox.information(self, "Documentation", 
            "Full documentation available at: https://greenfinanceai.docs")

    def show_about(self):
        """Show about dialog"""
        about_text = """
        Green Finance AI Platform
        Version 1.0
        
        A comprehensive tool for ESG project evaluation 
        and portfolio optimization.
        
        © 2024 Green Finance AI
        """
        QMessageBox.about(self, "About", about_text)

    def update_ui_for_new_project(self):
        """Update UI elements for new project"""
        
        self.portfolio_tab.reset()
        self.risk_tab.reset()
        self.update_header_stats()

    def update_ui_with_data(self):
        """Update UI elements with new data"""
        self.project_scoring_tab.update_data()
        self.portfolio_tab.update_data()
        self.risk_tab.update_data()
        self.update_header_stats()

    def update_header_stats(self):
        """Update header statistics"""
        stats = self.project_evaluator.get_summary_stats()
        # Update stats in header (implement based on your header structure)

    def export_project_data(self, file_path):
        """Export project data to file"""
        data = {
            'project_data': self.project_evaluator.get_data().to_dict(),
            'settings': {
                'autosave': self.settings.value('autosave'),
                'theme': self.settings.value('theme')
            }
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_project(self, file_path):
        """Load project data from file"""
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.project_evaluator.set_data(pd.DataFrame(data['project_data']))
            self.apply_theme(data['settings']['theme'])
            self.setup_autosave()
            self.update_ui_with_data()

    def setup_ui(self):
        """Setup the main UI components"""
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Initialize tab widget
        self.tab_widget = QTabWidget(self)
        self.project_scoring_tab = ProjectScoringTab(self.project_evaluator)
        self.portfolio_tab = PortfolioOptimizationTab(self.project_evaluator)
        self.risk_tab = RiskAnalysisTab(self.project_evaluator)

        self.tab_widget.addTab(self.project_scoring_tab, "Project Scoring")
        self.tab_widget.addTab(self.portfolio_tab, "Portfolio Optimization")
        self.tab_widget.addTab(self.risk_tab, "Risk Analysis")

        layout.addWidget(self.tab_widget)
        self.setCentralWidget(central_widget)

    def setup_menubar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        new_action = QAction(QIcon(), "New Project", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon(), "Open Project", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon(), "Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        import_action = QAction(QIcon(), "Import Data", self)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        export_action = QAction(QIcon(), "Export Results", self)
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction(QIcon(), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        settings_action = QAction(QIcon(), "Settings", self)
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_action = QAction(QIcon(), "Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        documentation_action = QAction(QIcon(), "Documentation", self)
        documentation_action.triggered.connect(self.show_documentation)
        help_menu.addAction(documentation_action)

        about_action = QAction(QIcon(), "About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(16, 16))

        new_action = QAction(QIcon(), "New Project", self)
        new_action.triggered.connect(self.new_project)
        toolbar.addAction(new_action)

        open_action = QAction(QIcon(), "Open Project", self)
        open_action.triggered.connect(self.open_project)
        toolbar.addAction(open_action)

        save_action = QAction(QIcon(), "Save Project", self)
        save_action.triggered.connect(self.save_project)
        toolbar.addAction(save_action)

        import_action = QAction(QIcon(), "Import Data", self)
        import_action.triggered.connect(self.import_data)
        toolbar.addAction(import_action)

        export_action = QAction(QIcon(), "Export Results", self)
        export_action.triggered.connect(self.export_results)
        toolbar.addAction(export_action)

        self.addToolBar(toolbar)

    def setup_statusbar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.setStatusBar(self.status_bar)

    def show_welcome_message(self):
        """Show welcome message in the status bar"""
        self.status_bar.showMessage("Welcome to Green Finance AI Platform", 5000)

# Run the application
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

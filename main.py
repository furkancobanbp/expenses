import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from models.finance_manager import FinanceManager
from controllers.app_controller import AppController
from views.main_window import MainWindow

def main():
    # Set application attributes
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setStyle("Fusion")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application stylesheet for a more modern, sleek look
    app.setStyleSheet("""
        /* Main Application */
        QMainWindow {
            background-color: #f8f9fa;
        }
        
        /* Typography */
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #212529;
        }
        
        QLabel {
            font-size: 13px;
        }
        
        /* Header */
        QLabel[objectName="header"] {
            font-size: 18px;
            font-weight: bold;
            color: #3a4f9b;
            padding: 5px;
            max-height: 30px;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-size: 13px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 8px;
            background-color: #ffffff;
            color: #3a4f9b;
            /* Box shadow effect */
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            top: -8px;
            padding: 0 5px;
            background-color: #ffffff;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 500;
            color: #495057;
            min-height: 30px;
        }
        
        QPushButton:hover {
            background-color: #e9ecef;
            border-color: #ced4da;
        }
        
        QPushButton:pressed {
            background-color: #dee2e6;
        }
        
        /* Primary Action Button */
        QPushButton[objectName="primaryButton"] {
            background-color: #3a4f9b;
            color: white;
            border: none;
        }
        
        QPushButton[objectName="primaryButton"]:hover {
            background-color: #2c3e80;
        }
        
        QPushButton[objectName="primaryButton"]:pressed {
            background-color: #233170;
        }
        
        /* Form Controls */
        QComboBox, QLineEdit, QDateEdit {
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 6px;
            background-color: white;
            font-size: 13px;
            min-height: 25px;
            selection-background-color: #3a4f9b;
        }
        
        QComboBox:focus, QLineEdit:focus, QDateEdit:focus {
            border: 2px solid #3a4f9b;
            padding: 5px;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 25px;
        }
        
        QComboBox::down-arrow {
            width: 10px;
            height: 10px;
            image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="%233a4f9b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>');
        }
        
        QDateEdit::drop-down {
            border: none;
            width: 25px;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: none;
            background-color: #ffffff;
            border-radius: 8px;
            padding: 2px;
            /* Box shadow effect */
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        QTabBar::tab {
            background-color: #e9ecef;
            border: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            min-width: 80px;
            padding: 8px 15px;
            font-size: 13px;
            font-weight: 500;
            color: #6c757d;
            margin-right: 3px;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
            color: #3a4f9b;
            font-weight: bold;
            /* Subtle bottom border indicator */
            border-bottom: 3px solid #3a4f9b;
        }
        
        QTabBar::tab:!selected {
            margin-top: 3px;
        }
        
        QTabBar::tab:hover {
            background-color: #dee2e6;
        }
        
        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background: #f8f9fa;
            width: 8px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #ced4da;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #adb5bd;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        /* Form styles */
        QFormLayout {
            spacing: 12px;
        }
        
        /* Value displays (income, expense, net worth) */
        QLabel[objectName="valueLabel"] {
            font-size: 18px;
            font-weight: bold;
            padding: 3px;
            border-radius: 4px;
        }
    """)
    
    # Initialize models, controllers, and views
    finance_manager = FinanceManager("finance_data.json")
    controller = AppController(finance_manager)
    main_window = MainWindow(controller)
    
    # Show main window
    main_window.show()
    
    # Run application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
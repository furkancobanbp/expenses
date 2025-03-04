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
            font-size: 14px;
        }
        
        /* Header */
        QLabel[objectName="header"] {
            font-size: 26px;
            font-weight: bold;
            color: #3a4f9b;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            margin-top: 15px;
            padding-top: 10px;
            background-color: #ffffff;
            color: #3a4f9b;
            /* Box shadow effect */
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            top: -10px;
            padding: 0 7px;
            background-color: #ffffff;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            color: #495057;
            min-height: 38px;
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
            border-radius: 6px;
            padding: 10px;
            background-color: white;
            font-size: 14px;
            min-height: 25px;
            selection-background-color: #3a4f9b;
        }
        
        QComboBox:focus, QLineEdit:focus, QDateEdit:focus {
            border: 2px solid #3a4f9b;
            padding: 9px;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            width: 12px;
            height: 12px;
            image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="%233a4f9b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>');
        }
        
        QDateEdit::drop-down {
            border: none;
            width: 30px;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: none;
            background-color: #ffffff;
            border-radius: 10px;
            padding: 5px;
            /* Box shadow effect */
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        QTabBar::tab {
            background-color: #e9ecef;
            border: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 100px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 500;
            color: #6c757d;
            margin-right: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
            color: #3a4f9b;
            font-weight: bold;
            /* Subtle bottom border indicator */
            border-bottom: 3px solid #3a4f9b;
        }
        
        QTabBar::tab:!selected {
            margin-top: 4px;
        }
        
        QTabBar::tab:hover {
            background-color: #dee2e6;
        }
        
        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background: #f8f9fa;
            width: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #ced4da;
            border-radius: 5px;
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
            spacing: 15px;
        }
        
        /* Value displays (income, expense, net worth) */
        QLabel[objectName="valueLabel"] {
            font-size: 22px;
            font-weight: bold;
            padding: 5px;
            border-radius: 6px;
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
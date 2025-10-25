# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from ui.main_window import MainWindow

def main():
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
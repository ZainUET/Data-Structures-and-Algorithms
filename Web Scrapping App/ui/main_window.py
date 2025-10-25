# ui/main_window.py
import sys
import os
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableView, QComboBox, QLineEdit,
                             QLabel, QProgressBar, QTabWidget, QGroupBox,
                             QCheckBox, QSpinBox, QSplitter, QHeaderView,
                             QMessageBox, QFileDialog, QMenu, QAction, QApplication,
                             QTableWidget, QTableWidgetItem, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# Add the core directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.database import ProjectDatabase
from core.scraper import AdvancedScraper
from core.sorting_algorithms import SortingAlgorithms

class ScrapingThread(QThread):
    """Thread for scraping to prevent GUI freezing"""
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, scraper, target_count, url):
        super().__init__()
        self.scraper = scraper
        self.target_count = target_count
        self.url = url

    def run(self):
        try:
            self.scraper.target_count = self.target_count
            success = self.scraper.scrape_from_website(self.url)
            if success:
                self.finished.emit()
            else:
                self.error_occurred.emit("Scraping failed - no data retrieved")
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS200 - Advanced Data Scraper & Analyzer")
        self.setGeometry(100, 50, 1400, 900)
        
        # Initialize components
        self.database = ProjectDatabase()
        self.scraper = AdvancedScraper(self.database.db_path)
        self.sorting_algorithms = SortingAlgorithms()
        self.current_data = []
        
        self.setup_ui()
        self.setup_connections()
        
        # Timer for progress updates
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        
        # Initialize algorithm info
        self.update_algorithm_info()
    
    def setup_ui(self):
        """Create the main user interface"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header section
        header_label = QLabel("CS200 - Data Structures & Algorithms Project")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setStyleSheet("padding: 15px; background-color: #2c3e50; color: white; border-radius: 5px;")
        main_layout.addWidget(header_label)
        
        # Create tabs for different functionalities
        self.tabs = QTabWidget()
        
        # Data Management Tab
        self.data_tab = QWidget()
        self.setup_data_tab()
        self.tabs.addTab(self.data_tab, "📊 Data Management")
        
        # Sorting Tab
        self.sorting_tab = QWidget()
        self.setup_sorting_tab()
        self.tabs.addTab(self.sorting_tab, "🔢 Sorting Algorithms")
        
        # Search Tab
        self.search_tab = QWidget()
        self.setup_search_tab()
        self.tabs.addTab(self.search_tab, "🔍 Search & Filter")
        
        main_layout.addWidget(self.tabs)
        
        # Status label
        self.status_label = QLabel("Ready to start. Enter a website URL and click 'Start Scraping'.")
        self.status_label.setStyleSheet("padding: 10px; background-color: #ecf0f1; border-radius: 5px; border-left: 5px solid #3498db;")
        main_layout.addWidget(self.status_label)
    
    def setup_data_tab(self):
        """Setup the data management tab"""
        layout = QVBoxLayout(self.data_tab)
        
        # Scraping control section
        scraping_group = QGroupBox("Web Scraping Controls")
        scraping_layout = QVBoxLayout(scraping_group)
        
        # URL Input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Website URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., http://books.toscrape.com)")
        self.url_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.url_input.setText("http://books.toscrape.com")  # Default URL
        url_layout.addWidget(self.url_input)
        
        # Supported websites info
        self.supported_btn = QPushButton("ℹ️ Supported Sites")
        self.supported_btn.setStyleSheet("padding: 8px; background-color: #3498db; color: white; border-radius: 4px;")
        self.supported_btn.clicked.connect(self.show_supported_websites)
        url_layout.addWidget(self.supported_btn)
        
        scraping_layout.addLayout(url_layout)
        
        # Target count
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Target Entity Count:"))
        self.target_spinbox = QSpinBox()
        self.target_spinbox.setRange(100, 100000)
        self.target_spinbox.setValue(1000)  # Start with smaller number for testing
        self.target_spinbox.setStyleSheet("padding: 5px;")
        count_layout.addWidget(self.target_spinbox)
        
        count_layout.addWidget(QLabel("Current Count:"))
        self.current_count_label = QLabel("0")
        self.current_count_label.setStyleSheet("padding: 5px; background-color: #f8f9fa; border: 1px solid #ddd;")
        count_layout.addWidget(self.current_count_label)
        
        count_layout.addStretch()
        scraping_layout.addLayout(count_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("🚀 Start Scraping")
        self.pause_btn = QPushButton("⏸️ Pause")
        self.resume_btn = QPushButton("▶️ Resume")
        self.stop_btn = QPushButton("🛑 Stop")
        self.load_btn = QPushButton("📥 Load Data")
        
        # Style buttons
        button_style = """
            QPushButton {
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """
        
        self.start_btn.setStyleSheet(button_style + "background-color: #27ae60; color: white;")
        self.pause_btn.setStyleSheet(button_style + "background-color: #f39c12; color: white;")
        self.resume_btn.setStyleSheet(button_style + "background-color: #3498db; color: white;")
        self.stop_btn.setStyleSheet(button_style + "background-color: #e74c3c; color: white;")
        self.load_btn.setStyleSheet(button_style + "background-color: #9b59b6; color: white;")
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.resume_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.load_btn)
        
        scraping_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-size: 12px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 3px;
            }
        """)
        scraping_layout.addWidget(self.progress_bar)
        
        layout.addWidget(scraping_group)
        
        # Data table
        table_group = QGroupBox("Data Preview (First 100 Records)")
        table_layout = QVBoxLayout(table_group)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(10)  # Show most important columns
        self.data_table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Year", "Price", "Rating", 
            "Pages", "Category", "Stock", "Format"
        ])
        
        # Style the table
        self.data_table.setStyleSheet("""
            QTableWidget {
                font-size: 11px;
                gridline-color: #bdc3c7;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 6px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        self.data_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Title column
        table_layout.addWidget(self.data_table)
        
        layout.addWidget(table_group)
    
    def setup_sorting_tab(self):
        """Setup the sorting algorithms tab"""
        layout = QVBoxLayout(self.sorting_tab)
        
        # Sorting controls
        sorting_group = QGroupBox("Sorting Configuration")
        sorting_layout = QVBoxLayout(sorting_group)
        
        # Multi-level sorting setup
        multi_level_layout = QHBoxLayout()
        multi_level_layout.addWidget(QLabel("Multi-Level Sorting:"))
        
        self.level1_combo = QComboBox()
        self.level1_combo.addItem("Select first level...", None)
        self.level2_combo = QComboBox()
        self.level2_combo.addItem("Select second level...", None)
        self.level3_combo = QComboBox()
        self.level3_combo.addItem("Select third level...", None)
        
        multi_level_layout.addWidget(self.level1_combo)
        multi_level_layout.addWidget(self.level2_combo)
        multi_level_layout.addWidget(self.level3_combo)
        
        sorting_layout.addLayout(multi_level_layout)
        
        # Algorithm selection
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Primary Algorithm:"))
        
        self.algo_combo = QComboBox()
        algorithms = SortingAlgorithms.get_algorithm_info()
        for algo_key, algo_info in algorithms.items():
            self.algo_combo.addItem(algo_info["name"], algo_key)
        
        self.algo_combo.setStyleSheet("padding: 8px; font-size: 14px; min-width: 150px;")
        algo_layout.addWidget(self.algo_combo)
        
        # Sort order
        algo_layout.addWidget(QLabel("Order:"))
        self.order_combo = QComboBox()
        self.order_combo.addItems(["Ascending", "Descending"])
        self.order_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        algo_layout.addWidget(self.order_combo)
        
        # Sort button
        self.sort_btn = QPushButton("🔢 Sort Data")
        self.sort_btn.setStyleSheet("padding: 10px 20px; background-color: #9b59b6; color: white; font-weight: bold; border-radius: 5px;")
        algo_layout.addWidget(self.sort_btn)
        
        sorting_layout.addLayout(algo_layout)
        
        # Algorithm info
        algo_info_group = QGroupBox("Algorithm Information")
        algo_info_layout = QVBoxLayout(algo_info_group)
        
        self.algo_info_text = QTextEdit()
        self.algo_info_text.setReadOnly(True)
        self.algo_info_text.setMaximumHeight(120)
        self.algo_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        algo_info_layout.addWidget(self.algo_info_text)
        
        sorting_layout.addWidget(algo_info_group)
        
        # Results section
        results_group = QGroupBox("Sorting Results")
        results_layout = QVBoxLayout(results_group)
        
        results_info_layout = QHBoxLayout()
        results_info_layout.addWidget(QLabel("Sorting Time:"))
        self.time_label = QLabel("-- ms")
        self.time_label.setStyleSheet("padding: 5px; background-color: #e8f6f3; border-radius: 3px;")
        results_info_layout.addWidget(self.time_label)
        
        results_info_layout.addWidget(QLabel("Records Sorted:"))
        self.sorted_count_label = QLabel("0")
        self.sorted_count_label.setStyleSheet("padding: 5px; background-color: #e8f6f3; border-radius: 3px;")
        results_info_layout.addWidget(self.sorted_count_label)
        
        results_info_layout.addStretch()
        results_layout.addLayout(results_info_layout)
        
        # Sorted data table
        self.sorted_table = QTableWidget()
        self.sorted_table.setColumnCount(10)
        self.sorted_table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Year", "Price", "Rating", 
            "Pages", "Category", "Stock", "Format"
        ])
        self.sorted_table.setStyleSheet("""
            QTableWidget {
                font-size: 11px;
                gridline-color: #bdc3c7;
            }
            QHeaderView::section {
                background-color: #27ae60;
                color: white;
                padding: 6px;
                font-weight: bold;
                border: none;
            }
        """)
        self.sorted_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        results_layout.addWidget(self.sorted_table)
        
        sorting_layout.addWidget(results_group)
        layout.addWidget(sorting_group)
    
    def setup_search_tab(self):
        """Setup the search and filter tab"""
        layout = QVBoxLayout(self.search_tab)
        
        # Search controls
        search_group = QGroupBox("Search & Filter")
        search_layout = QVBoxLayout(search_group)
        
        # Search term
        search_term_layout = QHBoxLayout()
        search_term_layout.addWidget(QLabel("Search Term:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setStyleSheet("padding: 8px; font-size: 14px;")
        search_term_layout.addWidget(self.search_input)
        
        search_term_layout.addWidget(QLabel("Search in:"))
        self.search_column_combo = QComboBox()
        self.search_column_combo.addItem("All Columns", "all")
        search_term_layout.addWidget(self.search_column_combo)
        
        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.setStyleSheet("padding: 8px 15px; background-color: #3498db; color: white; border-radius: 4px;")
        search_term_layout.addWidget(self.search_btn)
        
        search_layout.addLayout(search_term_layout)
        
        # Advanced filters
        filters_group = QGroupBox("Advanced Filters")
        filters_layout = QVBoxLayout(filters_group)
        
        # Price filter
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Price Range:"))
        self.min_price = QLineEdit()
        self.min_price.setPlaceholderText("Min")
        self.min_price.setStyleSheet("padding: 5px;")
        price_layout.addWidget(self.min_price)
        
        price_layout.addWidget(QLabel("to"))
        self.max_price = QLineEdit()
        self.max_price.setPlaceholderText("Max")
        self.max_price.setStyleSheet("padding: 5px;")
        price_layout.addWidget(self.max_price)
        
        price_layout.addStretch()
        filters_layout.addLayout(price_layout)
        
        # Rating filter
        rating_layout = QHBoxLayout()
        rating_layout.addWidget(QLabel("Minimum Rating:"))
        self.min_rating = QComboBox()
        self.min_rating.addItems(["Any", "3.0+", "3.5+", "4.0+", "4.5+"])
        self.min_rating.setStyleSheet("padding: 5px;")
        rating_layout.addWidget(self.min_rating)
        
        rating_layout.addStretch()
        filters_layout.addLayout(rating_layout)
        
        search_layout.addWidget(filters_group)
        
        # Search results
        results_group = QGroupBox("Search Results")
        results_layout = QVBoxLayout(results_group)
        
        results_info_layout = QHBoxLayout()
        results_info_layout.addWidget(QLabel("Found:"))
        self.found_count_label = QLabel("0 records")
        self.found_count_label.setStyleSheet("padding: 5px; background-color: #d5dbdb; border-radius: 3px;")
        results_info_layout.addWidget(self.found_count_label)
        results_info_layout.addStretch()
        
        results_layout.addLayout(results_info_layout)
        
        self.search_table = QTableWidget()
        self.search_table.setColumnCount(10)
        self.search_table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Year", "Price", "Rating", 
            "Pages", "Category", "Stock", "Format"
        ])
        self.search_table.setStyleSheet("""
            QTableWidget {
                font-size: 11px;
                gridline-color: #bdc3c7;
            }
            QHeaderView::section {
                background-color: #e67e22;
                color: white;
                padding: 6px;
                font-weight: bold;
                border: none;
            }
        """)
        self.search_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        results_layout.addWidget(self.search_table)
        
        search_layout.addWidget(results_group)
        layout.addWidget(search_group)
    
    def setup_connections(self):
        """Connect signals and slots"""
        # Data tab connections
        self.start_btn.clicked.connect(self.start_scraping)
        self.pause_btn.clicked.connect(self.pause_scraping)
        self.resume_btn.clicked.connect(self.resume_scraping)
        self.stop_btn.clicked.connect(self.stop_scraping)
        self.load_btn.clicked.connect(self.load_data)
        
        # Sorting tab connections
        self.sort_btn.clicked.connect(self.sort_data)
        self.algo_combo.currentIndexChanged.connect(self.update_algorithm_info)
        
        # Search tab connections
        self.search_btn.clicked.connect(self.search_data)
        
        # Initialize combo boxes
        self.update_column_combos()
        
        # Initially disable buttons
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.sort_btn.setEnabled(False)
    
    def update_column_combos(self):
        """Update all column combo boxes with available attributes"""
        columns = [
            ("title", "Title"),
            ("author", "Author"), 
            ("publication_year", "Publication Year"),
            ("price", "Price"),
            ("rating", "Rating"),
            ("page_count", "Page Count"),
            ("category", "Category"),
            ("stock_quantity", "Stock Quantity"),
            ("format_type", "Format Type"),
            ("publisher", "Publisher"),
            ("language", "Language")
        ]
        
        # Clear all combos
        self.level1_combo.clear()
        self.level2_combo.clear()
        self.level3_combo.clear()
        self.search_column_combo.clear()
        
        # Add options
        self.level1_combo.addItem("Select first level...", None)
        self.level2_combo.addItem("Select second level...", None)
        self.level3_combo.addItem("Select third level...", None)
        self.search_column_combo.addItem("All Columns", "all")
        
        for col_key, col_name in columns:
            self.level1_combo.addItem(col_name, col_key)
            self.level2_combo.addItem(col_name, col_key)
            self.level3_combo.addItem(col_name, col_key)
            self.search_column_combo.addItem(col_name, col_key)
    
    def show_supported_websites(self):
        """Show information about supported websites"""
        supported_info = """
        <h3>Supported Websites for Scraping:</h3>
        <ul>
        <li><b>http://books.toscrape.com</b> - Book store with 1000+ books</li>
        <li><b>http://quotes.toscrape.com</b> - Famous quotes website</li>
        <li><b>Other websites</b> - Will generate mock data based on your URL</li>
        </ul>
        <p><i>You can try any website URL, but only supported sites will have real data scraping.</i></p>
        """
        
        QMessageBox.information(self, "Supported Websites", supported_info)
    
    def update_algorithm_info(self):
        """Update algorithm information display"""
        algo_key = self.algo_combo.currentData()
        algorithms = SortingAlgorithms.get_algorithm_info()
        
        if algo_key in algorithms:
            info = algorithms[algo_key]
            text = f"<b>{info['name']}</b><br>"
            text += f"<b>Time Complexity:</b> {info['time_complexity']}<br>"
            text += f"<b>Space Complexity:</b> {info['space_complexity']}<br>"
            text += f"<b>Stable:</b> {'Yes' if info['stable'] else 'No'}<br>"
            text += f"<b>Description:</b> {info['description']}"
            self.algo_info_text.setHtml(text)
    
    def start_scraping(self):
        """Start the scraping process from the provided URL"""
        url = self.url_input.text().strip()
        target_count = self.target_spinbox.value()
        
        if not url:
            QMessageBox.warning(self, "URL Required", "Please enter a website URL to scrape!")
            return
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Set the URL in scraper
        self.scraper.set_target_url(url)
        self.scraper.target_count = target_count
        
        # Start scraping in a separate thread
        self.scraping_thread = ScrapingThread(self.scraper, target_count, url)
        self.scraping_thread.progress_updated.connect(self.update_progress)
        self.scraping_thread.finished.connect(self.scraping_finished)
        self.scraping_thread.error_occurred.connect(self.scraping_error)
        self.scraping_thread.start()
        
        # Start progress updates
        self.progress_timer.start(100)  # Update every 100ms
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, target_count)
        self.status_label.setText(f"Scraping in progress... Scraping from {url}")
        
        # Update button states
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.load_btn.setEnabled(False)
    
    def pause_scraping(self):
        self.scraper.pause_scraping()
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(True)
        self.status_label.setText("Scraping paused")
    
    def resume_scraping(self):
        self.scraper.resume_scraping()
        self.resume_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.status_label.setText("Scraping resumed")
    
    def stop_scraping(self):
        self.scraper.stop_scraping()
        self.progress_timer.stop()
        self.progress_bar.setVisible(False)
        self.status_label.setText("Scraping stopped")
        
        # Reset button states
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.load_btn.setEnabled(True)
    
    def scraping_finished(self):
        """Called when scraping completes successfully"""
        self.progress_timer.stop()
        self.progress_bar.setVisible(False)
        
        count = self.database.get_entity_count()
        self.current_count_label.setText(f"{count:,}")
        self.status_label.setText(f"✅ Completed! Generated {count:,} entities from {self.url_input.text()}")
        
        # Reset button states
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.load_btn.setEnabled(True)
        self.sort_btn.setEnabled(True)
        
        # Load and display data
        self.load_data()
        
        QMessageBox.information(self, "Success", f"Successfully generated {count:,} entities from {self.url_input.text()}!")
    
    def scraping_error(self, error_message):
        """Called when scraping encounters an error"""
        self.progress_timer.stop()
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"❌ Scraping error: {error_message}")
        
        # Reset button states
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.load_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Scraping Error", f"An error occurred during scraping:\n{error_message}")
    
    def update_progress(self):
        """Update progress bar from scraper's progress queue"""
        try:
            while True:
                progress = self.scraper.progress_queue.get_nowait()
                self.progress_bar.setValue(progress)
                self.current_count_label.setText(f"{progress:,}")
        except:
            pass
    
    def load_data(self):
        """Load data from database and display in tables"""
        try:
            entities = self.database.get_all_entities()
            count = len(entities)
            
            if count == 0:
                QMessageBox.information(self, "No Data", "No data found. Please scrape some data first.")
                return
            
            self.current_data = entities
            self.current_count_label.setText(f"{count:,}")
            self.status_label.setText(f"📊 Loaded {count:,} entities from database")
            
            # Display first 100 records in preview table
            preview_data = entities[:100]
            self.display_data_in_table(self.data_table, preview_data)
            
            # Update sorted count label
            self.sorted_count_label.setText(f"{count:,}")
            
            # Enable sort button
            self.sort_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Error loading data: {str(e)}")
    
    def display_data_in_table(self, table, data):
        """Display data in a QTableWidget"""
        if not data:
            table.setRowCount(0)
            return
        
        table.setRowCount(len(data))
        
        for row_num, entity in enumerate(data):
            # Entity structure: (id, title, author, isbn, publisher, publication_year, 
            # category, price, rating, page_count, language, description, stock_quantity, format_type, scraped_date, source_url)
            
            table.setItem(row_num, 0, QTableWidgetItem(str(entity[0])))  # ID
            table.setItem(row_num, 1, QTableWidgetItem(str(entity[1])))  # Title
            table.setItem(row_num, 2, QTableWidgetItem(str(entity[2])))  # Author
            table.setItem(row_num, 3, QTableWidgetItem(str(entity[5])))  # Year
            table.setItem(row_num, 4, QTableWidgetItem(f"${entity[7]:.2f}" if entity[7] else "$0.00"))  # Price
            table.setItem(row_num, 5, QTableWidgetItem(str(entity[8])))  # Rating
            table.setItem(row_num, 6, QTableWidgetItem(str(entity[9])))  # Pages
            table.setItem(row_num, 7, QTableWidgetItem(str(entity[6])))  # Category
            table.setItem(row_num, 8, QTableWidgetItem(str(entity[12]))) # Stock
            table.setItem(row_num, 9, QTableWidgetItem(str(entity[13]))) # Format
        
        # Resize columns to content
        table.resizeColumnsToContents()
    
    def sort_data(self):
        """Sort data using selected algorithm"""
        if not self.current_data:
            QMessageBox.warning(self, "No Data", "Please load some data first!")
            return
        
        algorithm_key = self.algo_combo.currentData()
        reverse = self.order_combo.currentText() == "Descending"
        
        # Get primary column for sorting
        primary_column = self.level1_combo.currentData()
        if not primary_column:
            QMessageBox.warning(self, "Select Column", "Please select a column to sort by!")
            return
        
        self.status_label.setText(f"Sorting using {self.algo_combo.currentText()} by {primary_column}...")
        
        # Convert database rows to dictionaries for sorting
        columns = ["id", "title", "author", "isbn", "publisher", "publication_year", 
                  "category", "price", "rating", "page_count", "language", "description", 
                  "stock_quantity", "format_type", "scraped_date", "source_url"]
        
        entity_dicts = []
        for entity in self.current_data:
            entity_dict = dict(zip(columns, entity))
            entity_dicts.append(entity_dict)
        
        # Perform sorting
        try:
            sorted_data = None
            time_taken = 0
            
            if algorithm_key == "bubble":
                sorted_data, time_taken = self.sorting_algorithms.bubble_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "insertion":
                sorted_data, time_taken = self.sorting_algorithms.insertion_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "selection":
                sorted_data, time_taken = self.sorting_algorithms.selection_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "quick":
                sorted_data, time_taken = self.sorting_algorithms.quick_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "merge":
                sorted_data, time_taken = self.sorting_algorithms.merge_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "counting":
                sorted_data, time_taken = self.sorting_algorithms.counting_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "radix":
                sorted_data, time_taken = self.sorting_algorithms.radix_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "bucket":
                sorted_data, time_taken = self.sorting_algorithms.bucket_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "pigeonhole":
                sorted_data, time_taken = self.sorting_algorithms.pigeonhole_sort(entity_dicts, primary_column, reverse)
            elif algorithm_key == "heap":
                sorted_data, time_taken = self.sorting_algorithms.heap_sort(entity_dicts, primary_column, reverse)
            
            # Convert back to tuple format for display
            sorted_entities = []
            for entity_dict in sorted_data:
                entity_tuple = tuple(entity_dict.get(col) for col in columns)
                sorted_entities.append(entity_tuple)
            
            # Display sorted data
            self.display_data_in_table(self.sorted_table, sorted_entities[:100])  # Show first 100
            
            # Update results
            self.time_label.setText(f"{time_taken} ms")
            self.sorted_count_label.setText(f"{len(sorted_entities):,}")
            self.status_label.setText(f"✅ Sorted {len(sorted_entities):,} entities using {self.algo_combo.currentText()} in {time_taken} ms")
            
            QMessageBox.information(self, "Sorting Complete", 
                                  f"Algorithm: {self.algo_combo.currentText()}\n"
                                  f"Column: {primary_column}\n"
                                  f"Order: {self.order_combo.currentText()}\n"
                                  f"Time: {time_taken} ms\n"
                                  f"Entities: {len(sorted_entities):,}")
        
        except Exception as e:
            QMessageBox.critical(self, "Sorting Error", f"Error during sorting: {str(e)}")
    
    def search_data(self):
        """Search data based on criteria"""
        if not self.current_data:
            QMessageBox.warning(self, "No Data", "Please load some data first!")
            return
        
        search_term = self.search_input.text().strip().lower()
        search_column = self.search_column_combo.currentData()
        
        if not search_term:
            QMessageBox.warning(self, "No Search Term", "Please enter a search term!")
            return
        
        # Perform search (simple linear search for now)
        results = []
        columns = ["id", "title", "author", "isbn", "publisher", "publication_year", 
                  "category", "price", "rating", "page_count", "language", "description", 
                  "stock_quantity", "format_type", "scraped_date", "source_url"]
        
        for entity in self.current_data:
            entity_dict = dict(zip(columns, entity))
            
            if search_column == "all":
                # Search in all string columns
                for col in ["title", "author", "category", "publisher", "description"]:
                    if search_term in str(entity_dict.get(col, "")).lower():
                        results.append(entity)
                        break
            else:
                # Search in specific column
                if search_term in str(entity_dict.get(search_column, "")).lower():
                    results.append(entity)
        
        # Apply additional filters
        filtered_results = self.apply_advanced_filters(results)
        
        # Display results
        self.display_data_in_table(self.search_table, filtered_results[:100])  # Show first 100
        self.found_count_label.setText(f"{len(filtered_results):,} records")
        
        self.status_label.setText(f"🔍 Found {len(filtered_results):,} records matching '{search_term}'")
    
    def apply_advanced_filters(self, data):
        """Apply advanced filters to search results"""
        filtered = data
        
        # Price filter
        min_price = self.min_price.text().strip()
        max_price = self.max_price.text().strip()
        
        if min_price or max_price:
            try:
                min_val = float(min_price) if min_price else 0
                max_val = float(max_price) if max_price else float('inf')
                
                filtered = [entity for entity in filtered if min_val <= (entity[7] or 0) <= max_val]
            except ValueError:
                pass  # Invalid price input
        
        # Rating filter
        min_rating = self.min_rating.currentText()
        if min_rating != "Any":
            try:
                rating_val = float(min_rating.replace("+", ""))
                filtered = [entity for entity in filtered if (entity[8] or 0) >= rating_val]
            except ValueError:
                pass
        
        return filtered

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
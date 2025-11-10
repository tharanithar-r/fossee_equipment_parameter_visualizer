from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
                             QFileDialog, QMessageBox, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from theme_manager import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self, api_client, theme_manager=None):
        super().__init__()
        self.api_client = api_client
        self.current_dataset = None
        self.current_summary = None
        self.theme_manager = theme_manager or ThemeManager()
        self.init_ui()
        self.apply_theme()
        self.load_datasets()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel('Chemical Equipment Parameter Visualizer')
        title.setStyleSheet('font-size: 20px; font-weight: bold;')
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = QPushButton('☀️ Light' if self.theme_manager.current_theme == 'light' else '🌙 Dark')
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        upload_btn = QPushButton('Upload CSV')
        upload_btn.clicked.connect(self.upload_csv)
        header_layout.addWidget(upload_btn)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.load_datasets)
        header_layout.addWidget(refresh_btn)
        
        pdf_btn = QPushButton('Download PDF')
        pdf_btn.clicked.connect(self.download_pdf)
        header_layout.addWidget(pdf_btn)
        
        main_layout.addLayout(header_layout)
        
        # Dataset Selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel('Select Dataset:'))
        self.dataset_combo = QComboBox()
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_changed)
        selector_layout.addWidget(self.dataset_combo)
        selector_layout.addStretch()
        main_layout.addLayout(selector_layout)
        
        # Statistics Group
        stats_group = QGroupBox('Summary Statistics')
        stats_layout = QGridLayout()
        
        self.total_label = QLabel('Total: 0')
        self.avg_flowrate_label = QLabel('Avg Flowrate: 0')
        self.avg_pressure_label = QLabel('Avg Pressure: 0')
        self.avg_temp_label = QLabel('Avg Temperature: 0')
        
        stats_layout.addWidget(self.total_label, 0, 0)
        stats_layout.addWidget(self.avg_flowrate_label, 0, 1)
        stats_layout.addWidget(self.avg_pressure_label, 1, 0)
        stats_layout.addWidget(self.avg_temp_label, 1, 1)
        
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Type Distribution Chart
        self.type_chart = FigureCanvas(Figure(figsize=(5, 4)))
        charts_layout.addWidget(self.type_chart)
        
        # Parameters Chart
        self.params_chart = FigureCanvas(Figure(figsize=(5, 4)))
        charts_layout.addWidget(self.params_chart)
        
        main_layout.addLayout(charts_layout)
        
        # Equipment Table
        table_group = QGroupBox('Equipment Details')
        table_layout = QVBoxLayout()
        
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.equipment_table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(self.equipment_table)
        
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)
    
    def apply_theme(self):
        """Apply current theme to the window"""
        self.setStyleSheet(self.theme_manager.get_stylesheet())
        # Update charts if they exist
        if hasattr(self, 'current_summary') and self.current_summary:
            self.update_type_chart()
            self.update_params_chart()
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = self.theme_manager.toggle_theme()
        self.theme_btn.setText('☀️ Light' if new_theme == 'light' else '🌙 Dark')
        self.apply_theme()
    
    def load_datasets(self):
        try:
            datasets = self.api_client.get_datasets()
            self.dataset_combo.clear()
            for dataset in datasets:
                self.dataset_combo.addItem(dataset['name'], dataset['id'])
            
            if datasets:
                self.on_dataset_changed(0)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load datasets: {str(e)}')
    
    def on_dataset_changed(self, index):
        if index < 0:
            return
        
        dataset_id = self.dataset_combo.itemData(index)
        if not dataset_id:
            return
        
        try:
            self.current_dataset = self.api_client.get_dataset(dataset_id)
            self.current_summary = self.api_client.get_summary(dataset_id)
            self.update_ui()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def update_ui(self):
        if not self.current_dataset or not self.current_summary:
            return
        
        # Update statistics
        stats = self.current_summary['statistics']
        self.total_label.setText(f"Total Equipment: {self.current_summary['total_count']}")
        self.avg_flowrate_label.setText(f"Avg Flowrate: {stats['flowrate']['avg']:.2f}")
        self.avg_pressure_label.setText(f"Avg Pressure: {stats['pressure']['avg']:.2f}")
        self.avg_temp_label.setText(f"Avg Temperature: {stats['temperature']['avg']:.2f}")
        
        # Update charts
        self.update_type_chart()
        self.update_params_chart()
        
        # Update table
        self.update_table()
    
    def update_type_chart(self):
        self.type_chart.figure.clear()
        
        # Set figure background color based on theme
        colors_dict = self.theme_manager.get_colors()
        self.type_chart.figure.patch.set_facecolor(colors_dict['card'])
        
        ax = self.type_chart.figure.add_subplot(111)
        ax.set_facecolor(colors_dict['card'])
        
        type_dist = self.current_summary['type_distribution']
        labels = [t['equipment_type'] for t in type_dist]
        sizes = [t['count'] for t in type_dist]
        chart_colors = self.theme_manager.get_chart_colors()
        
        # Set text colors based on theme
        text_color = colors_dict['foreground']
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=chart_colors[:len(labels)],
               textprops={'color': text_color})
        ax.set_title('Equipment Type Distribution', color=text_color)
        self.type_chart.draw()
    
    def update_params_chart(self):
        self.params_chart.figure.clear()
        
        # Set figure background color based on theme
        colors_dict = self.theme_manager.get_colors()
        self.params_chart.figure.patch.set_facecolor(colors_dict['card'])
        
        ax = self.params_chart.figure.add_subplot(111)
        ax.set_facecolor(colors_dict['card'])
        
        stats = self.current_summary['statistics']
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        avg_values = [stats['flowrate']['avg'], stats['pressure']['avg'], stats['temperature']['avg']]
        min_values = [stats['flowrate']['min'], stats['pressure']['min'], stats['temperature']['min']]
        max_values = [stats['flowrate']['max'], stats['pressure']['max'], stats['temperature']['max']]
        
        x = range(len(parameters))
        width = 0.25
        
        chart_colors = self.theme_manager.get_chart_colors()
        text_color = colors_dict['foreground']
        
        ax.bar([i - width for i in x], avg_values, width, label='Average', color=chart_colors[0])
        ax.bar(x, min_values, width, label='Min', color=chart_colors[1])
        ax.bar([i + width for i in x], max_values, width, label='Max', color=chart_colors[3])
        
        ax.set_xlabel('Parameters', color=text_color)
        ax.set_ylabel('Values', color=text_color)
        ax.set_title('Parameter Statistics', color=text_color)
        ax.set_xticks(x)
        ax.set_xticklabels(parameters)
        ax.tick_params(colors=text_color)
        
        legend = ax.legend()
        legend.get_frame().set_facecolor(colors_dict['card'])
        for text in legend.get_texts():
            text.set_color(text_color)
        
        # Set spine colors
        for spine in ax.spines.values():
            spine.set_edgecolor(colors_dict['border'])
        
        self.params_chart.draw()
    
    def update_table(self):
        equipment = self.current_dataset['equipment']
        self.equipment_table.setRowCount(len(equipment))
        
        for i, eq in enumerate(equipment):
            self.equipment_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            self.equipment_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            self.equipment_table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.1f}"))
            self.equipment_table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.1f}"))
            self.equipment_table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.1f}"))
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if not file_path:
            return
        
        try:
            self.api_client.upload_dataset(file_path)
            QMessageBox.information(self, 'Success', 'Dataset uploaded successfully')
            self.load_datasets()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def download_pdf(self):
        if not self.current_dataset:
            QMessageBox.warning(self, 'Warning', 'Please select a dataset first')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF', f"{self.current_dataset['name']}_report.pdf", 'PDF Files (*.pdf)'
        )
        if not file_path:
            return
        
        try:
            self.api_client.download_pdf(self.current_dataset['id'], file_path)
            QMessageBox.information(self, 'Success', 'PDF downloaded successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Download failed: {str(e)}')
        
        stats = self.current_summary['statistics']
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        avg_values = [stats['flowrate']['avg'], stats['pressure']['avg'], stats['temperature']['avg']]
        min_values = [stats['flowrate']['min'], stats['pressure']['min'], stats['temperature']['min']]
        max_values = [stats['flowrate']['max'], stats['pressure']['max'], stats['temperature']['max']]
        
        x = range(len(parameters))
        width = 0.25
        
        ax.bar([i - width for i in x], avg_values, width, label='Average', color='#3b82f6')
        ax.bar(x, min_values, width, label='Min', color='#10b981')
        ax.bar([i + width for i in x], max_values, width, label='Max', color='#ef4444')
        
        ax.set_xlabel('Parameters')
        ax.set_ylabel('Values')
        ax.set_title('Parameter Statistics')
        ax.set_xticks(x)
        ax.set_xticklabels(parameters)
        ax.legend()
        
        self.params_chart.draw()
    
    def update_table(self):
        equipment = self.current_dataset['equipment']
        self.equipment_table.setRowCount(len(equipment))
        
        for i, eq in enumerate(equipment):
            self.equipment_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            self.equipment_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            self.equipment_table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.1f}"))
            self.equipment_table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.1f}"))
            self.equipment_table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.1f}"))
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if not file_path:
            return
        
        # Clean up previous worker if exists and is still running
        if self.upload_worker is not None and self.upload_worker.isRunning():
            self.upload_worker.quit()
            self.upload_worker.wait()
        
        self.spinner.set_message("Uploading dataset...")
        self.center_spinner()
        self.spinner.start()
        
        self.upload_worker = UploadDatasetWorker(self.api_client, file_path)
        self.upload_worker.finished.connect(self.on_upload_finished)
        self.upload_worker.error.connect(self.on_upload_error)
        self.upload_worker.finished.connect(self.upload_worker.deleteLater)
        self.upload_worker.error.connect(self.upload_worker.deleteLater)
        self.upload_worker.start()
        
    def on_upload_finished(self):
        self.spinner.stop()
        QMessageBox.information(self, 'Success', 'Dataset uploaded successfully')
        self.load_datasets()
        
    def on_upload_error(self, error_msg):
        self.spinner.stop()
        QMessageBox.critical(self, 'Error', f'Upload failed: {error_msg}')
    
    def download_pdf(self):
        if not self.current_dataset:
            QMessageBox.warning(self, 'Warning', 'Please select a dataset first')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF', f"{self.current_dataset['name']}_report.pdf", 'PDF Files (*.pdf)'
        )
        if not file_path:
            return
        
        # Clean up previous worker if exists
        if self.download_worker is not None:
            self.download_worker.quit()
            self.download_worker.wait()
        
        self.spinner.set_message("Downloading PDF...")
        self.center_spinner()
        self.spinner.start()
        
        self.download_worker = DownloadPDFWorker(self.api_client, self.current_dataset['id'], file_path)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.finished.connect(self.download_worker.deleteLater)
        self.download_worker.error.connect(self.download_worker.deleteLater)
        self.download_worker.start()
        
    def on_download_finished(self):
        self.spinner.stop()
        QMessageBox.information(self, 'Success', 'PDF downloaded successfully')
        
    def on_download_error(self, error_msg):
        self.spinner.stop()
        QMessageBox.critical(self, 'Error', f'Download failed: {error_msg}')
    
    def closeEvent(self, event):
        """Clean up threads when window closes"""
        # Stop and wait for all running threads
        workers = [self.load_worker, self.details_worker, self.upload_worker, self.download_worker]
        for worker in workers:
            if worker is not None and worker.isRunning():
                worker.quit()
                worker.wait()
        
        event.accept()

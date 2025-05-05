from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QLabel, QComboBox,
    QPushButton, QLineEdit, QTabWidget, QTextEdit,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from datetime import datetime
from typing import Optional, Dict, Any

from ..database.db_manager import DatabaseManager
from ..models.database_models import FraudIncident

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.session = self.db.get_session()
        self.current_incident: Optional[FraudIncident] = None
        
        self.setWindowTitle("Fraud Incident Analysis")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create filter section
        filter_layout = QHBoxLayout()
        
        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "open", "closed", "investigating", "resolved"])
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(self.status_filter)
        
        # Priority filter
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All", "low", "medium", "high", "critical"])
        filter_layout.addWidget(QLabel("Priority:"))
        filter_layout.addWidget(self.priority_filter)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search incidents...")
        filter_layout.addWidget(self.search_box)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Create splitter for table and details
        content_layout = QHBoxLayout()
        
        # Create incidents table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Incident ID", "Title", "Status", 
            "Priority", "Report Date", "Risk Score"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_incident_selected)
        content_layout.addWidget(self.table)
        
        # Create details panel
        self.details_panel = QTabWidget()
        self.setup_details_panel()
        content_layout.addWidget(self.details_panel)
        
        # Set the content layout stretch factors
        content_layout.setStretch(0, 1)  # Table takes 1 part
        content_layout.setStretch(1, 1)  # Details takes 1 part
        
        layout.addLayout(content_layout)
        
        # Connect filter signals
        self.status_filter.currentTextChanged.connect(self.refresh_data)
        self.priority_filter.currentTextChanged.connect(self.refresh_data)
        self.search_box.textChanged.connect(self.refresh_data)
        
        # Initial data load
        self.refresh_data()
    
    def setup_details_panel(self):
        """Setup the details panel tabs"""
        # Overview tab
        overview_widget = QWidget()
        overview_layout = QVBoxLayout(overview_widget)
        self.overview_text = QTextEdit()
        self.overview_text.setReadOnly(True)
        overview_layout.addWidget(self.overview_text)
        self.details_panel.addTab(overview_widget, "Overview")
        
        # Transactions tab
        transactions_widget = QWidget()
        transactions_layout = QVBoxLayout(transactions_widget)
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels([
            "Transaction ID", "Date", "Type", "Amount", "Status"
        ])
        transactions_layout.addWidget(self.transactions_table)
        self.details_panel.addTab(transactions_widget, "Transactions")
        
        # Investigation Notes tab
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        self.notes_text = QTextEdit()
        self.notes_text.setReadOnly(True)
        notes_layout.addWidget(self.notes_text)
        self.details_panel.addTab(notes_widget, "Investigation Notes")
    
    @pyqtSlot()
    def refresh_data(self):
        """Refresh the incidents table with filtered data"""
        try:
            # Build query
            query = self.session.query(FraudIncident)
            
            # Apply filters
            if self.status_filter.currentText() != "All":
                query = query.filter(FraudIncident.status == self.status_filter.currentText())
            
            if self.priority_filter.currentText() != "All":
                query = query.filter(FraudIncident.priority == self.priority_filter.currentText())
            
            # Apply search
            search_text = self.search_box.text().strip()
            if search_text:
                query = query.filter(
                    FraudIncident.title.ilike(f"%{search_text}%") |
                    FraudIncident.incident_id.ilike(f"%{search_text}%")
                )
            
            # Execute query
            incidents = query.all()
            
            # Update table
            self.table.setRowCount(len(incidents))
            for row, incident in enumerate(incidents):
                self.table.setItem(row, 0, QTableWidgetItem(incident.incident_id))
                self.table.setItem(row, 1, QTableWidgetItem(incident.title))
                self.table.setItem(row, 2, QTableWidgetItem(incident.status))
                self.table.setItem(row, 3, QTableWidgetItem(incident.priority))
                self.table.setItem(row, 4, QTableWidgetItem(
                    incident.report_date.strftime("%Y-%m-%d %H:%M") if incident.report_date else ""
                ))
                self.table.setItem(row, 5, QTableWidgetItem(str(incident.risk_score or "")))
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh data: {str(e)}")
    
    def on_incident_selected(self):
        """Handle incident selection"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        incident_id = self.table.item(selected_items[0].row(), 0).text()
        self.current_incident = self.session.query(FraudIncident).filter_by(incident_id=incident_id).first()
        
        if self.current_incident:
            self.update_details_panel()
    
    def update_details_panel(self):
        """Update the details panel with current incident data"""
        if not self.current_incident:
            return
        
        # Update Overview tab
        overview = f"""
        Title: {self.current_incident.title}
        Status: {self.current_incident.status}
        Priority: {self.current_incident.priority}
        Report Date: {self.current_incident.report_date}
        
        Fraud Type: {self.current_incident.fraud_type}
        Sub Type: {self.current_incident.sub_type}
        Risk Score: {self.current_incident.risk_score}
        
        AI Involvement: {"Yes" if self.current_incident.ai_involvement else "No"}
        Detection Method: {self.current_incident.detection_method}
        """
        self.overview_text.setText(overview)
        
        # Update Transactions tab
        self.transactions_table.setRowCount(len(self.current_incident.transactions))
        for row, tx in enumerate(self.current_incident.transactions):
            self.transactions_table.setItem(row, 0, QTableWidgetItem(tx.transaction_id))
            self.transactions_table.setItem(row, 1, QTableWidgetItem(
                tx.transaction_date.strftime("%Y-%m-%d %H:%M") if tx.transaction_date else ""
            ))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(tx.transaction_type))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(f"${tx.amount:,.2f}"))
            self.transactions_table.setItem(row, 4, QTableWidgetItem(tx.payment_method))
        
        # Update Investigation Notes tab
        notes = "\n\n".join([
            f"[{note.timestamp}] {note.user_id}:\n{note.note}"
            for note in self.current_incident.investigation_notes
        ])
        self.notes_text.setText(notes)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.session.close()
        self.db.close()
        super().closeEvent(event)
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QDockWidget, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QListWidget
)
from PyQt5.QtCore import Qt
from plugin_interface import PluginInterface

class DatabaseBrowserPlugin(PluginInterface):
    def initialize(self):
        self.dock_widget = QDockWidget("Database Browser", self.ide)
        self.dock_widget.setObjectName("DatabaseBrowserDockWidget")
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.db_path_input = QLineEdit()
        self.browse_button = QPushButton("Datenbank auswählen")
        self.browse_button.clicked.connect(self.browse_database)
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("SQL-Abfrage hier eingeben...")
        self.execute_button = QPushButton("Abfrage ausführen")
        self.execute_button.clicked.connect(self.execute_query)
        self.show_queries_button = QPushButton("Meistgenutzte Abfragen anzeigen")
        self.show_queries_button.clicked.connect(self.show_common_queries)
        self.show_all_data_button = QPushButton("Gesamten Datenbankinhalt anzeigen")
        self.show_all_data_button.clicked.connect(self.show_all_data)
        self.results_table = QTableWidget()

        self.layout.addWidget(QLabel("Datenbankpfad:"))
        self.layout.addWidget(self.db_path_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(QLabel("SQL-Abfrage:"))
        self.layout.addWidget(self.query_input)
        self.layout.addWidget(self.execute_button)
        self.layout.addWidget(self.show_queries_button)
        self.layout.addWidget(self.show_all_data_button)
        self.layout.addWidget(self.results_table)

        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.dock_widgets["database_browser_dock"] = self.dock_widget

        self.ide.console_output.appendPlainText("Database Browser Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("Database Browser Plugin deaktiviert")

    def browse_database(self):
        options = QFileDialog.Options()
        db_path, _ = QFileDialog.getOpenFileName(self.widget, "Datenbank auswählen", "", "SQLite-Datenbanken (*.sqlite *.db);;Alle Dateien (*)", options=options)
        if db_path:
            self.db_path_input.setText(db_path)

    def execute_query(self):
        db_path = self.db_path_input.text()
        if not db_path:
            QMessageBox.warning(self.widget, "Fehler", "Bitte wählen Sie eine Datenbank aus.")
            return
        
        query = self.query_input.toPlainText()
        if not query:
            QMessageBox.warning(self.widget, "Fehler", "Bitte geben Sie eine SQL-Abfrage ein.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            self.display_results(cursor, results)
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self.widget, "Datenbankfehler", str(e))

    def display_results(self, cursor, results):
        self.results_table.clear()
        headers = [description[0] for description in cursor.description]
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setRowCount(len(results))

        for row_idx, row in enumerate(results):
            for col_idx, item in enumerate(row):
                self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def show_common_queries(self):
        common_queries = [
            "SELECT * FROM table_name;",
            "SELECT column1, column2 FROM table_name;",
            "INSERT INTO table_name (column1, column2) VALUES (value1, value2);",
            "UPDATE table_name SET column1 = value1 WHERE condition;",
            "DELETE FROM table_name WHERE condition;"
        ]

        dialog = QDialog(self.widget)
        dialog.setWindowTitle("Meistgenutzte Abfragen")
        layout = QVBoxLayout(dialog)
        query_list = QListWidget()
        for query in common_queries:
            query_list.addItem(query)
        layout.addWidget(query_list)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_all_data(self):
        db_path = self.db_path_input.text()
        if not db_path:
            QMessageBox.warning(self.widget, "Fehler", "Bitte wählen Sie eine Datenbank aus.")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            if not tables:
                QMessageBox.warning(self.widget, "Fehler", "Die Datenbank enthält keine Tabellen.")
                conn.close()
                return

            dialog = QDialog(self.widget)
            dialog.setWindowTitle("Gesamter Datenbankinhalt")
            layout = QVBoxLayout(dialog)

            for table_name in tables:
                table_name = table_name[0]
                cursor.execute(f"SELECT * FROM {table_name};")
                results = cursor.fetchall()
                headers = [description[0] for description in cursor.description]
                
                table_widget = QTableWidget()
                table_widget.setColumnCount(len(headers))
                table_widget.setHorizontalHeaderLabels(headers)
                table_widget.setRowCount(len(results))

                for row_idx, row in enumerate(results):
                    for col_idx, item in enumerate(row):
                        table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

                layout.addWidget(QLabel(f"Tabelle: {table_name}"))
                layout.addWidget(table_widget)

            dialog.setLayout(layout)
            dialog.exec_()
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self.widget, "Datenbankfehler", str(e))

def create_plugin(ide):
    return DatabaseBrowserPlugin(ide)

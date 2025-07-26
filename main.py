import sys
import sqlite3
from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5 import QtCore
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class FinanceManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("finui.ui", self)
        self.setWindowTitle("PERSONAL FINANCE MANAGER")
        self.setWindowIcon(QIcon("budget.png"))

        # UI Connections
        self.findChild(QtWidgets.QPushButton, "btn_summary").clicked.connect(self.show_summary)
        self.findChild(QtWidgets.QPushButton, "btn_add_expense").clicked.connect(self.add_expense)
        self.findChild(QtWidgets.QPushButton, "btn_edit_expense").clicked.connect(self.edit_expense)
        self.findChild(QtWidgets.QPushButton, "btn_delete_expense").clicked.connect(self.delete_expense)

        self.income_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_income")
        self.deducted_output = self.findChild(QtWidgets.QLineEdit, "lineEdit_deducted")
        self.remaining_output = self.findChild(QtWidgets.QLineEdit, "lineEdit_remaining")
        self.expense_name_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_expense_name")
        self.expense_amount_input = self.findChild(QtWidgets.QLineEdit, "lineEdit_expense_amount")
        self.months_spin = self.findChild(QtWidgets.QSpinBox, "spinbox_months")
        self.expense_table = self.findChild(QtWidgets.QTableWidget, "table_expenses")

        # Database setup
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.load_income()
        self.load_expenses()
        self.update_summary()

        # -------------- Enforcing Fonts and Styles ----------------
        from PyQt5.QtGui import QFont, QColor, QPalette

        # Title Label
        title_label = self.findChild(QtWidgets.QLabel, "label_title")
        if title_label:
            title_font = QFont("Calisto MT", 30, QFont.Bold)
            title_label.setFont(title_font)
            title_label.setStyleSheet("color: rgb(255, 105, 97);")  # Coral red

        # Group Titles (e.g., Monthly Income Summary, Expense Tracker)
        group_labels = ["label_income_summary", "label_expense_tracker", "label_progress_summary"]
        for label_name in group_labels:
            label = self.findChild(QtWidgets.QLabel, label_name)
            if label:
                group_font = QFont("Times New Roman", 12, QFont.Bold)
                group_font.setItalic(True)
                label.setFont(group_font)

        # Green Italic Labels (e.g., Monthly Income, Total Deducted, etc.)
        info_labels = [
            "label_monthly_income", "label_total_deducted", "label_remaining",
            "label_name", "label_amount", "label_select_months"
        ]
        for label_name in info_labels:
            label = self.findChild(QtWidgets.QLabel, label_name)
            if label:
                font = QFont("Arial", 10)
                font.setItalic(True)
                label.setFont(font)
                label.setStyleSheet("color: green;")

        # Buttons
        button_names = ["btn_add_expense", "btn_edit_expense", "btn_delete_expense", "btn_summary"]
        for btn_name in button_names:
            btn = self.findChild(QtWidgets.QPushButton, btn_name)
            if btn:
                btn.setStyleSheet("""
                    QPushButton {
                        color: green;
                        background-color: white;
                        border: 1px solid green;
                        padding: 5px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #eaffea;
                    }
                """)

        # Table Header Font
        header = self.expense_table.horizontalHeader()
        header_font = QFont("Times New Roman", 10)
        header_font.setBold(True)
        header.setFont(header_font)

        # Footer Quote
        footer_label = self.findChild(QtWidgets.QLabel, "label_quote")
        if footer_label:
            font = QFont("Georgia", 10, QFont.Bold)
            font.setItalic(True)
            footer_label.setFont(font)
            footer_label.setStyleSheet("color: #996633;")  # Brownish-orange



    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY,
                amount REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount REAL,
                date TEXT
            )
        ''')
        self.conn.commit()

    def load_income(self):
        self.cursor.execute("SELECT amount FROM income ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            self.income_input.setText(str(result[0]))

    def save_income(self):
        try:
            income = float(self.income_input.text())
            self.cursor.execute("INSERT INTO income(amount) VALUES (?)", (income,))
            self.conn.commit()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid income value.")

    def add_expense(self):
        try:
            name = self.expense_name_input.text()
            amount = float(self.expense_amount_input.text())
            date = datetime.now().strftime("%Y-%m-%d")

            self.save_income()

            self.cursor.execute("INSERT INTO expenses(name, amount, date) VALUES (?, ?, ?)", (name, amount, date))
            self.conn.commit()

            self.expense_name_input.clear()
            self.expense_amount_input.clear()

            self.load_expenses()
            self.update_summary()
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid expense data.")

    def load_expenses(self):
        self.expense_table.setRowCount(0)
        self.cursor.execute("SELECT id, name, amount, date FROM expenses")
        for row_idx, (exp_id, name, amount, date) in enumerate(self.cursor.fetchall()):
            self.expense_table.insertRow(row_idx)
            self.expense_table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.expense_table.setItem(row_idx, 1, QTableWidgetItem(f"{amount:.2f}"))
            self.expense_table.setItem(row_idx, 2, QTableWidgetItem(date))

            # Store ID in row (invisible role)
            self.expense_table.setItem(row_idx, 2, QTableWidgetItem(date))
            self.expense_table.item(row_idx, 0).setData(QtCore.Qt.UserRole, exp_id)

    def get_selected_expense_id(self):
        row = self.expense_table.currentRow()
        if row < 0:
            return None
        item = self.expense_table.item(row, 0)
        return item.data(QtCore.Qt.UserRole)

    def delete_expense(self):
        if not self.get_selected_expense_id:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a record first.")
            return

        confirm = QtWidgets.QMessageBox.question(self, "Confirm", "Are you sure to delete this employee?")
        if confirm != QtWidgets.QMessageBox.Yes:
            return

        exp_id = self.get_selected_expense_id()
        if exp_id:
            self.cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
            self.conn.commit()
            self.load_expenses()
            self.update_summary()

    def edit_expense(self):
        exp_id = self.get_selected_expense_id()
        if exp_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to edit.")
            return

        name = self.expense_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Expense name cannot be empty.")
            return

        try:
            amount = float(self.expense_amount_input.text())
            self.cursor.execute("UPDATE expenses SET name = ?, amount = ? WHERE id = ?", (name, amount, exp_id))
            self.conn.commit()
            self.load_expenses()
            self.update_summary()
            self.expense_name_input.clear()
            self.expense_amount_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount.")

    def update_summary(self):
        try:
            income = float(self.income_input.text())
            self.cursor.execute("SELECT SUM(amount) FROM expenses")
            total_deducted = self.cursor.fetchone()[0] or 0
            remaining_percent = ((income - total_deducted) / income) * 100 if income != 0 else 0

            self.deducted_output.setText(f"{total_deducted:.2f}")
            self.remaining_output.setText(f"{remaining_percent:.2f}%")
        except:
            pass

    def show_summary(self):
        months = self.months_spin.value()
        income = float(self.income_input.text()) if self.income_input.text() else 0
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = self.cursor.fetchone()[0] or 0
        savings = (income * months) - total_expenses
        avg_expense = total_expenses / months if months else 0

        msg = f"Summary for {months} month(s):\n\n" \
              f"Total Expenses: ₹{total_expenses:.2f}\n" \
              f"Avg Monthly Expense: ₹{avg_expense:.2f}\n" \
              f"Estimated Savings: ₹{savings:.2f}"

        QMessageBox.information(self, "Progress Summary", msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FinanceManager()
    window.show()
    sys.exit(app.exec_())
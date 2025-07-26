# personal-finanace-manager-using-python-with-ui
💰 Personal Finance Manager using Python + PyQt5
A desktop application designed to help users manage their monthly income, expenses, savings, and financial trends. Built using Python, PyQt5, and SQLite, it features a clean UI and provides useful insights through charts and summaries.


🧠 About the Project:
This application allows users to track their finances and manage their money more efficiently. With a focus on simplicity and visibility, users can:
	- Set and update monthly income
	- Add, edit, or delete monthly expenses
	- Automatically calculate deductions and savings
	- View expense and savings trends over 6/12 months
	- Visualize financial data with graphs
	- Store data persistently using SQLite


🔧 How I Made It – Step-by-Step:
1. Installed Python 3.10.11
	- Configured and added it to the system PATH

2. Set up PyQt5 and SQLite
	- Used pip install pyqt5 for UI framework
	- Created and connected SQLite database for transaction storage

3. Designed UI with Qt Designer
	- Built the .ui file with inputs for income, expenses, and summary

4. Integrated Matplotlib
	- Used for showing charts of expense trends and savings progress


🖌️ UI Design (via Qt Designer):
The interface is structured into intuitive sections:
	- Income Input – Enter monthly income
	- Expense Table – Add/edit/delete monthly expenses
	- Deductions Panel – View total deductions and remaining balance
	- Summary Button – Shows savings and visual charts
	- Graph Button (Optional) – Toggle to view trends with matplotlib


💻 Core Functionalities

| Feature                           | Description                                                                                 |
|------------------------------   |----------------------------------------------------------------------------------|
| Income Management       | Add and persist monthly income with live updates                          |
| Expense Tracking            | Add/edit/delete recurring or custom expenses                                 |
| Summary View               | Display total deductions, remaining balance, and savings                 |
| Graphs & Trends            | Show savings/expense trends over selected months using Matplotlib |
| Data Persistence             | Store all entries in SQLite for long-term tracking                             |
| Clean & Responsive UI   | PyQt5-based layout with a modern and user-friendly design            |


🧑‍💻 Technologies Used
	- Python 3.10.11
	- PyQt5 – for GUI
	- Qt Designer – to create .ui interface files
	- SQLite – lightweight database for persistent storage
	- Matplotlib – for rendering financial charts and graphs


🚀 How to Run the Project
1. Clone the Repository:
```bash
git clone https://github.com/yourusername/finance-manager.git
cd finance-manager

2. Install Required Libraries:
pip install PyQt5 matplotlib

3. Run the Application:
python main.py


📂 File Structure
finance-manager/
├── main.py                    # Main entry script
├── database.py              # Handles SQLite database operations
├── ui_main.ui                # UI file created using Qt Designer
├── finance_utils.py         # Logic for calculations and summaries
├── graph_plotter.py        # Handles graph display with Matplotlib
├── README.md           # Project documentation
├── /screenshots              # Output images folder


🖼️ Output Screenshots:
1.Home Page Overview: Displays the main interface with options to input income, add expenses, and view summary.
2.Monthly Income Input: Shows the screen where users enter their monthly income.
3.Add Monthly Expenses: Demonstrates the form used to add recurring or one-time expenses with category and amount fields.
4.Expense Table View: Presents the interactive table listing all added expenses with options to edit or delete.
5.Financial Summary Window: Displays total income, deductions, and remaining balance in a summarized format.
6.Graphical Trend Analysis: Shows savings and expense trends over 6 or 12 months using graphs.
7.Edit/Delete Functionality: Demonstrates the user’s ability to update or remove existing entries from the expense table.


📌 Future Improvements

	- Add export to Excel/PDF options
	- Set financial goals and alerts
	- Monthly email reports
	- Dark/light mode toggle
	- User login system for multi-user support


📝 License
This project is open-source under the MIT License.


🙋‍♀️ Author  
Created by [Khushi Singh](https://github.com/khushi2728)



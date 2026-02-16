🏢 Leave Management System (MCP Server)

A simple Leave Management System built using FastMCP.
This system allows employees to apply for leave, check balances, view history, and enables HR to approve or reject requests.

It is implemented as an MCP (Model Context Protocol) server exposing structured tools for leave operations.

🚀 Features

✅ Apply for leave (Casual, Sick, Maternity, Paternity, Unpaid)

✅ Automatic leave balance deduction

✅ Gender-based leave validation (Maternity / Paternity)

✅ Leave approval & rejection by manager

✅ Leave balance tracking

✅ Leave history tracking

✅ View all pending requests

✅ Text-based leave analysis summary

✅ Greeting resource endpoint

🧠 System Overview

The system maintains an in-memory employee leave database:

Employee ID

Name

Gender

Leave balance

Leave history

Approval tracking (approved/rejected/pending)

⚠️ Note: This implementation uses in-memory storage (dictionary). Data resets when the server restarts.

📂 Project Structure
.
├── server.py   # Main MCP server
└── README.md

🛠 Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/leave-management-system.git
cd leave-management-system

2️⃣ Install Dependencies
pip install mcp


(Ensure you have Python 3.9+ installed.)

▶️ Running the Server
python server.py


The MCP server will start and expose the registered tools.

🔧 Available MCP Tools
1️⃣ Apply Leave
apply_leave(
    employee_id: str,
    leave_dates: List[str],
    reason: str,
    leave_type: str
)


Example:

apply_leave("E001", ["2026-02-20"], "Medical checkup", "sick")

2️⃣ Get Leave Balance
get_leave_balance(employee_id: str)


Returns:

{
  "casual": 10,
  "sick": 8,
  "maternity": 90,
  "unpaid": 9999
}

3️⃣ Get Leave History
get_leave_history(employee_id: str)


Returns a list of leave records with:

Date

Reason

Type

Status

Applied date

Approval details

4️⃣ Manage Leave (Approve/Reject)
manage_leave(
    employee_id: str,
    leave_date: str,
    action: str,
    manager_name: str
)


Example:

manage_leave("E001", "2026-02-20", "approve", "HR Manager")


If rejected (non-unpaid leave), the leave balance is restored automatically.

5️⃣ List Pending Requests
list_pending_requests()


Returns all leave requests with status "pending".

6️⃣ Leave Analysis
leave_analysis()


Returns a text summary like:

Leave Balance Summary:
- Alice: 18 days remaining (casual:10, sick:8)
- Bob: 18 days remaining (casual:10, sick:8)

7️⃣ Greeting Resource

Resource endpoint:

greeting://{name}


Example:

greeting://Alice


Response:

Hello, Alice! Welcome to Leave Management System.

👥 Default Employees

The system initializes with 5 sample employees:

ID	Name	Gender
E001	Alice	Female
E002	Bob	Male
E003	Charlie	Male
E004	David	Male
E005	Eva	Female
🧾 Leave Rules Implemented

✔ Casual Leave

✔ Sick Leave

✔ Maternity Leave (Female only)

✔ Paternity Leave (Male only)

✔ Unpaid Leave (Unlimited, no balance deduction)

✔ Rejected leave restores balance (except unpaid)


📈 Possible Improvements

Add database support (PostgreSQL / MongoDB)

Add authentication & role management

Add REST API wrapper

Add date validation & conflict detection

Add dashboard frontend

Add reporting & analytics

🧪 Example Workflow

Employee applies for leave

Leave is stored as pending

Manager reviews pending requests

Manager approves or rejects

System updates status and balance automatically

🏗 Built With

Python

FastMCP

📄 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Developed as a demonstration MCP-based Leave Management System.

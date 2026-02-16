from mcp.server.fastmcp import FastMCP
from typing import List, Dict
from datetime import date

# ✅ Employee data structure
employee_leaves = {
    "E001": {"name": "Alice", "gender": "female", "balance": {"casual": 10, "sick": 8, "maternity": 90, "unpaid": 9999}, "history": []},
    "E002": {"name": "Bob", "gender": "male", "balance": {"casual": 10, "sick": 8, "paternity": 15, "unpaid": 9999}, "history": []},
    "E003": {"name": "Charlie", "gender": "male", "balance": {"casual": 10, "sick": 8, "paternity": 15, "unpaid": 9999}, "history": []},
    "E004": {"name": "David", "gender": "male", "balance": {"casual": 10, "sick": 8, "paternity": 15, "unpaid": 9999}, "history": []},
    "E005": {"name": "Eva", "gender": "female", "balance": {"casual": 10, "sick": 8, "maternity": 90, "unpaid": 9999}, "history": []}
}

# ✅ Initialize MCP server
mcp = FastMCP("LeaveManagementSystem")

# ✅ Tool: Apply leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str], reason: str, leave_type: str) -> str:
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    leave_type = leave_type.lower()
    emp = employee_leaves[employee_id]
    if leave_type not in emp["balance"]:
        return f"Invalid leave type. Available: {', '.join(emp['balance'].keys())}"

    if leave_type == "maternity" and emp["gender"] != "female":
        return "Maternity leave is only for female employees."
    if leave_type == "paternity" and emp["gender"] != "male":
        return "Paternity leave is only for male employees."

    requested = len(leave_dates)

    if leave_type == "unpaid":
        for d in leave_dates:
            emp["history"].append({"date": d, "reason": reason, "type": leave_type, "status": "pending", "applied_on": str(date.today())})
        return f"Unpaid leave applied for {requested} day(s)."

    if emp["balance"][leave_type] < requested:
        return f"Insufficient {leave_type} balance. Available: {emp['balance'][leave_type]}"

    for d in leave_dates:
        emp["history"].append({"date": d, "reason": reason, "type": leave_type, "status": "pending", "applied_on": str(date.today())})
    emp["balance"][leave_type] -= requested
    return f"{leave_type.capitalize()} leave applied for {requested} day(s). Remaining: {emp['balance'][leave_type]}."

# ✅ Tool: Get balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> Dict[str, int]:
    return employee_leaves.get(employee_id, {}).get("balance", {})

# ✅ Tool: Get history
@mcp.tool()
def get_leave_history(employee_id: str) -> List[dict]:
    return employee_leaves.get(employee_id, {}).get("history", [])

# ✅ Tool: Approve/Reject leave
@mcp.tool()
def manage_leave(employee_id: str, leave_date: str, action: str, manager_name: str) -> str:
    if employee_id not in employee_leaves:
        return "Employee ID not found."
    for leave in employee_leaves[employee_id]["history"]:
        if leave["date"] == leave_date and leave["status"] == "pending":
            leave["status"] = "approved" if action.lower() == "approve" else "rejected"
            leave["approved_on"] = str(date.today())
            leave["approved_by"] = manager_name
            if action.lower() == "reject" and leave["type"] != "unpaid":
                employee_leaves[employee_id]["balance"][leave["type"]] += 1
            return f"Leave {action.upper()} for {employee_id} on {leave_date}"
    return "No pending leave for that date."

# ✅ Tool: Pending requests
@mcp.tool()
def list_pending_requests() -> List[dict]:
    pending = []
    for emp_id, data in employee_leaves.items():
        for leave in data["history"]:
            if leave["status"] == "pending":
                pending.append({"employee_id": emp_id, "employee_name": data["name"], **leave})
    return pending

# ✅ Tool: Text-based leave analysis (No charts)
@mcp.tool()
def leave_analysis() -> str:
    analysis = "Leave Balance Summary:\n"
    for emp_id, emp in employee_leaves.items():
        total = sum(v for k, v in emp["balance"].items() if k != "unpaid")
        analysis += f"- {emp['name']}: {total} days remaining ({', '.join(f'{k}:{v}' for k,v in emp['balance'].items() if k != 'unpaid')})\n"
    return analysis

# ✅ Resource
@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to Leave Management System."

if __name__ == "__main__":
    mcp.run()

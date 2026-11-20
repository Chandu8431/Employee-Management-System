import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# 1. Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Default XAMPP/WAMP user
        password="",          # Default XAMPP/WAMP password
        database="ems"
    )

# Helper: Generic Table Loader
def load_table_data(tree, table_name):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error loading {table_name}:\n{err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Helper: Generic Record Inserter
def insert_record(query, values, tree, table_name, clear_entries):
    if any(v == "" for v in values):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", f"Record added to {table_name}!")
        for entry in clear_entries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
        load_table_data(tree, table_name)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error inserting into {table_name}:\n{err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# ================= MAIN WINDOW SETUP =================
root = tk.Tk()
root.title("Employee Management System (EMS)")
root.geometry("700x550")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=20)

# ================= TAB 1: DEPARTMENTS (dept_det) =================
tab_dept = ttk.Frame(notebook,style="Card.TFrame")
notebook.add(tab_dept, text="Departments")

form_dept = tk.LabelFrame(tab_dept, text="Add Department", padx=10, pady=10)
form_dept.pack(fill="x", padx=10, pady=10)

tk.Label(form_dept, text="Dept ID:").grid(row=0, column=0, sticky="w", pady=5)
ent_dept_id = tk.Entry(form_dept, width=25)
ent_dept_id.grid(row=0, column=1, padx=10)

tk.Label(form_dept, text="Dept Name:").grid(row=1, column=0, sticky="w", pady=5)
ent_dept_name = tk.Entry(form_dept, width=25)
ent_dept_name.grid(row=1, column=1, padx=10)

tree_dept = ttk.Treeview(tab_dept, columns=("dept_id", "dept_name"), show="headings")
tree_dept.heading("dept_id", text="Dept ID")
tree_dept.heading("dept_name", text="Department Name")
tree_dept.pack(fill="both", expand=True, padx=10, pady=10)

btn_add_dept = tk.Button(
    form_dept, text="Add Department", bg="#2196F3", fg="white", font=("Arial", 9, "bold"),
    command=lambda: insert_record(
        "INSERT INTO dept_det (dept_id, dept_name) VALUES (%s, %s)",
        (ent_dept_id.get().strip(), ent_dept_name.get().strip()),
        tree_dept, "dept_det", [ent_dept_id, ent_dept_name]
    )
)
btn_add_dept.grid(row=2, column=0, columnspan=2, pady=8)

# ================= TAB 2: EMPLOYEES (emp_det) =================
tab_emp = ttk.Frame(notebook)
notebook.add(tab_emp, text="Employees")

form_emp = tk.LabelFrame(tab_emp, text="Add Employee", padx=10, pady=10)
form_emp.pack(fill="x", padx=10, pady=10)

tk.Label(form_emp, text="Emp ID (e.g., E1001):").grid(row=0, column=0, sticky="w", pady=3)
ent_emp_id = tk.Entry(form_emp, width=25)
ent_emp_id.grid(row=0, column=1, padx=10)

tk.Label(form_emp, text="Name:").grid(row=1, column=0, sticky="w", pady=3)
ent_emp_name = tk.Entry(form_emp, width=25)
ent_emp_name.grid(row=1, column=1, padx=10)

tk.Label(form_emp, text="Email:").grid(row=2, column=0, sticky="w", pady=3)
ent_emp_email = tk.Entry(form_emp, width=25)
ent_emp_email.grid(row=2, column=1, padx=10)

tk.Label(form_emp, text="Dept ID:").grid(row=0, column=2, sticky="w", pady=3)
ent_emp_dept = tk.Entry(form_emp, width=20)
ent_emp_dept.grid(row=0, column=3, padx=10)

tk.Label(form_emp, text="Salary:").grid(row=1, column=2, sticky="w", pady=3)
ent_emp_sal = tk.Entry(form_emp, width=20)
ent_emp_sal.grid(row=1, column=3, padx=10)

tree_emp = ttk.Treeview(tab_emp, columns=("emp_id", "name", "email", "dept_id", "salary"), show="headings")
for col, title in [("emp_id", "Emp ID"), ("name", "Name"), ("email", "Email"), ("dept_id", "Dept ID"), ("salary", "Salary")]:
    tree_emp.heading(col, text=title)
    tree_emp.column(col, width=110)
tree_emp.pack(fill="both", expand=True, padx=10, pady=10)

btn_add_emp = tk.Button(
    form_emp, text="Add Employee", bg="#2196F3", fg="white", font=("Arial", 9, "bold"),
    command=lambda: insert_record(
        "INSERT INTO emp_det (emp_id, name, email, dept_id, salary) VALUES (%s, %s, %s, %s, %s)",
        (ent_emp_id.get().strip(), ent_emp_name.get().strip(), ent_emp_email.get().strip(),
         ent_emp_dept.get().strip(), ent_emp_sal.get().strip()),
        tree_emp, "emp_det", [ent_emp_id, ent_emp_name, ent_emp_email, ent_emp_dept, ent_emp_sal]
    )
)
btn_add_emp.grid(row=3, column=0, columnspan=4, pady=8)

# ================= TAB 3: LEAVES (leave_det) =================
tab_leave = ttk.Frame(notebook)
notebook.add(tab_leave, text="Leaves")

form_leave = tk.LabelFrame(tab_leave, text="Add Leave", padx=10, pady=10)
form_leave.pack(fill="x", padx=10, pady=10)

tk.Label(form_leave, text="Emp ID (e.g., E1001):").grid(row=0, column=0, sticky="w", pady=5)
ent_leave_emp = tk.Entry(form_leave, width=25)
ent_leave_emp.grid(row=0, column=1, padx=10)

tk.Label(form_leave, text="Leave Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
ent_leave_date = tk.Entry(form_leave, width=25)
ent_leave_date.grid(row=1, column=1, padx=10)

tk.Label(form_leave, text="Leave Status:").grid(row=2, column=0, sticky="w", pady=5)
combo_leave_status = ttk.Combobox(form_leave, values=["Pending", "Approved", "Denied", "Sick"], width=22)
combo_leave_status.set("Pending")
combo_leave_status.grid(row=2, column=1, padx=10)

tree_leave = ttk.Treeview(tab_leave, columns=("emp_id", "leave_date", "leave_status"), show="headings")
for col, title in [("emp_id", "Emp ID"), ("leave_date", "Leave Date"), ("leave_status", "Status")]:
    tree_leave.heading(col, text=title)
tree_leave.pack(fill="both", expand=True, padx=10, pady=10)

btn_add_leave = tk.Button(
    form_leave, text="Add Leave", bg="#4CAF50", fg="white", font=("Arial", 9, "bold"),
    command=lambda: insert_record(
        "INSERT INTO leave_det (emp_id, leave_date, leave_status) VALUES (%s, %s, %s)",
        (ent_leave_emp.get().strip(), ent_leave_date.get().strip(), combo_leave_status.get().strip()),
        tree_leave, "leave_det", [ent_leave_emp, ent_leave_date]
    )
)
btn_add_leave.grid(row=3, column=0, columnspan=2, pady=8)

# ================= TAB 4: SALARY (salary) =================
tab_sal = ttk.Frame(notebook)
notebook.add(tab_sal, text="Salary ")

form_sal = tk.LabelFrame(tab_sal, text="Add Salary Record", padx=10, pady=10)
form_sal.pack(fill="x", padx=10, pady=10)

tk.Label(form_sal, text="Emp ID:").grid(row=0, column=0, sticky="w", pady=4)
ent_sal_emp = tk.Entry(form_sal, width=25)
ent_sal_emp.grid(row=0, column=1, padx=10)

tk.Label(form_sal, text="Employee Name (ename):").grid(row=1, column=0, sticky="w", pady=4)
ent_sal_name = tk.Entry(form_sal, width=25)
ent_sal_name.grid(row=1, column=1, padx=10)

tk.Label(form_sal, text="Base Salary (base_sal):").grid(row=0, column=2, sticky="w", pady=4)
ent_sal_amt = tk.Entry(form_sal, width=20)
ent_sal_amt.grid(row=0, column=3, padx=10)

tk.Label(form_sal, text="Salary Status:").grid(row=1, column=2, sticky="w", pady=4)
combo_sal_status = ttk.Combobox(form_sal, values=["approved", "pending"], width=17)
combo_sal_status.set("approved")
combo_sal_status.grid(row=1, column=3, padx=10)

tree_sal = ttk.Treeview(tab_sal, columns=("emp_id", "ename", "base_sal", "sal_status"), show="headings")
for col, title in [("emp_id", "Emp ID"), ("ename", "Employee Name"), ("base_sal", "Base Salary"), ("sal_status", "Status")]:
    tree_sal.heading(col, text=title)
tree_sal.pack(fill="both", expand=True, padx=10, pady=10)

btn_add_sal = tk.Button(
    form_sal, text="Add Salary", bg="#2196F3", fg="white", font=("Arial", 9, "bold"),
    command=lambda: insert_record(
        "INSERT INTO salary (emp_id, ename, base_sal, sal_status) VALUES (%s, %s, %s, %s)",
        (ent_sal_emp.get().strip(), ent_sal_name.get().strip(), ent_sal_amt.get().strip(), combo_sal_status.get().strip()),
        tree_sal, "salary", [ent_sal_emp, ent_sal_name, ent_sal_amt]
    )
)
btn_add_sal.grid(row=2, column=0, columnspan=4, pady=8)

#Load ALL tables on startup
load_table_data(tree_dept,"dept_det")
load_table_data(tree_emp,"emp_det")
load_table_data(tree_leave,"leave_det")
load_table_data(tree_sal,"salary")

root.mainloop()








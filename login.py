from tkinter import *
from tkinter import messagebox
from employee_db import connect_database  # Your database functions
from dashboard import open_dashboard      # Function to open dashboard after login

def login_window():
    def check_login():
        emp_id = empid_entry.get()
        password = password_entry.get()

        if not emp_id or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        cursor, connection = connect_database()
        if cursor is None or connection is None:
            messagebox.showerror("Error", "Database connection failed")
            return

        try:
            cursor.execute("USE inventory_management_system")
            cursor.execute("SELECT name, password FROM employee_data WHERE emp_id=%s", (emp_id,))
            result = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Database query failed: {str(e)}")
            return
        finally:
            if connection: connection.close()
            if cursor: cursor.close()

        if result and result[1] == password:
            messagebox.showinfo("Success", f"Welcome {result[0]}!")
            root.destroy()  # Close login window
            open_dashboard(result[0])  # Pass employee name to dashboard
        else:
            messagebox.showerror("Error", "Invalid Employee ID or Password")

    root = Tk()
    root.title("Employee Login")
    root.geometry("400x250+500+200")
    root.resizable(0, 0)
    root.config(bg="white")

    Label(root, text="Employee Login", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    Label(root, text="Employee ID:", bg="white", font=("Arial", 12)).pack(pady=5)
    empid_entry = Entry(root, font=("Arial", 12))
    empid_entry.pack(pady=5)

    Label(root, text="Password:", bg="white", font=("Arial", 12)).pack(pady=5)
    password_entry = Entry(root, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)

    Button(root, text="Login", font=("Arial", 12), bg="#4caf50", fg="white", width=10,
           command=check_login).pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    login_window()

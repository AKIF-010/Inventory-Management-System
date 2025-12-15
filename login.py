from tkinter import *
from tkinter import messagebox
import os  # 1. Add this import to run external files
from employee_db import connect_database
from dashboard import open_dashboard

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
            
            # 2. UPDATE QUERY: We added 'user_type' to the SELECT statement
            cursor.execute("SELECT name, password, user_type FROM employee_data WHERE emp_id=%s", (emp_id,))
            result = cursor.fetchone()
            
        except Exception as e:
            messagebox.showerror("Error", f"Database query failed: {str(e)}")
            return
        finally:
            if connection: connection.close()
            if cursor: cursor.close()

        if result and result[1] == password:
            # result[0] is Name, result[1] is Password, result[2] is User Type
            user_type = result[2]
            
            messagebox.showinfo("Success", f"Welcome {result[0]}!\nLogged in as {user_type}")
            root.destroy()

            # 3. LOGIC CHECK: Open file based on User Type
            if user_type == "Employee":
                # Opens billing.py directly
                os.system("python billing.py") 
            else:
                # Opens the Admin Dashboard
                open_dashboard(result[0])
                
        else:
            messagebox.showerror("Error", "Invalid Employee ID or Password")

    # --- Main Window ---
    root = Tk()
    root.title("Employee Login")
    root.geometry("500x350+480+180")
    root.resizable(0, 0)
    root.config(bg="#e6ecf0")

    # --- Center Card Frame ---
    card_frame = Frame(root, bg="white", bd=0, highlightthickness=2, highlightbackground="#d1d9e6")
    card_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)

    # Title
    Label(card_frame, text="Login", font=("Helvetica", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(20,10))

    # Employee ID
    Label(card_frame, text="ID", font=("Helvetica", 12), bg="white", anchor=W).pack(fill=X, padx=40, pady=(10,0))
    empid_entry = Entry(card_frame, font=("Helvetica", 12), bd=1, relief=SOLID)
    empid_entry.pack(fill=X, padx=40, pady=5)

    # Password
    Label(card_frame, text="Password", font=("Helvetica", 12), bg="white", anchor=W).pack(fill=X, padx=40, pady=(10,0))
    password_entry = Entry(card_frame, font=("Helvetica", 12), bd=1, relief=SOLID, show="*")
    password_entry.pack(fill=X, padx=40, pady=5)

    # Login Button
    def on_enter(e):
        login_btn['bg'] = "#2980b9"
    def on_leave(e):
        login_btn['bg'] = "#3498db"

    login_btn = Button(card_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white",
                       activebackground="#2980b9", cursor="hand2", bd=0, relief=RIDGE, command=check_login)
    login_btn.pack(pady=25, ipadx=10, ipady=5)
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    root.mainloop()


if __name__ == "__main__":
    login_window()
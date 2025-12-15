from tkinter import *
from tkinter import ttk, messagebox
from employee_db import connect_database 
# NOTE: Ensure employee_db.py is in the same folder

def sales_form(window):
    # 1. Main Frame Setup
    sales_frame = Frame(window, width=1070, height=598, bg='white')
    sales_frame.place(x=200, y=71)
    
    # Title
    title = Label(sales_frame, text="Manage Sales & View Bills", font=("goudy old style", 20, "bold"), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

    # ================= VARIABLES =================
    bill_no_var = StringVar()

    # ================= SEARCH BAR =================
    search_frame = Frame(sales_frame, bg="white", bd=2, relief=RIDGE)
    search_frame.place(x=50, y=50, width=600, height=40)

    lbl_search = Label(search_frame, text="Bill No:", bg="white", font=("times new roman", 15, "bold"))
    lbl_search.place(x=10, y=5)

    txt_search = Entry(search_frame, textvariable=bill_no_var, font=("times new roman", 15), bg="lightyellow")
    txt_search.place(x=100, y=5, width=180)

    btn_search = Button(search_frame, text="Search", font=("times new roman", 12, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=lambda: search_bill())
    btn_search.place(x=300, y=4, width=120, height=28)

    btn_clear = Button(search_frame, text="Clear", font=("times new roman", 12, "bold"), bg="gray", fg="white", cursor="hand2", command=lambda: clear_search())
    btn_clear.place(x=440, y=4, width=120, height=28)

    # ================= SALES TABLE (Left Side) =================
    sales_list_frame = Frame(sales_frame, bd=3, relief=RIDGE)
    sales_list_frame.place(x=50, y=100, width=600, height=450)

    scrolly = Scrollbar(sales_list_frame, orient=VERTICAL)
    scrollx = Scrollbar(sales_list_frame, orient=HORIZONTAL)

    # Columns: Bill No, Date, Customer Name, Phone, Net Pay
    # Note: 'bill_txt' is fetched but not shown in a column, we use it internally
    Sales_Table = ttk.Treeview(sales_list_frame, columns=("bill_no", "date", "name", "phone", "amount"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=Sales_Table.xview)
    scrolly.config(command=Sales_Table.yview)

    Sales_Table.heading("bill_no", text="Bill No.")
    Sales_Table.heading("date", text="Date")
    Sales_Table.heading("name", text="Customer Name")
    Sales_Table.heading("phone", text="Phone")
    Sales_Table.heading("amount", text="Amount")

    Sales_Table.column("bill_no", width=120)
    Sales_Table.column("date", width=100)
    Sales_Table.column("name", width=150)
    Sales_Table.column("phone", width=100)
    Sales_Table.column("amount", width=100)

    Sales_Table["show"] = "headings"
    Sales_Table.pack(fill=BOTH, expand=1)

    # ================= BILL AREA (Right Side) =================
    bill_area_frame = Frame(sales_frame, bd=3, relief=RIDGE)
    bill_area_frame.place(x=700, y=100, width=320, height=450)

    lbl_title_bill = Label(bill_area_frame, text="Customer Bill Area", font=("goudy old style", 15, "bold"), bg="orange").pack(side=TOP, fill=X)

    scrolly2 = Scrollbar(bill_area_frame, orient=VERTICAL)
    bill_txt_area = Text(bill_area_frame, font=("times new roman", 12), bg="lightyellow", yscrollcommand=scrolly2.set)
    scrolly2.pack(side=RIGHT, fill=Y)
    scrolly2.config(command=bill_txt_area.yview)
    bill_txt_area.pack(fill=BOTH, expand=1)

    # ================= FUNCTIONS =================

    def fetch_data():
        """Fetches all bills from database and puts them in the table"""
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute("USE inventory_management_system")
            # Select everything (including bill_txt)
            cursor.execute("SELECT bill_no, date, customer_name, customer_phone, net_pay, bill_txt FROM bill_data")
            rows = cursor.fetchall()
            
            Sales_Table.delete(*Sales_Table.get_children())
            
            for row in rows:
                # We insert the row. Even though we only defined 5 columns, 
                # Treeview stores the 6th element (bill_txt) in the values list invisibly.
                Sales_Table.insert('', END, values=row)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def get_data(event):
        """When a row is clicked, show the bill text on the right side"""
        try:
            row_id = Sales_Table.focus() # Get selected row ID
            content = Sales_Table.item(row_id) # Get data of that row
            row = content['values']
            
            if not row:
                return

            # row structure: [bill_no, date, name, phone, amount, bill_txt]
            # Since bill_txt is the 6th item (index 5)
            # Note: Sometimes Treeview returns text with \n as spaces, so we grab exact index
            
            # Accessing index 5 for bill_txt
            # If the treeview cut it off, we might need to fetch by ID, 
            # but usually, it stores the full tuple.
            
            # Let's write the text to the side area
            bill_txt_area.delete('1.0', END)
            # In some Tkinter versions, values might treat large text oddly.
            # If so, we can query DB by Bill No. Let's try direct access first:
            if len(row) >= 6:
                bill_txt_area.insert(END, row[5])
            else:
                # Fallback: Query DB if the text didn't transfer fully
                print_bill_from_db(row[0])

        except Exception as e:
            pass # Clicked empty area

    def print_bill_from_db(bill_no):
        """Helper to fetch text if treeview click fails"""
        cursor, connection = connect_database()
        try:
            cursor.execute("USE inventory_management_system")
            cursor.execute("SELECT bill_txt FROM bill_data WHERE bill_no=%s", (bill_no,))
            row = cursor.fetchone()
            if row:
                bill_txt_area.insert(END, row[0])
        finally:
            cursor.close()
            connection.close()

    def search_bill():
        """Search by Bill Number"""
        if bill_no_var.get() == "":
            messagebox.showerror("Error", "Search input should be required")
            return
            
        cursor, connection = connect_database()
        try:
            cursor.execute("USE inventory_management_system")
            cursor.execute("SELECT bill_no, date, customer_name, customer_phone, net_pay, bill_txt FROM bill_data WHERE bill_no LIKE %s", ('%' + bill_no_var.get() + '%',))
            rows = cursor.fetchall()
            
            if len(rows) != 0:
                Sales_Table.delete(*Sales_Table.get_children())
                for row in rows:
                    Sales_Table.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No Bill Found")
        except Exception as e:
             messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def clear_search():
        bill_no_var.set("")
        fetch_data()

    # ================= BINDINGS & INITIALIZATION =================
    Sales_Table.bind("<ButtonRelease-1>", get_data) # On Click event
    fetch_data() # Load data when frame opens

    return sales_frame
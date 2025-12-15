from tkinter import *
from time import strftime
from tkinter import ttk
from employee_db import connect_database 
from tkinter import messagebox
import os 
import random 
import sys # <--- 1. ADD THIS IMPORT

# Placeholder for database connection logic
# NOTE: connect_database is assumed to be defined in employee_db.py

window = Tk()
window.title('Inventory Management System')
window.geometry('1270x668+0+0')
window.resizable(0, 0)
window.config(bg='white')

# ==================== GET LOGGED IN USER ====================
# Default to "Admin" if file is run directly, otherwise get from Login
current_user = "Admin"
if len(sys.argv) > 1:
    current_user = sys.argv[1]
# ============================================================

# ==================== GLOBAL VARIABLES FOR DATA BINDING ====================
# Variables for input entries
cart_input_name = StringVar()
cart_input_qty = StringVar()
cart_input_price = StringVar()
cart_input_discount = StringVar()

# Variables to store the actual data of the currently selected product
selected_pid = IntVar()
selected_product_stock_qty = IntVar()

# ==================== CART DATA STRUCTURE ====================
# Structure: [pid, name, price (original), discount, qty, subtotal]
cart_data = []
# ===================================================================================


HEADER_HEIGHT = 70
MAX_Y = 660
HEADER_Y_OFFSET = 80
NEW_FRAME_HEIGHT = MAX_Y - HEADER_Y_OFFSET

# ===================== TOP HEADER =====================

def logout():
    op = messagebox.askyesno("Confirm", "Do you really want to logout?")
    if op == True:
        window.destroy() 
        os.system("python login.py") 

top_frame = Frame(window, bg='#1D293D', height=HEADER_HEIGHT+7, width=1270)
top_frame.place(x=0, y=0)
top_frame.grid_propagate(False)

top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=0)

# UPDATED: Display the user name here
welcome_label = Label(
    top_frame,
    text=f'Welcome, {current_user} | IMS PRO', 
    font=('Tahoma', 16, 'bold'),
    bg='#1D293D',
    fg='white',
    anchor=W
)
welcome_label.grid(row=0, column=0, sticky=W, padx=15, pady=8)

# Load logout image with error handling
try:
    logout_img = PhotoImage(file="logout_icon.png")
except TclError:
    logout_img = PhotoImage(width=1, height=1)

logout_btn = Button(
    top_frame,
    text=" Logout",
    image=logout_img,
    compound=LEFT,
    font=('Tahoma', 11, 'bold'),
    bg='#E5E7EB',
    fg='#1F2937',
    activebackground='#D1D5DB',
    activeforeground='#111827',
    bd=0,
    padx=14,
    pady=6,
    cursor='hand2',
    command=logout 
)
logout_btn.grid(row=0, column=1, sticky=E, padx=20, pady=6)

date_label = Label(
    top_frame,
    font=('Verdana', 13),
    bg='#374151',
    fg='white',
    anchor=W,
    width=1270
)
date_label.grid(row=1, column=0, columnspan=2, sticky=W)

# ... (Keep all your Product/Cart Functions the same until Generate Bill) ...


def generate_bill():
    """Generates the bill text in the bill_text widget."""
    global cart_data
    
    if not cart_data:
        messagebox.showwarning("Warning", "Cart is empty. Please add products first.")
        return

    # 1. Gather Customer and Total Data
    customer_name = customer_name_entry.get().strip()
    customer_phone = customer_phone_entry.get().strip()
    
    try:
        total_gross = float(bill_amount_label.cget("text").split('\n')[1])
        total_discount = float(discount_label.cget("text").split('\n')[1])
        net_pay = float(net_pay_label.cget("text").split('\n')[1])
    except:
        messagebox.showerror("Error", "Billing totals could not be read. Please try again.")
        return

    
    # Generate a unique Bill ID
    bill_id = strftime("%Y%m%d%H%M%S") + str(random.randint(10, 99))
    
    # 2. Build Bill Header (UPDATED TO SHOW BILLER NAME)
    bill_content = f"""
========================================
|          INVENTORY MANAGEMENT        |
|               SALES BILL             |
========================================
Bill ID: {bill_id}
Date: {strftime('%d-%m-%Y')}
Time: {strftime('%I:%M:%S %p')}
Biller: {current_user}
Customer: {customer_name if customer_name else 'N/A'}
Phone: {customer_phone if customer_phone else 'N/A'}
----------------------------------------
| Product       QTY   @Disc  Net Price|
----------------------------------------
"""

    # 3. Build Bill Items 
    for item in cart_data:
        pid, name, price, discount_rate, qty, subtotal = item
        disc_unit_price = price * (1 - discount_rate / 100.0)
        name_short = (name[:13] + '..') if len(name) > 15 else name
        item_line = f"| {name_short:<13} {qty:<5} {disc_unit_price:6.2f} {subtotal:8.2f} |\n"
        bill_content += item_line

    # 4. Build Bill Footer
    bill_content += f"""----------------------------------------
Gross Amount: \t\t{total_gross:10.2f}
Discount:     \t\t-{total_discount:9.2f}
========================================
NET PAYABLE:  \t\t{net_pay:10.2f}
========================================
|   Thank You For Your Business!   |
========================================
    """

    # 5. Display in Text Widget
    bill_text.delete(1.0, END)
    bill_text.insert(END, bill_content)
    
    return bill_id, net_pay 

# ... (Rest of your code remains the same) ...

# ======================= PRODUCT LIST FUNCTIONS =========================#


def clear_product_data():
    """Clears all product selection entries and resets global variables."""
    # Reset StringVars which clears the Entry fields
    cart_input_name.set('')
    cart_input_price.set('')
    cart_input_discount.set('')
    cart_input_qty.set('')

    # Reset Global Data Variables
    selected_pid.set(0)
    selected_product_stock_qty.set(0)

    # Update Stock label
    try:
        stock_label.config(text=f'Available Stock: 0', fg='black')
    except NameError:
        pass

    # Make Name, Price, Discount entries editable again (NORMAL)
    # CRITICAL FIX: Ensure Quantity is also set to NORMAL
    try:
        cart_product_frame_name.config(state=NORMAL)
        cart_product_frame_price.config(state=NORMAL)
        cart_product_frame_discount.config(state=NORMAL)
        cart_product_frame_qty.config(state=NORMAL) 
    except NameError:
        pass


def search_product():
    pid = search_txt.get().strip()

    if pid == "":
        messagebox.showwarning("Warning", "Please enter Product ID")
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_management_system')
        cursor.execute(
            'SELECT id,name,price,discount,quantity,status FROM product_data WHERE id=%s',
            (pid,)
        )
        record = cursor.fetchone()

        treeview.delete(*treeview.get_children())
        clear_product_data()  # Clear cart entries on search results change

        if record:
            treeview.insert('', END, values=record)
        else:
            messagebox.showinfo("Not Found", "No product found with this PID")

    except Exception as e:
        messagebox.showerror('Error', f'Error due to : {str(e)}')

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


def show_all_products():
    search_txt.delete(0, END)
    treeview_data(treeview)
    clear_product_data()  # Clear cart entries on show all


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        # Handle case where database connection is not established
        treeview.delete(*treeview.get_children())
        return

    try:
        cursor.execute('USE inventory_management_system')
        cursor.execute(
            'SELECT id,name,price,discount,quantity,status FROM product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error loading products: {str(e)}')
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass

# ======================= PRODUCT LIST FRAME =========================#


Product_frame = Frame(window, bg='white', bd=2, relief=RIDGE)
Product_frame.place(x=5, y=HEADER_Y_OFFSET, width=400, height=NEW_FRAME_HEIGHT)
Product_title = Label(Product_frame, text='All Products', font=(
    'times new roman', 15, 'bold'), bg='#242623', fg='white')
Product_title.pack(side=TOP, fill=X)

search_frame = Frame(Product_frame, bg='white', bd=2, relief=RIDGE)
search_frame.pack(side=TOP, fill=X)

search_by = Label(
    search_frame, text='PID', font=('times new roman', 12, 'bold'), bg='white'
)
search_by.grid(row=0, column=0, padx=6, pady=4, sticky=W)

search_txt = Entry(
    search_frame, font=('times new roman', 12), bd=2, relief=RIDGE, width=17
)
search_txt.grid(row=0, column=1, padx=6, pady=4, sticky=W)

search_btn = Button(
    search_frame, text='Search', font=('times new roman', 12), bg='#4caf50', fg='white', cursor='hand2', width=7, command=lambda: search_product()
)
search_btn.grid(row=0, column=2, padx=8, pady=4)

show_all_btn = Button(
    search_frame, text='Show All', font=('times new roman', 12), bg='#2196f3', fg='white', cursor='hand2', width=7, command=lambda: show_all_products()
)
show_all_btn.grid(row=0, column=3, padx=6, pady=4)

treeview_frame = Frame(Product_frame, bd=3, relief=RIDGE)
treeview_frame.pack(fill=BOTH, expand=1)
Scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
Scrolly.pack(side=RIGHT, fill=Y)
Scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
Scrollx.pack(side=BOTTOM, fill=X)
treeview = ttk.Treeview(treeview_frame, columns=(
    'pid', 'name', 'price', 'discount', 'qty', 'status'), show='headings')
treeview.configure(yscrollcommand=Scrolly.set, xscrollcommand=Scrollx.set)
Scrolly.config(command=treeview.yview)
Scrollx.config(command=treeview.xview)
treeview.heading('pid', text='PID')
treeview.heading('name', text='Name')
treeview.heading('price', text='Price')
treeview.heading('discount', text='Discount')
treeview.heading('qty', text='Quantity')
treeview.heading('status', text='Status')
treeview.column('pid', width=100)
treeview.column('name', width=100)
treeview.column('price', width=70)
treeview.column('discount', width=70)
treeview.column('qty', width=70)
treeview.column('status', width=80)

treeview.pack(fill=BOTH, expand=1)
treeview_data(treeview)

# ======================= CUSTOMER (Fixed Height) =========================#

CUSTOMER_FRAME_HEIGHT = 70
customer_frame = Frame(window, bg='white', bd=2, relief=RIDGE)
customer_frame.place(x=410, y=HEADER_Y_OFFSET, width=500,
                     height=CUSTOMER_FRAME_HEIGHT)
customer_title = Label(customer_frame, text='Customer Details', font=(
    'times new roman', 15, 'bold'), bg='#242623', fg='white')
customer_title.pack(side=TOP, fill=X)
customer_name_label = Label(
    customer_frame, text='Name', font=('times new roman', 12, 'bold'), bg='white')
customer_name_label.place(x=5, y=35)
customer_name_entry = Entry(customer_frame, font=(
    'times new roman', 12), bd=2, relief=RIDGE)
customer_name_entry.place(x=70, y=35, width=140)
customer_phone_label = Label(
    customer_frame, text='Phone No.', font=('times new roman', 12, 'bold'), bg='white')
customer_phone_label.place(x=240, y=35)
customer_phone_entry = Entry(customer_frame, font=(
    'times new roman', 12), bd=2, relief=RIDGE)
customer_phone_entry.place(x=340, y=35, width=140)

# ======================= calculator and cart =========================#

CAL_CART_Y = HEADER_Y_OFFSET + CUSTOMER_FRAME_HEIGHT + 4  # 4px gap
ADD_CART_FRAME_HEIGHT = 140
CAL_CART_HEIGHT = (MAX_Y - CAL_CART_Y) - ADD_CART_FRAME_HEIGHT - 4

cal_cart_frame = Frame(window, bg='white', bd=2, relief=RIDGE)
cal_cart_frame.place(x=410, y=CAL_CART_Y, width=500, height=CAL_CART_HEIGHT)

# calculator frame
calculator_frame = Frame(cal_cart_frame, bg='white', bd=1, relief=RIDGE)
calculator_frame.place(x=5, y=5, width=240, height=CAL_CART_HEIGHT - 10)

# ===================== CALCULATOR =====================

calc_var = StringVar()

calc_entry = Entry(
    calculator_frame,
    textvariable=calc_var,
    font=('Arial', 18),
    bd=5,
    relief=RIDGE,
    justify=RIGHT
)
calc_entry.grid(row=0, column=0, columnspan=4, padx=5,
                 pady=8, ipady=8, sticky="nsew")


def press(key):
    if key == 'C':
        calc_var.set('')
    elif key == '=':
        try:
            calc_var.set(str(eval(calc_var.get())))
        except:
            calc_var.set('Error')
    else:
        calc_var.set(calc_var.get() + key)


buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ('C', 5, 0)
]

for (text, row, col) in buttons:
    btn = Button(
        calculator_frame,
        text=text,
        font=('Arial', 12, 'bold'),
        bg='#F3F4F6' if text not in (
            '=', 'C') else '#EF4444' if text == 'C' else '#22C55E',
        fg='black' if text not in ('C', '=') else 'white',
        bd=1,
        cursor='hand2',
        command=lambda t=text: press(t)
    )
    btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")


for i in range(6):
    calculator_frame.rowconfigure(i, weight=1)

for i in range(4):
    calculator_frame.columnconfigure(i, weight=1)

# ===================== CART FUNCTIONS =====================

def clear_all_transaction(suppress_popup=False):
    """Resets the entire sales transaction."""
    global cart_data
    
    # 1. Clear Customer Details
    customer_name_entry.delete(0, END)
    customer_phone_entry.delete(0, END)
    
    # 2. Clear Cart Data and Display
    cart_data = []
    # This calls calculate_totals, which needs the bill labels to exist!
    refresh_cart_treeview() 
    
    # 3. Clear Bill Text Area
    bill_text.delete(1.0, END)
    bill_text.insert(END, "\n\n\t\t--- New Transaction Initiated ---")
    
    # 4. Clear Product Selection Area
    clear_product_data()
    
    # Only show popup if suppress_popup is False
    if not suppress_popup:
        messagebox.showinfo("Reset", "Transaction cleared successfully.")


def calculate_totals():
    global cart_data
    total_bill_gross = 0.0
    total_discount_value = 0.0
    total_products = len(cart_data)
    
    # Calculate totals from the global cart_data list
    for item in cart_data:
        # item structure: [pid, name, price, discount_rate, qty, subtotal]
        unit_price = item[2]
        discount_rate = item[3] / 100.0
        qty = item[4]
        
        # Gross amount for this product
        gross_amount = unit_price * qty
        
        # Calculate discount amount for this product
        discount_amount = gross_amount * discount_rate
        
        total_bill_gross += gross_amount
        total_discount_value += discount_amount
        
    net_pay = total_bill_gross - total_discount_value
    
    # Update UI labels
    try:
        cart_total_products_label.config(text=f'Total Products: {total_products}')
        bill_amount_label.config(text=f'Bill\n{total_bill_gross:.2f}')
        discount_label.config(text=f'Dis\n{total_discount_value:.2f}')
        net_pay_label.config(text=f'Net\n{net_pay:.2f}')
    except NameError:
        # This catches errors if we try to calculate before labels exist
        pass


def refresh_cart_treeview():
    """
    Clears and repopulates the cart treeview from the global cart_data list.
    Displays the UNIT PRICE *AFTER* DISCOUNT in the 'Price' column.
    """
    treeview_cart.delete(*treeview_cart.get_children())
    
    for item in cart_data:
        # item structure: [pid, name, price (original), discount_rate, qty, subtotal]
        
        original_price = item[2]
        discount_rate = item[3]
        
        # Calculate the unit price AFTER discount
        discount_factor = (100 - discount_rate) / 100.0
        discounted_unit_price = original_price * discount_factor
        
        
        # We display: PID, Name, Discounted Unit Price, Discount %, Quantity
        display_values = [
            item[0], 
            item[1], 
            f'{discounted_unit_price:.2f}', 
            f'{item[3]}%', 
            item[4]
        ]
        treeview_cart.insert('', END, values=display_values)
        
    calculate_totals() # Recalculate and update billing area


def add_to_cart():
    # 1. Validation: Check if a product is selected
    pid = selected_pid.get()
    if pid == 0:
        messagebox.showwarning(
            "Warning", "Please select a product from the list first.")
        return

    # 2. Validation: Check Quantity input
    try:
        qty_input = cart_input_qty.get().strip()
        if not qty_input:
            messagebox.showwarning("Warning", "Please enter the quantity.")
            return

        qty_to_add = int(qty_input)
        if qty_to_add <= 0:
            messagebox.showwarning(
                "Warning", "Quantity must be a positive integer.")
            return

    except ValueError:
        messagebox.showerror("Error", "Quantity must be a valid integer.")
        return

    # Fetch data from StringVars (which were populated in get_data_from_list)
    product_name = cart_input_name.get()
    try:
        price = float(cart_input_price.get())
        discount_rate = int(cart_input_discount.get())
        stock_qty = selected_product_stock_qty.get()
    except ValueError:
        messagebox.showerror(
            "Error", "Internal product data error (Price/Discount). Clear and re-select product.")
        return

    # 3. Stock Check
    if qty_to_add > stock_qty:
        messagebox.showwarning(
            "Stock Low", f"Insufficient stock for {product_name}. Available: {stock_qty}")
        return

    # Calculate subtotal 
    discount_factor = (100 - discount_rate) / 100.0
    subtotal = (price * qty_to_add) * discount_factor

    # 4. Cart Management: Check if product already exists
    item_found = False
    for i, item in enumerate(cart_data):
        if item[0] == pid:
            # Item found: Update quantity

            # Check if updated quantity exceeds stock
            new_qty = qty_to_add
            if new_qty > stock_qty:
                messagebox.showwarning(
                    "Stock Limit", f"New quantity ({new_qty}) exceeds available stock ({stock_qty}).")
                return  # Stop the update

            cart_data[i][4] = new_qty
            # Update subtotal
            cart_data[i][5] = (price * new_qty) * discount_factor 

            item_found = True
            messagebox.showinfo(
                "Cart Updated", f"Quantity for {product_name} updated to {new_qty}.")
            break

    # If item not found, add new item to cart
    if not item_found:
        cart_data.append([
            pid,
            product_name,
            price, # original price
            discount_rate,
            qty_to_add,
            subtotal
        ])
        messagebox.showinfo("Success", f"{product_name} added to cart.")

    # 5. Refresh UI and clear input
    refresh_cart_treeview()
    clear_product_data()


def finalize_sale_and_save():
    """Generates bill, updates DB stock, saves bill to DB, and saves to file."""
    global cart_data
    
    if not cart_data:
        messagebox.showwarning("Cannot Save", "Cart is empty. No transaction to save.")
        return

    # 1. Generate Bill Preview
    result = generate_bill()
    if not result:
        return
        
    bill_id, net_pay = result
    
    # Get the full text content of the bill
    bill_content = bill_text.get(1.0, END)
    
    # Get Customer Details
    c_name = customer_name_entry.get().strip()
    c_phone = customer_phone_entry.get().strip()
    current_date = strftime('%d-%m-%Y')

    if not messagebox.askyesno("Confirm Sale", f"Final Net Payable is {net_pay:.2f}.\nProceed to finalize sale?"):
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("DB Error", "Failed to connect to database.")
        return

    try:
        connection.autocommit = False # Start transaction
        cursor.execute('USE inventory_management_system')
        
        # ---------------------------------------------------------
        # A. Update Stock in Product Table
        # ---------------------------------------------------------
        for item in cart_data:
            pid, name, price, discount_rate, qty, subtotal = item
            update_query = 'UPDATE product_data SET quantity = quantity - %s WHERE id = %s'
            cursor.execute(update_query, (qty, pid))
            
        # ---------------------------------------------------------
        # B. Save Bill Text into Database (New Feature)
        # ---------------------------------------------------------
        insert_query = """
            INSERT INTO bill_data (bill_no, date, customer_name, customer_phone, net_pay, bill_txt) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            bill_id, 
            current_date, 
            c_name, 
            c_phone, 
            str(net_pay), 
            bill_content
        ))
        
        connection.commit() # Commit changes if both steps succeed
        
        # ---------------------------------------------------------
        # C. Save Local Text File (Backup)
        # ---------------------------------------------------------
        if not os.path.exists("Bills"):
            os.makedirs("Bills")
        full_path = os.path.join("Bills", f"Bill_{bill_id}.txt")
        with open(full_path, 'w') as f:
            f.write(bill_content)
        
        messagebox.showinfo("Success", f"Sale finalized.\nStock Updated.\nBill Saved to Database & File.")

        # 4. Reset Transaction
        clear_all_transaction(suppress_popup=True) 
        show_all_products() 

    except Exception as e:
        connection.rollback() # Undo everything if error occurs
        messagebox.showerror('DB Error', f'Transaction Failed. Rolled back.\nError: {str(e)}')
    
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
# ===================== END CART FUNCTIONS =======================


# cart frame
cart_frame = Frame(cal_cart_frame, bg='white', bd=1, relief=RIDGE)
cart_frame.place(x=250, y=5, width=245, height=CAL_CART_HEIGHT - 10)
cart_title = Label(cart_frame, text='Cart Details', font=(
    'times new roman', 12, 'bold'), bg='#242623', fg='white')
cart_title.pack(side=TOP, fill=X)
cart_total_products_label = Label(
    cart_frame, text='Total Products: 0', font=('times new roman', 12, 'bold'), bg='white')
cart_total_products_label.pack(side=TOP, anchor=S, padx=5)
# treeview for cart
treeview_frame_cart = Frame(cart_frame, bd=3, relief=RIDGE)
treeview_frame_cart.pack(fill=BOTH, expand=1)
Scrolly_cart = Scrollbar(treeview_frame_cart, orient=VERTICAL)
Scrolly_cart.pack(side=RIGHT, fill=Y)
Scrollx_cart = Scrollbar(treeview_frame_cart, orient=HORIZONTAL)
Scrollx_cart.pack(side=BOTTOM, fill=X)
treeview_cart = ttk.Treeview(treeview_frame_cart, columns=(
    'pid', 'name', 'price', 'discount', 'qty'), show='headings')
treeview_cart.configure(yscrollcommand=Scrolly_cart.set,
                         xscrollcommand=Scrollx_cart.set)
Scrolly_cart.config(command=treeview_cart.yview)
Scrollx_cart.config(command=treeview_cart.xview)
treeview_cart.heading('pid', text='PID')
treeview_cart.heading('name', text='Name')
treeview_cart.heading('price', text='Price')
treeview_cart.heading('discount', text='Discount')
treeview_cart.heading('qty', text='Quantity')
treeview_cart.column('pid', width=100)
treeview_cart.column('name', width=100)
treeview_cart.column('price', width=70)
treeview_cart.column('discount', width=70)
treeview_cart.column('qty', width=70)
treeview_cart.pack(fill=BOTH, expand=1)

# ======================= PRODUCT SELECTION LOGIC =========================#


def get_data_from_list(event):
    """
    Fetches data from the selected row, populates the Add Cart frame,
    performs a status check, and locks fields.
    """
    clear_product_data()

    selected_row = treeview.focus()
    if not selected_row:
        return

    content = treeview.item(selected_row)
    values = content['values']

    if not values:
        return

    # Data structure: (id, name, price, discount, quantity, status)
    try:
        pid = values[0]
        name = values[1]
        price = float(values[2])
        discount = int(values[3])
        qty = int(values[4])
        status = values[5]
    except (IndexError, ValueError) as e:
        messagebox.showerror(
            'Data Error', f'Failed to parse product data: {e}')
        return

    # 1. Status Check
    if status.lower() == 'inactive':
        messagebox.showwarning(
            'Product Inactive', f'Product "{name}" is currently NOT FOR SALE and cannot be added to the cart.')
        clear_product_data()
        return

    # 2. Update internal variables
    selected_pid.set(pid)
    selected_product_stock_qty.set(qty)

    # 3. Populate entry fields (using StringVar bindings)
    cart_input_name.set(name)
    cart_input_price.set(f'{price:.2f}')
    cart_input_discount.set(discount)
    cart_input_qty.set('')  # IMPORTANT: Quantity input is BLANK

    # 4. Check if item is already in cart and pre-fill quantity
    for item in cart_data:
        if item[0] == pid:
            cart_input_qty.set(item[4])
            break

    # 5. Update Stock label
    stock_label.config(
        text=f'Available Stock: {qty}', fg='green' if qty > 0 else 'red')

    # 6. Make fetched entries read-only (user only inputs Quantity)
    cart_product_frame_name.config(state='readonly')
    cart_product_frame_price.config(state='readonly')
    cart_product_frame_discount.config(state='readonly')
    
    # CRITICAL FIX: Ensure Quantity is editable and set focus
    cart_product_frame_qty.config(state=NORMAL)
    cart_product_frame_qty.focus()


# BINDING: When a row is clicked, call get_data_from_list
treeview.bind('<ButtonRelease-1>', get_data_from_list)


# ======================= Add cart frame =========================#

ADD_CART_FRAME_HEIGHT = 140
add_cart_frame = Frame(window, bg='white', bd=2, relief=RIDGE)
ADD_CART_Y = MAX_Y - ADD_CART_FRAME_HEIGHT
add_cart_frame.place(x=410, y=ADD_CART_Y, width=500,
                     height=ADD_CART_FRAME_HEIGHT)

cart_product_frame = Frame(add_cart_frame, bg='white')
cart_product_frame.place(x=5, y=2, width=490, height=60)

cart_product_name_label = Label(
    cart_product_frame, text='Product Name', font=('times new roman', 12, 'bold'), bg='white')
cart_product_name_label.grid(row=0, column=0, padx=5)
cart_product_qty_label = Label(cart_product_frame, text='Quantity', font=(
    'times new roman', 12, 'bold'), bg='white')
cart_product_qty_label.grid(row=0, column=1, padx=5)
cart_product_price_label = Label(cart_product_frame, text='Price', font=(
    'times new roman', 12, 'bold'), bg='white')
cart_product_price_label.grid(row=0, column=2, padx=5)
# Discount label
cart_product_discount_label = Label(cart_product_frame, text='Discount (%)', font=(
    'times new roman', 12, 'bold'), bg='white')
cart_product_discount_label.grid(row=0, column=3, padx=5)


# Entries (MODIFIED: Added textvariable binding)
cart_product_frame_name = Entry(cart_product_frame, textvariable=cart_input_name, font=(
    'times new roman', 12), bd=2, relief=RIDGE, width=13)
cart_product_frame_name.grid(row=1, column=0, padx=5)

cart_product_frame_qty = Entry(cart_product_frame, textvariable=cart_input_qty, font=(
    'times new roman', 12), bd=2, relief=RIDGE, width=13)
cart_product_frame_qty.grid(row=1, column=1, padx=5)

cart_product_frame_price = Entry(cart_product_frame, textvariable=cart_input_price, font=(
    'times new roman', 12), bd=2, relief=RIDGE, width=13)
cart_product_frame_price.grid(row=1, column=2, padx=5)
# Discount entry
cart_product_frame_discount = Entry(cart_product_frame, textvariable=cart_input_discount, font=(
    'times new roman', 12), bd=2, relief=RIDGE, width=13)
cart_product_frame_discount.grid(row=1, column=3, padx=5)

for i in range(4):
    cart_product_frame.columnconfigure(i, weight=1)


add_frame = Frame(add_cart_frame, bg='white')
add_frame.place(x=5, y=70, width=490, height=60)

# Stock label updated
stock_label = Label(
    add_frame, text='Available Stock: 0', font=('times new roman', 12, 'bold'), bg='white')
stock_label.pack(side=LEFT, padx=(5, 0))

# Clear button (MODIFIED: added command)
clear_button = Button(
    add_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#f44336', fg='white', cursor='hand2', width=10, height=1, command=clear_product_data)
clear_button.pack(side=RIGHT, padx=(5, 15))
add_or_update_cart_button = Button(
    add_frame, text='Add | Update Cart', font=('times new roman', 12, 'bold'), bg='#4caf50', fg='white', cursor='hand2', width=15, height=1, command=add_to_cart)
add_or_update_cart_button.pack(side=RIGHT, padx=5)

# Initialize data and field states
clear_product_data()


# ======================= BILLING AREA =====================#

BILL_BUTTON_FRAME_HEIGHT = 140
BILL_FRAME_HEIGHT = NEW_FRAME_HEIGHT - \
    BILL_BUTTON_FRAME_HEIGHT - 4  # Recalculated height

billframe = Frame(window, bg='white', bd=2, relief=RIDGE)
billframe.place(x=920, y=HEADER_Y_OFFSET, width=340, height=BILL_FRAME_HEIGHT)

billframe_title = Label(billframe, text='Billing Area', font=(
    'times new roman', 15, 'bold'), bg='#242623', fg='white')
billframe_title.pack(side=TOP, fill=X)

Scrolly_bill = Scrollbar(billframe, orient=VERTICAL)
Scrolly_bill.pack(side=RIGHT, fill=Y)
bill_text = Text(billframe, yscrollcommand=Scrolly_bill.set,
                 bg='white', fg='black', font=('times new roman', 12))
bill_text.pack(fill=BOTH, expand=1)
Scrolly_bill.config(command=bill_text.yview)


# ======================= BILLING BUTTONS =====================#

bill_button_frame = Frame(window, bg='white', bd=2, relief=RIDGE)
BILL_BUTTON_Y = MAX_Y - BILL_BUTTON_FRAME_HEIGHT
bill_button_frame.place(x=920, y=BILL_BUTTON_Y, width=340,
                         height=BILL_BUTTON_FRAME_HEIGHT)

bill_amount_label = Label(
    bill_button_frame,
    text='Bill\n0.00',
    font=('Arial', 12, 'bold'),
    bg='#4A90E2',
    fg='white',
    width=10,
    height=2,
    justify=CENTER
)
bill_amount_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

discount_label = Label(
    bill_button_frame,
    text='Dis\n0.00',  
    font=('Arial', 12, 'bold'),
    bg='#7ED321',
    fg='white',
    width=10,
    height=2,
    justify=CENTER
)
discount_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

net_pay_label = Label(
    bill_button_frame,
    text='Net\n0.00',
    font=('Arial', 12, 'bold'),
    bg='#D0021B',
    fg='white',
    width=10,
    height=2,
    justify=CENTER
)
net_pay_label.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

# -------- Row 1 : Buttons --------
generate_preview_button = Button(
    bill_button_frame,
    text='Preview Bill', # Renamed 'Print' to 'Preview Bill' for clarity
    font=('Arial', 12, 'bold'),
    bg='#50E3C2',
    fg='white',
    width=10,
    height=2,
    cursor='hand2',
    command=generate_bill # Bound to generate_bill for preview
)
generate_preview_button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

clear_all_button = Button(
    bill_button_frame,
    text='Clear All', # Renamed 'Clear' to 'Clear All' for clarity
    font=('Arial', 12, 'bold'),
    bg='gray',
    fg='white',
    width=10,
    height=2,
    cursor='hand2',
    command=clear_all_transaction
)
clear_all_button.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

generate_save_button = Button(
    bill_button_frame,
    text='Save', # Renamed 'Save' to 'Finalize & Save'
    font=('Arial', 12, 'bold'),
    bg='#9013FE',
    fg='white',
    width=10,
    height=2,
    cursor='hand2',
    command=finalize_sale_and_save # Bound to the final logic
)
generate_save_button.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

# Grid resize safety
for i in range(3):
    bill_button_frame.columnconfigure(i, weight=1)
for i in range(2):
    bill_button_frame.rowconfigure(i, weight=1)

# Initialize bill text area after EVERYTHING is defined
# MOVED HERE TO FIX NAME ERROR
clear_all_transaction(suppress_popup=True) 

window.mainloop()
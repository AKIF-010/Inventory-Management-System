from tkinter import *
from time import strftime
from tkinter import messagebox
from employee_db import employee_form, connect_database
from supplier_db import supplier_form
from category_db import category_form
from products_db import product_form
from sales_db import sales_form


Current_frame = None

def show_form(form_function):
    global Current_frame
    if Current_frame:
        Current_frame.place_forget()
    Current_frame = form_function(window)

def open_dashboard(employee_name="Admin"):
    global window, total_emp_count, total_supplier_count, total_category_count, total_product_count, total_sales_count

    window = Tk()
    window.title('Inventory Management System')
    window.geometry('1270x668+0+0')
    window.resizable(0,0)
    window.config(bg='white')

    HEADER_HEIGHT = 70
    MENU_WIDTH = 200
    HEADER_WIDTH = 1270 - MENU_WIDTH
    CARD_START_Y = 155

    ORIGINAL_BG = '#1D293D'
    HOVER_BG = '#155DFC'

    def on_enter(event):
        event.widget.config(bg=HOVER_BG)
    def on_leave(event):
        event.widget.config(bg=ORIGINAL_BG)

    # --- Top Frame ---
    top_frame = Frame(window, bg='white', height=HEADER_HEIGHT, width=HEADER_WIDTH)
    top_frame.place(x=MENU_WIDTH, y=0)
    top_frame.grid_propagate(False)

    welcome_label = Label(top_frame, text=f'Welcome, {employee_name}', font=('Tahoma', 16), bg='white', fg='black', anchor=W)
    welcome_label.grid(row=0, column=0, sticky=W, padx=10, pady=5)

    date_label = Label(top_frame, font=('Verdana', 13), bg='white', fg='black', anchor=W)
    date_label.grid(row=1, column=0, sticky=W, padx=10)

    def update_time():
        current_time = strftime('%I:%M:%S %p')
        current_date = strftime('%d-%m-%Y')
        date_label.config(text=f"Date: {current_date}      Time: {current_time}")
        date_label.after(1000, update_time)

    update_time()

    # --- Left Menu ---
    leftframe = Frame(window, bg=ORIGINAL_BG)
    leftframe.place(x=0, y=0, relheight=1, width=200)

    manu_image = PhotoImage(file='inventory.png')
    manu = Label(leftframe, image=manu_image, compound=LEFT, text=' IMS PRO',
                 font=('times new roman',20), bg=ORIGINAL_BG, fg='white', anchor=W, padx=10, height=70, width=200)
    manu.pack(fill=X)

    active_bg_color = HOVER_BG

    # --- Menu Buttons ---
    def create_menu_button(parent, img_file, text, command):
        img = PhotoImage(file=img_file)
        btn = Button(parent, image=img, compound=LEFT, text=f' {text}', font=('times new roman',18), anchor=W,
                     padx=10, bd=0, bg=ORIGINAL_BG, fg='white', cursor='hand2', activebackground=active_bg_color,
                     command=command)
        btn.image = img
        btn.pack(fill=X, pady=10)
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn

    create_menu_button(leftframe, 'employee1.png', 'Employee', lambda: show_form(employee_form))
    create_menu_button(leftframe, 'supplier.png', 'Supplier', lambda: show_form(supplier_form))
    create_menu_button(leftframe, 'category.png', 'Categories', lambda: show_form(category_form))
    create_menu_button(leftframe, 'product.png', 'Products', lambda: show_form(product_form))
    create_menu_button(leftframe, 'category.png', 'Sales', lambda: show_form(sales_form))
    create_menu_button(leftframe, 'taxes.png', 'Tax', lambda: tax_window())
    create_menu_button(leftframe, 'exit.png', 'Exit', lambda: window.destroy())

    # --- Dashboard Cards ---
    def create_card(x, y, color, title, var, img_file):
        frame = Frame(window, bg=color, bd=0)
        frame.place(x=x, y=y, height=150, width=250)
        Label(frame, text=title, font=('times new roman', 12), fg='white', bg=color).place(x=15, y=15)
        Label(frame, textvariable=var, font=('times new roman', 40, 'bold'), fg='white', bg=color).place(x=15, y=50)
        img = PhotoImage(file=img_file)
        lbl = Label(frame, image=img, bg=color)
        lbl.image = img
        lbl.place(relx=0.9, rely=0.55, anchor=E)
        return frame

    total_emp_count = StringVar(value="0")
    total_supplier_count = StringVar(value="0")
    total_category_count = StringVar(value="0")
    total_product_count = StringVar(value="0")
    total_sales_count = StringVar(value="0")  # static (no sales table)

    create_card(400, CARD_START_Y, "#3A78F2", "Total Employees", total_emp_count, "employee1.png")
    create_card(800, CARD_START_Y, "#7030A0", "Total Suppliers", total_supplier_count, "supplier.png")
    create_card(400, CARD_START_Y + 175, "#008000", "Total Categories", total_category_count, "category.png")
    create_card(800, CARD_START_Y + 175, "#FF4500", "Total Products", total_product_count, "product.png")
    create_card(600, CARD_START_Y + 350, "#00B09E", "Total Sales", total_sales_count, "sale.png")  # static

    # --- Update counts ---
    def update():
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute("USE inventory_management_system")

        cursor.execute("SELECT * FROM employee_data")
        total_emp_count.set(str(len(cursor.fetchall())))

        cursor.execute("SELECT * FROM supplier_data")
        total_supplier_count.set(str(len(cursor.fetchall())))

        cursor.execute("SELECT * FROM category_data")
        total_category_count.set(str(len(cursor.fetchall())))

        cursor.execute("SELECT * FROM product_data")
        total_product_count.set(str(len(cursor.fetchall())))

        cursor.close()
        connection.close()

    update()

    # --- Auto-refresh dashboard counts ---
    def refresh_counts():
        update()  # Call the update function to refresh all counts
        window.after(3000, refresh_counts)  # Repeat every 3 seconds
    
    refresh_counts()  # Start auto-refreshing

    
    # --- Tax Window ---
    def tax_window():
        def save_tax():
            value = tax_count.get()
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            cursor.execute('USE inventory_management_system')
            cursor.execute('CREATE TABLE IF NOT EXISTS tax_data(id INT PRIMARY KEY, tax DECIMAL(5,2))')
            cursor.execute('SELECT id FROM tax_data WHERE id=1')
            if cursor.fetchone():
                cursor.execute('UPDATE tax_data SET tax=%s WHERE id=1', (value,))
            else:
                cursor.execute('INSERT INTO tax_data(id, tax) VALUES(1, %s)', (value,))
            connection.commit()
            messagebox.showinfo('Success', f'{value}% tax added successfully!')
            connection.close()
            cursor.close()

        tax_root = Toplevel()
        tax_root.title('Enter Tax Percentage')
        tax_root.geometry('400x200+300+200')
        tax_root.resizable(0,0)
        tax_root.grab_set()

        Label(tax_root, text='Enter Tax Percentage (%)', font=('times new roman',14)).pack(pady=20)
        tax_count = Spinbox(tax_root, from_=0, to=100, font=('times new roman',14))
        tax_count.pack(pady=(0,20))

        Button(tax_root, text='Save', font=('times new roman',12), bg='#4caf50', fg='white',
               cursor='hand2', width=8, command=save_tax).pack()
    
    window.mainloop()
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from employee_db import connect_database
import os

def sales_form(window):
    global back_image
    
    # 1. Main Frame Setup (Matches Product Frame)
    sales_frame = Frame(window, width=1070, height=598, bg='white')
    sales_frame.place(x=200, y=71)

    # 2. Header and Back Button
    heading_label = Label(sales_frame, text='Manage Sales & View Bills', font=('times new roman', 16, 'bold'), bg="#0f4d7d", fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # Note: Ensure 'back.png' is in the same folder, just like in product_form
    back_image = PhotoImage(file='back.png')
    back_button = Button(sales_frame, image=back_image, bd=0, bg='white', cursor='hand2', command=lambda: sales_frame.place_forget())
    back_button.place(x=1, y=36)

    # ================= INTERNAL FUNCTIONS =================

    def fetch_sales_data(treeview):
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_management_system')
            # Fetching all columns including bill_txt
            cursor.execute('SELECT bill_no, date, customer_name, customer_phone, net_pay, bill_txt FROM bill_data')
            records = cursor.fetchall()
            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert('', END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to : {str(e)}')
        finally:
            try:
                cursor.close()
                connection.close()
            except:
                pass

    def search_sales(search_combobox, search_entry, treeview):
        if search_combobox.get() == 'Search BY' or search_combobox.get() == 'Select':
            messagebox.showwarning('Warning', 'Please select an Option')
            return
        if search_entry.get() == '':
            messagebox.showwarning('Warning', 'Please enter the value to search')
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('USE inventory_management_system')
            col_name = search_combobox.get()
            
            # Map UI names to Database Column names
            if col_name == "Bill No":
                query_col = "bill_no"
            elif col_name == "Customer Name":
                query_col = "customer_name"
            elif col_name == "Phone":
                query_col = "customer_phone"
            else:
                return # Should not happen

            # Using LIKE for flexible search
            query = f"SELECT bill_no, date, customer_name, customer_phone, net_pay, bill_txt FROM bill_data WHERE {query_col} LIKE %s"
            cursor.execute(query, ('%' + search_entry.get() + '%',))
            records = cursor.fetchall()
            
            treeview.delete(*treeview.get_children())
            if records:
                for record in records:
                    treeview.insert('', END, values=record)
            else:
                messagebox.showinfo('Info', 'No matching record found')
                
        except Exception as e:
            messagebox.showerror('Error', f'Error due to : {str(e)}')
        finally:
            try:
                cursor.close()
                connection.close()
            except:
                pass

    def clear_search(search_entry, treeview):
        search_entry.delete(0, END)
        fetch_sales_data(treeview)
        bill_text_area.delete(1.0, END)

    def select_data(event, treeview):
        selected = treeview.selection()
        if not selected:
            return
        item = treeview.item(selected[0])
        content = item.get('values', [])
        
        if not content:
            return
            
        # content structure: [bill_no, date, name, phone, amount, bill_txt]
        # bill_txt is at index 5
        
        # Display the bill text in the right frame
        bill_text_area.delete(1.0, END)
        
        # NOTE: Sometimes Treeview returns values as a string if they contain spaces. 
        # But usually for a tuple it works fine.
        try:
            # We grab the last element which is the bill text
            # Depending on how tkinter parses the tuple, we explicitly grab index 5
            bill_receipt = content[5] 
            bill_text_area.insert(END, bill_receipt)
        except IndexError:
            pass

    # ================= LAYOUT =================

    # --- Search Frame (Styled exactly like Product Form) ---
    search_frame = LabelFrame(sales_frame, text='Search Sales', font=('times new roman', 12, 'bold'), bg='white')
    search_frame.place(x=20, y=70, width=600, height=70) # Placed on left top

    search_combobox = ttk.Combobox(search_frame, values=('Bill No', 'Customer Name', 'Phone'), font=('times new roman', 13), state='readonly', cursor='hand2', width=15)
    search_combobox.grid(row=0, column=0, padx=10, pady=10)
    search_combobox.set('Bill No')

    search_entry = Entry(search_frame, font=('times new roman', 13), bg='lightyellow', width=16)
    search_entry.grid(row=0, column=1, padx=10)

    search_button = Button(search_frame, text='Search', font=('times new roman', 13), bg='#2196f3', fg='white', cursor='hand2', width=7,
                           command=lambda: search_sales(search_combobox, search_entry, treeview))
    search_button.grid(row=0, column=2, padx=10)

    showall_button = Button(search_frame, text='Show All', font=('times new roman', 13), bg='#607d8b', fg='white', cursor='hand2', width=7,
                            command=lambda: clear_search(search_entry, treeview))
    showall_button.grid(row=0, column=3, padx=10)


    # --- Left Side: Sales List (Treeview) ---
    sales_list_frame = Frame(sales_frame, bd=1, relief=RIDGE)
    sales_list_frame.place(x=20, y=150, width=600, height=430)

    scrolly = Scrollbar(sales_list_frame, orient=VERTICAL)
    scrollx = Scrollbar(sales_list_frame, orient=HORIZONTAL)
    
    # We include bill_txt in columns but we won't display it (we hide it)
    treeview = ttk.Treeview(sales_list_frame, columns=('bill_no', 'date', 'name', 'phone', 'amount', 'bill_txt'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)

    treeview.heading('bill_no', text='Bill No')
    treeview.heading('date', text='Date')
    treeview.heading('name', text='Customer Name')
    treeview.heading('phone', text='Phone')
    treeview.heading('amount', text='Amount')
    # bill_txt heading not needed as we hide column

    treeview.column('bill_no', width=120)
    treeview.column('date', width=80)
    treeview.column('name', width=120)
    treeview.column('phone', width=100)
    treeview.column('amount', width=80)
    treeview.column('bill_txt', width=0, stretch=NO) # HIDE THIS COLUMN

    treeview.pack(fill=BOTH, expand=1)


    # --- Right Side: Bill Receipt View ---
    bill_view_frame = Frame(sales_frame, bd=2, relief=RIDGE, bg='white')
    bill_view_frame.place(x=640, y=70, width=410, height=510)

    bill_title = Label(bill_view_frame, text="Bill Receipt View", font=('times new roman', 12, 'bold'), bg='#4caf50', fg='white')
    bill_title.pack(side=TOP, fill=X)

    scrolly2 = Scrollbar(bill_view_frame, orient=VERTICAL)
    bill_text_area = Text(bill_view_frame, font=("courier new", 10), bg="lightyellow", yscrollcommand=scrolly2.set)
    scrolly2.pack(side=RIGHT, fill=Y)
    scrolly2.config(command=bill_text_area.yview)
    bill_text_area.pack(fill=BOTH, expand=1)

    # --- Initialization ---
    fetch_sales_data(treeview)
    
    # Bind Click Event
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, treeview))

    return sales_frame
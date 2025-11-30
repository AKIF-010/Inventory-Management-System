from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from employee_db import connect_database


def select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, discount_spinbox):
    selected = treeview.selection()
    if not selected:
        return
    item = treeview.item(selected[0])
    content = item.get('values', [])
    if not content:
        return
    # Clear previous values
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    discount_spinbox.delete(0, END)
    # Insert new values (indexes based on: id,category,supplier,name,price,discount,discounted_price,quantity,status)
    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0, content[3])
    price_entry.insert(0, content[4])
    discount_spinbox.insert(0, content[5])
    quantity_entry.insert(0, content[7])  # content[6] is discounted_price, content[7] is quantity
    status_combobox.set(content[8])


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_management_system')
        cursor.execute('SELECT * FROM product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to : {str(e)}')
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass


def fetch_supplier_category(category_combobox, supplier_combobox):
    category_options = []

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_management_system')
        cursor.execute('SELECT name FROM category_data')
        names = cursor.fetchall()
        if names:
            category_combobox.set('Select')
            for name in names:
                category_options.append(name[0])
            category_combobox.config(values=category_options)

        supplier_options = []
        cursor.execute('SELECT name FROM supplier_data')
        names = cursor.fetchall()
        if names:
            supplier_combobox.set('Select')
            for name in names:
                supplier_options.append(name[0])
            supplier_combobox.config(values=supplier_options)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to : {e}')
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass


def clear_fields(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox):
    try:
        treeview.selection_remove(treeview.selection())
    except:
        pass
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    status_combobox.set('Select')
    discount_spinbox.delete(0, END)
    discount_spinbox.insert(0, 0)


def delete_product(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'Row is not selected')
        return

    row_dict = treeview.item(index[0])
    content = row_dict.get('values', [])
    if not content:
        messagebox.showerror('Error', 'No data in selected row')
        return

    record_id = content[0]
    ans = messagebox.askyesno('Confirm ', 'Do you really want to delete')
    if ans:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute('DELETE FROM product_data WHERE id=%s', (record_id,))
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Info', 'Record is Deleted')
            clear_fields(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                connection.close()
            except:
                pass


def update_product(category, supplier, name, price, discount, quantity, status, treeview):

    index = treeview.selection()
    if not index:
        messagebox.showerror("Error", "Row is not selected")
        return
    
    row = treeview.item(index[0])
    content = row["values"]
    product_id = content[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute("USE inventory_management_system")
    cursor.execute("SELECT category, supplier, name, price, discount, discounted_price, quantity, status FROM product_data WHERE id=%s", (product_id,))
    db_data = cursor.fetchone()

    if not db_data:
        messagebox.showerror("Error", "Product not found")
        return

    # Convert DB data into comparable format
    db_category, db_supplier, db_name, db_price, db_discount, db_disc_price, db_quantity, db_status = db_data

    # Calculate discounted price from new data
    new_discounted_price = round(float(price) * (1 - int(discount) / 100), 2)

    # Build new data tuple in same order as DB data
    new_data = (
        category,
        supplier,
        name,
        float(price),
        int(discount),
        new_discounted_price,
        int(quantity),
        status
    )

    # Compare old vs new
    if (
        str(db_category) == str(category) and
        str(db_supplier) == str(supplier) and
        str(db_name) == str(name) and
        float(db_price) == float(price) and
        int(db_discount) == int(discount) and
        float(db_disc_price) == float(new_discounted_price) and
        int(db_quantity) == int(quantity) and
        str(db_status) == str(status)
    ):
        messagebox.showinfo("Info", "No changes detected")
        return

    # Update product
    cursor.execute("""
        UPDATE product_data 
        SET category=%s, supplier=%s, name=%s, price=%s,
            discount=%s, discounted_price=%s, quantity=%s, status=%s
        WHERE id=%s
    """, (category, supplier, name, price, discount, new_discounted_price, quantity, status, product_id))

    connection.commit()
    messagebox.showinfo("Success", "Updated Successfully")
    treeview_data(treeview)


def save_product(category, supplier, name, price, discount, quantity, status, treeview):

    if category == 'Empty':
        messagebox.showerror('Error', 'Please add category')
        return
    elif supplier == 'Empty':
        messagebox.showerror('Error', 'Please add Supplier')
        return
    elif category == 'Select' or supplier == 'Select' or name == '' or price == '' or quantity == '' or status == 'Select':
        messagebox.showerror('Error', 'All fields are required')
        return
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_management_system')

            # Ensure table has discount and discounted_price columns
            cursor.execute('''CREATE TABLE IF NOT EXISTS product_data(
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                category VARCHAR(100),
                                supplier VARCHAR(100),
                                name VARCHAR(100),
                                price DECIMAL(10,2),
                                discount INT,
                                discounted_price DECIMAL(10,2),
                                quantity INT,
                                status VARCHAR(50)
                              )''')

            cursor.execute('SELECT * FROM product_data WHERE category=%s AND supplier=%s AND name=%s', (category, supplier, name))
            existing_product = cursor.fetchone()
            if existing_product:
                messagebox.showerror('Error', 'Product already EXISTS')
                return

            try:
                price_f = float(price)
            except:
                price_f = 0.0
            try:
                discount_i = int(discount)
            except:
                discount_i = 0
            try:
                quantity_i = int(quantity)
            except:
                quantity_i = 0

            discounted_price = round(price_f * (1 - discount_i / 100), 2)

            cursor.execute('INSERT INTO product_data (category, supplier, name, price, discount, discounted_price, quantity, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                           (category, supplier, name, price_f, discount_i, discounted_price, quantity_i, status))
            connection.commit()
            messagebox.showinfo('Success', 'Data is saved')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to : {e}')
        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                connection.close()
            except:
                pass


def search_product(search_combobox, search_entry, treeview):
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
        # column name is taken from combobox value - ensure it's one of allowed columns
        col = search_combobox.get()
        allowed = ('Category', 'Supplier', 'Name', 'Status')
        # map UI label to DB column names (case-sensitive depending on DB)
        col_map = {'Category': 'category', 'Supplier': 'supplier', 'Name': 'name', 'Status': 'status'}
        if col not in allowed:
            messagebox.showerror('Error', 'Invalid search column')
            return
        db_col = col_map[col]
        cursor.execute(f"SELECT * FROM product_data WHERE {db_col}=%s", (search_entry.get(),))
        record = cursor.fetchone()
        treeview.delete(*treeview.get_children())
        if record:
            treeview.insert('', END, values=record)
        else:
            messagebox.showinfo('Info', 'No matching record found')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to : {str(e)}')
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass


def show_all_product(search_entry, treeview):
    treeview_data(treeview)
    search_entry.delete(0, END)


def product_form(window):

    global back_image
    product_frame = Frame(window, width=1070, height=598, bg='white')
    product_frame.place(x=200, y=71)
    heading_label = Label(product_frame, text='Manage product Details', font=('times new roman', 16, 'bold'), bg="#0f4d7d", fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='back.png')
    back_button = Button(product_frame, image=back_image, bd=0, bg='white', cursor='hand2', command=lambda: product_frame.place_forget())
    back_button.place(x=1, y=36)

    left_frame = Frame(product_frame, bg='white', bd=1, relief=RIDGE)
    left_frame.place(x=10, y=80)

    category_label = Label(left_frame, text=' Category :', font=('times new roman', 14, 'bold'), bg='white')
    category_label.grid(row=0, column=0, padx=20, sticky='w')
    category_combobox = ttk.Combobox(left_frame, font=('times new roman', 12), state='readonly', cursor='hand2')
    category_combobox.grid(row=0, column=1)
    category_combobox.set('Empty')

    supplier_label = Label(left_frame, text=' Supplier :', font=('times new roman', 14, 'bold'), bg='white')
    supplier_label.grid(row=1, column=0, padx=20, sticky='w')
    supplier_combobox = ttk.Combobox(left_frame, font=('times new roman', 12), state='readonly', cursor='hand2')
    supplier_combobox.grid(row=1, column=1, pady=30)
    supplier_combobox.set('Empty')

    name_label = Label(left_frame, text=' Name :', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=2, column=0, padx=20, sticky='w')
    name_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
    name_entry.grid(row=2, column=1)

    price_label = Label(left_frame, text=' Price :', font=('times new roman', 14, 'bold'), bg='white')
    price_label.grid(row=3, column=0, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
    price_entry.grid(row=3, column=1, pady=30)

    discount_label = Label(left_frame, text=' Discount(%) :', font=('times new roman', 14, 'bold'), bg='white')
    discount_label.grid(row=4, column=0, sticky='w', padx=20)
    discount_spinbox = Spinbox(left_frame, from_=0, to=100, font=('times new roman', 14, 'bold'), width=17, bg='lightyellow')
    discount_spinbox.grid(row=4, column=1)

    quantity_label = Label(left_frame, text=' Quantity :', font=('times new roman', 14, 'bold'), bg='white')
    quantity_label.grid(row=5, column=0, padx=20, sticky='w', pady=(30, 0))
    quantity_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
    quantity_entry.grid(row=5, column=1, pady=(30, 0))

    status_label = Label(left_frame, text=' Status :', font=('times new roman', 14, 'bold'), bg='white')
    status_label.grid(row=6, column=0, padx=20, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=('times new roman', 12), state='readonly', cursor='hand2')
    status_combobox.grid(row=6, column=1, pady=30)
    status_combobox.set('Select')

    Button_frame = Frame(left_frame, bg='white')
    Button_frame.grid(row=7, columnspan=2, pady=30)
    save_button = Button(Button_frame, text='Save', font=('times new roman', 14, 'bold'), bg='#2196f3', fg='white', cursor='hand2', width=8,
                         command=lambda: save_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), discount_spinbox.get(), quantity_entry.get(), status_combobox.get(), treeview))
    save_button.grid(row=0, column=0, padx=20)
    update_button = Button(Button_frame, text='Update', font=('times new roman', 14, 'bold'), bg='#4caf50', fg='white', cursor='hand2', width=8,
                           command=lambda: update_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), discount_spinbox.get(), quantity_entry.get(), status_combobox.get(), treeview))
    update_button.grid(row=0, column=1)
    delete_button = Button(Button_frame, text='Delete', font=('times new roman', 14, 'bold'), bg='#f44336', fg='white', cursor='hand2', width=8,
                           command=lambda: delete_product(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox))
    delete_button.grid(row=0, column=2, padx=20)
    clear_button = Button(Button_frame, text='Clear', font=('times new roman', 14, 'bold'), bg='#607d8b', fg='white', cursor='hand2', width=8,
                          command=lambda: clear_fields(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox))
    clear_button.grid(row=0, column=3, padx=(0, 20))

    search_frame = LabelFrame(product_frame, text='Search Product', font=('times new roman', 12, 'bold'), bg='white')
    search_frame.place(x=520, y=70, width=540)

    search_combobox = ttk.Combobox(search_frame, values=('Category', 'Supplier', 'Name', 'Status'), font=('times new roman', 13), state='readonly', cursor='hand2', width=15)
    search_combobox.grid(row=0, column=0, padx=10, pady=10)
    search_combobox.set('Select')

    search_entry = Entry(search_frame, font=('times new roman', 13), bg='lightyellow', width=16)
    search_entry.grid(row=0, column=1, padx=10)

    search_button = Button(search_frame, text='Search', font=('times new roman', 13), bg='#2196f3', fg='white', cursor='hand2', width=7,
                           command=lambda: search_product(search_combobox, search_entry, treeview))
    search_button.grid(row=0, column=2, padx=10)

    showall_button = Button(search_frame, text='Show All', font=('times new roman', 13), bg='#607d8b', fg='white', cursor='hand2', width=7,
                            command=lambda: show_all_product(search_entry, treeview))
    showall_button.grid(row=0, column=3, padx=10)

    treeview_frame = Frame(product_frame)
    treeview_frame.place(x=520, y=150, height=410, width=540)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=('ID', 'Category', 'Supplier', 'Name', 'Price', 'Discount', 'Discounted_Price', 'Quantity', 'Status'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, height=20)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)

    treeview.heading('ID', text='ID')
    treeview.heading('Category', text='Category')
    treeview.heading('Supplier', text='Supplier')
    treeview.heading('Name', text='Name')
    treeview.heading('Price', text='Price')
    treeview.heading('Discount', text='Discount')
    treeview.heading('Discounted_Price', text='Discounted Price')
    treeview.heading('Quantity', text='Quantity')
    treeview.heading('Status', text='Status')
    treeview.column('ID', width=70)
    treeview.column('Category', width=150)
    treeview.column('Supplier', width=150)
    treeview.column('Name', width=100)
    treeview.column('Price', width=70)
    treeview.column('Quantity', width=70)
    treeview.column('Status', width=70)
    treeview.pack()
    treeview_data(treeview)
    fetch_supplier_category(category_combobox, supplier_combobox)
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, discount_spinbox))

    return product_frame

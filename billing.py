from tkinter import *
from time import strftime
from tkinter import ttk
from employee_db import connect_database
from tkinter import messagebox
window = Tk()
window.title('Inventory Management System')
window.geometry('1270x668+0+0')
window.resizable(0,0)
window.config(bg='white')

HEADER_HEIGHT = 70

# ===================== TOP HEADER =====================
top_frame = Frame(window, bg='#1D293D', height=HEADER_HEIGHT+7, width=1270)
top_frame.place(x=0, y=0)
top_frame.grid_propagate(False)

# Grid configuration
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=0)

# ===================== WELCOME LABEL =====================
welcome_label = Label(
    top_frame,
    text='Welcome To IMS PRO',
    font=('Tahoma', 16, 'bold'),
    bg='#1D293D',
    fg='white',
    anchor=W
)
welcome_label.grid(row=0, column=0, sticky=W, padx=15, pady=8)

# ===================== LOGOUT BUTTON WITH ICON =====================
logout_img = PhotoImage(file="logout_icon.png")  # 32px black icon

logout_btn = Button(
    top_frame,
    text=" Logout",
    image=logout_img,
    compound=LEFT,
    font=('Tahoma', 11, 'bold'),
    bg='#E5E7EB',          # light gray
    fg='#1F2937',          # dark blue-gray
    activebackground='#D1D5DB',
    activeforeground='#111827',
    bd=0,
    padx=14,
    pady=6,
    cursor='hand2'
)
logout_btn.grid(row=0, column=1, sticky=E, padx=20, pady=6)

# ===================== DATE & TIME BAR =====================
date_label = Label(
    top_frame,
    font=('Verdana', 13),
    bg='#374151',
    fg='white',
    anchor=W,
    width=1270
)
date_label.grid(row=1, column=0, columnspan=2, sticky=W)

def update_time():
    current_time = strftime('%I:%M:%S %p')
    current_date = strftime('%d-%m-%Y')
    date_label.config(text=f"  Date: {current_date}      Time: {current_time}")
    date_label.after(1000, update_time)

update_time()

#======================= PRODUCT LIST =========================#

def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_management_system')
        cursor.execute('SELECT id,name,price,discount,quantity,status FROM product_data')
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

Product_frame = Frame(window, bg='white',bd=2, relief=RIDGE)
Product_frame.place(x=5, y=80, width=400, height=550)
Product_title = Label(Product_frame, text='All Products', font=('times new roman', 15, 'bold'), bg='#242623', fg='white')
Product_title.pack(side=TOP, fill=X)

search_frame = Frame(Product_frame, bg='white', bd=2, relief=RIDGE)
search_frame.pack(side=TOP, fill=X)

search_by = Label(
    search_frame,
    text='PID',
    font=('times new roman', 12, 'bold'),
    bg='white'
)
search_by.grid(row=0, column=0, padx=6, pady=4, sticky=W)

search_txt = Entry(
    search_frame,
    font=('times new roman', 12),
    bd=2,
    relief=RIDGE,
    width=17      # increased width
)
search_txt.grid(row=0, column=1, padx=6, pady=4, sticky=W)

search_btn = Button(
    search_frame,
    text='Search',
    font=('times new roman', 12),
    bg='#4caf50',
    fg='white',
    cursor='hand2',
    width=7           # increased button width
)
search_btn.grid(row=0, column=2, padx=8, pady=4)

show_all_btn = Button(
    search_frame,
    text='Show All',
    font=('times new roman', 12),
    bg='#2196f3',
    fg='white',
    cursor='hand2',
    width=7           # increased button width
)
show_all_btn.grid(row=0, column=3, padx=6, pady=4)

treeview_frame = Frame(Product_frame, bd=3, relief=RIDGE)
treeview_frame.pack(fill=BOTH, expand=1)
Scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
Scrolly.pack(side=RIGHT, fill=Y)
Scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
Scrollx.pack(side=BOTTOM, fill=X)
treeview=ttk.Treeview(treeview_frame, columns=('pid','name','price','discount','qty','status'), show='headings')
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

#======================= CUSTOMER =========================#

customer_frame = Frame(window, bg='white',bd=2, relief=RIDGE)
customer_frame.place(x=410, y=80, width=500, height=70)
customer_title = Label(customer_frame, text='Customer Details', font=('times new roman', 15, 'bold'), bg='#242623', fg='white')
customer_title.pack(side=TOP, fill=X)
customer_name_label = Label(
    customer_frame,
    text='Name',
    font=('times new roman', 12, 'bold'),bg='white')
customer_name_label.place(x=5, y=35)
customer_name_entry = Entry(customer_frame, font=('times new roman', 12), bd=2, relief=RIDGE)
customer_name_entry.place(x=70, y=35, width=140)
customer_phone_label = Label(
    customer_frame,
    text='Phone No.',
    font=('times new roman', 12, 'bold'),bg='white')
customer_phone_label.place(x=240, y=35)
customer_phone_entry = Entry(customer_frame, font=('times new roman', 12), bd=2, relief=RIDGE)
customer_phone_entry.place(x=340, y=35, width=140)

#======================= calculator and cart =========================#

cal_cart_frame = Frame(window, bg='white',bd=2, relief=RIDGE)
cal_cart_frame.place(x=410, y=160, width=500, height=370)
# calculator frame
calculator_frame = Frame(cal_cart_frame, bg='white',bd=1, relief=RIDGE)
calculator_frame.place(x=5, y=5, width=240, height=360)
# cart frame
cart_frame = Frame(cal_cart_frame, bg='white',bd=1, relief=RIDGE)
cart_frame.place(x=250, y=5, width=245, height=360)
cart_title = Label(cart_frame, text='Cart Details', font=('times new roman', 12, 'bold'), bg='#242623', fg='white')
cart_title.pack(side=TOP, fill=X)
cart_total_products_label = Label(
    cart_frame,text='Total Products: 0', font=('times new roman', 12, 'bold'), bg='white')
cart_total_products_label.pack(side=TOP, anchor=S, padx=5)
# treeview for cart
treeview_frame_cart = Frame(cart_frame, bd=3, relief=RIDGE)
treeview_frame_cart.pack(fill=BOTH, expand=1)
Scrolly_cart = Scrollbar(treeview_frame_cart, orient=VERTICAL)
Scrolly_cart.pack(side=RIGHT, fill=Y)
Scrollx_cart = Scrollbar(treeview_frame_cart, orient=HORIZONTAL)
Scrollx_cart.pack(side=BOTTOM, fill=X)
treeview_cart=ttk.Treeview(treeview_frame_cart, columns=('pid','name','price','qty'), show='headings')
treeview_cart.configure(yscrollcommand=Scrolly_cart.set, xscrollcommand=Scrollx_cart.set)
Scrolly_cart.config(command=treeview_cart.yview)
Scrollx_cart.config(command=treeview_cart.xview)
treeview_cart.heading('pid', text='PID')
treeview_cart.heading('name', text='Name')
treeview_cart.heading('price', text='Price')
treeview_cart.heading('qty', text='Quantity')
treeview_cart.column('pid', width=100)
treeview_cart.column('name', width=100)
treeview_cart.column('price', width=70)
treeview_cart.column('qty', width=70)
treeview_cart.pack(fill=BOTH, expand=1)

#======================= Add cart frame =========================#

add_cart_frame = Frame(window, bg='white',bd=2, relief=RIDGE)
add_cart_frame.place(x=410, y=540, width=500, height=90)

cart_product_frame = Frame(add_cart_frame, bg='white')
cart_product_frame.place(x=5, y=2, width=490, height=60)
cart_product_name_label = Label(
    cart_product_frame,text='Product Name', font=('times new roman', 12, 'bold'), bg='white')
cart_product_name_label.grid(row=0, column=0, padx=5)
cart_product_qty_label = Label(cart_product_frame,text='Quantity', font=('times new roman', 12, 'bold'), bg='white')
cart_product_qty_label.grid(row=0, column=1, padx=5)
cart_product_price_label = Label(cart_product_frame,text='Price', font=('times new roman', 12, 'bold'), bg='white')
cart_product_price_label.grid(row=0, column=2, padx=5)
cart_product_frame_name = Entry(cart_product_frame, font=('times new roman', 12), bd=2, relief=RIDGE,width=18)
cart_product_frame_name.grid(row=1, column=0, padx=5)
cart_product_frame_qty = Entry(cart_product_frame, font=('times new roman', 12), bd=2, relief=RIDGE,width=18)
cart_product_frame_qty.grid(row=1, column=1, padx=5)
cart_product_frame_price = Entry(cart_product_frame, font=('times new roman', 12), bd=2, relief=RIDGE,width=18)
cart_product_frame_price.grid(row=1, column=2, padx=5)

add_frame=Frame(add_cart_frame, bg='white')
add_frame.place(x=5, y=60, width=490, height=20)

stock_label = Label(
    add_frame,text='Available Stock: 0', font=('times new roman', 12, 'bold'), bg='white')
stock_label.pack(side=LEFT, padx=(5,0))
clear_button = Button(
    add_frame,text='Clear', font=('times new roman', 12, 'bold'), bg='#f44336', fg='white', cursor='hand2', width=10)
clear_button.pack(side=RIGHT, padx=(5,15))
add_or_update_cart_button = Button(
    add_frame,text='Add | Update Cart', font=('times new roman', 12, 'bold'), bg='#4caf50', fg='white', cursor='hand2', width=15)
add_or_update_cart_button.pack(side=RIGHT, padx=5)

window.mainloop()

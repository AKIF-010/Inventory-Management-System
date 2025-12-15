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
calc_entry.grid(row=0, column=0, columnspan=4, padx=5, pady=8, ipady=8, sticky="nsew")

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

# Button layout
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
        width=5,
        height=2,
        bg='#F3F4F6' if text not in ('=', 'C') else '#EF4444' if text == 'C' else '#22C55E',
        fg='black' if text not in ('C', '=') else 'white',
        bd=1,
        cursor='hand2',
        command=lambda t=text: press(t)
    )
    btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

# Function to handle key presses
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

# Bind Enter key to '='
calculator_frame.bind_all('<Return>', lambda event: press('='))


# Make grid responsive
for i in range(6):
    calculator_frame.rowconfigure(i, weight=1)

for i in range(4):
    calculator_frame.columnconfigure(i, weight=1)



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


#======================= BILLING AREA =====================#

billframe = Frame(window, bg='white',bd=2, relief=RIDGE)
billframe.place(x=920, y=80, width=340, height=450)

billframe_title = Label(billframe, text='Billing Area', font=('times new roman', 15, 'bold'), bg='#242623', fg='white')
billframe_title.pack(side=TOP, fill=X)

Scrolly_bill = Scrollbar(billframe, orient=VERTICAL)
Scrolly_bill.pack(side=RIGHT, fill=Y)
bill_text = Text(billframe, yscrollcommand=Scrolly_bill.set, bg='white', fg='black', font=('times new roman', 12))
bill_text.pack(fill=BOTH, expand=1)
Scrolly_bill.config(command=bill_text.yview)

#======================= BILLING BUTTONS =====================#
bill_button_frame = Frame(window, bg='white',bd=2, relief=RIDGE)
bill_button_frame.place(x=920, y=540, width=340, height=90)

bill_amount_label = Label(
    bill_button_frame,
    text='Bill\n0',
    font=('Arial', 10, 'bold'),
    bg='#4A90E2',
    fg='white',
    width=9,
    height=2,
    justify=CENTER
)
bill_amount_label.grid(row=0, column=0, padx=2, pady=2)

discount_label = Label(
    bill_button_frame,
    text='Dis\n2%',
    font=('Arial', 10, 'bold'),
    bg='#7ED321',
    fg='white',
    width=9,
    height=2,
    justify=CENTER
)
discount_label.grid(row=0, column=1, padx=2, pady=2)

net_pay_label = Label(
    bill_button_frame,
    text='Net\n0',
    font=('Arial', 10, 'bold'),
    bg='#D0021B',
    fg='white',
    width=9,
    height=2,
    justify=CENTER
)
net_pay_label.grid(row=0, column=2, padx=2, pady=2)

# -------- Row 1 : Buttons --------
print_button = Button(
    bill_button_frame,
    text='Print',
    font=('Arial', 10, 'bold'),
    bg='#50E3C2',
    fg='white',
    width=9,
    height=1,
    cursor='hand2'
)
print_button.grid(row=1, column=0, padx=2, pady=2)

clear_all_button = Button(
    bill_button_frame,
    text='Clear',
    font=('Arial', 10, 'bold'),
    bg='gray',
    fg='white',
    width=9,
    height=1,
    cursor='hand2'
)
clear_all_button.grid(row=1, column=1, padx=2, pady=2)

generate_save_button = Button(
    bill_button_frame,
    text='Save',
    font=('Arial', 10, 'bold'),
    bg='#9013FE',
    fg='white',
    width=9,
    height=1,
    cursor='hand2'
)
generate_save_button.grid(row=1, column=2, padx=2, pady=2)

# Grid resize safety
for i in range(3):
    bill_button_frame.columnconfigure(i, weight=1) 


window.mainloop()

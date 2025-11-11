from tkinter import *

from employee_db import employee_form 
from time import strftime
import datetime

window=Tk()

window.title('Inventory Management System')
window.geometry('1270x668+0+0')
window.resizable(0,0)
window.config(bg='white')

HEADER_HEIGHT = 70
MENU_WIDTH = 200
HEADER_WIDTH = 1270 - MENU_WIDTH

# --- Position Constants ---
HEADER_BOTTOM_Y = HEADER_HEIGHT + 1 
DASHBOARD_TITLE_Y = HEADER_BOTTOM_Y + 15 # Position for the new title (15px gap below header)
CARD_START_Y = DASHBOARD_TITLE_Y + 70 # Position for the first row of metric cards (70px gap below title)

# --- Top Header Frame ---
top_frame = Frame(window, bg='white', height=HEADER_HEIGHT, width=HEADER_WIDTH)
top_frame.place(x=MENU_WIDTH, y=0)
top_frame.grid_propagate(False)

top_border = Frame(window, bg="#E5E7EB", height=1, width=HEADER_WIDTH)
top_border.place(x=MENU_WIDTH, y=HEADER_HEIGHT)

top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=0)
top_frame.rowconfigure(0, weight=1)

# Left section (Welcome and Date/Time)
left_frame = Frame(top_frame, bg='white')
left_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

welcome_label = Label(left_frame, text='Welcome, Admin', font=('Tahoma', 16), bg='white', fg='black', anchor=W)
welcome_label.grid(row=0, column=0, sticky=W)

date_label = Label(left_frame, font=('Verdana', 13), bg='white', fg='black', anchor=W)
date_label.grid(row=1, column=0, sticky=W)

def update_time():
    current_time = strftime('%I:%M:%S %p')
    current_date = strftime('%d-%m-%Y')
    date_label.config(text=f"Date: {current_date}      Time: {current_time}")
    date_label.after(1000, update_time)

update_time()

# Right section (Logout Button - Vertically Centered)
right_frame = Frame(top_frame, bg='white')
right_frame.grid(row=0, column=1, sticky="nse", padx=20) 
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=1)

logout_button = Button(right_frame, text='Logout', font=('times new roman', 12, 'bold'), 
                       bg='gray', fg='white', bd=1, relief=RIDGE, cursor='hand2')
logout_button.grid(row=0, column=0, sticky="") 


# --- DASHBOARD OVERVIEW TITLE SECTION (NEW) ---
dashboard_title = Label(window, text="Dashboard Overview", font=("Arial", 20, "bold"), fg='#333333', bg='white', anchor=W)
dashboard_title.place(x=MENU_WIDTH + 20, y=DASHBOARD_TITLE_Y+10)

# ---------------------------------------------


# --- Left Menu Frame ---
leftframe = Frame(window, bg="#333333") 
leftframe.place(x=0,y=0,relheight=1,width=MENU_WIDTH)

# Place your IMS Pro header/logo here
Label(leftframe, text="IMS Pro", font=('times new roman', 20, 'bold'), fg='white', bg="#00415F").place(x=0, y=0, height=HEADER_HEIGHT, width=MENU_WIDTH)

# Placeholder menu button (for structure)
Label(leftframe, text="Menu Item 1", font=('times new roman', 16), fg='white', bg="#333333").place(x=0, y=100)


#left frame

leftframe = Frame(window,bg="#1D293D")
leftframe.place(x=0,y=0,relheight=1,width=200)

manu_image=PhotoImage(file='inventory.png')
manu=Label(leftframe,image=manu_image,compound=LEFT,text='  IMS PRO',font=('times new roman',20), bg="#1D293D",fg='white',anchor=W,padx=10,height=70,width=200)
manu.pack(fill=X)

border = Frame(leftframe, bg="#155DFC", height=1, width=200)
border.place(x=0,y=70)

active_bg_color = '#155DFC' # Hover color

employee_image=PhotoImage(file='employee1.png')
employee_button=Button(leftframe,image=employee_image,compound=LEFT,text='  Employee',font=('times new roman',18),anchor=W,padx=10,bd=0,bg="#1D293D",fg='white', cursor='hand2', activebackground=active_bg_color)
employee_button.pack(fill=X,pady=10)

supply_image=PhotoImage(file='supplier.png')
supply_button=Button(leftframe,image=supply_image,compound=LEFT,text='  Supplier',font=('times new roman',18),anchor=W,padx=10,bd=0,bg="#1D293D",fg='white', cursor='hand2', activebackground=active_bg_color)
supply_button.pack(fill=X,pady=10)

category_image=PhotoImage(file='category.png')
category_button=Button(leftframe,image=category_image,compound=LEFT,text='  Categories',font=('times new roman',18),anchor=W,padx=10,bd=0,bg="#1D293D",fg='white', cursor='hand2', activebackground=active_bg_color)
category_button.pack(fill=X,pady=10)

products_image=PhotoImage(file='product.png')
products_button=Button(leftframe,image=products_image,compound=LEFT,text='  Products',font=('times new roman',18),anchor=W,padx=10,bd=0,bg="#1D293D",fg='white', cursor='hand2', activebackground=active_bg_color)
products_button.pack(fill=X,pady=10)

sales_image=PhotoImage(file='category.png')
sales_button=Button(leftframe,image=sales_image,compound=LEFT,text='  Sales',font=('times new roman',18),anchor=W,padx=10,bd=0,bg="#1D293D",fg='white', cursor='hand2', activebackground=active_bg_color)
sales_button.pack(fill=X,pady=10)

exit_image=PhotoImage(file='exit.png')
exit_button=Button(leftframe,image=exit_image,compound=LEFT,text='  Exit',font=('times new roman',18),anchor=W,padx=10,bd=0,bg="#1D293D",fg='white', cursor='hand2', activebackground=active_bg_color)
exit_button.pack(fill=X,pady=10)

#frames (Adjusted Y coordinates to start at CARD_START_Y)

# --- Employee Frame ---
emp_frame = Frame(window, bg="#3A78F2", bd=0)
emp_frame.place(x=400, y=CARD_START_Y, height=150, width=250)
emp_frame.grid_propagate(False)

total_emp_text = Label(emp_frame, text="Total Employees", 
                       font=('times new roman', 12), fg='white', bg="#3A78F2")
total_emp_text.place(x=15, y=15)

total_emp_count = Label(emp_frame, text="0", 
                         font=('times new roman', 40, 'bold'), fg='white', bg="#3A78F2")
total_emp_count.place(x=15, y=50)

total_emp_image = PhotoImage(file='employee1.png')
total_emp_label = Label(emp_frame, image=total_emp_image, bg="#3A78F2")
total_emp_label.image = total_emp_image
total_emp_label.place(relx=0.9, rely=0.55, anchor=E)

# --- Supplier Frame ---
supplier_frame = Frame(window, bg="#7030A0", bd=0)
supplier_frame.place(x=800, y=CARD_START_Y, height=150, width=250)
supplier_frame.grid_propagate(False)

total_supplier_text = Label(supplier_frame, text="Total Suppliers", 
                       font=('times new roman', 12), fg='white', bg="#7030A0")
total_supplier_text.place(x=15, y=15)

total_supplier_count = Label(supplier_frame, text="0", 
                         font=('times new roman', 40, 'bold'), fg='white', bg="#7030A0")
total_supplier_count.place(x=15, y=50)

total_supplier_image = PhotoImage(file='supplier.png')
total_supplier_label = Label(supplier_frame, image=total_supplier_image, bg="#7030A0")
total_supplier_label.image = total_supplier_image
total_supplier_label.place(relx=0.9, rely=0.55, anchor=E)

# --- Category Frame ---
# Adjusted Y for second row, factoring in CARD_START_Y and a gap (e.g., 175px total offset)
category_frame = Frame(window, bg="#008000", bd=0)
category_frame.place(x=400, y=CARD_START_Y + 175, height=150, width=250) 
category_frame.grid_propagate(False)

total_category_text = Label(category_frame, text="Total Categories", 
                       font=('times new roman', 12), fg='white', bg="#008000")
total_category_text.place(x=15, y=15)

total_category_count = Label(category_frame, text="0", 
                         font=('times new roman', 40, 'bold'), fg='white', bg="#008000")
total_category_count.place(x=15, y=50)

total_category_image = PhotoImage(file='category.png')
total_category_label = Label(category_frame, image=total_category_image, bg="#008000")
total_category_label.image = total_category_image
total_category_label.place(relx=0.9, rely=0.55, anchor=E)

# --- Product Frame ---
product_frame = Frame(window, bg="#FF4500", bd=0)
product_frame.place(x=800, y=CARD_START_Y + 175, height=150, width=250)
product_frame.grid_propagate(False)

total_product_text = Label(product_frame, text="Total Products", 
                       font=('times new roman', 12), fg='white', bg="#FF4500")
total_product_text.place(x=15, y=15)

total_product_count = Label(product_frame, text="0", 
                         font=('times new roman', 40, 'bold'), fg='white', bg="#FF4500")
total_product_count.place(x=15, y=50)

total_product_image = PhotoImage(file='product.png')
total_product_label = Label(product_frame, image=total_product_image, bg="#FF4500")
total_product_label.image = total_product_image
total_product_label.place(relx=0.9, rely=0.55, anchor=E)

# --- Sales Frame ---
sales_frame = Frame(window, bg="#00B09E", bd=0)
sales_frame.place(x=600, y=CARD_START_Y + 350, height=150, width=250)
sales_frame.grid_propagate(False)

total_sales_text = Label(sales_frame, text="Total Sales", 
                       font=('times new roman', 12), fg='white', bg="#00B09E")
total_sales_text.place(x=15, y=15)

total_sales_count = Label(sales_frame, text="0", 
                         font=('times new roman', 40, 'bold'), fg='white', bg="#00B09E")
total_sales_count.place(x=15, y=50)

total_sales_image = PhotoImage(file='sale.png')
total_sales_label = Label(sales_frame, image=total_sales_image, bg="#00B09E")
total_sales_label.image = total_sales_image
total_sales_label.place(relx=0.9, rely=0.55, anchor=E)

window.mainloop()
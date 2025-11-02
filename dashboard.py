from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

def employee_form():
    global back_image
    employee_frame=Frame(window,width=1070,height=568,bg='white')
    employee_frame.place(x=200,y=100)
    heading_label=Label(employee_frame,text='Manage Employee Details',font=('times new roman',16,'bold'),bg="#0f4d7d",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    
    back_image=PhotoImage(file='back.png')
    back_button=Button(employee_frame,image=back_image,bd=0,bg='white',cursor='hand2',command=lambda: employee_frame.place_forget())
    back_button.place(x=1,y=30)
    
    top_frame=Frame(employee_frame,bg='white')
    top_frame.place(x=0,y=60,relwidth=1,height=235)
    
    search_frame=Frame(top_frame,bg='white')
    search_frame.pack()
    search_combobox=ttk.Combobox(search_frame,values=('ID','Name','Email'),font=('times new roman',12),state='readonly',cursor='hand2')
    search_combobox.set('Search By')
    search_combobox.grid(row=0,column=0,padx=20)
    search_entry=Entry(search_frame,font=('times new roman',12),bg="#EBEAC1")
    search_entry.grid(row=0,column=1)
    search_button=Button(search_frame,text='SEARCH',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d7d')
    search_button.grid(row=0,column=2,padx=20)
    show_button=Button(search_frame,text='Show All',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d7d')
    show_button.grid(row=0,column=3)
    
    
    horizontal_scroll=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scroll=Scrollbar(top_frame,orient=VERTICAL)
    employee_treeview=ttk.Treeview(top_frame,columns=('Emp ID','Name','Email','gender','dob','contact','employement_type',
                                                       'education','work_shift','address','doj','salary','user_type'),show='headings',
                                                      xscrollcommand=horizontal_scroll.set,yscrollcommand=vertical_scroll.set)
    horizontal_scroll.pack(side=BOTTOM,fill=X)
    vertical_scroll.pack(side=RIGHT,fill=Y,pady=(20,0))
    horizontal_scroll.config(command=employee_treeview.xview)
    vertical_scroll.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(20,0))
  
    employee_treeview.heading('Emp ID',text='Emp ID')
    employee_treeview.heading('Name',text='Name')  
    employee_treeview.heading('Email',text='Email')
    employee_treeview.heading('gender',text='Gender')
    employee_treeview.heading('dob',text='D.O.B')
    employee_treeview.heading('contact',text='Contact')
    employee_treeview.heading('employement_type',text='Employement Type')
    employee_treeview.heading('education',text='Education')
    employee_treeview.heading('work_shift',text='Work Shift')
    employee_treeview.heading('address',text='Address')
    employee_treeview.heading('doj',text='D.O.J')
    employee_treeview.heading('salary',text='Salary')
    employee_treeview.heading('user_type',text='User Type')
  
    employee_treeview.column('Emp ID',width=60)
    employee_treeview.column('Name',width=140)
    employee_treeview.column('Email',width=180)
    employee_treeview.column('gender',width=80)
    employee_treeview.column('dob',width=100)
    employee_treeview.column('contact',width=100)
    employee_treeview.column('employement_type',width=120)
    employee_treeview.column('education',width=120)
    employee_treeview.column('work_shift',width=100)
    employee_treeview.column('address',width=200)
    employee_treeview.column('doj',width=100)
    employee_treeview.column('salary',width=140)
    employee_treeview.column('user_type',width=140)
  
  
    emp_details_frame=Frame(employee_frame)
    emp_details_frame.place(x=0,y=300)
    
    emp_id_label=Label(emp_details_frame,text='EmpID',font=('times new roman',12,'bold'))
    emp_id_label.grid(row=0,column=0,padx=20,pady=10)
    empid_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    empid_entry.grid(row=0,column=1,padx=20,pady=10)
    
    name_label=Label(emp_details_frame,text='Name',font=('times new roman',12,'bold'))
    name_label.grid(row=0,column=2,padx=20,pady=10)
    name_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    name_entry.grid(row=0,column=3,padx=20,pady=10)
    
    email_label=Label(emp_details_frame,text='Email',font=('times new roman',12,'bold'))
    email_label.grid(row=0,column=4,padx=20,pady=10)
    email_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    email_entry.grid(row=0,column=5,padx=20,pady=10)
    
    gender_label=Label(emp_details_frame,text='Gender',font=('times new roman',12,'bold'))
    gender_label.grid(row=1,column=0,padx=20,pady=10)
    gender_combobox=ttk.Combobox(emp_details_frame,values=('Male','Female','Other'),font=('times new roman',12),state='readonly',cursor='hand2',width=18 ) 
    gender_combobox.grid(row=1,column=1,padx=20,pady=10)
    gender_combobox.set('Select Gender')
    
    dob_label=Label(emp_details_frame,text='Date of Birth',font=('times new roman',12,'bold'))
    dob_label.grid(row=1,column=2,padx=20,pady=10)
    dob_date_entry=DateEntry(emp_details_frame,width=18,font=('times new roman',12),date_pattern='dd-mm-yyyy',state='readonly')
    dob_date_entry.grid(row=1,column=3,padx=20,pady=10)
    
    contact_label=Label(emp_details_frame,text='Contact',font=('times new roman',12,'bold'))
    contact_label.grid(row=1,column=4)
    contact_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    contact_entry.grid(row=1,column=5,padx=20,pady=10)
    
    etyp_label=Label(emp_details_frame,text='Employement Type',font=('times new roman',12,'bold'))
    etyp_label.grid(row=2,column=0)
    etyp_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    etyp_entry.grid(row=2,column=1,padx=20,pady=10)
    
    edu_label=Label(emp_details_frame,text='Education',font=('times new roman',12,'bold'))
    edu_label.grid(row=2,column=2)
    edu_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    edu_entry.grid(row=2,column=3,padx=20,pady=10)
    
    wshift_label=Label(emp_details_frame,text='Work Shift',font=('times new roman',12,'bold'))
    wshift_label.grid(row=2,column=4)
    wshift_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    wshift_entry.grid(row=2,column=5,padx=20,pady=10)
    
    address_label=Label(emp_details_frame,text='address',font=('times new roman',12,'bold'))
    address_label.grid(row=3,column=0)
    address_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    address_entry.grid(row=3,column=1,padx=20,pady=10)
    
    doj_label=Label(emp_details_frame,text='Date of Join',font=('times new roman',12,'bold'))
    doj_label.grid(row=3,column=2)
    doj_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    doj_entry.grid(row=3,column=3,padx=20,pady=10)
    
    salary_label=Label(emp_details_frame,text='Salary',font=('times new roman',12,'bold'))
    salary_label.grid(row=3,column=4)
    salary_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    salary_entry.grid(row=3,column=5,padx=20,pady=10)
    
    utype_label=Label(emp_details_frame,text='User Type',font=('times new roman',12,'bold'))
    utype_label.grid(row=4,column=2)
    utype_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    utype_entry.grid(row=4,column=3,padx=20,pady=10)
    
    pw_label=Label(emp_details_frame,text='Password',font=('times new roman',12,'bold'))
    pw_label.grid(row=4,column=4)
    pw_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    pw_entry.grid(row=4,column=5,padx=20,pady=10)
    
    
    
    
    
    
window=Tk()

window.title('Dashboard')
window.geometry('1270x668+0+0')
window.resizable(0,0)
window.config(bg='white')

titleimage=PhotoImage(file='dashboard.png')
titleLabel=Label(window,image=titleimage,compound=LEFT,text='             Inventory Management System',font=('times new roman',40,'bold'),bg='#000080',fg='white',anchor='w',padx=15)
titleLabel.place(x=0,y=0,relwidth=1,height=70)

logoutButton=Button(window,text='LogOut',font=('times new roman',20,'bold'))
logoutButton.place(x=1100,y=10)

subtitleLabel = Label(window,
                      text='Welcome Admin\t\t Date : 01-01-2024\t\t Time : 12:00 PM', 
                      font=('times new roman', 15), 
                      bg="#325872", 
                      fg='white'
                    )
subtitleLabel.place(x=0, y=70, relwidth=1, height=30)

#left frame

leftframe = Frame(window,bd=2,relief=RIDGE)
leftframe.place(x=0,y=102,height=555,width=200)

lf_image=PhotoImage(file='leftframe_image.png')
leftframe_image=Label(leftframe,image=lf_image)
leftframe_image.pack()

manu=Label(leftframe,text='Manu',font=('times new roman',20,'bold'), bg="#00415F",fg='white')
manu.pack(fill=X)

employee_image=PhotoImage(file='employee.png')
employee_button=Button(leftframe,image=employee_image,compound=LEFT,text='  Employee',font=('times new roman',20,'bold'),anchor=W,padx=10,command=employee_form)
employee_button.pack(fill=X)

supply_image=PhotoImage(file='supplier.png')
supply_button=Button(leftframe,image=supply_image,compound=LEFT,text='  Supplier',font=('times new roman',20,'bold'),anchor=W,padx=10)
supply_button.pack(fill=X)

category_image=PhotoImage(file='categorization.png')
category_button=Button(leftframe,image=category_image,compound=LEFT,text='  Categories',font=('times new roman',20,'bold'),anchor=W,padx=10)
category_button.pack(fill=X)

products_image=PhotoImage(file='product.png')
products_button=Button(leftframe,image=products_image,compound=LEFT,text='  Products',font=('times new roman',20,'bold'),anchor=W,padx=10)
products_button.pack(fill=X)

sales_image=PhotoImage(file='sales.png')
sales_button=Button(leftframe,image=sales_image,compound=LEFT,text='  Sales',font=('times new roman',20,'bold'),anchor=W,padx=10)
sales_button.pack(fill=X)

exit_image=PhotoImage(file='exit.png')
exit_button=Button(leftframe,image=exit_image,compound=LEFT,text='  Exit',font=('times new roman',20,'bold'),anchor=W,padx=10)
exit_button.pack(fill=X)

#frames

#employee frame
emp_frame=Frame(window,bg="#4B7088",bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,height=170,width=280)

total_emp_image=PhotoImage(file='staff.png')
total_emp_label=Label(emp_frame,image=total_emp_image,bg="#4B7088")
total_emp_label.pack(pady=10)

total_emp_text=Label(emp_frame,text="Total Employee",font=('times new roman',15,'bold'),fg='white',bg="#4B7088")
total_emp_text.pack()

total_emp_count=Label(emp_frame,text="0",font=('times new roman',30,'bold'),fg='white',bg="#4B7088")
total_emp_count.pack()

#supplier frame
supplier_frame=Frame(window,bg="#4B7088",bd=3,relief=RIDGE)
supplier_frame.place(x=800,y=125,height=170,width=280)

total_supplier_image=PhotoImage(file='supplier_1.png')
total_supplier_label=Label(supplier_frame,image=total_supplier_image,bg="#4B7088")
total_supplier_label.pack(pady=10)

total_supplier_text=Label(supplier_frame,text="Total Supplier",font=('times new roman',15,'bold'),fg='white',bg="#4B7088")
total_supplier_text.pack()

total_supplier_count=Label(supplier_frame,text="0",font=('times new roman',30,'bold'),fg='white',bg="#4B7088")
total_supplier_count.pack()

#category frame
category_frame=Frame(window,bg="#4B7088",bd=3,relief=RIDGE)
category_frame.place(x=400,y=310,height=170,width=280)

total_category_image=PhotoImage(file='category.png')
total_category_label=Label(category_frame,image=total_category_image,bg="#4B7088")
total_category_label.pack(pady=10)

total_category_text=Label(category_frame,text="Total Category",font=('times new roman',15,'bold'),fg='white',bg="#4B7088")
total_category_text.pack()

total_category_count=Label(category_frame,text="0",font=('times new roman',30,'bold'),fg='white',bg="#4B7088")
total_category_count.pack()

#product frame
product_frame=Frame(window,bg="#4B7088",bd=3,relief=RIDGE)
product_frame.place(x=800,y=310,height=170,width=280)

total_product_image=PhotoImage(file='product_1.png')
total_product_label=Label(product_frame,image=total_product_image,bg="#4B7088")
total_product_label.pack(pady=10)

total_product_text=Label(product_frame,text="Total product",font=('times new roman',15,'bold'),fg='white',bg="#4B7088")
total_product_text.pack()

total_product_count=Label(product_frame,text="0",font=('times new roman',30,'bold'),fg='white',bg="#4B7088")
total_product_count.pack()

#sale frame
sales_frame=Frame(window,bg="#4B7088",bd=3,relief=RIDGE)
sales_frame.place(x=600,y=495,height=170,width=280)

total_sales_image=PhotoImage(file='sales_1.png')
total_sales_label=Label(sales_frame,image=total_sales_image,bg="#4B7088")
total_sales_label.pack(pady=10)

total_sales_text=Label(sales_frame,text="Total sales",font=('times new roman',15,'bold'),fg='white',bg="#4B7088")
total_sales_text.pack()

total_sales_count=Label(sales_frame,text="0",font=('times new roman',30,'bold'),fg='white',bg="#4B7088")
total_sales_count.pack()

window.mainloop()
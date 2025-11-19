from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def product_form(window):
    
    global back_image
    product_frame=Frame(window,width=1070,height=598,bg='white')
    product_frame.place(x=200,y=71)
    heading_label=Label(product_frame,text='Manage product Details',font=('times new roman',16,'bold'),bg="#0f4d7d",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    
    back_image=PhotoImage(file='back.png')
    back_button=Button(product_frame,image=back_image,bd=0,bg='white',cursor='hand2',command=lambda: product_frame.place_forget())
    back_button.place(x=1,y=36)
    
    left_frame=Frame(product_frame, bg='white',bd=1,relief=RIDGE)
    left_frame.place(x=10,y=80)
    
    category_label=Label(left_frame,text=' Category :',font=('times new roman',14,'bold'),bg='white')
    category_label.grid(row=0,column=0,padx=20,sticky='w')
    category_combobox=ttk.Combobox(left_frame,font=('times new roman',12),state='readonly',cursor='hand2' ) 
    category_combobox.grid(row=0,column=1)
    category_combobox.set('Empty')
    
    
    supplier_label=Label(left_frame,text=' Supplier :',font=('times new roman',14,'bold'),bg='white')
    supplier_label.grid(row=1,column=0,padx=20,sticky='w')
    supplier_combobox=ttk.Combobox(left_frame,font=('times new roman',12),state='readonly',cursor='hand2') 
    supplier_combobox.grid(row=1,column=1,pady=30)
    supplier_combobox.set('Empty')
    
    name_label=Label(left_frame,text=' Name :',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=2,column=0,padx=20,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    name_entry.grid(row=2,column=1)
    
    price_label=Label(left_frame,text=' Price :',font=('times new roman',14,'bold'),bg='white')
    price_label.grid(row=3,column=0,padx=20,sticky='w')
    price_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    price_entry.grid(row=3,column=1,pady=30)
    
    quantity_label=Label(left_frame,text=' Category :',font=('times new roman',14,'bold'),bg='white')
    quantity_label.grid(row=4,column=0,padx=20,sticky='w')
    quantity_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    quantity_entry.grid(row=4,column=1)
    
    status_label=Label(left_frame,text=' Category :',font=('times new roman',14,'bold'),bg='white')
    status_label.grid(row=5,column=0,padx=20,sticky='w')
    status_combobox=ttk.Combobox(left_frame,font=('times new roman',12),state='readonly',cursor='hand2') 
    status_combobox.grid(row=5,column=1,pady=30)
    status_combobox.set('Empty')
    
    Button_frame=Frame(left_frame, bg='white')
    Button_frame.grid(row=6,columnspan=2,pady=30)
    save_button=Button(Button_frame,text='Save',font=('times new roman',14,'bold'),bg='#2196f3',fg='white',cursor='hand2',width=8)
    save_button.grid(row=0,column=0,padx=20)    
    update_button=Button(Button_frame,text='Update',font=('times new roman',14,'bold'),bg='#4caf50',fg='white',cursor='hand2',width=8)
    update_button.grid(row=0,column=1)
    delete_button=Button(Button_frame,text='Delete',font=('times new roman',14,'bold'),bg='#f44336',fg='white',cursor='hand2',width=8)
    delete_button.grid(row=0,column=2,padx=20)  
    clear_button=Button(Button_frame,text='Clear',font=('times new roman',14,'bold'),bg='#607d8b',fg='white',cursor='hand2',width=8)
    clear_button.grid(row=0,column=3,padx=(0,20))
    
    
    search_frame=LabelFrame(product_frame, text='Search Product', font=('times new roman',12,'bold'),bg='white')
    search_frame.place(x=520,y=70)
    
    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name','Status'),font=('times new roman',13),state='readonly',cursor='hand2',width=15)
    search_combobox.grid(row=0,column=0,padx=10,pady=10)
    search_combobox.set('Select')
    
    search_entry=Entry(search_frame,font=('times new roman',13),bg='lightyellow',width=15)
    search_entry.grid(row=0,column=1,padx=10)
    
    search_button=Button(search_frame,text='Search',font=('times new roman',13),bg='#2196f3',fg='white',cursor='hand2',width=7)
    search_button.grid(row=0,column=2,padx=10)  
    
    showall_button=Button(search_frame,text='Show All',font=('times new roman',13),bg='#607d8b',fg='white',cursor='hand2',width=7)
    showall_button.grid(row=0,column=3,padx=10)
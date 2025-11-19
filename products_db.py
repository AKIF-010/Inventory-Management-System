from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from employee_db import connect_database



def select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox):
    selected = treeview.selection()
    if not selected:
        return
    item = treeview.item(selected[0])   
    content = item['values']            
    if not content:
        return
    # Clear previous values
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)

    # Insert new values
    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0, content[3])
    price_entry.insert(0, content[4])
    quantity_entry.insert(0, content[5])
    status_combobox.set(content[6])
 
    
def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('Select * from product_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to : {str(e)}')
    finally:
        connection.close()
        cursor.close()


def fetch_supplier_category(category_combobox,supplier_combobox):
    category_options=[]
    
    cursor,connection=connect_database()
    if not cursor or not connection:
        return 
    cursor.execute('use inventory_management_system')
    cursor.execute('Select name from category_data')
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_options.append(name[0])
        category_combobox.config(values=category_options) 
    
    supplier_options=[]
    cursor.execute('Select name from supplier_data')
    names=cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_options.append(name[0])
        supplier_combobox.config(values=supplier_options)

def clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.set('Select')
 
def delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
        index=treeview.selection()
        dict=treeview.item(index)
        content=dict['values']
        id=content[0]
        if not index:
           messagebox.showerror('Error','Row is not selected')
           return
        ans=messagebox.askyesno('Confirm ','Do you really want to delete')
        if ans:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return 
            try:
                cursor.execute('use inventory_management_system')
                cursor.execute('Delete from product_data where id=%s',id)
                connection.commit()
                treeview_data(treeview)
                messagebox.showinfo('Info','Record is Deleted')
                clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox)
            except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()
def update_product(category,supplier,name,price,quantity,status,treeview):
        index=treeview.selection()
        dict=treeview.item(index)
        content=dict['values']
        id=content[0]
        if not index:
           messagebox.showerror('Error','Row is not selected')
           return
        cursor,connection=connect_database()
        if not cursor or not connection:
            return 
        cursor.execute('use inventory_management_system')
        cursor.execute('select * from product_data where id = %s ',id)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        current_data=list(current_data)
        current_data[3]=str(current_data[3])
        current_data=tuple(current_data)
        quantity=int(quantity)
        new_data=(category,supplier,name,price,quantity,status)
        if current_data==new_data:
            messagebox.showinfo('Info','No changes detected')
            return
        cursor.execute('UPDATE product_data SET category=%s,supplier=%s,name=%s,price=%s,quantity=%s,status=%s where id=%s',
                       (category,supplier,name,price,quantity,status,id))
        connection.commit()
        messagebox.showinfo('Success','Updated Successfully')
        treeview_data(treeview)
    
def save_product(category,supplier,name,price,quantity,status,treeview):
    
    if category=='Empty':
        messagebox.showerror('Error','Please add category')
    elif supplier=='Empty':
        messagebox.showerror('Error','Please add Supplier')
    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return 
        cursor.execute('use inventory_management_system')
        
        cursor.execute('create table IF NOT EXISTS product_data(id INT AUTO_INCREMENT PRIMARY KEY,category varchar(100),'
                       'supplier varchar(100),name varchar(100),price DECIMAL(10,2),quantity INT, status varchar(50))')
        
        cursor.execute('Select * from product_data  Where category=%s AND supplier=%s AND name=%s',(category,supplier,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error','Product is EXISTS')
            return
        cursor.execute('INSERT INTO  product_data (category,supplier,name,price,quantity,status) VALUES(%s,%s,%s,%s,%s,%s)',(category,supplier,name,price,quantity,status))
        connection.commit()
        messagebox.showinfo('Success','Data is saved')
        treeview_data(treeview)

def search_product(search_combobox,search_entry,treeview):
    if search_combobox.get()=='Search BY':
        messagebox.showwarning('Warning','Please select an Option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning','Please enter the value to search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute(f'select * from product_data where {search_combobox.get()}=%s',search_entry.get())
            record=cursor.fetchone()
            treeview.delete(*treeview.get_children())
            treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to : {str(e)}')
        finally:
            connection.close()
            cursor.close()
   
def show_all_product(search_entry,treeview):
    treeview_data(treeview)
    search_entry.delete(0,END)
     
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
    
    quantity_label=Label(left_frame,text=' Quantity :',font=('times new roman',14,'bold'),bg='white')
    quantity_label.grid(row=4,column=0,padx=20,sticky='w')
    quantity_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    quantity_entry.grid(row=4,column=1)
    
    status_label=Label(left_frame,text=' Status :',font=('times new roman',14,'bold'),bg='white')
    status_label.grid(row=5,column=0,padx=20,sticky='w')
    status_combobox=ttk.Combobox(left_frame,values=('Active','Inactive'),font=('times new roman',12),state='readonly',cursor='hand2') 
    status_combobox.grid(row=5,column=1,pady=30)
    status_combobox.set('Select')
    
    Button_frame=Frame(left_frame, bg='white')
    Button_frame.grid(row=6,columnspan=2,pady=30)
    save_button=Button(Button_frame,text='Save',font=('times new roman',14,'bold'),bg='#2196f3',fg='white',cursor='hand2',width=8,command=lambda: save_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    save_button.grid(row=0,column=0,padx=20)    
    update_button=Button(Button_frame,text='Update',font=('times new roman',14,'bold'),bg='#4caf50',fg='white',cursor='hand2',width=8,command=lambda: update_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    update_button.grid(row=0,column=1)
    delete_button=Button(Button_frame,text='Delete',font=('times new roman',14,'bold'),bg='#f44336',fg='white',cursor='hand2',width=8,command=lambda: delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    delete_button.grid(row=0,column=2,padx=20)  
    clear_button=Button(Button_frame,text='Clear',font=('times new roman',14,'bold'),bg='#607d8b',fg='white',cursor='hand2',width=8,command=lambda: clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    clear_button.grid(row=0,column=3,padx=(0,20))
    
    
    search_frame=LabelFrame(product_frame, text='Search Product', font=('times new roman',12,'bold'),bg='white')
    search_frame.place(x=520,y=70,width=540)
    
    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name','Status'),font=('times new roman',13),state='readonly',cursor='hand2',width=15)
    search_combobox.grid(row=0,column=0,padx=10,pady=10)
    search_combobox.set('Select')
    
    search_entry=Entry(search_frame,font=('times new roman',13),bg='lightyellow',width=16)
    search_entry.grid(row=0,column=1,padx=10)
    
    search_button=Button(search_frame,text='Search',font=('times new roman',13),bg='#2196f3',fg='white',cursor='hand2',width=7,command=lambda: search_product(search_combobox,search_entry,treeview))
    search_button.grid(row=0,column=2,padx=10)  
    
    showall_button=Button(search_frame,text='Show All',font=('times new roman',13),bg='#607d8b',fg='white',cursor='hand2',width=7,command=lambda: show_all_product(search_entry,treeview))
    showall_button.grid(row=0,column=3,padx=10)
    
    treeview_frame=Frame(product_frame)
    treeview_frame.place(x=520,y=150,height=410,width=540)
    
    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(treeview_frame,columns=('ID','Category','Supplier','Name','Price','Quantity','Status'),show='headings',
                            yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,height=20)
    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    
    treeview.heading('ID',text='ID')
    treeview.heading('Category',text='Category')
    treeview.heading('Supplier',text='Supplier')
    treeview.heading('Name',text='Name')
    treeview.heading('Price',text='Price')
    treeview.heading('Quantity',text='Quantity')
    treeview.heading('Status',text='Status')
    treeview.column('ID',width=70)
    treeview.column('Category',width=150)
    treeview.column('Supplier',width=150)
    treeview.column('Name',width=100)
    treeview.column('Price',width=70)
    treeview.column('Quantity',width=70)
    treeview.column('Status',width=70)
    treeview.pack()
    treeview_data(treeview)
    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    
    return product_frame
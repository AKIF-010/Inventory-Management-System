from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee_db import connect_database

def clear_fields(invoice_entry,name_entry,contact_entry,description_entry):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_entry.delete(1.0,END)
    
    
def delete_supplier(invoice_entry,treeview,name_entry,contact_entry,description_entry):
    if invoice_entry=='':
        messagebox.showerror('Error','No row selected')
    else:
        messagebox_result=messagebox.askyesno('Confirm','Do you really want to delete this record?')
        if messagebox_result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('use inventory_management_system')
                cursor.execute('Select * from supplier_data where invoice_no=%s',invoice_entry)
                if not cursor.fetchone() :
                    messagebox.showerror('Error','Invalid Invoice number')
                    return

                cursor.execute('DELETE FROM supplier_data where invoice_no=%s',(
                    int(invoice_entry),
                ))
                connection.commit()
                clear_fields(invoice_entry,name_entry,contact_entry,description_entry)
                messagebox.showinfo('Success','Supplier deleted successfully')

                treeview_data(treeview)
            except Exception as e:
                messagebox.showerror('Error',f'Error due to : {str(e)}')

            finally:
                connection.close()
                cursor.close()



def search_supplier(search_entry,treeview):
    if search_entry=='':
        messagebox.showerror('Error','Invoice number is required for search')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('Select * from supplier_data where invoice_no=%s',search_entry)
            record=cursor.fetchone()
            treeview.delete(*treeview.get_children())
            treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to : {str(e)}')
        finally:
            connection.close()
            cursor.close()
def show_all_suppliers(treeview,search_entry):
    treeview_data(treeview)
    search_entry.delete(0,END)
    
 
def update_supplier(invoice_entry,name_entry,contact_entry,description_entry,treeview):
    if invoice_entry=='' or name_entry=='' or contact_entry=='' or description_entry=='':
        messagebox.showerror('Error','No row selected')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('Select * from supplier_data where invoice_no=%s',invoice_entry)
            if not cursor.fetchone() :
                messagebox.showerror('Error','Invalid Invoice number')
                return
            
            cursor.execute('UPDATE supplier_data SET name=%s,contact=%s,description=%s where invoice_no=%s',(
                name_entry,
                contact_entry,
                description_entry,
                int(invoice_entry)
            ))
            connection.commit()

            messagebox.showinfo('Success','Supplier updated successfully')

            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to : {str(e)}')
        
        finally:
            connection.close()
            cursor.close()
    
def select_data(event,invoice_entry,name_entry,contact_entry,description_entry):
    selected_row=event.widget.focus()
    data=event.widget.item(selected_row)
    record=data['values']
    if record:
        invoice_entry.delete(0,END)
        invoice_entry.insert(0,record[0])
        name_entry.delete(0,END)
        name_entry.insert(0,record[1])
        contact_entry.delete(0,END)
        contact_entry.insert(0,record[2])
        description_entry.delete(1.0,END)
        description_entry.insert(END,record[3])

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('Select * from supplier_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to : {str(e)}')
    finally:
        connection.close()
        cursor.close()
        
        
def add_supplier(invoice_entry,name_entry,contact_entry,description_entry,treeview):
    if invoice_entry=='' or name_entry=='' or contact_entry=='' or description_entry=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('Select * from supplier_data where invoice_no=%s',invoice_entry)
            if cursor.fetchone() :
                messagebox.showerror('Error','Invoice number already exists')
                return
            
            cursor.execute('create table IF NOT EXISTS supplier_data(invoice_no INT primary key, name varchar(50), contact varchar(15), description text)')

            cursor.execute('INSERT INTO supplier_data(invoice_no,name,contact,description) values(%s,%s,%s,%s)',(
                int(invoice_entry),
                name_entry,
                contact_entry,
                description_entry
            ))
            connection.commit()

            messagebox.showinfo('Success','Supplier added successfully')

            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to : {str(e)}')
        
        finally:
            connection.close()
            cursor.close()
def supplier_form(window):
    global back_image
    supplier_frame=Frame(window,width=1070,height=598,bg='white')
    supplier_frame.place(x=200,y=71)
    heading_label=Label(supplier_frame,text='Manage Supplier Details',font=('times new roman',16,'bold'),bg="#0f4d7d",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    
    
    back_image=PhotoImage(file='back.png')
    back_button=Button(supplier_frame,image=back_image,bd=0,bg='white',cursor='hand2',command=lambda: supplier_frame.place_forget())
    back_button.place(x=1,y=36)
    
    left_frame=Frame(supplier_frame,bg='white')
    left_frame.place(x=10,y=100)
    
    invoice_label=Label(left_frame,text='Invoice No :',font=('times new roman',14,'bold'),bg='white')
    invoice_label.grid(row=0,column=0,padx=20,sticky='w')
    invoice_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    invoice_entry.grid(row=0,column=1)
    
    name_label=Label(left_frame,text='Supplier Name :',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=20,pady=25,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    name_entry.grid(row=1,column=1)
     
    contact_label=Label(left_frame,text='Contact Number :',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=20,sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14),bg='lightyellow')
    contact_entry.grid(row=2,column=1)
    
    description_label=Label(left_frame,text='Description :',font=('times new roman',14,'bold'),bg='white',bd=2)
    description_label.grid(row=3,column=0,padx=20,pady=25,sticky='nw')
    description_entry=Text(left_frame,font=('times new roman',14),bg='lightyellow',width=20,height=4)
    description_entry.grid(row=3,column=1,pady=25)
     
    bottom_frame=Frame(left_frame,bg='white')
    bottom_frame.grid(row=4,columnspan=2,pady=10)
    
    add_button=Button(bottom_frame,text='Add',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: add_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_entry.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)
    
    update_button=Button(bottom_frame,text='Update',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: update_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_entry.get(1.0,END).strip(),treeview))
    update_button.grid(row=0,column=1)
    
    delete_button=Button(bottom_frame,text='Delete',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: delete_supplier(invoice_entry.get(),treeview,name_entry,contact_entry,description_entry))
    delete_button.grid(row=0,column=2,padx=20)
    
    clear_button=Button(bottom_frame,text='Clear',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: clear_fields(invoice_entry,name_entry,contact_entry,description_entry))
    clear_button.grid(row=0,column=3)
    
    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=490,y=100,width=580,height=400)
    
    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(fill=X)
    
    num_label=Label(search_frame,text='Invoice No :',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,20),sticky='w')
    
    search_entry=Entry(search_frame,font=('times new roman',14),bg='lightyellow')
    search_entry.grid(row=0,column=1)
    
    searth_button=Button(search_frame,text='Search',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: search_supplier(search_entry.get(),treeview))
    searth_button.grid(row=0,column=2,padx=20)
    
    show_button=Button(search_frame,text='Show All',font=('times new roman',14),width=8,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: show_all_suppliers(treeview,search_entry))
    show_button.grid(row=0,column=3)
    
    
    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(right_frame,columns=('Invoice No','Name','Contact','Description'),show='headings',
                            yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,height=15)
    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y,pady=(20,0))
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    
    treeview.pack(pady=(20,0))
    treeview.heading('Invoice No',text='Invoice No')
    treeview.heading('Name',text='Name')
    treeview.heading('Contact',text='Contact')
    treeview.heading('Description',text='Description')
    treeview.column('Invoice No',width=100)
    treeview.column('Name',width=150)
    treeview.column('Contact',width=150)
    treeview.column('Description',width=200)
    
    
    treeview_data(treeview)
    
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event,invoice_entry,name_entry,contact_entry,description_entry)) 
    
    return supplier_frame
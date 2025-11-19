from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee_db import connect_database

def clear_category_fields(entry_id,entry_name,text_description):
    entry_id.delete(0,END)
    entry_name.delete(0,END)
    text_description.delete('1.0',END)

def select_data(event,treeview,entry_id,entry_name,text_description):
    selected_row=treeview.focus()
    data=treeview.item(selected_row)
    record=data['values']
    entry_id.delete(0,END)
    entry_id.insert(0,record[0])
    entry_name.delete(0,END)
    entry_name.insert(0,record[1])
    text_description.delete('1.0',END)
    text_description.insert(END,record[2])

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('Select * from category_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to : {str(e)}')
    finally:
        connection.close()
        cursor.close()

def delete_category(cat_id,treeview):
    if cat_id=='':
        messagebox.showerror('Error','No row selected')
    else:
        messagebox_result=messagebox.askyesno('Confirm','Do you really want to delete this record?')
        if messagebox_result:
            cursor,connection=connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('use inventory_management_system')
                cursor.execute('Select * from category_data where Category_ID=%s',cat_id)
                if not cursor.fetchone() :
                    messagebox.showerror('Error','Invalid Category ID')
                    return

                cursor.execute('DELETE FROM category_data where Category_ID=%s',(
                    int(cat_id),
                ))
                connection.commit()

                messagebox.showinfo('Success','Category deleted successfully')

                treeview_data(treeview)
            except Exception as e:
                messagebox.showerror('Error',f'Error due to : {str(e)}')

            finally:
                connection.close()
                cursor.close()
    
    
    
def add_category(cat_id, cat_name, cat_description,treeview):
    if cat_id=='' or cat_name=='' or cat_description=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('Select * from category_data where Category_ID=%s',cat_id)
            if cursor.fetchone() :
                    messagebox.showerror('Error','Category number already exists')
                    return
            cursor.execute('create table IF NOT EXISTS category_data(Category_ID INT primary key, name varchar(50), description text)')
            cursor.execute('INSERT INTO category_data(Category_ID,name,description) values(%s,%s,%s)',(
                cat_id,
                cat_name,
                cat_description
            ))
            connection.commit()
            messagebox.showinfo('Success','Category added successfully')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to : {str(e)}')
        finally:
            connection.close()
            cursor.close()


def category_form(window):
    global back_image,logo
    category_frame=Frame(window,width=1070,height=598,bg='white')
    category_frame.place(x=200,y=71)
    heading_label=Label(category_frame,text='Manage Category Details',font=('times new roman',16,'bold'),bg="#0f4d7d",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    
    back_image=PhotoImage(file='back.png')
    back_button=Button(category_frame,image=back_image,bd=0,bg='white',cursor='hand2',command=lambda: category_frame.place_forget())
    back_button.place(x=1,y=36)
    
    
    logo=PhotoImage(file='category2.png')
    label=Label(category_frame,image=logo,bg='white')
    label.place(x=30,y=100)
    
    detail_frame=Frame(category_frame, bg='white')
    detail_frame.place(x=500,y=60)
    
    
    category_label=Label(detail_frame,text=' Category ID :',font=('times new roman',14,'bold'),bg='white')
    category_label.grid(row=0,column=0,padx=20,sticky='w')
    category_entry=Entry(detail_frame,font=('times new roman',14),bg='lightyellow')
    category_entry.grid(row=0,column=1,pady=10,sticky='w')
    
    name_label=Label(detail_frame,text=' Category Name :',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=20,sticky='w')
    name_entry=Entry(detail_frame,font=('times new roman',14),bg='lightyellow')
    name_entry.grid(row=1,column=1,pady=10,sticky='w')
    
    description_text_label=Label(detail_frame,text=' Description :',font=('times new roman',14,'bold'),bg='white')
    description_text_label.grid(row=2,column=0,padx=20,sticky='w')
    description_label=Text(detail_frame,height=6,width=22,bg='lightyellow')
    description_label.grid(row=2,column=1,pady=10,sticky='w')
    
    button_frame=Frame(detail_frame, bg='white')
    button_frame.grid(row=3,columnspan=2,pady=10,padx=40)
    
    add_button=Button(button_frame,text='Add',font=('times new roman',14,'bold'),bg='#2196f3',fg='white',cursor='hand2',width=8,command=lambda: add_category(category_entry.get(),name_entry.get(),description_label.get('1.0',END),treeview))
    add_button.grid(row=0,column=0,padx=20)
    delete_button=Button(button_frame,text='Delete',font=('times new roman',14,'bold'),bg='#f44336',fg='white',cursor='hand2',width=8,command=lambda: delete_category(category_entry.get(),treeview))
    delete_button.grid(row=0,column=1,padx=20)
    clear_button=Button(button_frame,text='Clear',font=('times new roman',14,'bold'),bg='#607d8b',fg='white',cursor='hand2',width=8,command=lambda: clear_category_fields(category_entry,name_entry,description_label))
    clear_button.grid(row=0,column=2,padx=20)
    
    
    treeview_frame=Frame(category_frame, bg='white')
    treeview_frame.place(x=530,y=340,height=200,width=500)
    
    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(treeview_frame,columns=('Category ID','Name','Description'),show='headings',
                            yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    
    treeview.heading('Category ID',text='Category ID')
    treeview.heading('Name',text='Name')
    treeview.heading('Description',text='Description')
    treeview.column('Category ID',width=100)
    treeview.column('Name',width=150)
    treeview.column('Description',width=240)
    treeview.pack()

    treeview_data(treeview)
    
    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,treeview,category_entry,name_entry,description_label))
    
    return category_frame
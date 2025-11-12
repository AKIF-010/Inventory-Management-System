from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pymysql

def select_data(event,empid_entry,name_entry,email_entry,gender_combobox,
                                                       dob_date_entry,contact_entry,etyp_combobox,edu_combobox,password_entry,
                                                       wshift_combobox,address_text,doj_date_entry,salary_entry,usertyp_combobox):
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content['values']
    clear_fields(empid_entry,name_entry,email_entry,
                    gender_combobox,dob_date_entry,contact_entry,
                    etyp_combobox,edu_combobox,password_entry,
                    wshift_combobox,address_text,doj_date_entry,
                    salary_entry,usertyp_combobox,False)
    empid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])    
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    etyp_combobox.set(row[6])
    edu_combobox.set(row[7])
    wshift_combobox.set(row[8])
    address_text.insert('1.0',row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0,row[11])
    usertyp_combobox.set(row[12])
    password_entry.insert(0,row[13])
    
def treeview_data():
    cursor,connection=connect_database()
    if cursor is None and connection is None:
        return
    cursor.execute('USE inventory_management_system')
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records=cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {str(e)}') 
    finally:
        connection.close()
        cursor.close()
def clear_fields(empid_entry,name_entry,email_entry,gender_combobox,
                dob_date_entry,contact_entry,etyp_combobox,edu_combobox,password_entry,
                wshift_combobox,address_text,doj_date_entry,salary_entry,usertyp_combobox,check):
    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    from datetime import date
    dob_date_entry.set_date(date.today()) 
    gender_combobox.set('Select Gender')
    contact_entry.delete(0,END)
    etyp_combobox.set('Select Type')
    edu_combobox.set('Select Education')
    wshift_combobox.set('Select Shift')
    address_text.delete('1.0',END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0,END)
    usertyp_combobox.set('Select User Type')
    password_entry.delete(0,END)
    if check: 
        employee_treeview.selection_remove(employee_treeview.selection())

def update_employee(emp_id, name, email, gender, dob, contact, employement_type, 
                    education, work_shift, address, doj, salary, user_type, password):
    selected=employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error','Please select a record to update')
    else:
        cursor,connection=connect_database()
        if cursor is None and connection is None:
            return
        cursor.execute('USE inventory_management_system')
        cursor.execute('SELECT * FROM employee_data WHERE emp_id=%s',(emp_id,))
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        address=address.strip()
        new_data=(name, email, gender, dob, contact, employement_type, 
                    education, work_shift, address, doj, salary, user_type, password)
        if current_data==new_data:
            messagebox.showinfo('Info','No changes detected to update')
            return
        cursor.execute('UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, '
                       'contact=%s, employement_type=%s, education=%s, work_shift=%s, address=%s, '
                       'doj=%s, salary=%s, user_type=%s, password=%s WHERE emp_id=%s',
                       (name, email, gender, dob, contact, employement_type, 
                        education, work_shift, address, doj, salary, user_type, password, emp_id,))
    connection.commit()
    treeview_data()
    messagebox.showinfo('Success','Record Updated Successfully')
def connect_database():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='#01#02#03abc') 
        cursor=connection.cursor()
    except:
        messagebox.showerror('Error','Database Connectivity Issue,Please Try Again') 
        return None, None
   
    return cursor,connection

def create_database_table():
    cursor,connection=connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_management_system')
    cursor.execute('USE inventory_management_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data(emp_id INT PRIMARY KEY, name VARCHAR(200),'
                   'email VARCHAR(200), gender VARCHAR(50), dob VARCHAR(50), contact VARCHAR(15), employement_type VARCHAR(50), '
                   'education VARCHAR(100), work_shift VARCHAR(50), address VARCHAR(200), doj VARCHAR(50), salary VARCHAR(50), user_type VARCHAR(50), password VARCHAR(20))')

def add_employee(emp_id, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, user_type, password):
    
    if (emp_id=='' or name=='' or email=='' or gender=='Select Gender'  or contact=='' or employement_type=='Select Type' or education=='Select Education' or
        work_shift=='Select Shift' or address=='\n' or salary=='' or user_type=='Select User Type' or password==''):
        messagebox.showerror('Error','All Fields are Required')
    else:
        cursor,connection=connect_database()
        if cursor is None and connection is None:
            return
        cursor.execute('USE inventory_management_system')
        try:
            cursor.execute('SELECT * FROM employee_data WHERE emp_id=%s',(emp_id,))
            if cursor.fetchone() :
                messagebox.showerror('Error','Employee ID already exists')
                return
            address=address.strip()
            cursor.execute('INSERT INTO employee_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(emp_id, name, email, gender, dob, 
                            contact, employement_type, education, work_shift, address, doj, salary, user_type, password))
            connection.commit()
            treeview_data()
            messagebox.showinfo('Success','Data Added Successfully')
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {str(e)}')
        finally:
            connection.close()
            cursor.close()
        
def fix_calendar_position(widget):
    def modified_popup(event): 

        x = widget.winfo_rootx()
        y = widget.winfo_rooty()
        
        if hasattr(widget, '_top_cal') and widget._top_cal is not None:
            widget._top_cal.geometry(f'+{x}+{y - 250}')
    widget.bind('<Button-1>', modified_popup, add='+')
    
def employee_form(window):
    global back_image,employee_treeview
    employee_frame=Frame(window,width=1070,height=598,bg='white')
    employee_frame.place(x=200,y=70)
    heading_label=Label(employee_frame,text='Manage Employee Details',font=('times new roman',16,'bold'),bg="#0f4d7d",fg='white')
    heading_label.place(x=0,y=0,relwidth=1)
    
    
    
    top_frame=Frame(employee_frame,bg='white')
    top_frame.place(x=0,y=35,relwidth=1,height=235)
    
    back_image=PhotoImage(file='back.png')
    back_button=Button(top_frame,image=back_image,bd=0,bg='white',cursor='hand2',command=lambda: employee_frame.place_forget())
    back_button.place(x=1,y=1)
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
  
    treeview_data()
    
    emp_details_frame=Frame(employee_frame,bg='white')
    emp_details_frame.place(x=15,y=300)
    
    emp_id_label=Label(emp_details_frame,text='EmpID',font=('times new roman',12,'bold'),bg='white')
    emp_id_label.grid(row=0,column=0,padx=20,pady=10,sticky='w')
    empid_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    empid_entry.grid(row=0,column=1,padx=20,pady=10)
    
    name_label=Label(emp_details_frame,text='Name',font=('times new roman',12,'bold'),bg='white')
    name_label.grid(row=0,column=2,padx=20,pady=10,sticky='w')
    name_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    name_entry.grid(row=0,column=3,padx=20,pady=10)
    
    email_label=Label(emp_details_frame,text='Email',font=('times new roman',12,'bold'),bg='white')
    email_label.grid(row=0,column=4,padx=20,pady=10,sticky='w')
    email_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    email_entry.grid(row=0,column=5,padx=20,pady=10)
    
    gender_label=Label(emp_details_frame,text='Gender',font=('times new roman',12,'bold'),bg='white')
    gender_label.grid(row=1,column=0,padx=20,pady=10,sticky='w')
    gender_combobox=ttk.Combobox(emp_details_frame,values=('Male','Female','Other'),font=('times new roman',12),state='readonly',cursor='hand2',width=18 ) 
    gender_combobox.grid(row=1,column=1)
    gender_combobox.set('Select Gender')
    
    dob_label=Label(emp_details_frame,text='Date of Birth',font=('times new roman',12,'bold'),bg='white')
    dob_label.grid(row=1,column=2,padx=20,pady=10,sticky='w')
    dob_date_entry=DateEntry(emp_details_frame,width=18,font=('times new roman',12),date_pattern='dd-mm-yyyy',state='readonly')
    dob_date_entry.grid(row=1,column=3)
    
    contact_label=Label(emp_details_frame,text='Contact',font=('times new roman',12,'bold'),bg='white')
    contact_label.grid(row=1,column=4,sticky='w',padx=20,pady=10)
    contact_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    contact_entry.grid(row=1,column=5,padx=20,pady=10)
    
    etyp_label=Label(emp_details_frame,text='Employement Type',font=('times new roman',12,'bold'),bg='white')
    etyp_label.grid(row=2,column=0,sticky='w',padx=20,pady=10)
    etyp_combobox=ttk.Combobox(emp_details_frame,font=('times new roman',12),values=('Full Time','Part Time','Contract','Casual','Intern'),state='readonly',cursor='hand2',width=18)
    etyp_combobox.grid(row=2,column=1)
    etyp_combobox.set('Select Type')
    
    education_options=['B.Tech','B.Com','BBA','MBA','M.Tech','M.Com','Diploma','High School','Other']
    edu_label=Label(emp_details_frame,text='Education',font=('times new roman',12,'bold'),bg='white')
    edu_label.grid(row=2,column=2,sticky='w',padx=20,pady=10)
    edu_combobox=ttk.Combobox(emp_details_frame,font=('times new roman',12),values=education_options,state='readonly',cursor='hand2',width=18)
    edu_combobox.grid(row=2,column=3)
    edu_combobox.set('Select Education')
    
    wshift_label=Label(emp_details_frame,text='Work Shift',font=('times new roman',12,'bold'),bg='white')
    wshift_label.grid(row=2,column=4,sticky='w',padx=20,pady=10)
    wshift_combobox=ttk.Combobox(emp_details_frame,font=('times new roman',12),values=('Morning','Evening','Night','Rotational'),state='readonly',cursor='hand2',width=18)
    wshift_combobox.grid(row=2,column=5)
    wshift_combobox.set('Select Shift')
    
    address_label=Label(emp_details_frame,text='Address',font=('times new roman',12,'bold'),bg='white')
    address_label.grid(row=3,column=0,padx=20,pady=10,sticky='w')
    address_text=Text(emp_details_frame,height=3,width=20,font=('times new roman',12),bg="lightyellow")
    address_text.grid(row=3,column=1,rowspan=2)
    
    doj_label=Label(emp_details_frame,text='Date of Join',font=('times new roman',12,'bold'),bg='white')
    doj_label.grid(row=3,column=2,padx=20,pady=10,sticky='w')
    doj_date_entry=DateEntry(emp_details_frame,width=18,font=('times new roman',12),date_pattern='dd-mm-yyyy',state='readonly')
    doj_date_entry.grid(row=3,column=3)
    fix_calendar_position(doj_date_entry)
    
    usertyp_label=Label(emp_details_frame,text='User Type',font=('times new roman',12,'bold'),bg='white')
    usertyp_label.grid(row=4,column=2,sticky='w',padx=20,pady=10)
    usertyp_combobox=ttk.Combobox(emp_details_frame,font=('times new roman',12),values=('Admin','Employee'),state='readonly',cursor='hand2',width=18)
    usertyp_combobox.set('Select User Type')
    usertyp_combobox.grid(row=4,column=3)
    
    salary_label=Label(emp_details_frame,text='Salary',font=('times new roman',12,'bold'),bg='white')
    salary_label.grid(row=3,column=4,sticky='w',padx=20,pady=10)
    salary_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    salary_entry.grid(row=3,column=5,padx=20,pady=10)
    
    password_label=Label(emp_details_frame,text='Password',font=('times new roman',12,'bold'),bg='white')
    password_label.grid(row=4,column=4,sticky='w',padx=20,pady=10)
    password_entry=Entry(emp_details_frame,font=('times new roman',12),bg="lightyellow")
    password_entry.grid(row=4,column=5,padx=20,pady=10)
    
    
    #bottom frame in employee frame
    save_frame=Frame(employee_frame,bg='white')
    save_frame.place(x=200,y=530,height=100)
    
    
    add_button=Button(save_frame,text='Add',
                      font=('times new roman',12),width=10,
                      cursor='hand2',fg='white',bg='#0f4d7d',
                      command=lambda: add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),
                                           dob_date_entry.get(),contact_entry.get(),etyp_combobox.get(),edu_combobox.get(),
                                           wshift_combobox.get(),address_text.get('1.0',END),doj_date_entry.get(),salary_entry.get(),
                                           usertyp_combobox.get(),password_entry.get())) 
    add_button.grid(row=0,column=0,padx=20)
    
    update_button=Button(save_frame,text='Update',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d7d',
                         command=lambda: update_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),
                                           dob_date_entry.get(),contact_entry.get(),etyp_combobox.get(),edu_combobox.get(),
                                           wshift_combobox.get(),address_text.get('1.0',END),doj_date_entry.get(),salary_entry.get(),
                                           usertyp_combobox.get(),password_entry.get()))
    update_button.grid(row=0,column=1,padx=20)
    
    delete_button=Button(save_frame,text='Delete',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d7d')
    delete_button.grid(row=0,column=2,padx=20)
    
    clear_button=Button(save_frame,text='Clear',font=('times new roman',12),width=10,cursor='hand2',fg='white',bg='#0f4d7d',command=lambda: clear_fields(empid_entry,name_entry,email_entry,gender_combobox,
                                                       dob_date_entry,contact_entry,etyp_combobox,edu_combobox,password_entry,
                                                       wshift_combobox,address_text,doj_date_entry,salary_entry,usertyp_combobox,True))
    clear_button.grid(row=0,column=3,padx=20)

    employee_treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,empid_entry,name_entry,email_entry,gender_combobox,
                                                       dob_date_entry,contact_entry,etyp_combobox,edu_combobox,password_entry,
                                                       wshift_combobox,address_text,doj_date_entry,salary_entry,usertyp_combobox))
    
    create_database_table()
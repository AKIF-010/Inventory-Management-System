from tkinter import *
def sales_form(window):
    
        sales_frame=Frame(window,width=1070,height=598,bg='white')
        sales_frame.place(x=200,y=71)
        heading_label=Label(sales_frame,text='Under maintenance',font=('times new roman',25,'bold'),bg="#e60000",fg='white')
        heading_label.place(x=0,y=240,relwidth=1)
        return sales_frame
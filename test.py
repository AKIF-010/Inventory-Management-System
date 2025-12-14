from tkinter import *
from tkinter import ttk

def open_billing():
    win = Tk()
    win.title("Billing / Sales Page")
    win.geometry("1500x800")
    win.config(bg="white")

    # ===================== TITLE BAR =====================
    title = Label(win, text="Inventory Management System",
                  font=("times new roman", 30, "bold"), bg="#03396c", fg="white", pady=10)
    title.pack(fill=X)

    # ===================== MAIN FRAME =====================
    main_frame = Frame(win, bg="white")
    main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

    # ===================== LEFT: PRODUCT LIST =====================
    product_frame = LabelFrame(main_frame, text="All Products", font=("times new roman", 14, "bold"),
                               bg="white", fg="black", bd=3, relief=RIDGE)
    product_frame.place(x=10, y=10, width=420, height=760)

    # Search Section
    search_frame = Frame(product_frame, bg="white")
    search_frame.pack(fill=X, pady=5)

    Label(search_frame, text="Search Product | By Name", font=("times new roman", 12, "bold"), bg="white").pack(anchor="w")
    search_entry = Entry(search_frame, font=("times new roman", 12), width=25)
    search_entry.pack(side=LEFT, padx=5, pady=5)

    Button(search_frame, text="Search", width=10).pack(side=LEFT, padx=2)
    Button(search_frame, text="Show All", width=10).pack(side=LEFT, padx=2)

    # Product Table
    product_table_frame = Frame(product_frame, bg="white", bd=2, relief=RIDGE)
    product_table_frame.pack(fill=BOTH, expand=True)

    product_table = ttk.Treeview(product_table_frame, columns=("pid", "name", "price", "qty", "status"),
                                 show="headings")

    for col in ("pid", "name", "price", "qty", "status"):
        product_table.heading(col, text=col.upper())
        product_table.column(col, width=60)

    product_table.pack(fill=BOTH, expand=True)

    # ===================== MIDDLE: CUSTOMER + CART + CALCULATOR =====================
    middle_frame = Frame(main_frame, bg="white")
    middle_frame.place(x=440, y=10, width=520, height=760)

    # Customer Details
    cust_frame = LabelFrame(middle_frame, text="Customer Details", font=("times new roman", 14, "bold"),
                            bg="white", fg="black", bd=3, relief=RIDGE)
    cust_frame.pack(fill=X)

    Label(cust_frame, text="Name:", bg="white", font=("times new roman", 12)).grid(row=0, column=0, padx=5, pady=5)
    Entry(cust_frame, width=20, font=("times new roman", 12)).grid(row=0, column=1, padx=5, pady=5)

    Label(cust_frame, text="Contact No:", bg="white", font=("times new roman", 12)).grid(row=0, column=2, padx=5, pady=5)
    Entry(cust_frame, width=20, font=("times new roman", 12)).grid(row=0, column=3, padx=5, pady=5)

    # Calculator Frame
    calc_frame = Frame(middle_frame, bg="white", bd=3, relief=RIDGE)
    calc_frame.pack(pady=10)

    calc_display = Entry(calc_frame, font=("arial", 20, "bold"), bd=5, relief=RIDGE, justify=RIGHT)
    calc_display.grid(row=0, column=0, columnspan=4, sticky="we")

    btn_texts = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("+", 1, 3),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("*", 3, 3),
        ("0", 4, 0), ("C", 4, 1), ("=", 4, 2), ("/", 4, 3),
    ]

    for txt, r, c in btn_texts:
        Button(calc_frame, text=txt, font=("arial", 15, "bold"), width=5, height=2).grid(row=r, column=c, padx=2, pady=2)

    # Cart Frame
    cart_frame = LabelFrame(middle_frame, text="Cart", font=("times new roman", 14, "bold"),
                            bg="white", fg="black", bd=3, relief=RIDGE)
    cart_frame.pack(fill=BOTH, expand=True)

    cart_table = ttk.Treeview(cart_frame, columns=("pid", "name", "price"), show="headings")
    for col in ("pid", "name", "price"):
        cart_table.heading(col, text=col.upper())
        cart_table.column(col, width=80)
    cart_table.pack(fill=BOTH, expand=True)

    # Product Details + Add/Update Frame
    bottom_mid_frame = Frame(middle_frame, bg="white", bd=3, relief=RIDGE)
    bottom_mid_frame.pack(fill=X, pady=5)

    Label(bottom_mid_frame, text="Product Name:", font=("times new roman", 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
    Entry(bottom_mid_frame, width=20).grid(row=0, column=1)

    Label(bottom_mid_frame, text="Price Per Qty:", font=("times new roman", 12), bg="white").grid(row=1, column=0, padx=5, pady=5)
    Entry(bottom_mid_frame, width=20).grid(row=1, column=1)

    Label(bottom_mid_frame, text="Quantity:", font=("times new roman", 12), bg="white").grid(row=2, column=0, padx=5, pady=5)
    Entry(bottom_mid_frame, width=20).grid(row=2, column=1)

    Button(bottom_mid_frame, text="Clear", width=15).grid(row=3, column=0, pady=10)
    Button(bottom_mid_frame, text="Add | Update", width=15).grid(row=3, column=1, pady=10)

    # ===================== RIGHT: CUSTOMER BILL AREA =====================
    bill_frame = LabelFrame(main_frame, text="Customer Bill Area", font=("times new roman", 14, "bold"),
                            bg="white", fg="black", bd=3, relief=RIDGE)
    bill_frame.place(x=970, y=10, width=520, height=760)

    bill_text = Text(bill_frame, font=("courier", 12))
    bill_text.pack(fill=BOTH, expand=True)

    # ===================== BOTTOM BILL BUTTONS =====================
    btn_frame = Frame(bill_frame, bg="white")
    btn_frame.pack(fill=X, pady=10)

    Button(btn_frame, text="Bill Amount", width=12).grid(row=0, column=0, padx=5)
    Button(btn_frame, text="Discount [5%]", width=12).grid(row=0, column=1, padx=5)
    Button(btn_frame, text="Net Pay", width=12).grid(row=0, column=2, padx=5)
    Button(btn_frame, text="Generate Bill", width=12).grid(row=0, column=3, padx=5)
    Button(btn_frame, text="Clear All", width=12).grid(row=0, column=4, padx=5)
    Button(btn_frame, text="Print", width=12).grid(row=0, column=5, padx=5)

    win.mainloop()


if __name__ == "__main__":
    open_billing()

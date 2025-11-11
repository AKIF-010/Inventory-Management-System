from tkinter import *
from time import strftime

window = Tk()
window.geometry("1070x100")
window.configure(bg='white')

# Set constant height and width for the header area
HEADER_HEIGHT = 70
HEADER_WIDTH = 1070

# --- Top Frame Container (Occupies the 1070x70 area starting at x=200) ---
# NOTE: The geometry is 1070 wide, but the frame starts at x=200.
# To make it work as a *header* in a larger app, you might adjust the width/x placement.
# For this code snippet, I'm setting it to the full window width minus 200 (1070-200=870) 
# and placing it starting at x=200, assuming a left menu of 200px (like your previous goal).
# If the window IS the header, simply start at x=0 and width=1070.
# Assuming you want it to occupy the full width of the visible window (1070-200=870), 
# starting at x=200.
top_frame = Frame(window, bg='white', height=HEADER_HEIGHT, width=870)
top_frame.place(x=200, y=0) 
top_frame.grid_propagate(False) # Prevent frame from resizing to fit content

top_border = Frame(window, bg="black", height=1, width=870)
top_border.place(x=200, y=HEADER_HEIGHT)

# Configure top_frame to use two columns
top_frame.columnconfigure(0, weight=1) # Left section takes up remaining space
top_frame.columnconfigure(1, weight=0) # Right section fits content size (Logout button)
top_frame.rowconfigure(0, weight=1) # Ensure the row expands vertically

# --- Left Section (Welcome and Date/Time) ---
left_frame = Frame(top_frame, bg='white')
# Grid left_frame to occupy the first column, sticky W for left alignment, 
# and sticky N+S to make it stretch vertically within its cell.
left_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5) 
# Use sticky W for text alignment within left_frame.

welcome_label = Label(left_frame, text='Welcome, Admin', font=('times new roman', 15, 'bold'), bg='white', fg='black', anchor=W)
welcome_label.grid(row=0, column=0, sticky=W)

date_label = Label(left_frame, font=('times new roman', 12), bg='white', fg='black', anchor=W)
date_label.grid(row=1, column=0, sticky=W)

def update_time():
    """Updates the date and time display every second."""
    current_time = strftime('%I:%M:%S %p')
    current_date = strftime('%d-%m-%Y')
    
    # Combined text for single label (cleaner appearance)
    date_label.config(text=f"Date: {current_date}      Time: {current_time}")
    date_label.after(1000, update_time)

update_time()

# --- Right Section (Logout Button) ---
right_frame = Frame(top_frame, bg='white')
# Grid right_frame to occupy the second column, sticky E for right alignment,
# and sticky N+S to make it stretch vertically within its cell.
right_frame.grid(row=0, column=1, sticky="nse", padx=20) 
right_frame.columnconfigure(0, weight=1) # Allow button to be centered horizontally
right_frame.rowconfigure(0, weight=1)   # Allow button to be centered vertically

logout_button = Button(right_frame, text='Logout', font=('times new roman', 12, 'bold'), 
                       bg='white', fg='#000080', bd=0, command=window.quit)
# Use grid on the button within right_frame, sticking to the center.
# The surrounding frame (right_frame) ensures it's vertically centered in the header area.
logout_button.grid(row=0, column=0, sticky="") 

window.mainloop()
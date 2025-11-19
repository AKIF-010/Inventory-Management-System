import tkinter as tk

root = tk.Tk()
root.overrideredirect(True)   # Remove default title bar
root.geometry("500x300")

# Custom title bar frame
title_bar = tk.Frame(root, bg="#1e90ff", height=30)
title_bar.pack(fill="x")

title_label = tk.Label(title_bar, text="My App", bg="#1e90ff", fg="white")
title_label.pack(side="left", padx=10)

# Drag window
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

title_bar.bind("<B1-Motion>", move_window)

# Close button
close_btn = tk.Button(title_bar, text="X", bg="red", fg="white",
                      command=root.destroy, bd=0)
close_btn.pack(side="right")

root.mainloop()

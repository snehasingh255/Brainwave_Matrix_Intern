from tkinter import *
from tkinter import messagebox
import inventory

def hide_output():
    output.grid_remove()

def show_output():
    output.grid(row=1, column=0, pady=10)
    output.delete(1.0, END)

def clear_entries():
    e_pid.delete(0, END)
    e_name.delete(0, END)
    e_qty.delete(0, END)

def show_entry_fields(pid=True, name=True, qty=True):
    entry_frame.grid()
    e_pid_label.grid(row=0, column=0, sticky="w") if pid else e_pid_label.grid_remove()
    e_pid.grid(row=0, column=1) if pid else e_pid.grid_remove()
    e_name_label.grid(row=1, column=0, sticky="w") if name else e_name_label.grid_remove()
    e_name.grid(row=1, column=1) if name else e_name.grid_remove()
    e_qty_label.grid(row=2, column=0, sticky="w") if qty else e_qty_label.grid_remove()
    e_qty.grid(row=2, column=1) if qty else e_qty.grid_remove()

def add_product_ui():
    hide_output()
    show_entry_fields(pid=True, name=True, qty=True)
    def submit():
        pid = e_pid.get()
        name = e_name.get()
        qty = e_qty.get()
        if not pid or not name or not qty:
            messagebox.showerror("All fields are mandatory!")
        elif pid and name and qty.isdigit():
            if inventory.add_product(pid, name, int(qty)):
                messagebox.showinfo("Success", "Product added.")
            else:
                messagebox.showwarning("Error","Product ID already exists.")
        else:
            messagebox.showerror("Error", "Invalid input.")
        clear_entries()
        entry_frame.grid_remove()
    action_button.config(text="Submit", command=submit)

def delete_product_ui():
    hide_output()
    show_entry_fields(pid=True, name=False, qty=False)
    def submit():
        pid = e_pid.get()
        if inventory.delete_product(pid):
            messagebox.showinfo("Deleted", f"Product {pid} removed.")
        else:
            messagebox.showerror("Error", "Product not found.")
        clear_entries()
        entry_frame.grid_remove()
    action_button.config(text="Submit", command=submit)

def view_inventory_ui():
    entry_frame.grid_remove()
    show_output()
    products = inventory.view_inventory()
    for pid, info in products.items():
        output.insert(END, f"{pid}: {info['name']} - Qty: {info['quantity']}\n")

def low_stock_ui():
    entry_frame.grid_remove()
    show_output()
    alert = inventory.low_stock_alert()
    if alert:
        for pid, info in alert.items():
            output.insert(END, f"LOW STOCK >> {pid}: {info['name']} - Qty: {info['quantity']}\n")
    else:
        output.insert(END, "No low stock items.\n")

def save_inventory_ui():
    inventory.save_inventory()
    messagebox.showinfo("Saved", "Inventory saved to file.")

def load_inventory_ui():
    inventory.load_inventory()
    messagebox.showinfo("Loaded", "Inventory loaded from file.")

root = Tk()
root.title("Inventory Dashboard")
root.geometry("600x500")
root.configure(bg="#f2f6fc")

# Frames
left_frame = Frame(root, bg="#2c3e50")
left_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ns")

right_frame = Frame(root, bg="#f2f6fc")
right_frame.grid(row=0, column=1, padx=30, pady=20, sticky="n")

# Sidebar Buttons
btn_cfg = {"width": 20, "padx": 10, "pady": 8, "bd": 0, "fg": "white", "bg": "#34495e", "activebackground": "#2980b9", "font": ("Segoe UI", 10, "bold")}
Button(left_frame, text="Add Product", command=add_product_ui, **btn_cfg).pack(pady=5)
Button(left_frame, text="View Inventory", command=view_inventory_ui, **btn_cfg).pack(pady=5)
Button(left_frame, text="Delete Product", command=delete_product_ui, **btn_cfg).pack(pady=5)
Button(left_frame, text="Low Stock Alert", command=low_stock_ui, **btn_cfg).pack(pady=5)
Button(left_frame, text="Save Inventory", command=save_inventory_ui, **btn_cfg).pack(pady=5)
Button(left_frame, text="Load Inventory", command=load_inventory_ui, **btn_cfg).pack(pady=5)

# Entry Frame
entry_frame = Frame(right_frame, bg="#f2f6fc")
entry_frame.grid(row=0, column=0, pady=10)

lbl_cfg = {"bg": "#f2f6fc", "font": ("Segoe UI", 10, "bold")}
entry_cfg = {"width": 30, "bg": "white", "font": ("Segoe UI", 10)}

e_pid_label = Label(entry_frame, text="Product ID", **lbl_cfg)
e_pid = Entry(entry_frame, **entry_cfg)

e_name_label = Label(entry_frame, text="Name", **lbl_cfg)
e_name = Entry(entry_frame, **entry_cfg)

e_qty_label = Label(entry_frame, text="Quantity", **lbl_cfg)
e_qty = Entry(entry_frame, **entry_cfg)

action_button = Button(entry_frame, text="Submit", width=15, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), bd=0)
action_button.grid(row=3, columnspan=2, pady=15)

entry_frame.grid_remove()

# Output box
output = Text(right_frame, height=20, width=65, bg="white", fg="#2c3e50", font=("Segoe UI", 10))
output.grid_remove()

root.mainloop()
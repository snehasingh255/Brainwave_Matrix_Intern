from tkinter import *
from tkinter import messagebox as mb
import authnti
import inventory

def show_pass():
    t2.config(show='' if t2.cget('show') == '*' else '*')

def attempt_login():
    if authnti.login(t1.get(), t2.get()):
        mb.showinfo("Login", "Login Successful")
        root.destroy()
        import inventory_gui 
    else:
        mb.showerror("Login", "Invalid credentials")
        t1.delete(0, END)
        t2.delete(0, END)

root = Tk()
root.title("Inventory System Login")
root.geometry('450x450')
l1=Label(root, text="Username:",font=("Times New Roman", 12, "bold italic"))
t1=Entry(root,font=("Times New Roman", 12, "bold italic"))
l2=Label(root, text="Password:",font=("Times New Roman", 12, "bold italic"))
t2=Entry(root,font=("Times New Roman", 12, "bold italic"),show='*')
cb_show = Checkbutton(root, text="Show Password", command=show_pass)
b1=Button(root,text="Login",font=("Times New Roman", 12, "bold italic"),command=attempt_login)

root.configure(bg="#f0f4f7")

l1.grid(row=0,column=0,pady=5)
t1.grid(row=0,column=1,pady=5)
l2.grid(row=1,column=0,pady=5)
t2.grid(row=1,column=1,pady=5)
cb_show.grid(row=2, column=1, sticky='w')
b1.grid(row=3,column=0,pady=5,padx=5)

btn_style = {"font": ("Segoe UI", 10, "bold"), "bg": "#0078D7", "fg": "white", "activebackground": "#005A9E"}

root.mainloop()
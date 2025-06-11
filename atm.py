from tkinter import *
from tkinter import messagebox as mb
from datetime import datetime
from tkinter import filedialog

class ATM:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM")
        self.root.geometry('500x400')
        self.root.configure(bg="#2E3B4E") 
        self.timeout_id = None
        self.root.bind_all("<Any-KeyPress>", self.reset_timer)
        self.root.bind_all("<Button>", self.reset_timer)
        self.withdraw_attempts = 0 
        self.accounts = {
            "sneha25": {"pin": "askl5", "savings": {"balance": 5000, "transactions": [], "withdraw_limit": 50000},
                       "current": {"balance": 8000, "transactions": [], "min_balance": 1000}},
            "shubham23": {"pin": "s252", "savings": {"balance": 6000, "transactions": [], "withdraw_limit": 50000},
                       "current": {"balance": 10000, "transactions": [], "min_balance": 1000}},
        }
        self.current_account = None
        self.account_type = None
        self.pin_attempts = 0
        self.setup_ui()

    def reset_timer(self,event=None):
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)
        self.timeout_id = self.root.after(300000, self.logout) 

    def logout(self):
        self.current_account = None
        self.account_type = None
        self.pin_attempts = 0
        self.withdraw_attempts = 0
        for frame_attr in ['main_frame', 'amount_frame', 'account_frame', 'pin_frame', 'welcome_frame']:
            if hasattr(self, frame_attr):
                getattr(self, frame_attr).pack_forget()
        mb.showinfo("Session Timeout", "Session expired due to inactivity.")
        self.setup_ui()

    def setup_ui(self):
        self.welcome_frame = Frame(self.root, bg="#2E3B4E")
        self.welcome_frame.pack(pady=20)
        Label(self.welcome_frame, text="INSERT CARD", font=("Arial", 16, "bold"), fg="white", bg="#2E3B4E").pack()
        self.card_entry = Entry(self.welcome_frame, font=("Arial", 12), width=20)
        self.card_entry.pack(pady=5)
        Button(self.welcome_frame, text="Insert Card", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.validate_card).pack(pady=5)

    def validate_card(self):
        card_number = self.card_entry.get().strip()
        if not card_number:
            mb.showerror("Error", "Please enter a card number!")
            return
        if card_number in self.accounts:
            self.current_account = self.accounts[card_number]
            self.card_entry.delete(0, END)
            self.welcome_frame.pack_forget()
            self.choose_account_type()
        else:
            mb.showerror("Error", "Invalid card number!")

    def choose_account_type(self):
        self.account_frame = Frame(self.root, bg="#2E3B4E")
        self.account_frame.pack(pady=20)
        Label(self.account_frame, text="Choose Account Type", font=("Arial", 12), fg="white", bg="#2E3B4E").pack()
        Button(self.account_frame, text="Savings", font=("Arial", 12), bg="#4CAF50", fg="white", command=lambda: self.set_account_type("savings")).pack(pady=5)
        Button(self.account_frame, text="Current", font=("Arial", 12), bg="#4CAF50", fg="white", command=lambda: self.set_account_type("current")).pack(pady=5)

    def set_account_type(self, account_type):
        self.account_type = account_type
        self.account_frame.pack_forget()
        self.ask_pin()

    def ask_pin(self):
        self.pin_frame = Frame(self.root, bg="#2E3B4E")
        self.pin_frame.pack(pady=20)
        Label(self.pin_frame, text="Enter PIN:", font=("Arial", 12), fg="white", bg="#2E3B4E").pack()
        self.pin_entry = Entry(self.pin_frame, font=("Arial", 12), show="*", width=15)
        self.pin_entry.pack(pady=5)
        Button(self.pin_frame, text="Submit PIN", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.verify_pin).pack(pady=5)

    def verify_pin(self):
        user_pin = self.pin_entry.get()
        if not user_pin:
            mb.showerror("Error", "Please enter your pin!")
            return
        if user_pin == self.current_account["pin"]:
            self.pin_entry.delete(0, END)
            self.pin_attempts = 0
            self.pin_frame.pack_forget()
            self.main_screen()
        else:
            self.pin_attempts += 1
            self.pin_entry.delete(0, END)
            if self.pin_attempts >= 3:
                mb.showerror("Error", "Too many incorrect attempts. Card locked!")
                self.pin_frame.pack_forget()
                self.setup_ui()
            else:
                mb.showerror("Error", f"Incorrect PIN! Attempts left: {3 - self.pin_attempts}")

    def main_screen(self):
        self.main_frame = Frame(self.root, bg="#2E3B4E")
        self.main_frame.pack(pady=20, fill="both", expand=True)

        # Left frame for title and amount entry
        self.left_frame = Frame(self.main_frame, bg="#2E3B4E")
        self.left_frame.pack(side=LEFT, fill="both", expand=True, padx=(20, 10))

        Label(self.left_frame, text="WELCOME TO ATM", font=("Arial", 16, "bold"), fg="white", bg="#2E3B4E").pack(anchor="w", pady=(60, 10))

        # Amount entry frame inside left_frame, initially hidden
        self.amount_frame = Frame(self.left_frame, bg="#2E3B4E")
        # don't pack yet — only pack in show_entry when needed

        # Right frame for buttons
        right_frame = Frame(self.main_frame, bg="#2E3B4E")
        right_frame.pack(side=RIGHT, fill="y", padx=(10, 20))

        button_frame = Frame(right_frame, bg="#2E3B4E")
        button_frame.pack()

        Button(button_frame, text="Balance", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=self.show_balance).pack(pady=5)
        Button(button_frame, text="Deposit", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=lambda: self.show_entry('deposit')).pack(pady=5)
        Button(button_frame, text="Withdraw", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=lambda: self.show_entry('withdraw')).pack(pady=5)
        Button(button_frame, text="Transaction History", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=self.show_transactions).pack(pady=5)
        Button(button_frame, text="Download Statement", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=self.download_statement).pack(pady=5)
        Button(button_frame, text="Remove Card", font=("Arial", 12), bg="#FF0000", fg="white", width=20, command=self.remove_card).pack(pady=5)


    def show_entry(self, trans_type):
        self.transaction_type = trans_type
        for widget in self.amount_frame.winfo_children():
            widget.destroy()
        Label(self.amount_frame, text="Enter amount:", font=("Arial", 12), fg="white", bg="#2E3B4E").pack(pady=5)
        self.amount_entry = Entry(self.amount_frame, font=("Arial", 12), width=15)
        self.amount_entry.pack(pady=5)
        Button(self.amount_frame, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.process_transaction).pack(pady=5)

        # Pack amount_frame just below the title on the left side if not already packed
        if not self.amount_frame.winfo_ismapped():
            self.amount_frame.pack(pady=10, anchor="w")

    def show_transactions(self):
        transactions = self.current_account[self.account_type]["transactions"]
        if not transactions:
            mb.showinfo("Transaction History", "No transactions yet.")
            return
        formatted = "\n".join(
            f"{txn['date']} {txn['time']} - {txn['type']} ₹{txn['amount']}"
            for txn in transactions
        )
        mb.showinfo("Transaction History", formatted)

    def download_statement(self):
        transactions = self.current_account[self.account_type]["transactions"]
        if not transactions:
            mb.showerror("Error", "No transactions to save!")
            return
        bank_name = "ICICI Bank"
        branch_name = "Premier Plaza Branch, Pune"
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        
        with open(file_path, "w") as file:
            file.write(f"Bank: {bank_name}\n")
            file.write(f"Branch: {branch_name}\n")
            file.write(f"Account Type: {self.account_type.capitalize()}\n")
            file.write("Transaction History:\n")
            file.write("-" * 50 + "\n")
            file.write(f"{'Date':<12}{'Time':<10}{'Type':<10}{'Amount':>10}\n")
            file.write("-" * 50 + "\n")

            for txn in transactions:
                file.write(f"{txn['date']:<12}{txn['time']:<10}{txn['type']:<10}{txn['amount']:>10}\n")

            file.write("-" * 50 + "\n")

        mb.showinfo("Success", "Mini statement downloaded successfully.")
        
    def remove_card(self):
        self.current_account = None
        self.account_type = None
        self.pin_attempts = 0
        if hasattr(self, 'main_frame'):
            self.main_frame.pack_forget()
        if hasattr(self, 'amount_frame'):
            self.amount_frame.pack_forget()  # to Hide amount entry after card removal
        mb.showinfo("Success", "Card removed safely.\nThanks for using ICICI Bank!")
        self.setup_ui()

    def process_transaction(self):
        amount = self.get_amount()
        if amount is None or amount <= 0:
            mb.showerror("Error", "Enter a valid positive amount.")
            return

        account = self.current_account[self.account_type]
        if "transactions" not in account:
            account["transactions"] = []

        if not hasattr(self, 'transaction_type') or self.transaction_type not in ["withdraw", "deposit"]:
            mb.showerror("Error", "Invalid transaction type.")
            return

        if self.transaction_type == 'withdraw':
            if self.withdraw_attempts >= 3:
                mb.showerror("Error", "Too many failed attempts! Withdrawal locked.")
                return
            if self.account_type == "savings" and amount > account["withdraw_limit"]:
                mb.showerror("Error", f"Cannot withdraw more than ₹{account['withdraw_limit']} at once.")
                return
            if self.account_type == "current" and (account["balance"] - amount) < account["min_balance"]:
                mb.showerror("Error", "Minimum balance of ₹1000 must be maintained in the current account.")
                return
            if amount > account["balance"]:
                mb.showerror("Error", "Insufficient balance!")
                return
            
            account["balance"] -= amount
            self.withdraw_attempts = 0  
            transaction_type = "Withdraw"
        else:
            account["balance"] += amount
            transaction_type = "Deposit"

        account["transactions"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": "Withdraw" if self.transaction_type == "withdraw" else "Deposit",
            "amount": amount
        })
        mb.showinfo("Success", f"{transaction_type} of ₹{amount} completed successfully.")
        self.amount_entry.delete(0, END)
        if hasattr(self, 'amount_frame'):
            self.amount_frame.pack_forget()
            
    def get_amount(self):
        try:
            amount = int(self.amount_entry.get())
            return amount if amount > 0 else None
        except ValueError:
            mb.showerror("Error", "Enter a valid amount.")
            return None

    def show_balance(self):
        mb.showinfo("Balance Info", f"Your {self.account_type.capitalize()} account balance is ₹{self.current_account[self.account_type]['balance']}")

root = Tk()
atm = ATM(root)
root.mainloop()
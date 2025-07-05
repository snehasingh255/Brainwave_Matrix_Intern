inventory = {}
import json

def save_users(users, filename="users.json"):
    with open(filename, "w") as f:
        json.dump(users, f)

def load_users(filename="users.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def add_product(product_id, name, quantity):
    if product_id in inventory:
        return False
    inventory[product_id] = {"name": name, "quantity": quantity}
    return True 

def update_quantity(product_id, quantity):
    if product_id in inventory:
        inventory[product_id]["quantity"] = quantity
        return True
    return False

def save_inventory(filename="inventory.json"):
    with open(filename, "w") as f:
        json.dump(inventory, f)

def load_inventory(filename="inventory.json"):
    global inventory
    try:
        with open(filename, "r") as f:
            inventory = json.load(f)
    except FileNotFoundError:
        inventory = {}

def view_inventory():             #- Data persistence: Right now, the inventory lives only in memory.
    return inventory

def delete_product(product_id):          
    if product_id in inventory:
        del inventory[product_id]
        return True
    return False

def low_stock_alert(count=10):          #returns products with quantity below a threshold
    return {pid: info for pid, info in inventory.items() if info["quantity"] <  count}

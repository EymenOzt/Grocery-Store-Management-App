#-------------Developer: Ömür Eymen Öztürk---------------------------------
#-------------Developer Social Media Accounts-------------------------------
#Instagram: omureymenozt
#GitHUB:https://github.com/EymenOzt
#-----------------------------------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

#Data Files
PRODUCTS_FILE = "products.json"
SALES_FILE = "sales.json"

#Data Structures
products = []
cart = []

#Stock Update
def update_stock_window():
    selected = listbox_products.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a product to update stock.")
        return

    product_index = selected[0]
    product = products[product_index]

    window = tk.Toplevel(root)
    window.title("Update Stock")

    lbl = tk.Label(window, text=f"New stock amount for {product['name']}:")
    lbl.pack(pady=10)

    entry_stock = tk.Entry(window)
    entry_stock.pack(pady=5)
    entry_stock.insert(0, str(product["stock"]))

    def save():
        try:
            new_stock = int(entry_stock.get())
            products[product_index]["stock"] = new_stock
            save_products()
            update_product_list()
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    btn_save = tk.Button(window, text="Save", command=save)
    btn_save.pack(pady=10)

#Load Products
if os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            products = data
        else:
            products = list(data.values())

#Save Products
def save_products():
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

#Update Product List
def update_product_list():
    listbox_products.delete(0, tk.END)
    for product in products:
        listbox_products.insert(tk.END, f"{product['name']} - {product['price']} TL - Stock: {product['stock']}")

#Add Product
def add_product():
    name = entry_name.get()
    price = entry_price.get()
    discount = entry_discount.get()
    category = entry_category.get()

    try:
        price = float(price)
        discount = float(discount) if discount else 0.0
    except ValueError:
        messagebox.showerror("Error", "Price and discount must be numbers.")
        return

    price *= (1 - discount / 100)

    for product in products:
        if product["name"].lower() == name.lower():
            messagebox.showerror("Error", "This product already exists.")
            return

    new_product = {"name": name, "price": round(price, 2), "stock": 10, "category": category}
    products.append(new_product)
    save_products()
    update_product_list()

#Delete Product
def delete_product():
    selected = listbox_products.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a product to delete.")
        return
    del products[selected[0]]
    save_products()
    update_product_list()

#Update Price
def update_price():
    selected = listbox_products.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a product to update.")
        return

    try:
        new_price = float(entry_price.get())
        discount = float(entry_discount.get()) if entry_discount.get() else 0.0
    except ValueError:
        messagebox.showerror("Error", "Enter a valid price/discount.")
        return

    new_price *= (1 - discount / 100)
    products[selected[0]]["price"] = round(new_price, 2)
    save_products()
    update_product_list()

#Add to Cart
def add_to_cart():
    selected = listbox_products.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a product to add to the cart.")
        return

    try:
        quantity = int(quantity_entry.get())
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid positive quantity!")
        return

    product = products[selected[0]]

    if product["stock"] < quantity:
        messagebox.showerror("Stock Error", f"Only {product['stock']} available in stock!")
        return

    product["stock"] -= quantity
    for _ in range(quantity):
        cart.append(product)

    update_product_list()
    update_cart()

#Remove from Cart
def remove_from_cart():
    selected = listbox_cart.curselection()
    if not selected:
        return
    product = cart[selected[0]]
    product["stock"] += 1
    del cart[selected[0]]
    update_product_list()
    update_cart()

#Clear Cart
def clear_cart():
    for product in cart:
        product["stock"] += 1
    cart.clear()
    update_product_list()
    update_cart()

#Export Cart
def export_cart():
    with open("cart_output.txt", "w", encoding="utf-8") as f:
        for product in cart:
            f.write(f"{product['name']} - {product['price']} TL\n")
    messagebox.showinfo("Success", "Cart exported.")

#Complete Purchase
def complete_purchase():
    if not cart:
        messagebox.showerror("Error", "Cart is empty.")
        return

    sale = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "products": cart[:],
        "total": sum([p["price"] for p in cart])
    }

    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, "r", encoding="utf-8") as f:
            sales = json.load(f)
    else:
        sales = []

    sales.append(sale)
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=4, ensure_ascii=False)

    cart.clear()
    update_cart()
    messagebox.showinfo("Success", "Purchase completed.")

#Show Order History
def show_order_history():
    if not os.path.exists(SALES_FILE):
        messagebox.showinfo("Info", "No orders yet.")
        return

    window = tk.Toplevel(root)
    window.title("Order History")
    listbox = tk.Listbox(window, width=80)
    listbox.pack(padx=10, pady=10)

    with open(SALES_FILE, "r", encoding="utf-8") as f:
        sales = json.load(f)
        for s in sales:
            listbox.insert(tk.END, f"{s['date']} | Total: {s['total']} TL | Products: {[p['name'] for p in s['products']]}")

#Update Cart
def update_cart():
    listbox_cart.delete(0, tk.END)
    total = 0
    for product in cart:
        listbox_cart.insert(tk.END, f"{product['name']} - {product['price']} TL")
        total += product['price']
    lbl_total.config(text=f"Total: {total:.2f} TL")

#Search Product
def search_product():
    search = entry_search.get().lower()
    listbox_products.delete(0, tk.END)
    for product in products:
        if search in product['name'].lower():
            listbox_products.insert(tk.END, f"{product['name']} - {product['price']} TL - Stock: {product['stock']}")

#Graph
def sales_graph():
    if not os.path.exists(SALES_FILE):
        messagebox.showerror("Error", "No sales yet.")
        return

    with open(SALES_FILE, "r", encoding="utf-8") as f:
        sales = json.load(f)

    product_counts = {}
    for s in sales:
        for p in s['products']:
            product_counts[p['name']] = product_counts.get(p['name'], 0) + 1

    product_names = list(product_counts.keys())
    quantities = list(product_counts.values())

    plt.figure(figsize=(10,6))
    plt.bar(product_names, quantities, color="skyblue")
    plt.xlabel("Products")
    plt.ylabel("Quantity Sold")
    plt.title("Best Selling Products")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#GUI
root = tk.Tk()
root.title("Grocery Product System")
root.geometry("950x600")
root.configure(bg="#f0f0f0")

frame_left = tk.Frame(root, bg="#f0f0f0")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_right = tk.Frame(root, bg="#f0f0f0")
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

lbl_products = tk.Label(frame_left, text="Products", bg="#f0f0f0", font=("Arial", 12, "bold"))
lbl_products.pack()

listbox_products = tk.Listbox(frame_left)
listbox_products.pack(fill=tk.BOTH, expand=True)

entry_search = tk.Entry(frame_left)
entry_search.pack(pady=5, fill=tk.X)

btn_search = tk.Button(frame_left, text="Search", command=search_product, bg="#007f3f", fg="white")
btn_search.pack(pady=5, fill=tk.X)

entry_name = tk.Entry(frame_left)
entry_name.pack(pady=2, fill=tk.X)
entry_name.insert(0, "Product Name")

entry_price = tk.Entry(frame_left)
entry_price.pack(pady=2, fill=tk.X)
entry_price.insert(0, "Price")

entry_discount = tk.Entry(frame_left)
entry_discount.pack(pady=2, fill=tk.X)
entry_discount.insert(0, "Discount (%)")

entry_category = tk.Entry(frame_left)
entry_category.pack(pady=2, fill=tk.X)
entry_category.insert(0, "Category")

btn_add = tk.Button(frame_left, text="Add Product", command=add_product, bg="#5fbf00", fg="white")
btn_add.pack(pady=5, fill=tk.X)

btn_delete = tk.Button(frame_left, text="Delete Product", command=delete_product, bg="#ff0000", fg="white")
btn_delete.pack(pady=5, fill=tk.X)

btn_update_stock = tk.Button(frame_left, text="Update Stock", command=update_stock_window, bg="#2626ff", fg="white")
btn_update_stock.pack(pady=5, fill=tk.X)

btn_update_price = tk.Button(frame_left, text="Update Price & Discount", command=update_price, bg="#007fff", fg="white")
btn_update_price.pack(pady=5, fill=tk.X)

lbl_cart = tk.Label(frame_right, text="Cart", bg="#f0f0f0", font=("Arial", 12, "bold"))
lbl_cart.pack()

listbox_cart = tk.Listbox(frame_right)
listbox_cart.pack(fill=tk.BOTH, expand=True)

lbl_total = tk.Label(frame_right, text="Total: 0 TL", bg="#f0f0f0", font=("Arial", 14, "bold"))
lbl_total.pack(pady=5)

btn_add_cart = tk.Button(frame_right, text="Add to Cart", command=add_to_cart, bg="#5fbf00", fg="white")
btn_add_cart.pack(pady=5, fill=tk.X)

btn_remove_cart = tk.Button(frame_right, text="Remove from Cart", command=remove_from_cart, bg="#e50909", fg="white")
btn_remove_cart.pack(pady=5, fill=tk.X)

btn_clear_cart = tk.Button(frame_right, text="Clear Cart", command=clear_cart, bg="#ff0000", fg="white")
btn_clear_cart.pack(pady=5, fill=tk.X)

btn_export_cart = tk.Button(frame_right, text="Export Cart", command=export_cart, bg="#007fff", fg="white")
btn_export_cart.pack(pady=5, fill=tk.X)

btn_complete_purchase = tk.Button(frame_right, text="Complete Purchase", command=complete_purchase, bg="#3232bc", fg="white")
btn_complete_purchase.pack(pady=5, fill=tk.X)

btn_order_history = tk.Button(root, text="Order History", command=show_order_history, bg="#007fff", fg="white")
btn_order_history.pack(pady=5)

btn_sales_graph = tk.Button(root, text="Sales Graph", command=sales_graph, bg="#007f3f", fg="white")
btn_sales_graph.pack(pady=5)

quantity_frame = tk.Frame(frame_right, bg="#f0f0f0")
quantity_frame.pack(pady=10)

quantity_label = tk.Label(quantity_frame, text="Quantity:", bg="#f0f0f0", font=("Arial", 10))
quantity_label.pack(side=tk.LEFT)

quantity_entry = tk.Entry(quantity_frame, width=5)
quantity_entry.insert(0, "1")
quantity_entry.pack(side=tk.LEFT, padx=5)

quantity_frame.pack_configure(anchor='center')

update_product_list()
root.mainloop()

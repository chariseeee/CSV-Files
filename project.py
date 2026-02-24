import csv

system = {}

# LOAD FROM CSV
def load_from_csv():
    try:
        with open("inventory.csv", "r") as file:
            reader = csv.DictReader(file)
            system.clear()

            for row in reader:
                system[row["name"]] = {
                    "category": row["category"],
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"]),
                    "reorder_level": int(row["reorder_level"])
                }

        print("Inventory loaded from CSV.")

    except FileNotFoundError:   
        print("No CSV file found. Starting with empty inventory.")


# SAVE TO CSV
def save_to_csv():
    with open("inventory.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "category", "quantity", "price", "reorder_level"])

        for name, data in system.items():
            writer.writerow([
                name,
                data["category"],
                data["quantity"],
                data["price"],
                data["reorder_level"]
            ])

    print("Inventory saved to CSV.")


# INPUT HELPERS
def get_int(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("Invalid input. Enter a whole number.")


def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            print("Enter positive number.")
        except ValueError:
            print("Invalid input. Enter a valid price.")


# ADD ITEM
def add_item():
    name = input("Item Name: ").strip()

    if name in system:
        print("Item already exists.")
        choice = input("Do you want to update it? (yes/no): ").lower()
        if choice != "yes":
            return

    category = input("Category: ").strip()
    quantity = get_int("Quantity: ")
    price = get_float("Unit Price: ")
    reorder_level = get_int("Reorder Level: ")

    system[name] = {
        "category": category,
        "quantity": quantity,
        "price": price,
        "reorder_level": reorder_level
    }

    print("Item added/updated successfully.")


# VIEW INVENTORY
def view_inventory():

    if not system:
        print("Inventory empty.")
        return

    print("""
What do you want to view?

1. quantity
2. price
3. category
4. reorder_level
""")

    choice = input("Enter choice: ").strip()

    mapping = {
        "1": "quantity",
        "2": "price",
        "3": "category",
        "4": "reorder_level"
    }

    if choice not in mapping:
        print("Invalid choice.")
        return

    field = mapping[choice]

    print(f"\n{field.upper()}")
    print("-" * 25)

    for name, data in system.items():
        print(f"{name}: {data[field]}")

# UPDATE STOCK
def update_stock():
    name = input("Enter item name: ")

    if name not in system:
        print("Item not found.")
        return

    quantity = get_int("Enter new quantity: ")
    system[name]["quantity"] = quantity

    print("Stock updated.")

    if quantity <= system[name]["reorder_level"]:
        print(f"LOW STOCK ALERT: {name} is below reorder level!")


# FILTER CATEGORY
def view_stock_by_category():
    category = input("Enter category: ").lower()
    found = False

    for name, data in system.items():
        if data["category"].lower() == category:
            print(name, data)
            found = True

    if not found:
        print("No items found.")


# FILTER LOW STOCK
def view_stock_to_reorder():
    found = False

    for name, data in system.items():
        if data["quantity"] <= data["reorder_level"]:
            print(name, data)
            found = True

    if not found:
        print("No items need reorder.")


# EXIT
def exit_program():
    choice = input("Save before exiting? (yes/no): ").lower()
    if choice == "yes":
        save_to_csv()

    print("Goodbye.")
    exit()


# MAIN PROGRAM
load_from_csv()

while True:
    print("""
=== Trojan Construction Shop Inventory Tracker ===

1. Add New Item
2. View Inventory
3. Update Stock
4. Filter by Category
5. Filter Stock to Reorder
6. Save to CSV
7. Load from CSV
8. Exit
""")

    choice = input("Enter choice: ")

    if choice == "1":
        add_item()
    elif choice == "2":
        view_inventory()
    elif choice == "3":
        update_stock()
    elif choice == "4":
        view_stock_by_category()
    elif choice == "5":
        view_stock_to_reorder()
    elif choice == "6":
        save_to_csv()
    elif choice == "7":
        load_from_csv()
    elif choice == "8":
        exit_program()
    else:
        print("Invalid choice.")
import csv

system = {} # for dictionary

# LOAD FROM CSV
def load_from_csv():
    try: # run the code then except if  error
        with open("inventory.csv", "r") as file: # close after use, r = read, save as file
            reader = csv.DictReader(file)
            system.clear() # refresh your old data

            for row in reader: # row means horizontal output
                system[row["Item"]] = {
                    "Category": row["Category"],
                    "Quantity": int(row["Quantity"]),
                    "Unit Price": float(row["Unit Price"]),
                    "Reorder Level": int(row["Reorder Level"])
                }

        print("Inventory loaded from CSV.")

    except FileNotFoundError:   
        print("No CSV file found. Starting with empty inventory.")


# SAVE TO CSV
def save_to_csv():
    with open("inventory.csv", "w", newline="") as file: # newline for no extra bottom space, w = write
        writer = csv.writer(file) # write in csv format
        writer.writerow(["Item", "Category", "Quantity", "Unit Price", "Reorder Level"])
# header, row format, and converted to string

        for name, data in system.items():
            writer.writerow([
                name,
                data["Category"],
                data["Quantity"],
                data["Unit Price"],
                data["Reorder Level"]
            ])

    print("Saving inventory to inventory.csv... Done!")


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
    name = input("Item Name: ").strip() # remove spaces

    if name in system: # checks if value exitsts
        print("Item already exists.")
        choice = input("Do you want to update it? (y/n): ").lower()
        if choice != "y":
            return

    category = input("Category: ").strip()
    quantity = get_int("Quantity: ") # para whole number lang
    price = get_float("Unit Price: ") # para decimal or positive number lang
    reorder_level = get_int("Reorder Level: ")

    system[name] = {
        "Category": category,
        "Quantity": quantity,
        "Unit Price": price,
        "Reorder Level": reorder_level
    }

    print("Item added/updated successfully.")


# VIEW INVENTORY
red = "\033[0;31m" # ASNI colors
default = "\033[0m"

def view_inventory():

    if not system: # if there are none found
        print("Inventory empty.")
        return

    # HEADERS
    # {value:number} number = no. of spaces
    print(red + f"{'Item Name':<30}{'Category':<25}" # <>^ = align right, left, center
          f"{'Quantity':>12}{'Unit Price':>15}{'Reorder Level':>15}" + default)
    print("_" * 100)

    # KEY VALUES
    for name, data in system.items():
        print(f"{name:<30}{data['Category']:<25}"
              f"{data['Quantity']:>12}{data['Unit Price']:>15}{data['Reorder Level']:>15}")


    print("""
Enter your choice:

1. Quantity
2. Unit Price
3. Category
""")

    choice = input("Enter choice: ").strip()

    sorting = {
        "1": "Quantity",
        "2": "Unit Price",
        "3": "Category",
    }

    if choice not in sorting:
        print("Invalid choice.")
        return

    table = sorting[choice]

    print(f"\n{table.upper()}") # \n means proceed to next code bago print
    print("_" * 50 ) # multiply dash

    for name, data in system.items(): # outline ng table
        print(f"{name}: {data[table]}") 

# UPDATE STOCK
def update_stock():
    name = input("Enter item name: ")

    if name not in system:
        print("Item not found.")
        return

    quantity = get_int("Enter new quantity: ")
    system[name]["Quantity"] = quantity # item input checks dict on key quantity

    print("Stock updated.")

    if quantity <= system[name]["Reorder Level"]:
        print(f"LOW STOCK ALERT: {name} is below reorder level!")


# FILTER CATEGORY / LOW STOCK
def filter_option():
    print("""
    1. Filter by Category
    2. Filter by Low Stock
    """)

    option = input("Enter choice: ").strip()


    if option == "1":
        view_stock_by_category()
    elif option == "2":
        view_stock_to_reorder()
    else:
        print("Invalid choice.")

def view_stock_by_category():
    category = input("Enter category: ").lower()
    check = False # boolean variable t/f

    for name, data in system.items():
        if data["Category"].lower() == category:
            print(name, data)
            check = True

    if not check:
        print("No items found.")


# FILTER LOW STOCK
def view_stock_to_reorder():
    check = False

    for name, data in system.items():
        if data["Quantity"] <= data["Reorder Level"]:
            print(name, data)
            check = True

    if not check:
        print("No items need reorder.")


# EXIT
def exit_program():
    choice = input("Save before exiting? (y/n): ").lower()
    if choice == "y":
        save_to_csv()

    print("Goodbye.")


# MAIN PROGRAM
load_from_csv()

purple = "\033[1;35m"
default = "\033[0m"

while True:
    print(purple + """
=== Trojan Construction Shop Inventory Tracker ===

1. Add New Item
2. View Inventory
3. Update Stock
4. Filter by Category / Low Stock
5. Save to CSV
6. Load from CSV
7. Exit
""" + default)

    choice = input("Enter choice: ")

    if choice == "1":
        add_item()
    elif choice == "2":
        view_inventory()
    elif choice == "3":
        update_stock()
    elif choice == "4":
        filter_option()
    elif choice == "5":
        save_to_csv()
    elif choice == "6":
        load_from_csv()
    elif choice == "7":
        exit_program()
        break
    else:
        print("Invalid choice.")

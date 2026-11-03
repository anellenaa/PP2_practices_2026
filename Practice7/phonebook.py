import csv
from connect import connect


# 1. Create the table
def create_table():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE
            )
        """)
        conn.commit()
        print("Table is ready.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 2. Insert data from a CSV file
def insert_from_csv():
    filename = input("CSV file name (press Enter for contacts.csv): ")
    if filename == "":
        filename = "contacts.csv"

    conn = connect()
    cur = conn.cursor()
    try:
        file = open(filename, "r")
        reader = csv.reader(file)
        next(reader)  # skip the first line (column names)

        count = 0
        for row in reader:
            name = row[0]
            phone = row[1]
            # if the phone already exists, skip this row
            cur.execute(
                "INSERT INTO contacts (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (name, phone)
            )
            count = count + cur.rowcount
        file.close()

        conn.commit()
        print(count, "contacts added from the file.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 3. Insert data from the console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact added.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 4. Update a contact (first name or phone)
def update_contact():
    print("1 - change name")
    print("2 - change phone")
    choice = input("Your choice: ")

    conn = connect()
    cur = conn.cursor()
    try:
        if choice == "1":
            phone = input("Enter the phone of the contact: ")
            new_name = input("Enter new name: ")
            cur.execute(
                "UPDATE contacts SET first_name = %s WHERE phone = %s",
                (new_name, phone)
            )
        elif choice == "2":
            name = input("Enter the name of the contact: ")
            new_phone = input("Enter new phone: ")
            cur.execute(
                "UPDATE contacts SET phone = %s WHERE first_name = %s",
                (new_phone, name)
            )
        else:
            print("Wrong choice.")
            return

        conn.commit()
        if cur.rowcount == 0:
            print("Contact not found.")
        else:
            print("Contact updated.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 5. Query contacts with different filters
def search_contacts():
    print("1 - show all contacts")
    print("2 - search by name")
    print("3 - search by phone prefix")
    choice = input("Your choice: ")

    conn = connect()
    cur = conn.cursor()
    try:
        if choice == "1":
            cur.execute("SELECT id, first_name, phone FROM contacts ORDER BY id")
        elif choice == "2":
            name = input("Enter name (or a part of it): ")
            cur.execute(
                "SELECT id, first_name, phone FROM contacts WHERE first_name ILIKE %s",
                ("%" + name + "%",)
            )
        elif choice == "3":
            prefix = input("Enter the beginning of the phone: ")
            cur.execute(
                "SELECT id, first_name, phone FROM contacts WHERE phone LIKE %s",
                (prefix + "%",)
            )
        else:
            print("Wrong choice.")
            return

        rows = cur.fetchall()
        if len(rows) == 0:
            print("Nothing found.")
        else:
            for row in rows:
                print(row[0], row[1], row[2])
    except Exception as error:
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 6. Delete a contact by name or phone
def delete_contact():
    print("1 - delete by name")
    print("2 - delete by phone")
    choice = input("Your choice: ")

    conn = connect()
    cur = conn.cursor()
    try:
        if choice == "1":
            name = input("Enter name: ")
            cur.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
        elif choice == "2":
            phone = input("Enter phone: ")
            cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
        else:
            print("Wrong choice.")
            return

        conn.commit()
        print(cur.rowcount, "contact(s) deleted.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# Main menu
def main():
    create_table()

    while True:
        print()
        print("===== PhoneBook =====")
        print("1. Insert from CSV file")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("0. Exit")
        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Wrong choice, try again.")


main()
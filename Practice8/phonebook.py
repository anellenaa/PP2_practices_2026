from connect import connect


# Load functions.sql and procedures.sql into the database
def load_sql_files():
    conn = connect()
    cur = conn.cursor()
    try:
        for filename in ["functions.sql", "procedures.sql"]:
            file = open(filename, "r", encoding="utf-8")
            cur.execute(file.read())
            file.close()
        conn.commit()
        print("Functions and procedures are ready.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 1. Search by pattern (function)
def search_by_pattern():
    pattern = input("Enter a part of name or phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
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


# 2. Insert or update one contact (procedure)
def upsert_one():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print("Done.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 3. Insert many contacts (procedure with a loop and validation)
def insert_many():
    names = []
    phones = []
    while True:
        name = input("Name (press Enter to finish): ")
        if name == "":
            break
        names.append(name)
        phones.append(input("Phone: "))
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_many_contacts(%s::text[], %s::text[], %s::text[])",
            (names, phones, [])
        )
        bad_data = cur.fetchone()[0]
        conn.commit()
        if bad_data:
            print("Incorrect data:")
            for item in bad_data:
                print(" -", item)
        else:
            print("All contacts were added.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# 4. Pagination (function)
def show_page():
    limit = int(input("Limit (rows per page): "))
    offset = int(input("Offset (rows to skip): "))
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
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


# 5. Delete by name or phone (procedure)
def delete_one():
    value = input("Enter name or phone to delete: ")
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Done.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# Main menu
def main():
    load_sql_files()
    while True:
        print()
        print("===== PhoneBook (Practice 8) =====")
        print("1. Search by pattern")
        print("2. Insert or update one contact")
        print("3. Insert many contacts")
        print("4. Show contacts by pages")
        print("5. Delete contact")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == "1":
            search_by_pattern()
        elif choice == "2":
            upsert_one()
        elif choice == "3":
            insert_many()
        elif choice == "4":
            show_page()
        elif choice == "5":
            delete_one()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Wrong choice, try again.")


main()
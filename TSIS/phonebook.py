import csv
import json
import os
from connect import connect

FOLDER = os.path.dirname(os.path.abspath(__file__))
PHONE_TYPES = ["home", "work", "mobile"]

# Allowed sort options (only these strings go into ORDER BY)
SORTS = {
    "1": "c.first_name",
    "2": "c.birthday NULLS LAST",
    "3": "c.created_at",
}

# One query to show contacts with group and ALL phones
LIST_SQL = """
    SELECT c.id, c.first_name, c.email, c.birthday, g.name,
           COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '-')
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    {where}
    GROUP BY c.id, c.first_name, c.email, c.birthday, c.created_at, g.name
    ORDER BY {order}
"""


# Load schema.sql and procedures.sql into the database
def load_sql_files():
    conn = connect()
    cur = conn.cursor()
    try:
        for filename in ["schema.sql", "procedures.sql"]:
            file = open(os.path.join(FOLDER, filename), "r", encoding="utf-8")
            cur.execute(file.read())
            file.close()
        conn.commit()
        print("Database is ready.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


def print_contacts(rows):
    if len(rows) == 0:
        print("Nothing found.")
        return
    for r in rows:
        print(f"{r[1]} | email: {r[2] or '-'} | birthday: {r[3] or '-'} "
              f"| group: {r[4] or '-'} | phones: {r[5]}")


def ask_phone_type():
    t = input("Phone type (home / work / mobile, Enter = mobile): ").strip().lower()
    if t == "":
        return "mobile"
    if t not in PHONE_TYPES:
        print("Wrong type, 'mobile' will be used.")
        return "mobile"
    return t


def choose_sort():
    print("Sort by: 1 - name, 2 - birthday, 3 - date added")
    return SORTS.get(input("Your choice: ").strip(), "c.first_name")


# Find the group id by name (creates the group if it does not exist)
def get_group_id(cur, group_name):
    if not group_name:
        return None
    group_name = group_name.strip().capitalize()
    cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (group_name,))
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


# Insert one contact and its first phone. Returns the contact id.
# update_existing=False: if the phone already exists -> return None
# update_existing=True : if the phone already exists -> update email/birthday/group
def insert_contact(cur, name, phone, email, birthday, group, phone_type,
                   update_existing=False):
    group_id = get_group_id(cur, group)
    if update_existing:
        conflict = ("ON CONFLICT (phone) DO UPDATE SET email = EXCLUDED.email, "
                    "birthday = EXCLUDED.birthday, group_id = EXCLUDED.group_id")
    else:
        conflict = "ON CONFLICT (phone) DO NOTHING"
    cur.execute(
        "INSERT INTO contacts (first_name, phone, email, birthday, group_id) "
        "VALUES (%s, %s, %s, %s, %s) " + conflict + " RETURNING id",
        (name, phone, email or None, birthday or None, group_id)
    )
    row = cur.fetchone()
    if row is None:
        return None
    cur.execute(
        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s) "
        "ON CONFLICT (contact_id, phone) DO NOTHING",
        (row[0], phone, phone_type)
    )
    return row[0]


# ---------- 3.2 console search, filter, sort, pages ----------

def run_list(where, params, order):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(LIST_SQL.format(where=where, order=order), params)
        print_contacts(cur.fetchall())
    except Exception as error:
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


def show_all():
    run_list("", (), choose_sort())


def filter_by_group():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM groups ORDER BY name")
        print("Groups:", ", ".join(r[0] for r in cur.fetchall()))
    finally:
        cur.close()
        conn.close()
    group = input("Enter group name: ").strip()
    run_list("WHERE g.name ILIKE %s", (group,), choose_sort())


def search_by_email():
    part = input("Enter a part of email (for example gmail): ").strip()
    run_list("WHERE c.email ILIKE %s", ("%" + part + "%",), choose_sort())


# Search by name / email / any phone (DB function search_contacts)
def search_all_fields():
    q = input("Enter text (name, email or phone): ").strip()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (q,))
        print_contacts(cur.fetchall())
    except Exception as error:
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# Pages with next / prev / quit (uses the DB function from Practice 8)
def browse_pages():
    try:
        limit = int(input("Rows per page (Enter = 3): ") or "3")
    except ValueError:
        print("Please enter a number.")
        return
    if limit < 1:
        print("Rows per page must be at least 1.")
        return

    offset = 0
    conn = connect()
    cur = conn.cursor()
    try:
        while True:
            cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            if len(rows) == 0 and offset > 0:
                print("This is the last page.")
                offset = offset - limit
                continue
            print("--- Page", offset // limit + 1, "---")
            if len(rows) == 0:
                print("Nothing found.")
            for row in rows:
                print(row[0], row[1], row[2])

            command = input("next / prev / quit: ").strip().lower()
            if command == "next":
                offset = offset + limit
            elif command == "prev":
                offset = max(0, offset - limit)
            elif command == "quit":
                break
            else:
                print("Please type next, prev or quit.")
    except Exception as error:
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# ---------- adding and changing contacts ----------

def insert_from_console():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    if name == "" or phone == "":
        print("Name and phone are required.")
        return
    phone_type = ask_phone_type()
    email = input("Enter email (or Enter to skip): ").strip()
    birthday = input("Enter birthday YYYY-MM-DD (or Enter to skip): ").strip()
    group = input("Enter group Family/Work/Friend/Other (or Enter to skip): ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        contact_id = insert_contact(cur, name, phone, email, birthday, group, phone_type)
        if contact_id is None:
            print("This phone already exists.")
        else:
            print("Contact added.")
        conn.commit()
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# Procedure add_phone
def add_phone():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = ask_phone_type()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# Procedure move_to_group
def move_to_group():
    name = input("Contact name: ").strip()
    group = input("Group name: ").strip().capitalize()
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Contact moved.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


# Procedure delete_contact (from Practice 8)
def delete_one():
    value = input("Enter name or phone to delete: ").strip()
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


# ---------- 3.3 import / export ----------

# CSV columns: first_name, phone, email, birthday, group, phone_type
def insert_from_csv():
    filename = input("CSV file name (press Enter for contacts.csv): ").strip()
    if filename == "":
        filename = "contacts.csv"

    conn = connect()
    cur = conn.cursor()
    try:
        file = open(filename, "r", encoding="utf-8-sig")
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            name = (row.get("first_name") or "").strip()
            phone = (row.get("phone") or "").strip()
            if name == "" or phone == "":
                continue
            phone_type = (row.get("phone_type") or "mobile").strip().lower()
            if phone_type not in PHONE_TYPES:
                phone_type = "mobile"
            insert_contact(
                cur, name, phone,
                (row.get("email") or "").strip(),
                (row.get("birthday") or "").strip(),
                (row.get("group") or "").strip(),
                phone_type,
                update_existing=True
            )
            count = count + 1
        file.close()
        conn.commit()
        print(count, "contacts processed from the file.")
    except Exception as error:
        conn.rollback()
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


def export_to_json():
    filename = input("JSON file name (Enter = contacts.json): ").strip()
    if filename == "":
        filename = "contacts.json"

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.id, c.first_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.id
        """)
        contacts = cur.fetchall()

        data = []
        for c in contacts:
            cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
                        (c[0],))
            phones = []
            for p in cur.fetchall():
                phones.append({"phone": p[0], "type": p[1]})
            data.append({
                "name": c[1],
                "email": c[2],
                "birthday": str(c[3]) if c[3] else None,
                "group": c[4],
                "phones": phones
            })

        file = open(filename, "w", encoding="utf-8")
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.close()
        print(len(data), "contacts exported to", filename)
    except Exception as error:
        print("Error:", error)
    finally:
        cur.close()
        conn.close()


def import_from_json():
    filename = input("JSON file name (Enter = contacts.json): ").strip()
    if filename == "":
        filename = "contacts.json"

    try:
        file = open(filename, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
    except Exception as error:
        print("Error:", error)
        return

    conn = connect()
    cur = conn.cursor()
    added = 0
    overwritten = 0
    skipped = 0
    for item in data:
        try:
            name = item.get("name")
            phones = item.get("phones") or []
            if not name or len(phones) == 0:
                print("Skipped (no name or no phones):", name)
                skipped = skipped + 1
                continue

            email = item.get("email")
            birthday = item.get("birthday")
            group = item.get("group")

            cur.execute("SELECT id FROM contacts WHERE first_name = %s", (name,))
            existing = cur.fetchone()

            if existing:
                answer = input(f"'{name}' already exists. skip or overwrite? ").strip().lower()
                if answer != "overwrite":
                    skipped = skipped + 1
                    continue
                contact_id = existing[0]
                cur.execute(
                    "UPDATE contacts SET email = %s, birthday = %s, group_id = %s, phone = %s "
                    "WHERE id = %s",
                    (email, birthday, get_group_id(cur, group), phones[0]["phone"], contact_id)
                )
                cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
                overwritten = overwritten + 1
            else:
                contact_id = insert_contact(
                    cur, name, phones[0]["phone"], email, birthday, group,
                    phones[0].get("type", "mobile")
                )
                if contact_id is None:
                    print(f"Skipped '{name}': phone {phones[0]['phone']} already belongs to another contact.")
                    skipped = skipped + 1
                    continue
                added = added + 1

            # add all phones of the contact
            for p in phones:
                phone_type = p.get("type", "mobile")
                if phone_type not in PHONE_TYPES:
                    phone_type = "mobile"
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s) "
                    "ON CONFLICT (contact_id, phone) DO NOTHING",
                    (contact_id, p["phone"], phone_type)
                )
            conn.commit()
        except Exception as error:
            conn.rollback()
            print(f"Error with '{item.get('name')}':", error)
            skipped = skipped + 1

    cur.close()
    conn.close()
    print(f"Import finished: {added} added, {overwritten} overwritten, {skipped} skipped.")


# ---------- main menu ----------

def main():
    load_sql_files()

    while True:
        print()
        print("===== PhoneBook (TSIS 1) =====")
        print("1. Insert from CSV file")
        print("2. Insert from console")
        print("3. Add phone to a contact")
        print("4. Move contact to a group")
        print("5. Search (name / email / any phone)")
        print("6. Filter by group")
        print("7. Search by email")
        print("8. Show all contacts (sorted)")
        print("9. Show contacts by pages")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Delete contact")
        print("0. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            add_phone()
        elif choice == "4":
            move_to_group()
        elif choice == "5":
            search_all_fields()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            show_all()
        elif choice == "9":
            browse_pages()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            delete_one()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Wrong choice, try again.")


main()
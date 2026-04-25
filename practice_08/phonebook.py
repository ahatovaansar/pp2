from connect import conn, cur


def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Done")


def search():
    pattern = input("Search: ")

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    if not rows:
        print("No results")
    else:
        for row in rows:
            print(row)


def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)


def delete():
    value = input("Enter name or phone: ")

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    print("Deleted")


def menu():
    while True:
        print("\n=== PHONEBOOK ===")
        print("1. Add/Update")
        print("2. Search")
        print("3. Pagination")
        print("4. Delete")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            search()
        elif choice == "3":
            pagination()
        elif choice == "4":
            delete()
        elif choice == "5":
            break
        else:
            print("Invalid")


menu()

cur.close()
conn.close()
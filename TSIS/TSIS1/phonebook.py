import psycopg2
from connect import connect
import json


# =========================
# EXPORT JSON
# =========================
def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    data = {}

    for name, email, birthday, group, phone, p_type in rows:
        if name not in data:
            data[name] = {
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group,
                "phones": []
            }

        if phone:
            data[name]["phones"].append({
                "number": phone,
                "type": p_type
            })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(list(data.values()), f, indent=4)

    conn.close()
    print("Exported to contacts.json!")


# =========================
# IMPORT JSON
# =========================
def import_json():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for contact in data:
        name = contact.get("name")
        email = contact.get("email")

        if not name:
            continue

        # ✅ проверка дублей (ВАЖНО)
        cur.execute(
            "SELECT id FROM contacts WHERE name=%s OR email=%s",
            (name, email)
        )
        existing = cur.fetchone()

        if existing:
            contact_id = existing[0]
        else:
            cur.execute(
                "INSERT INTO contacts(name, email) VALUES (%s, %s) RETURNING id",
                (name, email)
            )
            contact_id = cur.fetchone()[0]

        # группа
        if contact.get("group"):
            cur.execute("SELECT id FROM groups WHERE name=%s", (contact["group"],))
            g = cur.fetchone()

            if not g:
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                    (contact["group"],)
                )
                group_id = cur.fetchone()[0]
            else:
                group_id = g[0]

            cur.execute(
                "UPDATE contacts SET group_id=%s WHERE id=%s",
                (group_id, contact_id)
            )

        # телефоны
        for phone in contact.get("phones", []):
            cur.execute(
                "SELECT 1 FROM phones WHERE contact_id=%s AND phone=%s",
                (contact_id, phone["number"])
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, phone["number"], phone["type"])
                )

    conn.commit()
    conn.close()
    print("Imported from contacts.json!")


# =========================
# ADD CONTACT
# =========================
def add_contact():
    conn = connect()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")

    cur.execute(
        "INSERT INTO contacts(name, email) VALUES (%s, %s)",
        (name, email)
    )

    conn.commit()
    conn.close()
    print("Contact added!")


# =========================
# ADD PHONE
# =========================
def add_phone():
    conn = connect()
    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("Phone: ")
    p_type = input("Type (home/work/mobile): ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))

    conn.commit()
    conn.close()


# =========================
# SHOW CONTACTS
# =========================
def show_contacts():
    conn = connect()
    cur = conn.cursor()

    sort = input("Sort by (name/birthday/date): ")

    if sort == "name":
        order = "c.name"
    elif sort == "birthday":
        order = "c.birthday"
    else:
        order = "c.created_at"

    cur.execute(f"""
        SELECT c.name, p.phone, c.email
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY {order}
    """)

    for row in cur.fetchall():
        print(row)

    conn.close()


# =========================
# PAGINATION
# =========================
def paginate():
    conn = connect()
    cur = conn.cursor()

    limit = 2
    offset = 0

    while True:
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        rows = cur.fetchall()

        for row in rows:
            print(row)

        action = input("next / prev / quit: ")

        if action == "next":
            offset += limit
        elif action == "prev":
            offset = max(0, offset - limit)
        else:
            break

    conn.close()


# =========================
# SEARCH
# =========================
def search():
    conn = connect()
    cur = conn.cursor()

    query = input("Search: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))

    for row in cur.fetchall():
        print(row)

    conn.close()


# =========================
# MOVE GROUP
# =========================
def move_group():
    conn = connect()
    cur = conn.cursor()

    name = input("Contact name: ")
    group = input("Group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    conn.close()


# =========================
# FILTER
# =========================
def filter_by_group():
    conn = connect()
    cur = conn.cursor()

    group = input("Group: ")

    cur.execute("""
        SELECT c.name, p.phone, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    conn.close()


# =========================
# DELETE
# =========================
def delete_contact():
    conn = connect()
    cur = conn.cursor()

    name = input("Name: ")

    cur.execute("CALL delete_contact(%s)", (name,))

    conn.commit()
    conn.close()


# =========================
# MENU
# =========================
while True:
    print("\n=== TSIS1 PHONEBOOK ===")
    print("1. Add contact")
    print("2. Add phone")
    print("3. Show contacts")
    print("4. Search")
    print("5. Move to group")
    print("6. Delete")
    print("7. Export JSON")
    print("8. Import JSON")
    print("9. Filter by group")
    print("10. Pagination")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        add_phone()
    elif choice == "3":
        show_contacts()
    elif choice == "4":
        search()
    elif choice == "5":
        move_group()
    elif choice == "6":
        delete_contact()
    elif choice == "7":
        export_json()
    elif choice == "8":
        import_json()
    elif choice == "9":
        filter_by_group()
    elif choice == "10":
        paginate()
    elif choice == "0":
        break
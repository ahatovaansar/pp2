import psycopg2
from connect import connect

def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added!")





def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Updated!")


def delete_contact(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!") 

def search_contact(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name=%s",
        (name,)
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def search_by_phone_prefix(prefix):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

import csv

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported!") 


while True:
    print("\n1. Add contact")
    print("2. Show contacts")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Import from CSV")
    print("6. Search contact")
    print("7. Search by phone prefix")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        add_contact(name, phone)

    elif choice == "2":
        show_contacts()

    elif choice == "3":
        name = input("Name: ").strip()
        phone = input("New phone: ").strip()
        update_contact(name, phone)

    elif choice == "4":
        name = input("Name: ").strip()
        delete_contact(name)
    
    elif choice == "5":
        insert_from_csv("contacts.csv")
    
    elif choice == "6":
         name = input("Enter name: ").strip()
         search_contact(name)
    
    elif choice == "7":
        prefix = input("Enter phone prefix: ").strip()
        search_by_phone_prefix(prefix)

    elif choice == "0":
        break



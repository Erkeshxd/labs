import psycopg2
from config import config

# Function to insert a person's details into the database
def insert_people(name, surname, phone):
    # SQL query to insert a new person into the PhoneBook table, 
    # but ignore duplicate entries with the same name, surname, and phone
    sql = "INSERT INTO PhoneBook(Name, Surname, Phone) VALUES(%s, %s, %s) ON CONFLICT (Name, Surname, Phone) DO NOTHING"
    conn = None
    try:
        # Fetch database connection parameters from the config function
        params = config()
        conn = psycopg2.connect(**params)  # Establish connection
        cur = conn.cursor()  # Create a cursor to execute SQL queries
        # Execute the insert query with the provided name, surname, and phone
        cur.executemany(sql, [(name, surname, phone)])
        conn.commit()  # Commit the transaction to save changes
        cur.close()  # Close the cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any error that occurs
    finally:
        # Ensure the connection is closed, even if an error occurs
        if conn is not None:
            conn.close()

# Function to upload contact details from a CSV file
def upload_from_csv():
    import csv
    # Open the CSV file for reading
    with open('contact.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Read the CSV as a dictionary
        for row in reader:  # Loop through each row in the CSV
            # Extract name, surname, and phone from the row
            name = row['name']
            surname = row['surname']
            phone = row['phone']
            # Call the insert_people function to insert each contact into the database
            insert_people(name, surname, phone)

# Function to delete a person from the database based on name and surname
def delete_person(name, surname):
    # SQL query to delete a person based on their name and surname
    sql = "DELETE FROM PhoneBook WHERE Name = %s AND Surname = %s"
    conn = None
    try:
        params = config()  # Fetch database connection parameters
        conn = psycopg2.connect(**params)  # Establish connection
        cur = conn.cursor()  # Create a cursor to execute SQL queries
        # Execute the delete query with the provided name and surname
        cur.execute(sql, (name, surname))
        conn.commit()  # Commit the transaction
        cur.close()  # Close the cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any error that occurs
    finally:
        # Ensure the connection is closed
        if conn is not None:
            conn.close()

# Function to update a person's name in the database
def update_name(old_name, surname, new_name):
    # SQL query to update the name of a person with a given surname
    sql = "UPDATE Phonebook SET Name = %s WHERE Name = %s AND Surname = %s"
    conn = None
    try:
        params = config()  # Fetch database connection parameters
        conn = psycopg2.connect(**params)  # Establish connection
        cur = conn.cursor()  # Create a cursor to execute SQL queries
        # Execute the update query with the old name, surname, and new name
        cur.execute(sql, (new_name, old_name, surname))
        conn.commit()  # Commit the transaction
        cur.close()  # Close the cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any error that occurs
    finally:
        # Ensure the connection is closed
        if conn is not None:
            conn.close()

# Function to update a person's surname in the database
def update_surname(name, old_surname, new_surname):
    # SQL query to update the surname of a person with a given name
    sql = "UPDATE Phonebook SET Surname = %s WHERE Name = %s AND Surname = %s"
    conn = None
    try:
        params = config()  # Fetch database connection parameters
        conn = psycopg2.connect(**params)  # Establish connection
        cur = conn.cursor()  # Create a cursor to execute SQL queries
        # Execute the update query with the name, old surname, and new surname
        cur.execute(sql, (new_surname, name, old_surname))
        conn.commit()  # Commit the transaction
        cur.close()  # Close the cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any error that occurs
    finally:
        # Ensure the connection is closed
        if conn is not None:
            conn.close()

# Function to update a person's phone number in the database
def update_phone(name, surname, old_phone, new_phone):
    # SQL query to update the phone number of a person with a given name and surname
    sql = "UPDATE Phonebook SET Phone = %s WHERE Name = %s AND Surname = %s AND Phone = %s"
    conn = None
    try:
        params = config()  # Fetch database connection parameters
        conn = psycopg2.connect(**params)  # Establish connection
        cur = conn.cursor()  # Create a cursor to execute SQL queries
        # Execute the update query with the old phone, name, surname, and new phone
        cur.execute(sql, (new_phone, name, surname, old_phone))
        conn.commit()  # Commit the transaction
        cur.close()  # Close the cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any error that occurs
    finally:
        # Ensure the connection is closed
        if conn is not None:
            conn.close()

# Main program that interacts with the user
if __name__ == '__main__':
    # Display menu options for the user
    print("""What do you want to do?
1) Add Person
2) Delete Person
3) Change Name
4) Change Surname
5) Change Phone
6) Upload from CSV
""")
    option = int(input())  # Get the user's choice

    # Perform the appropriate action based on user input
    if option == 1:
        name = str(input("Name: "))
        surname = str(input("Surname: "))
        phone = str(input("Phone Number: "))
        insert_people(name, surname, phone)  # Insert the new person
        print("Completed!")
        
    elif option == 2:
        name = str(input("Enter the name: "))
        surname = str(input("Enter the surname: "))
        delete_person(name, surname)  # Delete the person
        print("Completed!")

    elif option == 3:
        oldname = str(input("The name of the person you want to change: "))
        surname = str(input("The surname of the person you want to change: "))
        newname = str(input("Enter the new name: "))
        update_name(oldname, surname, newname)  # Update the name
        print("Completed!")

    elif option == 4:
        name = str(input("The name of the person you want to change: "))
        oldsurname = str(input("The surname of the person you want to change: "))
        newsurname = str(input("Enter the new surname: "))
        update_surname(name, oldsurname, newsurname)  # Update the surname
        print("Completed!")
    
    elif option == 5:
        name = str(input("The name of the person you want to change: "))
        surname = str(input("The surname of the person you want to change: "))
        oldphone = str(input("The phone number of the person you want to change: "))
        newphone = str(input("Enter the new phone number: "))
        update_phone(name, surname, oldphone, newphone)  # Update the phone number
        print("Completed!")
        
    elif option == 6:
        upload_from_csv()  # Upload contacts from CSV
        print("Completed!")
    else:
        print("Invalid option selected")

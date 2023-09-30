# coding: utf-8
import sqlite3


# Connect to the database
conn = sqlite3.connect('exercise4.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Create the Books table
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
    BookID VARCHAR(20) PRIMARY KEY,
    Title TEXT,
    Author TEXT,
    ISBN TEXT,
    Status TEXT
)''')

# Create the Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
    UserID VARCHAR(20) PRIMARY KEY,
    Name TEXT,
    Email TEXT
)''')

# Create the Reservations table
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
    ReservationID VARCHAR(20) PRIMARY KEY,
    BookID VARCHAR(20),
    UserID VARCHAR(20),
    ReservationDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books (BookID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
)''')


cursor.execute('''INSERT INTO Books (BookID, Title, Author, ISBN, Status) 
                VALUES (?, ?, ?, ?, ?)''', ("LB001", "BookTitle001", "Author001", "ISO0001", "1"))

cursor.execute('''INSERT INTO Users (UserID, Name, Email) 
                VALUES (?, ?, ?)''', ("LU001", "User001Name", "email@gmail.com"))

cursor.execute('''INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) 
                VALUES (?, ?, ?, ?)''', ("LR001", "LB001", "LU001", "2023/09/29 15:13"))

# The result will include the book’s reservation status, and the user’s details someone has reserved the said book
cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, 
                Users.Name, Users.Email, Reservations.ReservationDate 
                FROM Books 
                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                LEFT JOIN Users ON Users.UserID = Reservations.UserID
                WHERE Books.BookID = ?''', ("LB001",))
book_details = cursor.fetchone()

if book_details:
    print("Book Details:")
    print("BookID:", book_details[0])
    print("Title:", book_details[1])
    print("Author:", book_details[2])
    print("ISBN:", book_details[3])
    print("Status:", book_details[4])
    
    if book_details[5]:
        print("Reserved by:")
        print("Name:", book_details[5])
        print("Email:", book_details[6])
        print("Reservation Date:", book_details[7])
else:
    print("Book not found.")

# When accepting input from the user, your program must determine 
# based on the first two letters of the text if it’s a BookID (starts with LB), 
# UserID (starts with LU), or ReservationID (starts with LR). Otherwise, 
# the text entered is a Title.
input_text = input("Query content:")

if input_text.startswith("LB"):
    cursor.execute('''SELECT Books.Status 
                    FROM Books 
                    WHERE Books.BookID = ?''', (input_text,))
    status = cursor.fetchone()
    
    if status:
        print("Reservation Status:", status[0])
    else:
        print("Book not found.")
elif input_text.startswith("LU"):
    cursor.execute('''SELECT Books.Status 
                    FROM Books 
                    JOIN Reservations ON Books.BookID = Reservations.BookID
                    JOIN Users ON Reservations.UserID = Users.UserID
                    WHERE Users.UserID = ?''', (input_text,))
    status = cursor.fetchone()
    
    if status:
        print("Reservation Status:", status[0])
    else:
        print("User not found.")
elif input_text.startswith("LR"):
    cursor.execute('''SELECT Books.Status 
                    FROM Books 
                    JOIN Reservations ON Books.BookID = Reservations.BookID
                    WHERE Reservations.ReservationID = ?''', (input_text,))
    status = cursor.fetchone()
    
    if status:
        print("Reservation Status:", status[0])
    else:
        print("Reservation not found.")
else:
    cursor.execute('''SELECT Books.Status 
                    FROM Books 
                    WHERE Books.Title = ?''', (input_text,))
    status = cursor.fetchone()
    
    if status:
        print("Reservation Status:", status[0])
    else:
        print("Book not found.")

# Find all the books in the database.
cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
Users.Name, Users.Email, Reservations.ReservationDate
FROM Books
LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
LEFT JOIN Users ON Users.UserID = Reservations.UserID''')
all_books = cursor.fetchall()

if all_books:
    print("All Books:")
    for book in all_books:
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        if book[5]:
            print("Reserved by:")
            print("Name:", book[5])
            print("Email:", book[6])
            print("Reservation Date:", book[7])
        print()
else:
    print("No books found in the database.")

# Modify / update book details based on its BookID
book_id = input("BookID: ")
cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status 
                FROM Books 
                WHERE Books.BookID = ?''', (book_id,))
book_details = cursor.fetchone()

if book_details:
    print("Book Details:")
    print("BookID:", book_details[0])
    print("Title:", book_details[1])
    print("Author:", book_details[2])
    print("ISBN:", book_details[3])
    print("Status:", book_details[4])
    
    new_status = input("Enter new status: ")
    
    cursor.execute('''UPDATE Books 
                    SET Status = ? 
                    WHERE BookID = ?''', (new_status, book_id))
    conn.commit()
    print("Book details updated successfully.")
else:
    print("Book not found.")

# Delete a book based on its BookID
book_id = input("The BookID To Delete: ")
cursor.execute('''SELECT Books.BookID 
                FROM Books 
                WHERE Books.BookID = ?''', (book_id,))
book = cursor.fetchone()

if book:
    cursor.execute('''DELETE FROM Books 
                    WHERE BookID = ?''', (book_id,))
    cursor.execute('''DELETE FROM Reservations 
                    WHERE BookID = ?''', (book_id,))
    conn.commit()
    print("Book deleted successfully.")
else:
    print("Book not found.")

conn.commit()
conn.close()

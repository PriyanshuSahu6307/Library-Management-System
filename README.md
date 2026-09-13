
# 📚 Library Management System

A beginner-friendly **Library Management System built with Python** that allows users to manage books and members, borrow and return books, and store library data permanently using a **JSON file**.

This project was created to practice **Python Object-Oriented Programming (OOP), file handling, JSON, lists and dictionaries, functions, loops, exception handling, and date/time operations**.

---

## 🚀 Features

### 📖 Book Management

* Add new books to the library
* Store book title and author
* Specify the total number of copies
* Track available copies
* Automatically generate a unique Book ID
* Store the date and time when a book was added
* Display all available books

### 👤 Member Management

* Add new library members
* Store member name and email
* Automatically generate a unique Member ID
* Display all registered members
* Track books currently borrowed by each member

### 🔄 Borrow Book

* Borrow a book using Member ID and Book ID
* Check whether the member exists
* Check whether the book exists
* Check whether copies are available
* Decrease available copies after borrowing
* Store borrowing date and book information

### ↩️ Return Book

* Return previously borrowed books
* Display the member's borrowed books
* Select a book to return
* Increase available copies after returning
* Remove the book from the member's borrowed list

### 💾 Data Persistence

All library information is stored in:

```text
library.json
```

The data remains available even after the program is closed.

---

## 🛠️ Technologies Used

* **Python 3**
* `json` — storing and reading library data
* `random` — generating random IDs
* `string` — generating uppercase letters and digits
* `pathlib` — checking and creating the database file
* `datetime` — storing book addition and borrowing timestamps
* **Object-Oriented Programming (OOP)**
* Lists and Dictionaries
* File Handling
* Exception Handling

---

## 📂 Project Structure

```text
Library-Management/
│
├── main.py
├── library.json
└── README.md
```

### `main.py`

Contains the complete Python implementation of the Library Management System.

### `library.json`

Acts as the database and stores:

* Books
* Members
* Borrowed book information
* Available book copies
* Dates and timestamps

### `README.md`

Contains the documentation and instructions for the project.

---

## ⚙️ How It Works

The program uses a `Library` class to manage all library operations.

```python
class Library:
    database = "library.json"
    data = {
        "books": [],
        "members": []
    }
```

The class maintains two main collections:

```text
books
members
```

The information is stored inside `library.json`.

---

## 🆔 Automatic ID Generation

The project generates random IDs for books and members.

### Book ID

Example:

```text
B-A7X92
```

### Member ID

Example:

```text
M-K82P1
```

The ID is generated using uppercase letters and numbers.

```python
def gen_id(Prefix="B"):
    random_id = ""

    for i in range(5):
        random_id += random.choice(
            string.ascii_uppercase + string.digits
        )

    return Prefix + "-" + random_id
```

---

## 💾 JSON Database

The project checks whether `library.json` already exists.

If the file exists, the program loads the existing data.

If it doesn't exist, the program creates a new JSON database.

Example structure:

```json
{
    "books": [],
    "members": []
}
```

The `save_data()` method saves the current data:

```python
@classmethod
def save_data(cls):
    with open(cls.database, "w") as f:
        json.dump(cls.data, f, indent=4, default=str)
```

---

## 📖 Book Data Structure

Each book contains information such as:

```json
{
    "id": "B-A7X92",
    "title": "Python Programming",
    "author": "John Doe",
    "total_copies": 5,
    "available_copies": 5,
    "added_on": "2026-09-13 18:00:00"
}
```

The system uses:

* `total_copies` → Total copies owned by the library
* `available_copies` → Copies currently available for borrowing

When a book is borrowed:

```text
available_copies → decreases by 1
```

When a book is returned:

```text
available_copies → increases by 1
```

---

## 👤 Member Data Structure

Each member contains:

```json
{
    "id": "M-X82P1",
    "name": "Mr. X",
    "email": "example@gmail.com",
    "borowed": []
}
```

The `borowed` list stores information about books currently borrowed by that member.

> Note: The variable is named `borowed` in the current project code.

---

## 🔄 Borrowing Process

The borrowing process works as follows:

```text
Start
  ↓
Enter Member ID
  ↓
Check Member
  ↓
Enter Book ID
  ↓
Check Book
  ↓
Check Available Copies
  ↓
Create Borrow Entry
  ↓
Add Book to Member's Borrowed List
  ↓
Decrease Available Copies
  ↓
Save Data
  ↓
Finish
```

For example:

```text
Member ID: M-A82P1
Book ID: B-X92K7
```

If a copy is available, the book is added to the member's borrowed list.

---

## ↩️ Returning Process

The return process:

```text
Start
  ↓
Enter Member ID
  ↓
Find Member
  ↓
Display Borrowed Books
  ↓
Select Book
  ↓
Remove Book from Borrowed List
  ↓
Increase Available Copies
  ↓
Save Data
  ↓
Finish
```

---

## 🖥️ Application Menu

When the program starts, the following menu is displayed:

```text
==================================================
Library Management System
==================================================
1. Add Book
2. List Books
3. Add Members
4. List members
5. Borrow Book
6. Return Book
0. Exit the portal
--------------------------------------------------
What task you want to do
```

### Menu Options

| Option | Operation    |
| ------ | ------------ |
| 1      | Add Book     |
| 2      | List Books   |
| 3      | Add Member   |
| 4      | List Members |
| 5      | Borrow Book  |
| 6      | Return Book  |
| 0      | Exit Program |

---

## ▶️ How to Run the Project

### 1. Install Python

Make sure Python 3 is installed on your computer.

Check your Python version:

```bash
python --version
```

or:

```bash
py --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/PriyanshuSahu6307/Library-Management-System
```

### 3. Open the Project

```bash
cd Library-Management
```

### 4. Run the Program

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

---

## 🧪 Example Workflow

### Step 1 — Add a Book

```text
Enter book title : Python Programming
Enter the book author : John Doe
how many copies : 5
```

The system creates a book ID such as:

```text
B-X72K9
```

---

### Step 2 — Add a Member

```text
Enter the name :- Mr. X
please enter the email example@gmail.com
```

The system creates a member ID such as:

```text
M-A82P7
```

---

### Step 3 — Borrow a Book

```text
Enter the mermber ID : M-A82P7
enter the book id : B-X72K9
```

The available copies change:

```text
Before:
5 available

After:
4 available
```

---

### Step 4 — Return the Book

The system displays the member's borrowed books:

```text
Borrowed books

1. Python Programming (B-X72K9)

enter number to return : 1
```

The available copies increase again:

```text
4 available → 5 available
```

---

## 🧠 Python Concepts Practiced

This project helped practice several important Python concepts:

### 1. Object-Oriented Programming

The project uses a `Library` class to organize library operations.

### 2. Class Methods

The `save_data()` method uses:

```python
@classmethod
```

### 3. File Handling

The project uses:

```python
open()
```

to read and write the JSON database.

### 4. JSON

The project uses:

```python
json.load()
json.dump()
```

to manage persistent data.

### 5. Lists and Dictionaries

Books and members are represented using lists and dictionaries.

### 6. List Comprehension

The project searches for members and books using list comprehensions:

```python
members = [m for m in Library.data['members']
           if m['id'] == member_id]
```

### 7. Exception Handling

The return-book functionality uses `try` and `except` to handle invalid input.

### 8. Random ID Generation

The project uses:

```python
random
string.ascii_uppercase
string.digits
```

to generate IDs.

### 9. Date and Time

The `datetime` module is used to record when books are added and borrowed.

### 10. Path Handling

The `pathlib.Path` class is used to check whether the JSON database exists.

---

## 📈 Future Improvements

The current project is a beginner-level implementation. The following features can be added in future versions:

* 🔍 Search books by title or author
* 🗑️ Delete books
* ✏️ Update book information
* 👤 Delete or update members
* 📊 Display library statistics
* 📅 Add due dates for borrowed books
* ⚠️ Late-return detection
* 💰 Calculate fines for late returns
* 🔐 Admin login system
* 📧 Email notifications
* 🗄️ Replace JSON with SQLite/MySQL
* 🌐 Create a web interface using Flask or Django
* 🎨 Create a user interface using Streamlit
* 📱 Build an API using FastAPI
* 📊 Add dashboard and analytics

---

## 🔮 Future Version

A future version of this project can be developed as a complete web-based application:

```text
Python
   ↓
OOP
   ↓
JSON
   ↓
SQLite / MySQL
   ↓
Streamlit / Flask
   ↓
REST API
   ↓
Cloud Deployment
```

This would make the project more suitable as a portfolio project.

---

## 🎯 Learning Outcomes

By completing this project, I practiced:

* Python programming fundamentals
* Object-Oriented Programming
* File handling
* JSON data storage
* Data persistence
* Lists and dictionaries
* Functions and methods
* Exception handling
* Random ID generation
* Date and time handling
* Basic database concepts
* Building a menu-driven application
* Problem-solving and debugging

---


## 👨‍💻 Author

**Priyanshu Sahu**

This project was developed as part of my Python programming and project-based learning journey.

---

## ⭐ Support

If you found this project useful or helpful for learning Python, consider giving the repository a ⭐ star.

---

## 📄 License

This project is created for **educational and learning purposes**.

import importlib

# Load Streamlit dynamically so static analysis does not fail when the
# optional dependency is not installed in the selected Python environment.
st = importlib.import_module("streamlit")
import json
import random
import string
from pathlib import Path
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# LIBRARY CLASS
# =========================================================

class Library:

    database = "library.json"

    default_data = {
        "books": [],
        "members": []
    }

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    @classmethod
    def load_data(cls):

        if Path(cls.database).exists():

            try:
                with open(cls.database, "r") as file:
                    content = file.read().strip()

                    if content:
                        data = json.loads(content)

                        # Make sure required keys exist
                        data.setdefault("books", [])
                        data.setdefault("members", [])

                        # Fix old spelling if required
                        for member in data["members"]:
                            if "borowed" in member and "borrowed" not in member:
                                member["borrowed"] = member.pop("borowed")

                            member.setdefault("borrowed", [])

                        return data

            except (json.JSONDecodeError, OSError):
                pass

        # Create new database
        cls.save_data(cls.default_data.copy())

        return {
            "books": [],
            "members": []
        }

    # -----------------------------------------------------
    # SAVE DATA
    # -----------------------------------------------------

    @classmethod
    def save_data(cls, data):

        with open(cls.database, "w") as file:
            json.dump(
                data,
                file,
                indent=4,
                default=str
            )

    # -----------------------------------------------------
    # GENERATE ID
    # -----------------------------------------------------

    @staticmethod
    def gen_id(prefix="B"):

        random_id = ""

        for _ in range(5):
            random_id += random.choice(
                string.ascii_uppercase + string.digits
            )

        return prefix + "-" + random_id

    # -----------------------------------------------------
    # ADD BOOK
    # -----------------------------------------------------

    @classmethod
    def add_book(cls, data, title, author, copies):

        book = {
            "id": cls.gen_id("B"),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        data["books"].append(book)

        cls.save_data(data)

        return book

    # -----------------------------------------------------
    # ADD MEMBER
    # -----------------------------------------------------

    @classmethod
    def add_member(cls, data, name, email):

        member = {
            "id": cls.gen_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }

        data["members"].append(member)

        cls.save_data(data)

        return member

    # -----------------------------------------------------
    # BORROW BOOK
    # -----------------------------------------------------

    @classmethod
    def borrow_book(cls, data, member_id, book_id):

        member = next(
            (m for m in data["members"]
             if m["id"] == member_id),
            None
        )

        if not member:
            return False, "Member not found."

        book = next(
            (b for b in data["books"]
             if b["id"] == book_id),
            None
        )

        if not book:
            return False, "Book not found."

        if book["available_copies"] <= 0:
            return False, "No available copies of this book."

        # Prevent same member from borrowing same book twice
        already_borrowed = any(
            item["book_id"] == book_id
            for item in member["borrowed"]
        )

        if already_borrowed:
            return False, "This member has already borrowed this book."

        borrow_entry = {
            "book_id": book["id"],
            "title": book["title"],
            "borrow_on": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        member["borrowed"].append(borrow_entry)

        book["available_copies"] -= 1

        cls.save_data(data)

        return True, "Book borrowed successfully."

    # -----------------------------------------------------
    # RETURN BOOK
    # -----------------------------------------------------

    @classmethod
    def return_book(cls, data, member_id, borrowed_index):

        member = next(
            (m for m in data["members"]
             if m["id"] == member_id),
            None
        )

        if not member:
            return False, "Member not found."

        if not member["borrowed"]:
            return False, "This member has no borrowed books."

        if borrowed_index < 0 or borrowed_index >= len(member["borrowed"]):
            return False, "Invalid book selection."

        selected_book = member["borrowed"].pop(borrowed_index)

        book = next(
            (b for b in data["books"]
             if b["id"] == selected_book["book_id"]),
            None
        )

        if book:
            book["available_copies"] += 1

        cls.save_data(data)

        return True, "Book returned successfully."


# =========================================================
# LOAD DATABASE
# =========================================================

data = Library.load_data()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 Library System")

    st.write("Library Management Dashboard")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📚 Books",
            "➕ Add Book",
            "👥 Members",
            "➕ Add Member",
            "📥 Borrow Book",
            "📤 Return Book"
        ]
    )

    st.divider()

    st.caption("Library Management System")
    st.caption("Built with Python + Streamlit")


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("📚 Library Management System")

    st.subheader("Dashboard")

    st.write(
        "Manage books, members, borrowing and returning "
        "from one simple interface."
    )

    st.divider()

    # Statistics

    total_books = len(data["books"])

    total_members = len(data["members"])

    total_copies = sum(
        book["total_copies"]
        for book in data["books"]
    )

    available_copies = sum(
        book["available_copies"]
        for book in data["books"]
    )

    borrowed_copies = (
        total_copies - available_copies
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Book Titles",
            total_books
        )

    with col2:
        st.metric(
            "📦 Total Copies",
            total_copies
        )

    with col3:
        st.metric(
            "👥 Members",
            total_members
        )

    with col4:
        st.metric(
            "📖 Borrowed",
            borrowed_copies
        )

    st.divider()

    # Recent books

    st.subheader("📚 Recently Added Books")

    if data["books"]:

        recent_books = data["books"][-5:]
        recent_books.reverse()

        for book in recent_books:

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(
                    f"**{book['title']}**"
                )

            with col2:
                st.write(
                    f"Author: {book['author']}"
                )

            with col3:
                st.write(
                    f"{book['available_copies']}/"
                    f"{book['total_copies']}"
                )

    else:
        st.info("No books have been added yet.")


# =========================================================
# BOOKS PAGE
# =========================================================

elif page == "📚 Books":

    st.title("📚 Books")

    search = st.text_input(
        "🔎 Search books",
        placeholder="Search by title, author or ID..."
    )

    books = data["books"]

    if search:

        search = search.lower()

        books = [
            book for book in books
            if search in book["title"].lower()
            or search in book["author"].lower()
            or search in book["id"].lower()
        ]

    st.write(
        f"Showing **{len(books)}** book(s)"
    )

    if not books:

        st.info("No books found.")

    else:

        for book in books:

            st.markdown("---")

            col1, col2, col3, col4 = st.columns(
                [3, 2, 1, 1]
            )

            with col1:

                st.subheader(
                    f"📖 {book['title']}"
                )

                st.write(
                    f"**Author:** {book['author']}"
                )

                st.caption(
                    f"Book ID: {book['id']}"
                )

            with col2:

                st.write("Copies")

                st.write(
                    f"Total: **{book['total_copies']}**"
                )

                st.write(
                    f"Available: **{book['available_copies']}**"
                )

            with col3:

                if book["available_copies"] > 0:
                    st.success("Available")
                else:
                    st.error("Unavailable")

            with col4:

                st.write("Added on")

                st.caption(
                    book["added_on"]
                )


# =========================================================
# ADD BOOK
# =========================================================

elif page == "➕ Add Book":

    st.title("➕ Add New Book")

    st.write(
        "Enter the details of the new book below."
    )

    with st.form("add_book_form"):

        title = st.text_input(
            "Book Title",
            placeholder="Enter book title"
        )

        author = st.text_input(
            "Author",
            placeholder="Enter author name"
        )

        copies = st.number_input(
            "Number of Copies",
            min_value=1,
            value=1,
            step=1
        )

        submitted = st.form_submit_button(
            "📚 Add Book",
            use_container_width=True
        )

        if submitted:

            if not title.strip():

                st.error("Please enter the book title.")

            elif not author.strip():

                st.error("Please enter the author name.")

            else:

                book = Library.add_book(
                    data,
                    title.strip(),
                    author.strip(),
                    copies
                )

                st.success(
                    f"Book '{book['title']}' added successfully!"
                )

                st.info(
                    f"Book ID: {book['id']}"
                )


# =========================================================
# MEMBERS PAGE
# =========================================================

elif page == "👥 Members":

    st.title("👥 Members")

    search = st.text_input(
        "🔎 Search members",
        placeholder="Search by name, email or ID..."
    )

    members = data["members"]

    if search:

        search = search.lower()

        members = [
            member for member in members
            if search in member["name"].lower()
            or search in member["email"].lower()
            or search in member["id"].lower()
        ]

    st.write(
        f"Showing **{len(members)}** member(s)"
    )

    if not members:

        st.info("No members found.")

    else:

        for member in members:

            with st.container():

                col1, col2, col3 = st.columns(
                    [2, 3, 2]
                )

                with col1:

                    st.subheader(
                        f"👤 {member['name']}"
                    )

                    st.caption(
                        f"Member ID: {member['id']}"
                    )

                with col2:

                    st.write(
                        f"📧 {member['email']}"
                    )

                with col3:

                    st.metric(
                        "Borrowed",
                        len(member["borrowed"])
                    )

                if member["borrowed"]:

                    with st.expander(
                        "View Borrowed Books"
                    ):

                        for borrowed in member["borrowed"]:

                            st.write(
                                f"📖 **{borrowed['title']}**"
                            )

                            st.caption(
                                f"Book ID: {borrowed['book_id']} | "
                                f"Borrowed: {borrowed['borrow_on']}"
                            )

                st.divider()


# =========================================================
# ADD MEMBER
# =========================================================

elif page == "➕ Add Member":

    st.title("➕ Add New Member")

    with st.form("add_member_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter member name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter email address"
        )

        submitted = st.form_submit_button(
            "👤 Add Member",
            use_container_width=True
        )

        if submitted:

            if not name.strip():

                st.error("Please enter member name.")

            elif not email.strip():

                st.error("Please enter email.")

            else:

                member = Library.add_member(
                    data,
                    name.strip(),
                    email.strip()
                )

                st.success(
                    f"Member '{member['name']}' added successfully!"
                )

                st.info(
                    f"Member ID: {member['id']}"
                )


# =========================================================
# BORROW BOOK
# =========================================================

elif page == "📥 Borrow Book":

    st.title("📥 Borrow Book")

    if not data["members"]:

        st.warning(
            "No members available. Please add a member first."
        )

    elif not data["books"]:

        st.warning(
            "No books available. Please add a book first."
        )

    else:

        available_books = [
            book for book in data["books"]
            if book["available_copies"] > 0
        ]

        if not available_books:

            st.error(
                "There are currently no available books."
            )

        else:

            member_options = {
                f"{member['name']} ({member['id']})":
                    member["id"]
                for member in data["members"]
            }

            book_options = {
                f"{book['title']} - "
                f"{book['author']} "
                f"({book['available_copies']} available)":
                    book["id"]
                for book in available_books
            }

            with st.form("borrow_form"):

                selected_member = st.selectbox(
                    "👤 Select Member",
                    list(member_options.keys())
                )

                selected_book = st.selectbox(
                    "📖 Select Book",
                    list(book_options.keys())
                )

                submitted = st.form_submit_button(
                    "📥 Borrow Book",
                    use_container_width=True
                )

                if submitted:

                    member_id = member_options[
                        selected_member
                    ]

                    book_id = book_options[
                        selected_book
                    ]

                    success, message = Library.borrow_book(
                        data,
                        member_id,
                        book_id
                    )

                    if success:

                        st.success(
                            f"✅ {message}"
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"❌ {message}"
                        )


# =========================================================
# RETURN BOOK
# =========================================================

elif page == "📤 Return Book":

    st.title("📤 Return Book")

    members_with_books = [
        member for member in data["members"]
        if member["borrowed"]
    ]

    if not members_with_books:

        st.info(
            "No members currently have borrowed books."
        )

    else:

        member_options = {
            f"{member['name']} ({member['id']})":
                member["id"]
            for member in members_with_books
        }

        selected_member = st.selectbox(
            "👤 Select Member",
            list(member_options.keys())
        )

        member_id = member_options[
            selected_member
        ]

        member = next(
            m for m in data["members"]
            if m["id"] == member_id
        )

        borrowed_books = member["borrowed"]

        book_options = {
            f"{book['title']} "
            f"(Borrowed: {book['borrow_on']})":
                index
            for index, book in enumerate(borrowed_books)
        }

        selected_book = st.selectbox(
            "📖 Select Book to Return",
            list(book_options.keys())
        )

        if st.button(
            "📤 Return Book",
            use_container_width=True
        ):

            selected_index = book_options[
                selected_book
            ]

            success, message = Library.return_book(
                data,
                member_id,
                selected_index
            )

            if success:

                st.success(
                    f"✅ {message}"
                )

                st.rerun()

            else:

                st.error(
                    f"❌ {message}"
                )
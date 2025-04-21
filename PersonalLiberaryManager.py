import streamlit as st
import os
import json

LIBRARY_FILE = "library.txt"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)

# App layout
def main():
    st.title("📚 Personal Library Manager")
    library = st.session_state.get("library", load_library())

    menu = ["Add a Book", "Remove a Book", "Search Book", "Display All Books", "Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a Book":
        with st.form("add_book_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=0, step=1)
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Mystery", "Sci-Fi"])
            read = st.checkbox("Have you read this book?")
            submitted = st.form_submit_button("Add Book")
            if submitted:
                library.append({
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read
                })
                st.success("✅ Book added successfully!")
                st.session_state.library = library
                save_library(library)

    elif choice == "Remove a Book":
        titles = [book["title"] for book in library]
        title_to_remove = st.selectbox("Select book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != title_to_remove]
            st.success("✅ Book removed successfully!")
            st.session_state.library = library
            save_library(library)

    elif choice == "Search Book":
        search_type = st.radio("Search by", ["Title", "Author"])
        query = st.text_input("Enter search text").lower()
        if query:
            results = []
            for book in library:
                if (search_type == "Title" and query in book["title"].lower()) or \
                   (search_type == "Author" and query in book["author"].lower()):
                    results.append(book)

            if results:
                st.subheader("🔍 Matching Books")
                for book in results:
                    status = "Read" if book["read"] else "Unread"
                    st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
            else:
                st.warning("❌ No matching books found.")

    elif choice == "Display All Books":
        if not library:
            st.info("📚 Your library is empty.")
        else:
            st.subheader("📚 Your Library")
            for idx, book in enumerate(library, start=1):
                status = "Read" if book['read'] else "Unread"
                st.write(f"{idx}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    elif choice == "Statistics":
        total = len(library)
        if total == 0:
            st.info("📊 No books in the library.")
        else:
            read_books = sum(1 for book in library if book['read'])
            percent_read = (read_books / total) * 100
            st.metric("📘 Total Books", total)
            st.metric("📖 Books Read (%)", f"{percent_read:.1f}%")

if __name__ == "__main__":
    if "library" not in st.session_state:
        st.session_state.library = load_library()
    main()

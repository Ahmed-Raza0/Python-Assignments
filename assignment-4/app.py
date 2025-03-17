import streamlit as st
from supabase import create_client, Client
import pandas as pd
import dotenv
import os

# Custom CSS for Improved Styling
st.markdown(
    """
    <style>
        /* General App Styling */
        .stApp {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff !important;
            font-family: 'Arial', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            text-align: center; 
            font-weight: bold; 
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 12px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff6b6b;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 12px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .stSelectbox>div>div>div {
            border-radius: 12px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .stMarkdown {
            color: white !important;
        }
        .stSidebar {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.15);
        }
        .stSidebar .stSelectbox>div>div>div {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
        }
        .stSidebar .stSelectbox>div>div>div:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        .stSidebar .stButton>button {
            width: 100%;
            margin-top: 20px;
        }
        .book-card {
            background: rgba(255, 255, 255, 0.1);
            width: 230px; 
            border-radius: 12px; 
            padding: 20px; 
            box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.15); 
            text-align: center;
            margin-bottom: 15px; 
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            color: white;
        }
        .book-card:hover {
            transform: scale(1.05);
            box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.2);
        }
        .book-card h3 {
            margin: 0;
            color: white;
            font-weight: bold;
            font-size: 20px;
        }
        .book-card p {
            margin: 5px 0;
            color: #ddd;
            font-size: 16px;
        }
        .book-card .year {
            font-weight: bold;
            color: #ff4b4b;
        }
        .stAlert {
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .stAlert.success {
            background-color: #4CAF50;
            color: white;
        }
        .stAlert.error {
            background-color: #f44336;
            color: white;
        }
        .stAlert.warning {
            background-color: #ff9800;
            color: white;
        }
        .stAlert.info {
            background-color: #2196F3;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📚 Personal Library Manager")

def get_books():
    try:
        response = supabase.table("books").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching books: {e}")
        return []

def add_book(title, author, genre, year):
    if not title or not author or not genre or not year:
        st.error("All fields are required!")
        return

    supabase.table("books").insert({
        "title": title, "author": author, "genre": genre, "year": year
    }).execute()
    
    st.success(f"✅ '{title}' added successfully!")
    st.rerun()

def delete_book(book_id):
    supabase.table("books").delete().eq("id", book_id).execute()
    st.warning(f"❌ Book with ID {book_id} deleted!")
    st.rerun()

def update_book(book_id, title, author, genre, year):
    if not title or not author or not genre or not year:
        st.error("All fields are required!")
        return
    supabase.table("books").update({
        "title": title, "author": author, "genre": genre, "year": year
    }).eq("id", book_id).execute()
    st.success(f"✅ '{title}' updated successfully!")
    st.rerun()

menu = st.sidebar.selectbox("Menu", ["📖 View Books", "➕ Add Book", "✏️ Update Book", "🗑️ Delete Book"])

if menu == "📖 View Books":
    st.markdown('<h3>📚 Library Collection</h3>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search by Title, Author, or Genre").lower()
    books = get_books()
    if search_query:
        books = [book for book in books if search_query in book['title'].lower() or 
                 search_query in book['author'].lower() or search_query in book['genre'].lower()]
    if books:
        cols = st.columns(3)
        for index, book in enumerate(books):
            with cols[index % 3]:
                st.markdown(
                    f"""
                    <div class="book-card">
                        <h4>{book.get('title', 'Unknown')}</h4>
                        <p><strong>Author:</strong> {book.get('author', 'Unknown')}</p>
                        <p><strong>Genre:</strong> {book.get('genre', 'Unknown')}</p>
                        <p class="year"><strong>Year:</strong> {str(book.get('year', 'N/A'))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No books found. Try adding some!")

elif menu == "➕ Add Book":
    st.subheader("➕ Add New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Year", min_value=1000, max_value=2025, step=1)
    if st.button("Add Book"):
        add_book(title, author, genre, year)

elif menu == "✏️ Update Book":
    st.subheader("✏️ Update Book Details")
    books = get_books()
    book_options = {book["title"]: book["id"] for book in books}
    if book_options:
        selected_title = st.selectbox("Select Book", list(book_options.keys()))
        selected_id = book_options[selected_title]
        book = next((b for b in books if b["id"] == selected_id), None)
        if book:
            title = st.text_input("Title", book["title"])
            author = st.text_input("Author", book["author"])
            genre = st.text_input("Genre", book["genre"])
            year = st.number_input("Year", min_value=1000, max_value=2025, step=1, value=book["year"])
            if st.button("Update Book"):
                update_book(selected_id, title, author, genre, year)
    else:
        st.warning("No books available to update.")

elif menu == "🗑️ Delete Book":
    st.subheader("🗑️ Delete Book")
    books = get_books()
    book_options = {book["title"]: book["id"] for book in books}
    if book_options:
        selected_title = st.selectbox("Select Book", list(book_options.keys()))
        selected_id = book_options[selected_title]
        st.warning(f"Are you sure you want to delete '{selected_title}'?")
        if st.button("Yes, Delete"):
            delete_book(selected_id)
    else:
        st.warning("No books available to delete.")
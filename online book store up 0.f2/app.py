import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'bookstore.db'

# Initialize SQLite Database and create required tables if not exist
def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create Books Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        price REAL
    )
    ''')

    # Create Cart Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    ''')

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Insert sample data into books table (prices converted to INR and additional categories)
    cursor.executemany('''
    INSERT INTO books (title, category, description, price) VALUES (?, ?, ?, ?)
    ''', [
        ('Atomic Habits', 'Self-Help', 'A guide to building good habits and breaking bad ones', 1200),
        ('Bhagwat Geeta', 'Spirituality', 'Ancient Hindu text on spiritual wisdom', 1000),
        ('Reminder of Him', 'Romance', 'A heartfelt story of love and memory', 1050),
        ('Think and Grow Rich', 'Self-Help', 'A book on the power of personal beliefs and the path to success', 850),
        ('Enlightenment: The Only Revolution', 'Spirituality', 'A deep dive into the concept of enlightenment', 1100),
        ('The Power of Your Subconscious Mind', 'Self-Help', 'Understanding the power of the subconscious mind to shape your life', 1300),
        ('A Good Girl\'s Guide to Murder', 'Mystery', 'A thrilling mystery novel', 900),
        ('The Housemaid', 'Thriller', 'A gripping story of betrayal and suspense', 1000),
        ('The Art of Being Alone', 'Self-Help', 'A book on embracing solitude and personal growth', 950),
        ('The Monk Who Sold His Ferrari', 'Self-Help', 'A fable about fulfilling your dreams and reaching your destiny', 1050),
        ('Don\'t Believe Everything You Think', 'Psychology', 'A guide to questioning and changing harmful thought patterns', 850),
        ('The Art of War', 'Philosophy', 'Ancient Chinese military strategy and tactics', 700),
        ('The Silent Patient', 'Thriller', 'A psychological thriller about a woman who stopped speaking', 1100),
        ('Three Thousand Stitches', 'Biography', 'The inspiring story of a social activist', 900),
        ('The Complete Novels of Sherlock Holmes', 'Mystery', 'A collection of all Sherlock Holmes novels', 2200),
        ('The Mountain Is You', 'Self-Help', 'A book about overcoming self-sabotage', 1200),
        ('The Glorious Quran', 'Spirituality', 'The holy book of Islam', 1300),
        ('Holy Bible', 'Spirituality', 'The sacred scripture of Christianity', 1500),
        ('The Subtle Art of Not Giving a F*ck', 'Self-Help', 'A book about embracing life\'s challenges with a new perspective', 1300),
        ('The Alchemist', 'Fiction', 'A philosophical novel about following your dreams', 1000),
        ('Verity', 'Romance', 'A romantic thriller that keeps you guessing', 1050),
        ('The Midnight Library', 'Fiction', 'A novel about exploring the infinite possibilities of life choices', 1100),
        ('Deep Work', 'Self-Help', 'A book on focusing without distractions to achieve massive success', 1300),
        ('You Can', 'Self-Help', 'A motivational book about achieving your goals', 900),
        ('Sapiens: A Brief History of Humankind', 'Non-Fiction', 'A book about the history of the human species', 1500),
        ('Courage to Be Disliked', 'Philosophy', 'A guide to living a life free from the expectations of others', 1200),
        ('The 5 AM Club', 'Self-Help', 'A book on waking up early to transform your life', 1100),
        ('Anxious People', 'Fiction', 'A comedy-drama about life and personal struggles', 950),
        ('The 48 Laws of Power', 'Self-Help', 'A book about the principles of power and influence', 1300),
        ('It Ends with Us', 'Romance', 'A story about love and resilience', 1050),
        ('One Arranged Murder', 'Mystery', 'A thrilling mystery about an arranged marriage gone wrong', 1100),
        ('Siddhartha', 'Fiction', 'A novel about the spiritual journey of self-discovery', 850),
        ('The Five Love Languages', 'Self-Help', 'A book about understanding how different people give and receive love', 1000),
        ('The Blue Umbrella', 'Children', 'A charming story about a little girl and her blue umbrella', 600),
        ('Start with Why', 'Business', 'A book on the importance of understanding the purpose behind your actions', 1100),
        ('Think Like a Monk', 'Self-Help', 'A guide to leading a peaceful and purposeful life', 1200),
        ('Too Late', 'Thriller', 'A gripping crime novel about consequences', 1050),
        ('Corporate Chanakya', 'Business', 'A book on leadership and strategic thinking', 1200),
        ('The Diary of a CEO', 'Biography', 'A collection of reflections by a successful entrepreneur', 1500),
        ('Thinking, Fast and Slow', 'Psychology', 'A book about the two systems of thinking that drive our decisions', 1500),
        ('Do It Today', 'Self-Help', 'A guide to overcoming procrastination and taking action now', 850),
        ('The Diary of a Young Girl', 'Biography', 'The personal diary of Anne Frank', 650)
    ])

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    cart_count = 0
    username = ""

    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cart WHERE user_id=?', (user_id,))
        cart_count = cursor.fetchone()[0]
        
        # Fetch the username of the logged-in user
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        user = cursor.fetchone()
        if user:
            username = user[0]
        
        conn.close()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search_query:
        cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + search_query + '%',))
    elif category_filter:
        cursor.execute('SELECT * FROM books WHERE category=?', (category_filter,))
    else:
        cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('index.html', books=books, cart_count=cart_count, username=username)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')  # Create an 'about_us.html' template

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cart (user_id, book_id) VALUES (?, ?)', (user_id, book_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/book/<int:book_id>')
def book_details(book_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if book:
        cart_count = 0
        if 'user_id' in session:
            user_id = session['user_id']
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM cart WHERE user_id=?', (user_id,))
            cart_count = cursor.fetchone()[0]
            conn.close()
        
        return render_template('book_details.html', book=book, cart_count=cart_count)
    else:
        return "Book not found."

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password are provided
        if not username or not password:
            error = "Username or password is missing."
        else:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user_id'] = user[0]  # Store user ID in the session
                return redirect(url_for('home'))  # Redirect to the home page
            else:
                error = "Invalid username or password."

    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/cart')
def cart():
    cart_items = []
    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT books.title, books.category, books.price
        FROM cart
        JOIN books ON cart.book_id = books.id
        WHERE cart.user_id=?
        ''', (user_id,))
        cart_items = cursor.fetchall()
        conn.close()
    
    return render_template('cart.html', books_in_cart=cart_items)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        # Handle purchase details here (address, email, etc.)
        return render_template('confirm_purchase.html')

    return render_template('purchase.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

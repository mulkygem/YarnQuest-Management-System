from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "yarnquest",
    "autocommit": True,
}

SAMPLE_ITEMS = [
    {
        "name": "Premium Kenyan Cotton Yarn",
        "category": "Yarn",
        "price": "350.00",
        "image_url": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80",
        "location": "Nairobi",
        "description": "Soft, breathable yarn for all knit and crochet projects.",
        "in_stock": True,
        "vendor_name": "YarnQuest Demo",
    },
    {
        "name": "Ergonomic Crochet Hook Set",
        "category": "Hooks",
        "price": "820.00",
        "image_url": "https://images.unsplash.com/photo-1519741492343-18a2029fdeb3?auto=format&fit=crop&w=800&q=80",
        "location": "Mombasa",
        "description": "Complete hook set for comfortable long crafting sessions.",
        "in_stock": True,
        "vendor_name": "YarnQuest Demo",
    },
    {
        "name": "Precision Knitting Needles",
        "category": "Needles",
        "price": "450.00",
        "image_url": "https://images.unsplash.com/photo-1516910918606-6a45427f63a2?auto=format&fit=crop&w=800&q=80",
        "location": "Kisumu",
        "description": "Quality needles for fine and bulky yarn projects.",
        "in_stock": False,
        "vendor_name": "YarnQuest Demo",
    },
    {
        "name": "Flexible Measuring Tape",
        "category": "Measuring Tape",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80",
        "location": "Nakuru",
        "description": "Easy-to-read tape for accurate pattern measurements.",
        "in_stock": True,
        "vendor_name": "YarnQuest Demo",
    },
]


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT items.*, users.full_name AS vendor_name FROM items JOIN users ON items.vendor_id = users.id ORDER BY items.id DESC')
        items = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return items or SAMPLE_ITEMS


@app.route('/')
def index():
    items = get_items()
    cart_count = len(session.get('cart', []))
    return render_template('home.html', items=items, cart_count=cart_count, session=session)


@app.route('/crafters')
def crafters():
    items = get_items()
    cart_count = len(session.get('cart', []))
    return redirect(url_for('shop'))


@app.route('/shop')
def shop():
    items = get_items()
    cart_count = len(session.get('cart', []))
    
    # Extract unique categories from items
    categories = sorted(set(item.get('category', 'Other') for item in items if item.get('category')))
    
    return render_template('shop.html', items=items, categories=categories, cart_count=cart_count, session=session)


@app.route('/cart/add/<int:item_id>')
def cart_add(item_id):
    cart = session.get('cart', [])
    if item_id not in cart:
        cart.append(item_id)
        session['cart'] = cart
        flash('Item added to cart.', 'success')
    else:
        flash('Item is already in your cart.', 'info')
    return redirect(url_for('shop'))


@app.route('/cart/remove/<int:item_id>', methods=['GET', 'POST'])
def cart_remove(item_id):
    cart = session.get('cart', [])
    if item_id in cart:
        cart.remove(item_id)
        session['cart'] = cart
        flash('Item removed from cart.', 'warning')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    
    # If cart is empty, redirect to home page
    if not cart_items:
        flash('Your cart is empty. Start shopping!', 'info')
        return redirect(url_for('index'))
    
    items = []
    total = 0.00

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        placeholders = ','.join(['%s'] * len(cart_items))
        query = f'SELECT items.*, users.full_name AS vendor_name FROM items JOIN users ON items.vendor_id = users.id WHERE items.id IN ({placeholders})'
        cursor.execute(query, tuple(cart_items))
        items = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    # Convert prices to float and calculate total
    for item in items:
        item['price'] = float(item['price'])
    
    total = sum(item['price'] for item in items) if items else 0.00
    total = float(total)  # Ensure total is float
    
    return render_template('cart.html', items=items, total=total, cart_count=len(cart_items))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['full_name']
            # Redirect vendors to dashboard, crafters to shop
            if user['role'] == 'vendor':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('shop'))

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        phone = request.form.get('phone')
        location = request.form.get('location')
        contact_info = request.form.get('contact_info')

        password_hash = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (full_name, email, password_hash, role, phone, location, contact_info) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (full_name, email, password_hash, role, phone, location, contact_info),
            )
            conn.commit()
        except Error as e:
            flash(f'Error creating account: {e}', 'danger')
            return render_template('register.html')
        finally:
            cursor.close()
            conn.close()

        flash('Registration successful. You can now log in!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']
    user_data = None
    items = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()

        if role == 'vendor':
            cursor.execute('SELECT items.*, users.full_name AS vendor_name FROM items JOIN users ON items.vendor_id = users.id WHERE vendor_id = %s', (user_id,))
        else:
            cursor.execute('SELECT items.*, users.full_name AS vendor_name FROM items JOIN users ON items.vendor_id = users.id ORDER BY items.id DESC')

        items = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    sample_items = []
    if not items:
        sample_items = SAMPLE_ITEMS

    return redirect(url_for('shop'))


@app.route('/vendor/add-item', methods=['GET', 'POST'])
def add_item():
    if session.get('role') != 'vendor':
        return redirect(url_for('shop'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        location = request.form.get('location')
        description = request.form.get('description')
        in_stock = 1 if request.form.get('in_stock') == 'on' else 0

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (vendor_id, name, category, price, image_url, location, description, in_stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (session['user_id'], name, category, price, image_url, location, description, in_stock),
            )
            conn.commit()
            flash('Item added successfully.', 'success')
            return redirect(url_for('shop'))
        finally:
            cursor.close()
            conn.close()

    return render_template('add_item.html')


@app.route('/pay/<int:item_id>')
def pay(item_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    flash('Payment processing not yet implemented.', 'info')
    return redirect(url_for('shop'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

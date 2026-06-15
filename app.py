from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from mpesa import MpesaGateway

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
    cart = session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str] += 1
        flash('Item quantity updated in cart.', 'success')
    else:
        cart[item_id_str] = 1
        flash('Item added to cart.', 'success')
        
    session['cart'] = cart
    session.modified = True  
    return redirect(url_for('crafters'))

@app.route('/cart/remove/<int:item_id>')
def cart_remove(item_id):
    cart = session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        if cart[item_id_str] > 1:
            cart[item_id_str] -= 1  
            flash('Item quantity reduced.', 'warning')
        else:
            del cart[item_id_str]  
            flash('Item removed from cart.', 'warning')
            
        session['cart'] = cart  
        session.modified = True  
        
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})  
    items = []
    total = 0.00
    
    if cart:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            item_ids = list(cart.keys())
            placeholders = ','.join(['%s'] * len(item_ids))
            
            query = f'SELECT items.*, users.full_name AS vendor_name FROM items LEFT JOIN users ON items.vendor_id = users.id WHERE items.id IN ({placeholders})'
            cursor.execute(query, tuple(item_ids))
            items = cursor.fetchall()
        except Exception as e:
            print(f"Database error during cart parsing: {e}")
            items = []
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    if cart and not items:
        for sample in SAMPLE_ITEMS:
            if str(sample.get('id')) in cart:
                items.append(sample)

    if items:
        total = sum(float(item['price']) * cart.get(str(item['id']), 1) for item in items)
        
    cart_count = sum(cart.values())
    return render_template('cart.html', cart=cart, items=items, total=total, cart_count=cart_count)



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
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    sample_items = []
    if not items:
        sample_items = SAMPLE_ITEMS

    return render_template('dashboard.html', user=user_data, items=items, sample_items=sample_items, role=role)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('user_id') or session.get('role') != 'admin':
        flash("Access Denied: Platform Administrator security elevation required.", "danger")
        return redirect(url_for('login'))
    
    conn = None
    cursor = None
    orders_list = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                o.id AS order_id,
                o.delivery_status, 
                o.shipping_provider,
                o.tracking_number,
                o.assigned_rider,
                o.rider_contact,
                p.id AS payment_id,
                p.amount, 
                p.status AS payment_status,
                u.full_name AS customer_name, 
                i.name AS item_name
            FROM orders o
            JOIN payments p ON o.payment_id = p.id
            JOIN users u ON o.user_id = u.id
            JOIN items i ON p.item_id = i.id
            ORDER BY o.id DESC
        """)
        orders_list = cursor.fetchall()
    except Exception as e:
        flash(f"Error fetching logistical orders: {e}", "danger")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template('admin_dashboard.html', orders=orders_list)

@app.route('/admin/order/update/<int:order_id>', methods=['POST'])
def update_order_logistics(order_id):
    if not session.get('user_id') or session.get('role') != 'admin':
        flash("Action execution denied.", "danger")
        return redirect(url_for('login'))
        
    delivery_status = request.form.get('delivery_status')
    shipping_provider = request.form.get('shipping_provider')
    tracking_number = request.form.get('tracking_number')
    assigned_rider = request.form.get('assigned_rider')
    rider_contact = request.form.get('rider_contact')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE orders 
            SET delivery_status = %s, 
                shipping_provider = %s, 
                tracking_number = %s, 
                assigned_rider = %s, 
                rider_contact = %s
            WHERE id = %s
        """, (delivery_status, shipping_provider, tracking_number, assigned_rider, rider_contact, order_id))
        
        conn.commit()
        flash(f"Logistics update committed for Order #YQ-{order_id}!", "success")
    except Exception as e:
        flash(f"Database modification error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('admin_dashboard'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('cart'))
        
    items = []
    total = 0.00
    item_ids = list(cart.keys())

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        placeholders = ','.join(['%s'] * len(item_ids))
        
        query = f'SELECT items.*, users.full_name AS vendor_name FROM items LEFT JOIN users ON items.vendor_id = users.id WHERE items.id IN ({placeholders})'
        cursor.execute(query, tuple(item_ids))
        items = cursor.fetchall()
    except Exception as e:
        print(f"Database error during checkout fetch: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    if cart and not items:
        for sample in SAMPLE_ITEMS:
            if str(sample.get('id')) in cart:
                items.append(sample)

    if items:
        total = sum(float(item['price']) * cart.get(str(item['id']), 1) for item in items)

    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        user_id = session.get('user_id')
        
        if not user_id:
            flash("Please log in to complete checkout.", "danger")
            return redirect(url_for('login'))
        
        primary_item_id = items[0]['id'] if items else 1
        checkout_id = f"MOCK-REQ-{user_id}-{primary_item_id}" 

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO payments (user_id, item_id, payment_method, amount, status, checkout_request_id) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, primary_item_id, "MPESA-STK", total, "pending", checkout_id)
            )
            conn.commit()
            payment_row_id = cursor.lastrowid 
            
            cursor.execute(
                "INSERT INTO orders (user_id, payment_id, delivery_status) VALUES (%s, %s, 'pending')",
                (user_id, payment_row_id)
            )
            conn.commit()
        except Exception as database_error:
            print(f"Failed to record pending checkout payment: {database_error}")
            flash("Database error tracking your payment.", "danger")
            return redirect(url_for('cart'))
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

        mpesa = MpesaGateway()
        callback = "https://coil-chamomile-unfounded.ngrok-free.dev/api/v1/payments/callback"
        
        response = mpesa.trigger_stk_push(
            phone_number=phone_number,
            amount=total,
            callback_url=callback
        )
        
        if response.get("ResponseCode") == "0":
            real_checkout_id = response.get("CheckoutRequestID") 
            
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE payments SET checkout_request_id = %s WHERE id = %s",
                    (real_checkout_id, payment_row_id)
                )
                conn.commit()
            except Exception as update_error:
                print(f"Failed to update checkout ID: {update_error}")
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            session.pop('cart', None)
            flash("STK Push transaction dispatched successfully! Enter your M-PESA PIN to authorize.", "success")
            return redirect(url_for('order_status'))
        else:
            flash(f"M-PESA Gateway Notice: {response.get('ResultDesc', 'Insufficient Funds / Gateway Error')}. Saved as pending simulation.", "warning")
            session.pop('cart', None)
            return redirect(url_for('order_status'))

    return render_template('checkout.html', items=items, total=total, cart=cart)



@app.route('/pay/<int:item_id>')
def pay(item_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT phone FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        
        if not item or not user or not user.get('phone'):
            flash('Payment processing failed: Profile phone number or item details are missing.', 'danger')
            return redirect(url_for('dashboard'))
            
        mpesa = MpesaGateway()
        callback = "https://coil-chamomile-unfounded.ngrok-free.dev/api/v1/payments/callback"
        
        response = mpesa.trigger_stk_push(
            phone_number=user['phone'],
            amount=item['price'],
            callback_url=callback
        )
        
        if response.get("ResponseCode") == "0":
            checkout_id = response.get("CheckoutRequestID") 
            
            cursor.execute(
                "INSERT INTO payments (user_id, item_id, payment_method, amount, status, checkout_request_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, item_id, "MPESA-STK", item['price'], "pending", checkout_id)
            )
            conn.commit()
            payment_row_id = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO orders (user_id, payment_id, delivery_status) VALUES (%s, %s, 'pending')",
                (user_id, payment_row_id)
            )
            conn.commit()
            
            flash('STK Push request dispatched! Check your phone to input your M-PESA PIN.', 'success')
            return redirect(url_for('order_status'))
        else:
            flash(f"Safaricom API Error Logs: {str(response)}", 'warning')
            
    except Exception as e:
        flash(f"System Gateway Failure: {e}", "danger")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return redirect(url_for('dashboard'))   

@app.route('/api/v1/payments/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    
    stk_callback = data.get("Body", {}).get("stkCallback", {})
    result_code = stk_callback.get("ResultCode")
    checkout_request_id = stk_callback.get("CheckoutRequestID")
    
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        
        if result_code == 0:
            callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            mpesa_receipt_number = None
            
            for item in callback_metadata:
                if item.get("Name") == "MpesaReceiptNumber":
                    mpesa_receipt_number = item.get("Value")

            cursor.execute(
                "UPDATE payments SET status = 'completed', mpesa_receipt_number = %s WHERE checkout_request_id = %s AND status = 'pending'",
                (mpesa_receipt_number, checkout_request_id)
            )
            conn.commit()
            
        else:
            cursor.execute(
                "UPDATE payments SET status = 'failed' WHERE checkout_request_id = %s AND status = 'pending'",
                (checkout_request_id,)
            )
            conn.commit()
            
    except Exception as e:
        print(f"Callback processing error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})

@app.route('/order-status')
def order_status():
    if not session.get('user_id'):
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = None
    cursor = None
    order_data = None
    order_items = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT full_name, phone, location FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.execute("""
            SELECT p.id AS payment_id, p.status AS payment_status, p.amount,
                   o.id AS order_id, o.delivery_status, o.tracking_number, 
                   o.shipping_provider, o.assigned_rider, o.rider_contact, o.updated_at,
                   i.name AS item_name, i.description, i.image_url, v.full_name AS vendor_name
            FROM payments p
            LEFT JOIN orders o ON p.id = o.payment_id
            JOIN items i ON p.item_id = i.id
            JOIN users v ON i.vendor_id = v.id
            WHERE p.user_id = %s 
            ORDER BY p.id DESC LIMIT 1
        """, (user_id,))
        latest_pipeline = cursor.fetchone()
        
        if latest_pipeline:
            status_mapping = {
                "pending": "Processing Payment",
                "completed": "Order Confirmed & Paid",
                "failed": "Transaction Failed"
            }
            display_status = status_mapping.get(latest_pipeline['payment_status'], "Processing Request")
            
            formatted_date = latest_pipeline['updated_at'].strftime("%B %d, %Y") if latest_pipeline['updated_at'] else "Just now"

            try:
                raw_amount = float(latest_pipeline['amount'])
            except (ValueError, TypeError):
                raw_amount = 0.00

            order_data = {
                "id": latest_pipeline['order_id'] if latest_pipeline['order_id'] else latest_pipeline['payment_id'],
                "created_at": formatted_date,
                "customer_name": user['full_name'] if user else "Customer",
                "customer_phone": user['phone'] if user else "N/A",
                "shipping_address": user['location'] if user and user['location'] else "Not Specified",
                "subtotal": f"{raw_amount:,.2f}",
                "shipping_fee": "250.00" if latest_pipeline['delivery_status'] else "0.00",
                "total": f"{raw_amount:,.2f}",
                "status_text": display_status,
                "raw_status": latest_pipeline['payment_status'],
                "delivery_status": latest_pipeline['delivery_status'] if latest_pipeline['delivery_status'] else "pending",
                "tracking_number": latest_pipeline['tracking_number'],
                "shipping_provider": latest_pipeline['shipping_provider'],
                "assigned_rider": latest_pipeline['assigned_rider'],
                "rider_contact": latest_pipeline['rider_contact']
            }
            
            order_items = [{
                "name": latest_pipeline['item_name'],
                "quantity": 1,
                "vendor_name": latest_pipeline['vendor_name'],
                "price": f"{raw_amount:,.2f}"
            }]
            
    except Exception as e:
        flash(f"Error loading tracking metrics: {e}", "danger")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template('order_status.html', order=order_data, order_items=order_items)


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


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

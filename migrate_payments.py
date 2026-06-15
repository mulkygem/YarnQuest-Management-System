"""
Database migration for M-Pesa payment tracking
Run this to add orders and order_items tables to your database
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "yarnquest",
    "autocommit": True,
}

def create_orders_tables():
    """Create orders and order_items tables"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create orders table
        create_orders = """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            mpesa_receipt VARCHAR(20) UNIQUE,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_status (status)
        )
        """
        
        # Create order_items table
        create_order_items = """
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            item_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE RESTRICT,
            INDEX idx_order_id (order_id)
        )
        """
        
        # Create payment_logs table for debugging
        create_payment_logs = """
        CREATE TABLE IF NOT EXISTS payment_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            checkout_request_id VARCHAR(100),
            merchant_request_id VARCHAR(100),
            phone_number VARCHAR(20),
            amount DECIMAL(10, 2),
            status VARCHAR(50),
            mpesa_response JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_checkout_request (checkout_request_id)
        )
        """
        
        cursor.execute(create_orders)
        print("✓ Created 'orders' table")
        
        cursor.execute(create_order_items)
        print("✓ Created 'order_items' table")
        
        cursor.execute(create_payment_logs)
        print("✓ Created 'payment_logs' table")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("\n✓ Database migration completed successfully!")
        
    except Error as e:
        print(f"✗ Database error: {e}")
    except Exception as e:
        print(f"✗ Exception: {e}")

if __name__ == "__main__":
    create_orders_tables()

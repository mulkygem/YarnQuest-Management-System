#!/usr/bin/env python3
"""
Script to set up YarnQuest database schema
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
}

def setup_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🗄️  Setting up YarnQuest database...\n")
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS yarnquest CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database created")
        
        cursor.execute("USE yarnquest")
        
        # Create categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(100) NOT NULL UNIQUE,
              description TEXT,
              icon VARCHAR(50),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        print("✅ Categories table created")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
              id INT AUTO_INCREMENT PRIMARY KEY,
              full_name VARCHAR(150) NOT NULL,
              email VARCHAR(255) NOT NULL UNIQUE,
              password_hash VARCHAR(255) NOT NULL,
              role ENUM('crafter','vendor') NOT NULL,
              phone VARCHAR(50),
              location VARCHAR(255),
              contact_info VARCHAR(255),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        print("✅ Users table created")
        
        # Create items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
              id INT AUTO_INCREMENT PRIMARY KEY,
              vendor_id INT NOT NULL,
              name VARCHAR(255) NOT NULL,
              category VARCHAR(100) NOT NULL,
              price DECIMAL(10,2) NOT NULL,
              image_url VARCHAR(500) DEFAULT '',
              location VARCHAR(255) DEFAULT '',
              description TEXT,
              in_stock BOOLEAN DEFAULT TRUE,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (vendor_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Items table created")
        
        # Create payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
              id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT NOT NULL,
              item_id INT NOT NULL,
              payment_method VARCHAR(100) NOT NULL,
              amount DECIMAL(10,2) NOT NULL,
              status VARCHAR(50) DEFAULT 'pending',
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
              FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Payments table created")
        
        # Insert default categories
        categories = [
            ('Milk Cotton Yarns', 'Soft blend yarns with milk fiber for comfort', '🥛'),
            ('Acrylic Yarns', 'Durable and affordable acrylic yarn options', '✨'),
            ('Specialty / Novelty Yarns', 'Unique and fun textured yarns', '🎨'),
            ('Other Yarns', 'Premium and specialty natural fiber yarns', '🌿'),
        ]
        
        for cat_name, cat_desc, icon in categories:
            cursor.execute(
                "INSERT INTO categories (name, description, icon) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=name",
                (cat_name, cat_desc, icon)
            )
        print("✅ Categories inserted")
        
        conn.commit()
        print("\n🎉 Database setup complete!")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    setup_database()

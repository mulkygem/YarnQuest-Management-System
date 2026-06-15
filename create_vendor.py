#!/usr/bin/env python3
"""
Create a demo vendor account for YarnQuest
"""

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "yarnquest",
    "autocommit": True,
}

def create_demo_vendor():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("👨‍💼 Creating demo vendor account...\n")
        
        # Check if vendor already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", ("vendor@yarnquest.com",))
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ Vendor already exists (ID: {existing['id']})")
            print(f"   Email: {existing['email']}")
            print(f"   Name: {existing['full_name']}")
        else:
            # Create new vendor
            password_hash = generate_password_hash("password123")
            
            cursor.execute("""
                INSERT INTO users (full_name, email, password_hash, role, phone, location, contact_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                "YarnQuest Premium Supplier",
                "vendor@yarnquest.com",
                password_hash,
                "vendor",
                "+254-700-123-456",
                "Nairobi, Kenya",
                "supplier@yarnquest.com"
            ))
            
            print("✅ Vendor created successfully!")
            print("   📧 Email: vendor@yarnquest.com")
            print("   🔐 Password: password123")
            print("   📍 Location: Nairobi, Kenya")
        
        # Show all yarn products
        cursor.execute("""
            SELECT category, COUNT(*) as count FROM items 
            WHERE category IN ('Milk Cotton Yarns', 'Acrylic Yarns', 'Specialty / Novelty Yarns', 'Other Yarns')
            GROUP BY category ORDER BY category
        """)
        
        print("\n📊 Available yarn products:")
        total = 0
        for row in cursor.fetchall():
            print(f"   • {row['category']}: {row['count']} products")
            total += row['count']
        
        print(f"\n   Total: {total} products ready for sale!")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_demo_vendor()

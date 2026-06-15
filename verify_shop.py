#!/usr/bin/env python3
"""
Verify that the YarnQuest shop is properly set up
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "yarnquest",
}

def verify_setup():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Verifying YarnQuest Setup...\n")
        
        # Check database
        print("1️⃣  Database Status:")
        cursor.execute("SELECT DATABASE() as db")
        db = cursor.fetchone()
        print(f"   ✅ Connected to: {db['db']}\n")
        
        # Check tables
        print("2️⃣  Database Tables:")
        cursor.execute("""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'yarnquest'
        """)
        tables = cursor.fetchall()
        for table in tables:
            print(f"   ✅ {table['TABLE_NAME']}")
        print()
        
        # Check vendor
        print("3️⃣  Vendor Account:")
        cursor.execute("SELECT id, full_name, email, role FROM users WHERE role = 'vendor' LIMIT 1")
        vendor = cursor.fetchone()
        if vendor:
            print(f"   ✅ Vendor ID: {vendor['id']}")
            print(f"   ✅ Name: {vendor['full_name']}")
            print(f"   ✅ Email: {vendor['email']}\n")
        
        # Check categories
        print("4️⃣  Yarn Categories:")
        cursor.execute("SELECT COUNT(*) as count FROM categories")
        cat_count = cursor.fetchone()
        print(f"   ✅ Total categories: {cat_count['count']}")
        
        cursor.execute("SELECT name, icon FROM categories ORDER BY name")
        for cat in cursor.fetchall():
            print(f"      {cat['icon']} {cat['name']}")
        print()
        
        # Check products
        print("5️⃣  Yarn Products:")
        cursor.execute("SELECT COUNT(*) as count FROM items")
        item_count = cursor.fetchone()
        print(f"   ✅ Total items: {item_count['count']}\n")
        
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM items 
            GROUP BY category 
            ORDER BY category
        """)
        print("   📊 Products by category:")
        for row in cursor.fetchall():
            print(f"      • {row['category']}: {row['count']} products")
        print()
        
        # Show sample products
        print("6️⃣  Sample Products:")
        cursor.execute("""
            SELECT name, category, price, in_stock 
            FROM items 
            ORDER BY RAND() 
            LIMIT 3
        """)
        for product in cursor.fetchall():
            status = "✅ In Stock" if product['in_stock'] else "❌ Out of Stock"
            print(f"   • {product['name']}")
            print(f"     Category: {product['category']}")
            print(f"     Price: KES {product['price']}")
            print(f"     Status: {status}\n")
        
        print("🎉 Setup verification complete!")
        print("\n📝 Next: Start your Flask app with 'python app.py'")
        print("   Then visit: http://localhost:5000/shop")
        
    except Error as e:
        print(f"❌ Verification failed: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    verify_setup()

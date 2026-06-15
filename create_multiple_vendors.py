#!/usr/bin/env python3
"""
Script to create multiple vendors and distribute products among them
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

# New vendors to create
VENDORS = [
    {
        "full_name": "Precious",
        "email": "precious@yarnquest.com",
        "phone": "+254-700-111-001",
        "location": "Nairobi, Kenya",
    },
    {
        "full_name": "Allan",
        "email": "allan@yarnquest.com",
        "phone": "+254-700-111-002",
        "location": "Mombasa, Kenya",
    },
    {
        "full_name": "Fred",
        "email": "fred@yarnquest.com",
        "phone": "+254-700-111-003",
        "location": "Kisumu, Kenya",
    },
    {
        "full_name": "Tish",
        "email": "tish@yarnquest.com",
        "phone": "+254-700-111-004",
        "location": "Nakuru, Kenya",
    },
    {
        "full_name": "Gertrude",
        "email": "gertrude@yarnquest.com",
        "phone": "+254-700-111-005",
        "location": "Kiambu, Kenya",
    },
]

def create_multiple_vendors():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("👨‍💼 Creating multiple vendor accounts...\n")
        
        vendor_ids = []
        
        for vendor in VENDORS:
            # Check if vendor already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (vendor["email"],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"✅ {vendor['full_name']} already exists (ID: {existing['id']})")
                vendor_ids.append(existing['id'])
            else:
                # Create new vendor
                password_hash = generate_password_hash("password123")
                
                cursor.execute("""
                    INSERT INTO users (full_name, email, password_hash, role, phone, location, contact_info)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    vendor['full_name'],
                    vendor['email'],
                    password_hash,
                    "vendor",
                    vendor['phone'],
                    vendor['location'],
                    vendor['email']
                ))
                
                new_id = cursor.lastrowid
                vendor_ids.append(new_id)
                print(f"✅ Created {vendor['full_name']} (ID: {new_id})")
        
        print(f"\n📦 Distributing {len(vendor_ids)} vendors to products...")
        
        # Get all items
        cursor.execute("SELECT id FROM items ORDER BY id")
        items = cursor.fetchall()
        
        if not items:
            print("❌ No products found in database")
            return
        
        # Distribute items among vendors
        vendor_index = 0
        for item in items:
            vendor_id = vendor_ids[vendor_index % len(vendor_ids)]
            cursor.execute("UPDATE items SET vendor_id = %s WHERE id = %s", (vendor_id, item['id']))
            vendor_index += 1
        
        conn.commit()
        
        print(f"✅ Distributed {len(items)} products among vendors\n")
        
        # Show summary
        print("📊 Summary:")
        for idx, vendor_id in enumerate(vendor_ids):
            cursor.execute("""
                SELECT u.full_name, COUNT(i.id) as product_count 
                FROM users u 
                LEFT JOIN items i ON u.id = i.vendor_id 
                WHERE u.id = %s 
                GROUP BY u.id
            """, (vendor_id,))
            
            result = cursor.fetchone()
            if result:
                print(f"   • {result['full_name']}: {result['product_count']} products")
        
        print(f"\n🎉 Successfully created {len(vendor_ids)} vendors!")
        print("\n🔐 Login credentials for vendors:")
        for vendor in VENDORS:
            print(f"   • Email: {vendor['email']}, Password: password123")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_multiple_vendors()

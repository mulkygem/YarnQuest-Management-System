#!/usr/bin/env python3
"""
Script to update product locations to match their vendor's location
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

def update_product_locations():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("📍 Updating product locations to match vendor locations...\n")
        
        # Get all vendors with their locations
        cursor.execute("SELECT id, full_name, location FROM users WHERE role = 'vendor' AND id > 1")
        vendors = cursor.fetchall()
        
        total_updated = 0
        
        for vendor in vendors:
            # Update all items for this vendor
            cursor.execute(
                "UPDATE items SET location = %s WHERE vendor_id = %s",
                (vendor['location'], vendor['id'])
            )
            
            # Count how many items were updated
            cursor.execute("SELECT COUNT(*) as count FROM items WHERE vendor_id = %s", (vendor['id'],))
            count = cursor.fetchone()['count']
            
            print(f"✅ {vendor['full_name']}: Updated {count} products to {vendor['location']}")
            total_updated += count
        
        conn.commit()
        print(f"\n🎉 Successfully updated {total_updated} product locations!")
        
        # Show summary
        print("\n📊 Product Location Summary:")
        cursor.execute("""
            SELECT u.full_name, i.location, COUNT(i.id) as product_count 
            FROM items i 
            JOIN users u ON i.vendor_id = u.id 
            WHERE u.role = 'vendor' AND u.id > 1
            GROUP BY u.id, i.location
            ORDER BY u.id
        """)
        
        for row in cursor.fetchall():
            print(f"   • {row['full_name']}: {row['product_count']} products at {row['location']}")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    update_product_locations()

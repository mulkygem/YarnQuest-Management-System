#!/usr/bin/env python3
"""
Script to update vendor locations to different areas in Nairobi
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

# Vendor locations (all in Nairobi with different areas)
VENDOR_UPDATES = [
    {"email": "precious@yarnquest.com", "location": "Westlands, Nairobi"},
    {"email": "allan@yarnquest.com", "location": "Kilimani, Nairobi"},
    {"email": "fred@yarnquest.com", "location": "Karen, Nairobi"},
    {"email": "tish@yarnquest.com", "location": "Upper Hill, Nairobi"},
    {"email": "gertrude@yarnquest.com", "location": "Lavington, Nairobi"},
]

def update_vendor_locations():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("📍 Updating vendor locations to Nairobi areas...\n")
        
        for update in VENDOR_UPDATES:
            cursor.execute(
                "UPDATE users SET location = %s WHERE email = %s",
                (update['location'], update['email'])
            )
            
            # Get vendor name to display
            cursor.execute("SELECT full_name FROM users WHERE email = %s", (update['email'],))
            result = cursor.fetchone()
            if result:
                print(f"✅ {result['full_name']}: Updated to {update['location']}")
        
        conn.commit()
        print("\n🎉 Successfully updated all vendor locations!")
        
        # Show summary
        print("\n📊 Updated Vendor Locations:")
        cursor.execute("SELECT full_name, location FROM users WHERE role = 'vendor' ORDER BY id")
        for vendor in cursor.fetchall():
            print(f"   • {vendor['full_name']}: {vendor['location']}")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    update_vendor_locations()

#!/usr/bin/env python3
"""
Script to update item image URLs with actual images from static/images folder
"""

import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "yarnquest",
    "autocommit": True,
}

# Map product names to their image filenames
IMAGE_MAPPING = {
    "Rainbow Milk Cotton Yarn": "Rainbow Milk Cotton Yarn.avif",
    "Milk Cotton Supersaver": "Milk Cotton Supersaver.jpg",
    "Milk Cotton 4ply": "Milk Cotton 4ply.webp",
    "Baby Chenille Yarn": "Baby Chenille Yarn.jpg",
    "Alize Burcum Batik": "Alize Burcum Batik.jpg",
    "Variegated Matte Acrylic": "Variegated Matte Acrylic.jpg",
    "Premium Matte Acrylic": "Premium Matte Acrylic.webp",
    "Winter King 4ply Acrylic": "Winter King 4ply Acrylic.jpg",
    "Glow-in-the-Dark Yarn": "Glow-in-the-Dark Yarn.jpg",
    "T-Shirt Yarn": "T-Shirt Yarn.jpg",
    "Velvet Yarn": "Velvet Yarn.webp",
    "Chunky Cake Yarn": "Chunky Cake Yarn.webp",
    "Tweed Baby Yarn": "Tweed Baby Yarn.jpg",
    "Flowers Moonlight": "Flowers Moonlight.jpg",
    "Polypropylene Flat Yarn (PP Yarn)": "Polypropylene Flat Yarn (PP Yarn.jpg",
    "Organic Cotton Yarn": "organic cotton yarn.jpg",
}

def update_image_urls():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔄 Updating image URLs in database...\n")
        
        updated_count = 0
        
        # Get all items
        cursor.execute("SELECT id, name FROM items")
        items = cursor.fetchall()
        
        for item in items:
            item_name = item['name']
            item_id = item['id']
            
            if item_name in IMAGE_MAPPING:
                image_filename = IMAGE_MAPPING[item_name]
                image_url = f"/static/images/{image_filename}"
                
                cursor.execute(
                    "UPDATE items SET image_url = %s WHERE id = %s",
                    (image_url, item_id)
                )
                print(f"✅ {item_name}")
                print(f"   → {image_url}\n")
                updated_count += 1
            else:
                print(f"⚠️  {item_name} - No image mapping found\n")
        
        conn.commit()
        print(f"\n🎉 Successfully updated {updated_count} items with image URLs!")
        
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    update_image_urls()

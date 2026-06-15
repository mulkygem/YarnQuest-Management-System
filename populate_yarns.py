#!/usr/bin/env python3
"""
Script to insert yarn products into YarnQuest database
Run this script to populate the items table with organized yarn products
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

YARN_PRODUCTS = {
    "Milk Cotton Yarns": [
        {"name": "Rainbow Milk Cotton Yarn", "price": 450.00, "description": "100g, 200m, Acrylic + Milk Fiber blend. Soft and smooth for all projects."},
        {"name": "Milk Cotton Supersaver", "price": 650.00, "description": "200g of premium milk cotton. Great value for larger projects."},
        {"name": "Milk Cotton 4ply", "price": 350.00, "description": "50g per ball, 4ply weight. Perfect for delicate work and baby items."},
        {"name": "Baby Chenille Yarn", "price": 550.00, "description": "100g of ultra-soft chenille. Ideal for baby clothing and blankets."},
    ],
    "Acrylic Yarns": [
        {"name": "Alize Burcum Batik", "price": 380.00, "description": "100g, 210m, 100% Acrylic. Beautiful batik colors with excellent durability."},
        {"name": "Variegated Matte Acrylic", "price": 420.00, "description": "100g, 170m. Matte finish with gorgeous color variations."},
        {"name": "Premium Matte Acrylic", "price": 280.00, "description": "Smooth matte finish acrylic yarn. Perfect for beginners and everyday projects."},
        {"name": "Winter King 4ply Acrylic", "price": 320.00, "description": "50g, 100% Acrylic. Lightweight and warm for winter accessories."},
    ],
    "Specialty / Novelty Yarns": [
        {"name": "Glow-in-the-Dark Yarn", "price": 580.00, "description": "50g, 50m, Polyester. Creates glowing effects in the dark. Fun for unique projects."},
        {"name": "T-Shirt Yarn", "price": 620.00, "description": "100g, 30m. Upcycled t-shirt material for trendy, sustainable projects."},
        {"name": "Velvet Yarn", "price": 750.00, "description": "100g, 130m. Luxurious velvet texture. Creates beautiful, tactile finished pieces."},
        {"name": "Chunky Cake Yarn", "price": 680.00, "description": "200g, 257m. Pre-dyed color-changing yarn in chunky weight. Quick projects!"},
        {"name": "Tweed Baby Yarn", "price": 420.00, "description": "50g. Soft tweed blend perfect for delicate baby clothing and accessories."},
        {"name": "Flowers Moonlight", "price": 890.00, "description": "260g, 1000m. Lightweight moonlight yarn with subtle sheen. Great yardage value."},
        {"name": "Polypropylene Flat Yarn (PP Yarn)", "price": 480.00, "description": "115g, 70m. Durable flat yarn for bag making and home décor projects."},
    ],
    "Other Yarns": [
        {"name": "Organic Cotton Yarn", "price": 510.00, "description": "50g, 125m. 100% Organic cotton. Eco-friendly choice for sustainable crafting."},
    ],
}

CATEGORIES = {
    "Milk Cotton Yarns": {"description": "Soft blend yarns with milk fiber for comfort", "icon": "🥛"},
    "Acrylic Yarns": {"description": "Durable and affordable acrylic yarn options", "icon": "✨"},
    "Specialty / Novelty Yarns": {"description": "Unique and fun textured yarns", "icon": "🎨"},
    "Other Yarns": {"description": "Premium and specialty natural fiber yarns", "icon": "🌿"},
}


def insert_yarn_products():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # First, insert categories
        print("📚 Inserting categories...")
        for category_name, category_info in CATEGORIES.items():
            cursor.execute(
                """INSERT INTO categories (name, description, icon) 
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE name=name""",
                (category_name, category_info["description"], category_info["icon"])
            )
        conn.commit()
        print("✅ Categories inserted successfully!")
        
        # Insert products - using vendor_id 1 (demo vendor)
        print("\n🧶 Inserting yarn products...")
        total_inserted = 0
        
        for category, products in YARN_PRODUCTS.items():
            for product in products:
                cursor.execute(
                    """INSERT INTO items 
                       (vendor_id, name, category, price, location, description, in_stock) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (1, product["name"], category, product["price"], "Nairobi", product["description"], True)
                )
                total_inserted += 1
            conn.commit()
            print(f"  ✓ {len(products)} products added to '{category}'")
        
        print(f"\n🎉 Successfully inserted {total_inserted} yarn products!")
        
        # Show summary
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM items 
            WHERE category IN ('Milk Cotton Yarns', 'Acrylic Yarns', 'Specialty / Novelty Yarns', 'Other Yarns')
            GROUP BY category
            ORDER BY category
        """)
        
        print("\n📊 Summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} products")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("🚀 Starting YarnQuest Database Population\n")
    insert_yarn_products()
    print("\n✨ Done! Your shop is ready to go!")

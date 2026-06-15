-- Insert Yarn Products into YarnQuest Database
-- This script populates the items table with organized yarn products

-- First, ensure we have a vendor for these items (using vendor_id 1)
-- If vendor_id 1 doesn't exist, you may need to adjust this or create a vendor first

-- Milk Cotton Yarns Category
INSERT INTO items (vendor_id, name, category, price, location, description, in_stock) VALUES
(1, 'Rainbow Milk Cotton Yarn', 'Milk Cotton Yarns', 450.00, 'Nairobi', '100g, 200m, Acrylic + Milk Fiber blend. Soft and smooth for all projects.', TRUE),
(1, 'Milk Cotton Supersaver', 'Milk Cotton Yarns', 650.00, 'Nairobi', '200g of premium milk cotton. Great value for larger projects.', TRUE),
(1, 'Milk Cotton 4ply', 'Milk Cotton Yarns', 350.00, 'Nairobi', '50g per ball, 4ply weight. Perfect for delicate work and baby items.', TRUE),
(1, 'Baby Chenille Yarn', 'Milk Cotton Yarns', 550.00, 'Nairobi', '100g of ultra-soft chenille. Ideal for baby clothing and blankets.', TRUE);

-- Acrylic Yarns Category
INSERT INTO items (vendor_id, name, category, price, location, description, in_stock) VALUES
(1, 'Alize Burcum Batik', 'Acrylic Yarns', 380.00, 'Nairobi', '100g, 210m, 100% Acrylic. Beautiful batik colors with excellent durability.', TRUE),
(1, 'Variegated Matte Acrylic', 'Acrylic Yarns', 420.00, 'Nairobi', '100g, 170m. Matte finish with gorgeous color variations.', TRUE),
(1, 'Premium Matte Acrylic', 'Acrylic Yarns', 280.00, 'Nairobi', 'Smooth matte finish acrylic yarn. Perfect for beginners and everyday projects.', TRUE),
(1, 'Winter King 4ply Acrylic', 'Acrylic Yarns', 320.00, 'Nairobi', '50g, 100% Acrylic. Lightweight and warm for winter accessories.', TRUE);

-- Specialty / Novelty Yarns Category
INSERT INTO items (vendor_id, name, category, price, location, description, in_stock) VALUES
(1, 'Glow-in-the-Dark Yarn', 'Specialty / Novelty Yarns', 580.00, 'Nairobi', '50g, 50m, Polyester. Creates glowing effects in the dark. Fun for unique projects.', TRUE),
(1, 'T-Shirt Yarn', 'Specialty / Novelty Yarns', 620.00, 'Nairobi', '100g, 30m. Upcycled t-shirt material for trendy, sustainable projects.', TRUE),
(1, 'Velvet Yarn', 'Specialty / Novelty Yarns', 750.00, 'Nairobi', '100g, 130m. Luxurious velvet texture. Creates beautiful, tactile finished pieces.', TRUE),
(1, 'Chunky Cake Yarn', 'Specialty / Novelty Yarns', 680.00, 'Nairobi', '200g, 257m. Pre-dyed color-changing yarn in chunky weight. Quick projects!', TRUE),
(1, 'Tweed Baby Yarn', 'Specialty / Novelty Yarns', 420.00, 'Nairobi', '50g. Soft tweed blend perfect for delicate baby clothing and accessories.', TRUE),
(1, 'Flowers Moonlight', 'Specialty / Novelty Yarns', 890.00, 'Nairobi', '260g, 1000m. Lightweight moonlight yarn with subtle sheen. Great yardage value.', TRUE),
(1, 'Polypropylene Flat Yarn (PP Yarn)', 'Specialty / Novelty Yarns', 480.00, 'Nairobi', '115g, 70m. Durable flat yarn for bag making and home décor projects.', TRUE);

-- Other Yarns Category
INSERT INTO items (vendor_id, name, category, price, location, description, in_stock) VALUES
(1, 'Organic Cotton Yarn', 'Other Yarns', 510.00, 'Nairobi', '50g, 125m. 100% Organic cotton. Eco-friendly choice for sustainable crafting.', TRUE);

-- Optional: Update sample categories with icons if they don't exist
INSERT INTO categories (name, description, icon) VALUES
('Milk Cotton Yarns', 'Soft blend yarns with milk fiber for comfort', '🥛'),
('Acrylic Yarns', 'Durable and affordable acrylic yarn options', '✨'),
('Specialty / Novelty Yarns', 'Unique and fun textured yarns', '🎨'),
('Other Yarns', 'Premium and specialty natural fiber yarns', '🌿')
ON DUPLICATE KEY UPDATE name=name;

-- Verify insertion
SELECT category, COUNT(*) as product_count FROM items WHERE category IN ('Milk Cotton Yarns', 'Acrylic Yarns', 'Specialty / Novelty Yarns', 'Other Yarns') GROUP BY category;

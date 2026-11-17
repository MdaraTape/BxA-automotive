INSERT OR IGNORE INTO categories VALUES (1,'Premium vehicles'),(2,'Driving accessories');
INSERT OR IGNORE INTO access_needs VALUES (1,'Leg and foot mobility'),(2,'Hand and arm mobility'),(3,'Grip and dexterity'),(4,'Wheelchair use and transfers');
INSERT OR IGNORE INTO products VALUES
(1,1,'GLE 63 S 4MATIC+ SUV','vehicle',15000000,'Sample performance SUV with selectable colour and trim for a simulated purchase.'),
(2,1,'BMW X5 M Competition','vehicle',13800000,'Sample performance SUV with a configurable exterior and interior.'),
(3,2,'Wide grip key sleeve','accessory',1800,'A larger surface to hold when turning a compatible key.'),
(4,2,'Seat belt reach handle','accessory',2400,'An extended handle for reaching a compatible seat belt.'),
(5,2,'Foldable transfer board','accessory',12500,'A portable board for a supported transfer assessment.'),
(6,2,'Console organiser','accessory',5000,'Keeps small items within reach in the centre console.'),
(7,2,'Foldable sunshade','accessory',3200,'A lightweight shade that folds away between trips.'),
(8,2,'Door sill protection pad','accessory',3400,'Protects the sill while loading mobility equipment.'),
(9,2,'Wheelchair storage straps','accessory',4200,'Storage straps for an unoccupied folded wheelchair.'),
(10,2,'Large zip pull set','accessory',1600,'Loop pulls for bags and compatible vehicle storage covers.');
INSERT OR IGNORE INTO product_access_needs VALUES (3,2),(3,3),(4,2),(5,1),(5,4),(6,2),(8,4),(9,4),(10,2),(10,3);
INSERT OR IGNORE INTO vehicle_options VALUES
(1,1,'colour','Obsidian Black',0),(2,1,'colour','Polar White',80000),
(3,1,'trim','Standard',0),(4,1,'trim','Premium',450000),
(5,2,'colour','Carbon Black',0),(6,2,'colour','Alpine White',70000),
(7,2,'trim','Standard',0),(8,2,'trim','Executive',350000);

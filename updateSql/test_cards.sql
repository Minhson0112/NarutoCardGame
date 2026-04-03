-- SQL Script to insert test card templates for each tier
-- Path: updateSql/test_cards.sql

INSERT INTO card_templates 
(card_key, name, tier, element, health, armor, base_damage, crit_rate, speed, chakra, first_position, image_url, sell_price)
VALUES 
('sakura', 'Haruno Sakura', 'Genin', 'Thủy', 1200, 20, 80, 0.1, 0.05, 0, 0, 'sakura', 100)
ON DUPLICATE KEY UPDATE name=VALUES(name), tier=VALUES(tier), image_url=VALUES(image_url);

INSERT INTO card_templates 
(card_key, name, tier, element, health, armor, base_damage, crit_rate, speed, chakra, first_position, image_url, sell_price)
VALUES 
('neji', 'Hyuga Neji', 'Chunin', 'Thể', 1500, 30, 120, 0.15, 0.1, 0, 1, 'neji', 500)
ON DUPLICATE KEY UPDATE name=VALUES(name), tier=VALUES(tier), image_url=VALUES(image_url);

INSERT INTO card_templates 
(card_key, name, tier, element, health, armor, base_damage, crit_rate, speed, chakra, first_position, image_url, sell_price)
VALUES 
('konan', 'Konan', 'Jounin', 'Phong', 2500, 50, 200, 0.2, 0.15, 20, 0, 'konan', 2000)
ON DUPLICATE KEY UPDATE name=VALUES(name), tier=VALUES(tier), image_url=VALUES(image_url);

INSERT INTO card_templates 
(card_key, name, tier, element, health, armor, base_damage, crit_rate, speed, chakra, first_position, image_url, sell_price)
VALUES 
('tsunade', 'Tsunade', 'Kage', 'Thủy', 5000, 100, 350, 0.1, 0.05, 0, 1, 'tsunade', 10000)
ON DUPLICATE KEY UPDATE name=VALUES(name), tier=VALUES(tier), image_url=VALUES(image_url);

INSERT INTO card_templates 
(card_key, name, tier, element, health, armor, base_damage, crit_rate, speed, chakra, first_position, image_url, sell_price)
VALUES 
('naruto', 'Uzumaki Naruto', 'Legendary', 'Phong', 10000, 150, 600, 0.25, 0.2, 40, 0, 'naruto', 50000)
ON DUPLICATE KEY UPDATE name=VALUES(name), tier=VALUES(tier), image_url=VALUES(image_url);

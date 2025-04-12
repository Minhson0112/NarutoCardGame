CREATE TABLE challenges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_name VARCHAR(100) NOT NULL,
    card_strength INT NOT NULL,
    image_url_key VARCHAR(255) NOT NULL,
    narrative TEXT,
    bonus_ryo INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
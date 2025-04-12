CREATE TABLE gifcode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gif_code VARCHAR(100) NOT NULL,
    gif_name VARCHAR(255) NOT NULL,
    bonus_ryo INT DEFAULT NULL,
    card_key VARCHAR(50) DEFAULT NULL,
    weapon_key VARCHAR(50) DEFAULT NULL,
    expiration_date DATE,
    CONSTRAINT fk_card_key FOREIGN KEY (card_key) REFERENCES card_templates(card_key),
    CONSTRAINT fk_weapon_key FOREIGN KEY (weapon_key) REFERENCES weapon_templates(weapon_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE gifcode_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT NOT NULL,
    gifcode_id INT NOT NULL,
    rewarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_log_player FOREIGN KEY (player_id) REFERENCES players(player_id),
    CONSTRAINT fk_log_gifcode FOREIGN KEY (gifcode_id) REFERENCES gifcode(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

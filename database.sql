-- Tạo cơ sở dữ liệu (database)
SET FOREIGN_KEY_CHECKS = 0;
CREATE DATABASE IF NOT EXISTS naruto_card_game;
USE naruto_card_game;

-- --------------------------------------------------
-- 1. Bảng players: Lưu thông tin người chơi
-- --------------------------------------------------
DROP TABLE IF EXISTS players;
CREATE TABLE players (
    player_id BIGINT PRIMARY KEY,         -- Discord ID của người chơi
    username VARCHAR(100),                -- Tên hiển thị của người chơi
    coin_balance INT NOT NULL DEFAULT 0,  -- Số ryo (両) hiện có
    rank_points INT NOT NULL DEFAULT 0,   -- Điểm rank (sắt, đồng, ... cao thủ)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 2. Bảng card_templates: Mẫu thẻ bài
-- --------------------------------------------------
DROP TABLE IF EXISTS card_templates;
CREATE TABLE card_templates (
    card_key VARCHAR(50) PRIMARY KEY,        -- Ví dụ: "naruto_lv1"
    name VARCHAR(100) NOT NULL,              -- Tên thẻ (ví dụ: "Naruto")
    tier ENUM('Genin', 'Chunin', 'Jounin', 'Kage', 'Legendary') NOT NULL, -- Bậc của thẻ
    element VARCHAR(20),                     -- Hệ (ví dụ: Mộc, Hỏa, Thổ, Kim, Thủy, ...)
    base_power INT,                          -- Sức mạnh cơ bản của thẻ
    image_url TEXT,                          -- URL ảnh (ảnh tĩnh hoặc GIF cho thẻ VIP)
    sell_price INT NOT NULL DEFAULT 0,       -- Giá bán của thẻ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 3. Bảng player_cards: Thẻ bài của người chơi
-- --------------------------------------------------
DROP TABLE IF EXISTS player_cards;
CREATE TABLE player_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT NOT NULL,              -- Khóa ngoại đến bảng players
    card_key VARCHAR(50) NOT NULL,          -- Khóa ngoại đến bảng card_templates
    level INT NOT NULL DEFAULT 1,           -- Cấp độ của thẻ (1->2 cần 5 thẻ 2->3 cần 10 thẻ mỗi lần thẻ thăng cấp cần + thêm 5 so với lần trước, sức mạnh = sức mạnh cơ bản * cấp thẻ )
    quantity INT NOT NULL DEFAULT 1,        -- Số lượng của loại thẻ này mà người chơi sở hữu
    equipped BOOLEAN NOT NULL DEFAULT FALSE,-- Đánh dấu thẻ đã được trang bị hay chưa
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (card_key) REFERENCES card_templates(card_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 4. Bảng weapon_templates: Mẫu vũ khí
-- --------------------------------------------------
DROP TABLE IF EXISTS weapon_templates;
CREATE TABLE weapon_templates (
    weapon_key VARCHAR(50) PRIMARY KEY,      -- Ví dụ: "sword_basic"
    name VARCHAR(100) NOT NULL,              -- Tên vũ khí
    grade ENUM('Hạ cấp', 'Trung cấp', 'Cao cấp') NOT NULL, -- Bậc của vũ khí
    bonus_power INT,                         -- Sức mạnh cộng thêm khi trang bị
    image_url TEXT,                          -- URL ảnh của vũ khí
    sell_price INT NOT NULL DEFAULT 0,       -- Giá bán của vũ khí
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 5. Bảng player_weapons: Vũ khí của người chơi
-- --------------------------------------------------
DROP TABLE IF EXISTS player_weapons;
CREATE TABLE player_weapons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT NOT NULL,              -- Khóa ngoại đến bảng players
    weapon_key VARCHAR(50) NOT NULL,         -- Khóa ngoại đến bảng weapon_templates
    level INT NOT NULL DEFAULT 1,            -- logic nâng cấp tương thự thẻ
    quantity INT NOT NULL DEFAULT 1,         -- Số lượng của vũ khí này
    equipped_card_id INT DEFAULT NULL,       -- Nếu vũ khí đã được gắn vào thẻ (player_cards.id)
    slot_number INT DEFAULT NULL,            -- Số slot (ví dụ: slot 1, 2, 3)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (weapon_key) REFERENCES weapon_templates(weapon_key),
    FOREIGN KEY (equipped_card_id) REFERENCES player_cards(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 6. Bảng player_active_setup: Cấu hình trang bị (1 thẻ + 3 vũ khí)
-- --------------------------------------------------
DROP TABLE IF EXISTS player_active_setup;
CREATE TABLE player_active_setup (
    player_id BIGINT PRIMARY KEY,         -- Khóa ngoại đến players
    active_card_id INT NOT NULL,           -- ID của thẻ chiến chính từ player_cards
    weapon_slot1 INT DEFAULT NULL,         -- ID của vũ khí gắn vào slot 1 (player_weapons.id)
    weapon_slot2 INT DEFAULT NULL,         -- ID của vũ khí gắn vào slot 2
    weapon_slot3 INT DEFAULT NULL,         -- ID của vũ khí gắn vào slot 3
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (active_card_id) REFERENCES player_cards(id),
    FOREIGN KEY (weapon_slot1) REFERENCES player_weapons(id),
    FOREIGN KEY (weapon_slot2) REFERENCES player_weapons(id),
    FOREIGN KEY (weapon_slot3) REFERENCES player_weapons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 7. Bảng coin_transactions: Lịch sử giao dịch ryo (両)
-- --------------------------------------------------
DROP TABLE IF EXISTS coin_transactions;
CREATE TABLE coin_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT NOT NULL,          -- Khóa ngoại đến players
    `change` INT NOT NULL,                -- Số ryo thay đổi (dương: cộng, âm: trừ)
    reason VARCHAR(255),                -- Mô tả giao dịch (ví dụ: "Mở gacha basic", "PK thắng", "Gift card", ...)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 8. Bảng gacha_logs: Lịch sử mở thẻ (gacha)
-- --------------------------------------------------
DROP TABLE IF EXISTS gacha_logs;
CREATE TABLE gacha_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT NOT NULL,          -- Khóa ngoại đến players
    pack_type ENUM('basic', 'advanced', 'elite') NOT NULL, -- Loại gói mở thẻ
    card_key VARCHAR(50) NOT NULL,       -- Thẻ nhận được (khóa ngoại đến card_templates)
    coin_cost INT NOT NULL,              -- Số ryo tiêu dùng
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (card_key) REFERENCES card_templates(card_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 9. Bảng pk_battles: Lịch sử trận PK (đấu với người chơi)
-- --------------------------------------------------
DROP TABLE IF EXISTS pk_battles;
CREATE TABLE pk_battles (
    battle_id INT AUTO_INCREMENT PRIMARY KEY,
    attacker_id BIGINT NOT NULL,          -- Người tấn công (khóa ngoại đến players)
    defender_id BIGINT NOT NULL,          -- Người bị tấn công (khóa ngoại đến players)
    attacker_card_id INT NOT NULL,        -- Thẻ của người tấn công (khóa ngoại đến player_cards)
    defender_card_id INT NOT NULL,        -- Thẻ của người bị tấn công (khóa ngoại đến player_cards)
    result ENUM('win', 'loss', 'draw') NOT NULL,  -- Kết quả trận đấu từ góc nhìn người tấn công
    attacker_rank_change INT NOT NULL DEFAULT 0,  -- Thay đổi điểm rank của người tấn công
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attacker_id) REFERENCES players(player_id),
    FOREIGN KEY (defender_id) REFERENCES players(player_id),
    FOREIGN KEY (attacker_card_id) REFERENCES player_cards(id),
    FOREIGN KEY (defender_card_id) REFERENCES player_cards(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------
-- 10. Bảng gift_log: Lịch sử tặng thẻ (gift) của Dev/Admin
-- --------------------------------------------------
DROP TABLE IF EXISTS gift_log;
CREATE TABLE gift_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    giver_id BIGINT DEFAULT NULL,       -- Người tặng (Dev/Admin); có thể NULL nếu tự động
    receiver_id BIGINT NOT NULL,          -- Người nhận (khóa ngoại đến players)
    card_key VARCHAR(50) NOT NULL,        -- Thẻ được tặng (khóa ngoại đến card_templates)
    message TEXT,                         -- Lời nhắn kèm (nếu có)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (receiver_id) REFERENCES players(player_id),
    FOREIGN KEY (card_key) REFERENCES card_templates(card_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

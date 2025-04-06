CREATE TABLE IF NOT EXISTS gacha_pity_counter (
    player_id BIGINT NOT NULL,
    pack_type VARCHAR(50) NOT NULL,
    counter INT NOT NULL DEFAULT 0,
    PRIMARY KEY (player_id, pack_type),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

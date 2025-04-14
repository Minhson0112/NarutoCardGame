DROP TABLE IF EXISTS `daily_tasks`;

CREATE TABLE `daily_tasks` (
  `player_id` BIGINT NOT NULL,
  `mission_date` DATE NOT NULL,              -- Ngày hiện tại của nhiệm vụ hằng ngày, dùng để reset bộ đếm sau mỗi ngày
  `fight_win_count` INT NOT NULL DEFAULT 0,    -- Số lần chiến thắng khi dùng lệnh fight
  `fightwith_count` INT NOT NULL DEFAULT 0,    -- Số lần dùng lệnh fightwith
  `minigame_count` INT NOT NULL DEFAULT 0,     -- Số lần chơi minigame
  `shop_buy_count` INT NOT NULL DEFAULT 0,     -- Số lần mua trong cửa hàng
  `shop_sell_count` INT NOT NULL DEFAULT 0,    -- Số lần bán trong cửa hàng
  `stage_clear_count` INT NOT NULL DEFAULT 0,  -- Số lần vượt ải
  PRIMARY KEY (`player_id`),
  CONSTRAINT `fk_daily_tasks_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

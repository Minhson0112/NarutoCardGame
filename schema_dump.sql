SET FOREIGN_KEY_CHECKS=0;
-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: naruto_card_game
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `card_templates`
--

DROP TABLE IF EXISTS `card_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card_templates` (
  `card_key` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `tier` enum('Genin','Chunin','Jounin','Kage','Legendary') NOT NULL,
  `element` varchar(20) DEFAULT NULL,
  `base_power` int DEFAULT NULL,
  `image_url` text,
  `sell_price` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`card_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `challenges`
--

DROP TABLE IF EXISTS `challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `challenges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `card_name` varchar(100) NOT NULL,
  `card_strength` int NOT NULL,
  `image_url_key` varchar(255) NOT NULL,
  `narrative` text,
  `bonus_ryo` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coin_transactions`
--

DROP TABLE IF EXISTS `coin_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coin_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` bigint NOT NULL,
  `change` int NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `coin_transactions_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_claim_log`
--

DROP TABLE IF EXISTS `daily_claim_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_claim_log` (
  `player_id` bigint NOT NULL,
  `claim_date` date NOT NULL,
  PRIMARY KEY (`player_id`,`claim_date`),
  CONSTRAINT `daily_claim_log_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gacha_logs`
--

DROP TABLE IF EXISTS `gacha_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gacha_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` bigint NOT NULL,
  `pack_type` enum('basic','advanced','elite') NOT NULL,
  `card_key` varchar(50) NOT NULL,
  `coin_cost` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `card_key` (`card_key`),
  CONSTRAINT `gacha_logs_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `gacha_logs_ibfk_2` FOREIGN KEY (`card_key`) REFERENCES `card_templates` (`card_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gacha_pity_counter`
--

DROP TABLE IF EXISTS `gacha_pity_counter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gacha_pity_counter` (
  `player_id` bigint NOT NULL,
  `pack_type` varchar(50) NOT NULL,
  `counter` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`player_id`,`pack_type`),
  CONSTRAINT `gacha_pity_counter_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gifcode`
--

DROP TABLE IF EXISTS `gifcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gifcode` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gif_code` varchar(100) NOT NULL,
  `gif_name` varchar(255) NOT NULL,
  `bonus_ryo` int DEFAULT NULL,
  `card_key` varchar(50) DEFAULT NULL,
  `weapon_key` varchar(50) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_card_key` (`card_key`),
  KEY `fk_weapon_key` (`weapon_key`),
  CONSTRAINT `fk_card_key` FOREIGN KEY (`card_key`) REFERENCES `card_templates` (`card_key`),
  CONSTRAINT `fk_weapon_key` FOREIGN KEY (`weapon_key`) REFERENCES `weapon_templates` (`weapon_key`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gifcode_log`
--

DROP TABLE IF EXISTS `gifcode_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gifcode_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` bigint NOT NULL,
  `gifcode_id` int NOT NULL,
  `rewarded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_log_player` (`player_id`),
  KEY `fk_log_gifcode` (`gifcode_id`),
  CONSTRAINT `fk_log_gifcode` FOREIGN KEY (`gifcode_id`) REFERENCES `gifcode` (`id`),
  CONSTRAINT `fk_log_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gift_log`
--

DROP TABLE IF EXISTS `gift_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gift_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `giver_id` bigint DEFAULT NULL,
  `receiver_id` bigint NOT NULL,
  `card_key` varchar(50) NOT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `receiver_id` (`receiver_id`),
  KEY `card_key` (`card_key`),
  CONSTRAINT `gift_log_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `gift_log_ibfk_2` FOREIGN KEY (`card_key`) REFERENCES `card_templates` (`card_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pk_battles`
--

DROP TABLE IF EXISTS `pk_battles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pk_battles` (
  `battle_id` int NOT NULL AUTO_INCREMENT,
  `attacker_id` bigint NOT NULL,
  `defender_id` bigint NOT NULL,
  `attacker_card_id` int NOT NULL,
  `defender_card_id` int NOT NULL,
  `result` enum('win','loss','draw') NOT NULL,
  `attacker_rank_change` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`battle_id`),
  KEY `attacker_id` (`attacker_id`),
  KEY `defender_id` (`defender_id`),
  KEY `attacker_card_id` (`attacker_card_id`),
  KEY `defender_card_id` (`defender_card_id`),
  CONSTRAINT `pk_battles_ibfk_1` FOREIGN KEY (`attacker_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `pk_battles_ibfk_2` FOREIGN KEY (`defender_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `pk_battles_ibfk_3` FOREIGN KEY (`attacker_card_id`) REFERENCES `player_cards` (`id`),
  CONSTRAINT `pk_battles_ibfk_4` FOREIGN KEY (`defender_card_id`) REFERENCES `player_cards` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_active_setup`
--

DROP TABLE IF EXISTS `player_active_setup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_active_setup` (
  `player_id` bigint NOT NULL,
  `active_card_id` int DEFAULT NULL,
  `weapon_slot1` int DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`player_id`),
  KEY `active_card_id` (`active_card_id`),
  KEY `weapon_slot1` (`weapon_slot1`),
  CONSTRAINT `player_active_setup_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `player_active_setup_ibfk_2` FOREIGN KEY (`active_card_id`) REFERENCES `player_cards` (`id`),
  CONSTRAINT `player_active_setup_ibfk_3` FOREIGN KEY (`weapon_slot1`) REFERENCES `player_weapons` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_cards`
--

DROP TABLE IF EXISTS `player_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` bigint NOT NULL,
  `card_key` varchar(50) NOT NULL,
  `level` int NOT NULL DEFAULT '1',
  `quantity` int NOT NULL DEFAULT '1',
  `equipped` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `card_key` (`card_key`),
  CONSTRAINT `player_cards_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `player_cards_ibfk_2` FOREIGN KEY (`card_key`) REFERENCES `card_templates` (`card_key`)
) ENGINE=InnoDB AUTO_INCREMENT=470 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_weapons`
--

DROP TABLE IF EXISTS `player_weapons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_weapons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` bigint NOT NULL,
  `weapon_key` varchar(50) NOT NULL,
  `level` int NOT NULL DEFAULT '1',
  `quantity` int NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `equipped` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `weapon_key` (`weapon_key`),
  CONSTRAINT `player_weapons_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
  CONSTRAINT `player_weapons_ibfk_2` FOREIGN KEY (`weapon_key`) REFERENCES `weapon_templates` (`weapon_key`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `player_id` bigint NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `coin_balance` int NOT NULL DEFAULT '0',
  `rank_points` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `highest_rank_points` int NOT NULL DEFAULT '0',
  `winning_streak` int NOT NULL DEFAULT '0',
  `challenge_id` int DEFAULT NULL,
  PRIMARY KEY (`player_id`),
  KEY `fk_challenge_id` (`challenge_id`),
  CONSTRAINT `fk_challenge_id` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weapon_templates`
--

DROP TABLE IF EXISTS `weapon_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weapon_templates` (
  `weapon_key` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `grade` enum('Normal','Rare','Legendary') NOT NULL,
  `bonus_power` int DEFAULT NULL,
  `image_url` text,
  `sell_price` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`weapon_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-12 12:14:18
SET FOREIGN_KEY_CHECKS=1;


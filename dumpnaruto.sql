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
-- Dumping data for table `card_templates`
--

LOCK TABLES `card_templates` WRITE;
/*!40000 ALTER TABLE `card_templates` DISABLE KEYS */;
INSERT INTO `card_templates` VALUES ('Aburame_Shino','Aburame Shino','Genin','Phong',70,'shino',3000,'2025-04-05 04:13:56'),('Akatsuki_Itachi','Akatsuki Itachi','Legendary','Ho╠ëa',1000,'akatsukiitachi',500000,'2025-04-05 04:13:56'),('Akimichi_Choji','Akimichi Choji','Genin','Th├┤╠ë',140,'choji',3000,'2025-04-05 04:13:56'),('Chunin_Kakashi','Chunin Kakashi','Chunin','L├┤i',380,'chuninkakashi',20000,'2025-04-05 04:13:56'),('Deidara','Deidara','Chunin','Th├┤╠ë',360,'deidara',20000,'2025-04-05 04:13:56'),('Gaara','Gaara','Chunin','Th├┤╠ë',370,'gaara',20000,'2025-04-05 04:13:56'),('Gengetsu','Gengetsu','Jounin','Thu╠ëy',490,'gengetsu',80000,'2025-04-05 04:13:56'),('Haku','Haku','Legendary','Thu╠ëy',870,'haku',500000,'2025-04-05 04:13:56'),('Haruno_Sakura','Haruno Sakura','Genin','Thu╠ëy',80,'sakura',3000,'2025-04-05 04:13:56'),('Hatake_Kakashi','Hatake Kakashi','Legendary','L├┤i',890,'kakashi',500000,'2025-04-05 04:13:56'),('Hidan','Hidan','Chunin','Th├┤╠ë',300,'hidan',20000,'2025-04-05 04:13:56'),('Hokage_Kakashi','Hokage Kakashi','Kage','Thß╗ò',650,'hokagekakashi',200000,'2025-04-05 04:13:56'),('Hyuga_Hinata','Hyuga Hinata','Genin','Th├¬╠ë',100,'hinata',3000,'2025-04-05 04:13:56'),('Hyuga_Neji','Hyuga Neji','Chunin','Th├¬╠ë',250,'neji',20000,'2025-04-05 04:13:56'),('Inuzuka_Kiba','Inuzuka Kiba','Genin','Th├┤╠ë',130,'kiba',3000,'2025-04-05 04:13:56'),('Jiraiya','Jiraiya','Kage','Ho╠ëa',730,'jiraiya',200000,'2025-04-05 04:13:56'),('Kakuzu','Kakuzu','Chunin','Th├┤╠ë',390,'kakuzu',20000,'2025-04-05 04:13:56'),('Kankuro','Kankuro','Genin','Ho╠ëa',60,'kankuro',3000,'2025-04-05 04:13:56'),('Killer_Bee','Killer Bee','Jounin','Phong',500,'bee',80000,'2025-04-05 04:13:56'),('Kimimaro','Kimimaro','Chunin','Thß╗ò',310,'kimimaro',20000,'2025-04-05 04:13:56'),('Kisame','Kisame','Jounin','Thu╠ëy',460,'kisame',80000,'2025-04-05 04:13:56'),('Konan','Konan','Jounin','Ho╠ëa',450,'konan',80000,'2025-04-05 04:13:56'),('Konohamaru','Konohamaru','Genin','Ho╠ëa',200,'konohamaru',3000,'2025-04-05 04:13:56'),('Kushina','Kushina','Chunin','Phong',400,'kushina',20000,'2025-04-05 04:13:56'),('Kyuubi_Naruto','Kyuubi Naruto','Jounin','Phong',590,'9naruto',80000,'2025-04-05 04:13:56'),('Might_Guy','Might Guy','Kage','Th├¬╠ë',670,'guy',200000,'2025-04-05 04:13:56'),('Minato','Minato','Kage','L├┤i',740,'minato',200000,'2025-04-05 04:13:56'),('Momochi_Zabuza','Momochi Zabuza','Genin','Thu╠ëy',170,'zabuza',3000,'2025-04-05 04:13:56'),('Nara_Shikamaru','Nara Shikamaru','Chunin','Th├┤╠ë',260,'shikamaru',20000,'2025-04-05 04:13:56'),('Nohara_Rin','Nohara Rin','Chunin','Thu╠ëy',260,'rin',20000,'2025-04-05 04:13:56'),('Onoki','Onoki','Kage','Th├┤╠ë',690,'onoki',200000,'2025-04-05 04:13:56'),('Orochimaru','Orochimaru','Kage','Th├┤╠ë',720,'orochimaru',200000,'2025-04-05 04:13:56'),('Pain','Pain','Jounin','Phong',570,'pain',80000,'2025-04-05 04:13:56'),('RaikageIII','RaikageIII','Jounin','L├┤i',520,'raikage',80000,'2025-04-05 04:13:56'),('Rock_Lee','Rock Lee','Chunin','Th├¬╠ë',275,'lee',20000,'2025-04-05 04:13:56'),('Sarutobi_Asuma','Sarutobi Asuma','Chunin','Phong',290,'asuma',20000,'2025-04-05 04:13:56'),('Sarutobi_Hiruzen','Sarutobi Hiruzen','Kage','Ho╠ëa',750,'hiruzen',200000,'2025-04-05 04:13:56'),('Sasori','Sasori','Chunin','Phong',320,'sasori',20000,'2025-04-05 04:13:56'),('Senju_Hashirama','Senju Hashirama','Kage','Ho╠ëa',800,'hashirama',200000,'2025-04-05 04:13:56'),('Senju_Tobirama','Senju Tobirama','Kage','Th├¬╠ë',760,'tobirama',200000,'2025-04-05 04:13:56'),('Shimura_Danzo','Shimura Danzo','Legendary','Ho╠ëa',850,'danzo',500000,'2025-04-05 04:13:56'),('Six_Paths_Pain','Six Paths Pain','Legendary','Phong',950,'6pain',500000,'2025-04-05 04:13:56'),('Susanoo_Sasuke','Susanoo Sasuke','Legendary','Hß╗Åa',920,'susanoosasuke',500000,'2025-04-05 04:13:56'),('Temari','Temari','Genin','Phong',120,'temari',3000,'2025-04-05 04:13:56'),('TenTen','TenTen','Genin','Phong',53,'tenten',3000,'2025-04-05 04:13:56'),('Terumi_Mei','Terumi Mei','Kage','Thß╗ºy',700,'mei',200000,'2025-04-05 04:13:56'),('Tsunade','Tsunade','Kage','Thu╠ëy',710,'tsunade',200000,'2025-04-05 04:13:56'),('Uchiha_Itachi','Uchiha Itachi','Jounin','Ho╠ëa',530,'itachi',80000,'2025-04-05 04:13:56'),('Uchiha_Madara','Uchiha Madara','Kage','Ho╠ëa',780,'madara',200000,'2025-04-05 04:13:56'),('Uchiha_Obito','Uchiha Obito','Jounin','Ho╠ëa',480,'obito',80000,'2025-04-05 04:13:56'),('Uchiha_Sasuke','Uchiha Sasuke','Jounin','Ho╠ëa',590,'sasuke',80000,'2025-04-05 04:13:56'),('Umino_Iruka','Umino Iruka','Genin','Ho╠ëa',160,'iruka',3000,'2025-04-05 04:13:56'),('Uzumaki_Nagato','Uzumaki Nagato','Kage','Thu╠ëy',680,'nagato',200000,'2025-04-05 04:13:56'),('Uzumaki_Naruto','Uzumaki Naruto','Legendary','Phong',920,'naruto',500000,'2025-04-05 04:13:56'),('Yagura','Yagura','Chunin','Thu╠ëy',270,'yagura',20000,'2025-04-05 04:13:56'),('Yakushi_Kabuto','Yakushi Kabuto','Chunin','Thß╗ò',340,'kabuto',20000,'2025-04-05 04:13:56'),('Yamanaka_Ino','Yamanaka Ino','Genin','Thu╠ëy',50,'ino',3000,'2025-04-05 04:13:56'),('Yamanaka_Sai','Yamanaka Sai','Chunin','Ho╠ëa',330,'sai',20000,'2025-04-05 04:13:56'),('Yamato','Yamato','Chunin','Thu╠ëy',350,'yamato',20000,'2025-04-05 04:13:56'),('Yuhi_Kurenai','Yuhi Kurenai','Chunin','Phong',280,'kurenai',20000,'2025-04-05 04:13:56');
/*!40000 ALTER TABLE `card_templates` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `coin_transactions`
--

LOCK TABLES `coin_transactions` WRITE;
/*!40000 ALTER TABLE `coin_transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `coin_transactions` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `daily_claim_log`
--

LOCK TABLES `daily_claim_log` WRITE;
/*!40000 ALTER TABLE `daily_claim_log` DISABLE KEYS */;
INSERT INTO `daily_claim_log` VALUES (549152266712645645,'2025-04-05'),(549152266712645645,'2025-04-06'),(708004187644100649,'2025-04-06'),(751649103825469553,'2025-04-05'),(826672630785638410,'2025-04-05'),(995730123166851102,'2025-04-05'),(995730123166851102,'2025-04-06'),(1177638956767129730,'2025-04-05'),(1177638956767129730,'2025-04-06'),(1282732455157305477,'2025-04-06');
/*!40000 ALTER TABLE `daily_claim_log` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `gacha_logs`
--

LOCK TABLES `gacha_logs` WRITE;
/*!40000 ALTER TABLE `gacha_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `gacha_logs` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `gacha_pity_counter`
--

LOCK TABLES `gacha_pity_counter` WRITE;
/*!40000 ALTER TABLE `gacha_pity_counter` DISABLE KEYS */;
INSERT INTO `gacha_pity_counter` VALUES (549152266712645645,'card_advanced',0),(549152266712645645,'card_basic',1),(549152266712645645,'card_elite',0),(708004187644100649,'card_advanced',0),(708004187644100649,'card_basic',1),(708004187644100649,'card_elite',1),(751649103825469553,'card_advanced',3),(751649103825469553,'card_basic',8),(751649103825469553,'card_elite',4),(826672630785638410,'card_advanced',0),(826672630785638410,'card_basic',0),(826672630785638410,'card_elite',0),(995730123166851102,'card_advanced',5),(995730123166851102,'card_basic',2),(995730123166851102,'card_elite',1),(1177638956767129730,'card_advanced',0),(1177638956767129730,'card_basic',0),(1177638956767129730,'card_elite',0),(1282732455157305477,'card_advanced',0),(1282732455157305477,'card_basic',1),(1282732455157305477,'card_elite',0);
/*!40000 ALTER TABLE `gacha_pity_counter` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `gift_log`
--

LOCK TABLES `gift_log` WRITE;
/*!40000 ALTER TABLE `gift_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `gift_log` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `pk_battles`
--

LOCK TABLES `pk_battles` WRITE;
/*!40000 ALTER TABLE `pk_battles` DISABLE KEYS */;
/*!40000 ALTER TABLE `pk_battles` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `player_active_setup`
--

LOCK TABLES `player_active_setup` WRITE;
/*!40000 ALTER TABLE `player_active_setup` DISABLE KEYS */;
INSERT INTO `player_active_setup` VALUES (549152266712645645,NULL,NULL,'2025-04-05 13:17:35'),(708004187644100649,161,46,'2025-04-06 15:44:15'),(751649103825469553,NULL,NULL,'2025-04-05 13:07:14'),(826672630785638410,NULL,NULL,'2025-04-05 13:18:00'),(995730123166851102,160,49,'2025-04-06 15:40:11'),(1177638956767129730,140,33,'2025-04-06 14:25:13'),(1282732455157305477,NULL,NULL,'2025-04-06 10:25:04');
/*!40000 ALTER TABLE `player_active_setup` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_cards`
--

LOCK TABLES `player_cards` WRITE;
/*!40000 ALTER TABLE `player_cards` DISABLE KEYS */;
INSERT INTO `player_cards` VALUES (1,995730123166851102,'Kankuro',1,2,0,'2025-04-05 12:43:26'),(2,995730123166851102,'TenTen',1,1,0,'2025-04-05 12:45:20'),(3,995730123166851102,'Orochimaru',1,1,0,'2025-04-05 12:46:25'),(4,995730123166851102,'Onoki',1,6,0,'2025-04-05 12:47:29'),(5,995730123166851102,'Kushina',1,1,0,'2025-04-05 12:48:14'),(6,995730123166851102,'Haku',1,1,0,'2025-04-05 12:48:21'),(7,995730123166851102,'Hyuga_Hinata',1,1,0,'2025-04-05 13:04:55'),(8,995730123166851102,'Nohara_Rin',1,1,0,'2025-04-05 13:04:59'),(9,995730123166851102,'Konohamaru',1,1,0,'2025-04-05 13:05:07'),(10,995730123166851102,'Akatsuki_Itachi',1,1,0,'2025-04-05 13:05:14'),(11,751649103825469553,'Nara_Shikamaru',1,5,0,'2025-04-05 13:08:16'),(14,549152266712645645,'TenTen',1,1,0,'2025-04-05 13:18:50'),(39,1177638956767129730,'Umino_Iruka',1,6,0,'2025-04-05 13:28:21'),(40,751649103825469553,'Pain',1,2,0,'2025-04-05 13:29:51'),(41,751649103825469553,'Yagura',1,1,0,'2025-04-05 13:31:14'),(42,751649103825469553,'Uzumaki_Naruto',1,1,0,'2025-04-05 13:31:23'),(43,1177638956767129730,'Yamanaka_Ino',1,5,0,'2025-04-05 13:32:36'),(44,1177638956767129730,'Uchiha_Sasuke',1,1,0,'2025-04-05 13:32:56'),(45,1177638956767129730,'Pain',1,4,0,'2025-04-05 13:33:52'),(46,751649103825469553,'Aburame_Shino',1,3,0,'2025-04-05 13:34:18'),(47,751649103825469553,'Konan',1,2,0,'2025-04-05 13:34:22'),(48,1177638956767129730,'Yamato',1,1,0,'2025-04-05 13:34:58'),(49,1177638956767129730,'Sasori',1,3,0,'2025-04-05 13:35:46'),(50,1177638956767129730,'Temari',1,6,0,'2025-04-05 13:36:01'),(51,1177638956767129730,'Konohamaru',1,6,0,'2025-04-05 13:36:12'),(52,751649103825469553,'Rock_Lee',1,2,0,'2025-04-05 13:36:16'),(53,1177638956767129730,'Kakuzu',1,1,0,'2025-04-05 13:37:51'),(54,1177638956767129730,'Yuhi_Kurenai',1,1,0,'2025-04-05 13:38:12'),(55,751649103825469553,'Senju_Tobirama',1,1,0,'2025-04-05 13:38:25'),(56,1177638956767129730,'Tsunade',1,1,0,'2025-04-05 13:38:58'),(57,1177638956767129730,'Aburame_Shino',1,6,0,'2025-04-05 13:40:42'),(58,1177638956767129730,'Deidara',1,1,0,'2025-04-05 13:40:50'),(59,1177638956767129730,'Hidan',1,2,0,'2025-04-05 13:41:01'),(60,1177638956767129730,'Akimichi_Choji',1,3,0,'2025-04-05 13:41:14'),(61,1177638956767129730,'Momochi_Zabuza',1,3,0,'2025-04-05 13:41:43'),(62,751649103825469553,'Minato',1,1,0,'2025-04-05 13:41:46'),(63,1177638956767129730,'Inuzuka_Kiba',1,2,0,'2025-04-05 13:42:00'),(64,1177638956767129730,'Chunin_Kakashi',1,3,0,'2025-04-05 13:42:23'),(65,1177638956767129730,'Konan',1,2,0,'2025-04-05 13:42:40'),(66,1177638956767129730,'TenTen',1,3,0,'2025-04-05 13:42:50'),(67,1177638956767129730,'Kankuro',1,3,0,'2025-04-05 13:42:56'),(68,1177638956767129730,'Kimimaro',1,2,0,'2025-04-05 13:43:34'),(69,1177638956767129730,'Gengetsu',1,2,0,'2025-04-05 13:44:09'),(70,1177638956767129730,'Hatake_Kakashi',1,1,0,'2025-04-05 13:44:24'),(71,1177638956767129730,'Sarutobi_Asuma',1,1,0,'2025-04-05 13:47:17'),(72,751649103825469553,'Gaara',1,1,0,'2025-04-06 07:09:35'),(73,995730123166851102,'Pain',1,1,0,'2025-04-06 07:24:45'),(74,1177638956767129730,'RaikageIII',1,1,0,'2025-04-06 08:14:25'),(75,995730123166851102,'Umino_Iruka',1,1,0,'2025-04-06 08:33:12'),(76,708004187644100649,'Konan',1,3,0,'2025-04-06 08:59:28'),(77,549152266712645645,'Yakushi_Kabuto',1,1,0,'2025-04-06 08:59:44'),(78,549152266712645645,'Haku',1,1,0,'2025-04-06 08:59:59'),(79,708004187644100649,'Yamanaka_Ino',1,2,0,'2025-04-06 09:00:11'),(80,549152266712645645,'Haruno_Sakura',1,2,0,'2025-04-06 09:01:11'),(81,549152266712645645,'RaikageIII',1,1,0,'2025-04-06 09:01:17'),(82,549152266712645645,'Uzumaki_Naruto',1,2,0,'2025-04-06 09:01:38'),(85,708004187644100649,'Six_Paths_Pain',1,3,0,'2025-04-06 09:03:21'),(86,708004187644100649,'Uchiha_Sasuke',1,4,0,'2025-04-06 09:03:29'),(87,708004187644100649,'Inuzuka_Kiba',1,3,0,'2025-04-06 09:03:36'),(88,1177638956767129730,'Nohara_Rin',1,1,0,'2025-04-06 09:07:59'),(90,708004187644100649,'Akatsuki_Itachi',1,1,0,'2025-04-06 09:08:37'),(91,549152266712645645,'Konohamaru',1,1,0,'2025-04-06 09:09:17'),(92,549152266712645645,'Uchiha_Itachi',1,2,0,'2025-04-06 09:09:21'),(93,549152266712645645,'Uchiha_Sasuke',1,2,0,'2025-04-06 09:09:26'),(94,549152266712645645,'Yamanaka_Ino',1,1,0,'2025-04-06 09:09:30'),(95,549152266712645645,'Yamanaka_Sai',1,1,0,'2025-04-06 09:09:36'),(96,1177638956767129730,'Uchiha_Itachi',1,1,0,'2025-04-06 09:09:41'),(97,549152266712645645,'Deidara',1,1,0,'2025-04-06 09:09:52'),(98,549152266712645645,'Uchiha_Madara',1,1,0,'2025-04-06 09:10:06'),(99,549152266712645645,'Uzumaki_Nagato',1,1,0,'2025-04-06 09:10:33'),(100,549152266712645645,'Might_Guy',1,1,0,'2025-04-06 09:10:41'),(102,708004187644100649,'Sarutobi_Asuma',1,2,0,'2025-04-06 09:13:56'),(103,708004187644100649,'Terumi_Mei',1,2,0,'2025-04-06 09:14:29'),(104,708004187644100649,'Kyuubi_Naruto',1,5,0,'2025-04-06 09:14:33'),(106,708004187644100649,'Uzumaki_Nagato',1,1,0,'2025-04-06 09:16:02'),(107,708004187644100649,'Shimura_Danzo',1,3,0,'2025-04-06 09:16:13'),(108,708004187644100649,'Hyuga_Neji',1,2,0,'2025-04-06 09:18:56'),(109,708004187644100649,'Temari',1,1,0,'2025-04-06 09:24:27'),(110,708004187644100649,'Hokage_Kakashi',1,3,0,'2025-04-06 09:24:33'),(112,708004187644100649,'Haku',1,3,0,'2025-04-06 09:25:02'),(114,708004187644100649,'Uchiha_Itachi',1,1,0,'2025-04-06 09:25:12'),(117,708004187644100649,'Kisame',1,3,0,'2025-04-06 09:25:37'),(118,708004187644100649,'RaikageIII',1,2,0,'2025-04-06 09:25:40'),(120,708004187644100649,'Minato',1,1,0,'2025-04-06 09:26:49'),(121,708004187644100649,'Uchiha_Madara',1,3,0,'2025-04-06 09:27:04'),(123,708004187644100649,'Uzumaki_Naruto',1,4,0,'2025-04-06 09:27:39'),(132,1282732455157305477,'Hyuga_Hinata',1,1,0,'2025-04-06 10:25:27'),(134,1177638956767129730,'Hyuga_Hinata',1,1,0,'2025-04-06 12:40:55'),(135,1177638956767129730,'Yagura',1,2,0,'2025-04-06 12:42:01'),(136,1177638956767129730,'Rock_Lee',1,1,0,'2025-04-06 12:42:48'),(137,1177638956767129730,'Senju_Hashirama',1,1,0,'2025-04-06 12:43:52'),(138,1177638956767129730,'Hyuga_Neji',1,1,0,'2025-04-06 12:45:33'),(139,1177638956767129730,'Kisame',1,1,0,'2025-04-06 12:45:48'),(140,1177638956767129730,'Uzumaki_Naruto',1,2,1,'2025-04-06 12:46:01'),(141,1177638956767129730,'Yamanaka_Sai',1,1,0,'2025-04-06 12:51:02'),(142,1177638956767129730,'Haruno_Sakura',1,1,0,'2025-04-06 12:53:27'),(143,1177638956767129730,'Uchiha_Madara',1,1,0,'2025-04-06 12:53:34'),(144,751649103825469553,'Chunin_Kakashi',1,1,0,'2025-04-06 13:48:02'),(145,751649103825469553,'Hidan',1,1,0,'2025-04-06 13:48:06'),(146,751649103825469553,'Sarutobi_Asuma',1,1,0,'2025-04-06 13:48:11'),(147,751649103825469553,'Haku',1,1,0,'2025-04-06 13:48:13'),(148,751649103825469553,'Uchiha_Obito',1,1,0,'2025-04-06 13:48:16'),(149,751649103825469553,'Kyuubi_Naruto',1,1,0,'2025-04-06 13:48:21'),(150,751649103825469553,'Uchiha_Itachi',1,1,0,'2025-04-06 13:48:24'),(151,751649103825469553,'Six_Paths_Pain',1,1,0,'2025-04-06 13:48:27'),(152,751649103825469553,'Shimura_Danzo',1,2,0,'2025-04-06 13:48:40'),(153,751649103825469553,'Susanoo_Sasuke',1,1,0,'2025-04-06 13:49:00'),(154,1177638956767129730,'Killer_Bee',1,2,0,'2025-04-06 14:13:45'),(155,1177638956767129730,'Yakushi_Kabuto',1,1,0,'2025-04-06 14:14:49'),(156,1177638956767129730,'Shimura_Danzo',1,1,0,'2025-04-06 14:14:57'),(157,1177638956767129730,'Terumi_Mei',1,1,0,'2025-04-06 15:10:40'),(158,1177638956767129730,'Senju_Tobirama',1,1,0,'2025-04-06 15:11:06'),(160,995730123166851102,'Onoki',3,1,1,'2025-04-06 15:18:27'),(161,708004187644100649,'Akatsuki_Itachi',2,1,1,'2025-04-06 15:38:26'),(162,708004187644100649,'Six_Paths_Pain',2,1,0,'2025-04-06 15:40:25'),(163,549152266712645645,'Six_Paths_Pain',1,1,0,'2025-04-06 15:46:22'),(164,549152266712645645,'Nohara_Rin',1,1,0,'2025-04-06 15:46:40'),(165,549152266712645645,'Sarutobi_Asuma',1,1,0,'2025-04-06 15:46:58'),(166,708004187644100649,'Nara_Shikamaru',1,2,0,'2025-04-06 15:47:34'),(167,708004187644100649,'Akimichi_Choji',1,1,0,'2025-04-06 15:47:37'),(168,708004187644100649,'Kakuzu',1,1,0,'2025-04-06 15:47:39'),(169,549152266712645645,'Yuhi_Kurenai',1,1,0,'2025-04-06 15:52:16'),(170,549152266712645645,'Orochimaru',1,1,0,'2025-04-06 15:52:38'),(171,549152266712645645,'Hyuga_Hinata',1,1,0,'2025-04-06 15:52:58'),(172,549152266712645645,'Susanoo_Sasuke',1,1,0,'2025-04-06 15:53:08');
/*!40000 ALTER TABLE `player_cards` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_weapons`
--

LOCK TABLES `player_weapons` WRITE;
/*!40000 ALTER TABLE `player_weapons` DISABLE KEYS */;
INSERT INTO `player_weapons` VALUES (1,995730123166851102,'Shuriken',1,8,'2025-04-06 07:21:21',0),(2,995730123166851102,'Tansa',1,7,'2025-04-06 07:22:16',0),(3,995730123166851102,'Katana',1,3,'2025-04-06 07:22:23',0),(4,995730123166851102,'Knife',1,5,'2025-04-06 07:22:32',0),(5,995730123166851102,'Flail',1,6,'2025-04-06 07:22:36',0),(6,995730123166851102,'ChakraKnife',1,5,'2025-04-06 07:22:40',0),(7,995730123166851102,'Guandao',1,3,'2025-04-06 07:22:44',0),(8,995730123166851102,'Bow',1,6,'2025-04-06 07:22:52',0),(9,995730123166851102,'Kunai',1,6,'2025-04-06 07:22:59',0),(10,995730123166851102,'Kibaku',1,2,'2025-04-06 07:23:09',0),(11,995730123166851102,'Samehada',1,4,'2025-04-06 07:23:15',0),(12,995730123166851102,'Tessen',1,1,'2025-04-06 07:23:29',0),(13,995730123166851102,'Suna',1,1,'2025-04-06 07:24:06',0),(14,751649103825469553,'ChakraKnife',1,5,'2025-04-06 07:54:00',0),(15,751649103825469553,'Kibaku',1,15,'2025-04-06 07:54:05',0),(16,751649103825469553,'Katana',1,16,'2025-04-06 07:54:07',0),(17,751649103825469553,'Flail',1,6,'2025-04-06 07:59:59',0),(18,751649103825469553,'Kunai',1,10,'2025-04-06 08:00:04',0),(19,751649103825469553,'Guandao',1,7,'2025-04-06 08:00:22',0),(20,751649103825469553,'Bow',1,7,'2025-04-06 08:00:32',0),(21,751649103825469553,'Knife',1,6,'2025-04-06 08:00:35',0),(22,751649103825469553,'Shuriken',1,8,'2025-04-06 08:00:46',0),(23,751649103825469553,'Tansa',1,6,'2025-04-06 08:01:26',0),(24,751649103825469553,'Gudodama',1,1,'2025-04-06 08:01:43',0),(25,751649103825469553,'Suna',1,1,'2025-04-06 08:01:52',0),(26,751649103825469553,'Sansaju',1,2,'2025-04-06 08:02:05',0),(27,1177638956767129730,'Flail',1,3,'2025-04-06 08:15:39',0),(28,1177638956767129730,'ChakraKnife',1,2,'2025-04-06 08:15:59',0),(29,1177638956767129730,'Knife',1,2,'2025-04-06 08:16:13',0),(30,1177638956767129730,'Shuriken',1,3,'2025-04-06 08:16:36',0),(31,1177638956767129730,'Katana',1,6,'2025-04-06 08:17:16',0),(32,1177638956767129730,'Bow',1,1,'2025-04-06 08:19:53',0),(33,1177638956767129730,'Tansa',1,3,'2025-04-06 08:20:16',1),(34,1177638956767129730,'Guandao',1,1,'2025-04-06 08:21:02',0),(35,995730123166851102,'Enma',1,1,'2025-04-06 08:21:08',0),(36,995730123166851102,'Rinnegan',1,1,'2025-04-06 08:21:36',0),(37,1177638956767129730,'Kibaku',1,1,'2025-04-06 08:46:57',0),(38,549152266712645645,'Flail',1,1,'2025-04-06 09:02:49',0),(39,549152266712645645,'Katana',1,1,'2025-04-06 09:02:57',0),(40,708004187644100649,'Knife',1,4,'2025-04-06 09:13:41',0),(41,708004187644100649,'Kunai',1,6,'2025-04-06 09:18:48',0),(42,708004187644100649,'Guandao',1,5,'2025-04-06 09:19:25',0),(43,708004187644100649,'Shuriken',1,3,'2025-04-06 09:20:23',0),(44,708004187644100649,'Kibaku',1,2,'2025-04-06 09:20:28',0),(45,708004187644100649,'Katana',1,2,'2025-04-06 09:20:36',0),(46,708004187644100649,'Samehada',1,1,'2025-04-06 09:21:06',1),(47,708004187644100649,'Sansaju',1,1,'2025-04-06 09:21:57',0),(48,708004187644100649,'Flail',1,2,'2025-04-06 09:24:05',0),(49,995730123166851102,'Samehada',2,1,'2025-04-06 15:39:49',1),(50,708004187644100649,'Tansa',1,2,'2025-04-06 15:41:10',0),(51,708004187644100649,'Bow',1,2,'2025-04-06 15:42:14',0);
/*!40000 ALTER TABLE `player_weapons` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (549152266712645645,'Hali',0,0,'2025-04-05 13:17:35','2025-04-06 15:53:08'),(708004187644100649,'Th├ánh Huß╗│nh',866000000,0,'2025-04-06 08:56:05','2025-04-06 15:47:45'),(751649103825469553,'namhaii',810920000,0,'2025-04-05 13:07:14','2025-04-06 13:49:00'),(826672630785638410,'Hnaytoibuon',1000000,0,'2025-04-05 13:18:00','2025-04-06 08:58:21'),(995730123166851102,'Minh Sãín',881480000,0,'2025-04-05 11:04:13','2025-04-06 08:33:12'),(1177638956767129730,'Hß║í M├óy ─É├íng I├¬uuuuu',84370000,0,'2025-04-05 13:25:58','2025-04-06 15:11:20'),(1282732455157305477,'Babyboo',0,0,'2025-04-06 10:25:04','2025-04-06 10:25:27');
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Dumping data for table `weapon_templates`
--

LOCK TABLES `weapon_templates` WRITE;
/*!40000 ALTER TABLE `weapon_templates` DISABLE KEYS */;
INSERT INTO `weapon_templates` VALUES ('Bow','Bow','Normal',210,'Bow210',500000,'2025-04-06 06:35:25'),('ChakraKnife','ChakraKnife','Normal',170,'ChakraKnife170',500000,'2025-04-06 06:35:25'),('Enma','Enma','Rare',480,'Enma480',1500000,'2025-04-06 06:35:25'),('Flail','Flail','Normal',220,'Flail220',500000,'2025-04-06 06:35:25'),('Guandao','Guandao','Normal',180,'Guandao180',500000,'2025-04-06 06:35:25'),('Gudodama','Gudodama','Legendary',700,'Gudodama700',4000000,'2025-04-06 06:35:25'),('Katana','Katana','Normal',190,'Katana190',500000,'2025-04-06 06:35:25'),('Kibaku','Kibaku','Normal',230,'Kibaku230',500000,'2025-04-06 06:35:25'),('Knife','Knife','Normal',160,'Knife160',500000,'2025-04-06 06:35:25'),('Kunai','Kunai','Normal',150,'Kunai150',500000,'2025-04-06 06:35:25'),('Rinnegan','Rinnegan','Legendary',600,'Rinnegan600',4000000,'2025-04-06 06:35:25'),('Samehada','Samehada','Rare',500,'Samehada500',1500000,'2025-04-06 06:35:25'),('Sansaju','Sansaju','Rare',440,'Sansaju440',1500000,'2025-04-06 06:35:25'),('Shuriken','Shuriken','Normal',200,'Shuriken200',500000,'2025-04-06 06:35:25'),('Suna','Suna','Rare',450,'Suna450',1500000,'2025-04-06 06:35:25'),('Tansa','Tansa','Normal',250,'Tansa250',500000,'2025-04-06 06:35:25'),('Tessen','Tessen','Rare',430,'Tessen430',1500000,'2025-04-06 06:35:25');
/*!40000 ALTER TABLE `weapon_templates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-06 16:37:30

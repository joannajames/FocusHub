-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (x86_64)
--
-- Host: 127.0.0.1    Database: study_spots_db
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `bu_user_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_img` varchar(500) DEFAULT NULL,
  `personal_tags` text,
  `courses` text,
  `bu_college` enum('CAS','COM','ENG','MET','CFA','CGS','SAR','CDS','SHA','Pardee','Questrom','Kilachand','Wheelock') DEFAULT NULL,
  `degree` varchar(255) DEFAULT NULL,
  `academic_level` enum('Undergrad','Grad','PhD') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_access` tinyint DEFAULT NULL,
  `admin_role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `bu_user_id` (`bu_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'jojames@bu.edu','jojames','joanna.png',NULL,'CS673','MET','Computer Science','Grad','2025-04-19 21:00:52','2025-04-30 19:35:04',1,'Backend Developer'),(2,'cmphilip@bu.edu','cmphilip','christal.png','Aesthetic, H2O Stations, Indie (Non-Chain), Low Traffic, Smiley Service','CS673, CS662','MET','Computer Science','Grad','2025-04-19 21:00:52','2025-04-30 19:35:04',1,'Database Manager'),(3,'zara87@bu.edu','zara87','zahra.png',NULL,'CS673','MET','Computer Science','Grad','2025-04-19 21:00:52','2025-04-30 19:35:04',1,'Security Specialist'),(4,'rdhoda@bu.edu','rdhodha','raessa.png',NULL,'CS673','MET','Computer Science','Grad','2025-04-19 21:00:52','2025-04-30 19:35:04',1,'Frontend Developer');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30 15:39:17

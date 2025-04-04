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
-- Table structure for table `spots`
--

DROP TABLE IF EXISTS `spots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spots` (
  `spot_id` int NOT NULL AUTO_INCREMENT,
  `spot_name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `open_early` enum('Yes','No') DEFAULT NULL,
  `open_late` enum('Yes','No') DEFAULT NULL,
  `default_img_url` varchar(500) DEFAULT NULL,
  `has_outlets` enum('Yes','No') DEFAULT NULL,
  `has_food` enum('Yes','No') DEFAULT NULL,
  `has_printing` enum('Yes','No') DEFAULT NULL,
  `has_prayer_space` enum('Yes','No') DEFAULT NULL,
  `average_rating` decimal(3,2) DEFAULT '0.00',
  `has_spacious_seating` enum('Yes','No') DEFAULT NULL,
  `has_meeting_rooms` enum('Yes','No') DEFAULT NULL,
  `on_campus` enum('Yes','No') DEFAULT NULL,
  PRIMARY KEY (`spot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spots`
--

LOCK TABLES `spots` WRITE;
/*!40000 ALTER TABLE `spots` DISABLE KEYS */;
INSERT INTO `spots` VALUES (1,'Mugar Library Floors 1-3','771 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','No',NULL,NULL,0.00,'Yes','Yes','Yes'),(2,'Mugar Library Floors 4-5','771 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','No',NULL,NULL,0.00,'Yes','No','Yes'),(3,'Pavement Coffee','736 Commonwealth Ave, Brookline, MA 02446',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(4,'CDS Building First Floor','665 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','Yes'),(5,'CDS Building Third Floor','665 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','No',NULL,NULL,0.00,'Yes','No','Yes'),(6,'CDS Building Fifth Floor','665 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','Yes','Yes'),(7,'Starbucks East End','700 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(8,'Starbucks West End','874 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(9,'Caffe Nero','1047 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(10,'Life Alive Cafe','888 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(11,'Howard Thurman Center','808 Commonwealth Ave, Brookline, MA 02446',NULL,NULL,NULL,'Yes','No',NULL,NULL,0.00,'Yes','No','Yes'),(12,'LGBTQIA+ Student Center','808 Commonwealth Ave, Brookline, MA 02446',NULL,NULL,NULL,'Yes','No',NULL,NULL,0.00,'No','No','Yes'),(13,'Innovate@BU','730 Commonwealth Ave, Brookline, MA 02446',NULL,NULL,NULL,'Yes','No',NULL,NULL,0.00,'Yes','No','Yes'),(14,'GSU','775 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','Yes'),(15,'BU Fitness & Recreation Center','915 Commonwealth Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'No','No','Yes'),(16,'Cafe Landwer','900 Beacon St, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'No','No','No'),(17,'Tatte Bakery & Cafe','1003 Beacon St, Brookline, MA 02446',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'No','No','No'),(18,'Pavement Coffee Fenway','1334 Boylston St, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(19,'Tatte Bakery & Cafe Fenway','1352 Boylston St, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'No','No','No'),(20,'Starbucks Fenway','142-148 Brookline Ave, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(21,'Caffe Nero Fenway','1375 Boylston St, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'Yes','No','No'),(22,'Phinista','96 Peterborough St, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'No','No','No'),(23,'The Sipping Room','132 Jersey St, Boston, MA 02215',NULL,NULL,NULL,'Yes','Yes',NULL,NULL,0.00,'No','No','No');
/*!40000 ALTER TABLE `spots` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-04 17:14:23

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
  `default_img` varchar(500) DEFAULT NULL,
  `has_outlets` tinyint DEFAULT NULL,
  `has_food` tinyint DEFAULT NULL,
  `has_printing` tinyint DEFAULT NULL,
  `has_prayer_space` tinyint DEFAULT NULL,
  `avg_rating` decimal(3,1) DEFAULT NULL,
  `has_spacious_seating` tinyint DEFAULT NULL,
  `has_meeting_rooms` tinyint DEFAULT NULL,
  `on_campus` tinyint DEFAULT NULL,
  PRIMARY KEY (`spot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spots`
--

LOCK TABLES `spots` WRITE;
/*!40000 ALTER TABLE `spots` DISABLE KEYS */;
INSERT INTO `spots` VALUES (1,'Mugar Library Floors 1-3','771 Commonwealth Ave, Boston, MA 02215','Mugar_1.png',1,2,1,2,4.1,1,1,1),(2,'Mugar Library Floors 4-5','771 Commonwealth Ave, Boston, MA 02215','Mugar_2.png',1,2,1,2,3.2,1,2,1),(3,'Pavement Coffee','736 Commonwealth Ave, Brookline, MA 02446','Pavement.png',1,1,2,2,4.0,1,2,2),(4,'CDS Building First Floor','665 Commonwealth Ave, Boston, MA 02215','CDS_1.png',1,1,1,2,3.0,1,1,1),(5,'CDS Building Third Floor','665 Commonwealth Ave, Boston, MA 02215','CDS_2.png',1,2,2,2,4.3,1,1,1),(6,'CDS Building Fifth Floor','665 Commonwealth Ave, Boston, MA 02215','CDS_3.png',1,1,1,2,4.5,1,1,1),(7,'Starbucks East End','700 Commonwealth Ave, Boston, MA 02215','Starbucks_1.png',1,1,2,2,2.3,1,2,2),(8,'Starbucks West End','874 Commonwealth Ave, Boston, MA 02215','Starbucks_2.png',1,1,2,2,2.3,1,2,2),(9,'Caffe Nero','1047 Commonwealth Ave, Boston, MA 02215','Nero_1.png',1,1,2,2,4.5,1,2,2),(10,'Life Alive Cafe','888 Commonwealth Ave, Boston, MA 02215','Life_Alive.png',1,1,2,2,4.5,1,2,2),(11,'Howard Thurman Center','808 Commonwealth Ave, Brookline, MA 02446','Howard.png',1,2,2,1,4.0,1,1,1),(12,'LGBTQIA+ Student Center','808 Commonwealth Ave, Brookline, MA 02446','LGBTQIA.png',1,2,2,2,4.0,2,1,1),(13,'Innovate@BU','730 Commonwealth Ave, Brookline, MA 02446','Innovate.png',1,2,2,2,5.0,1,1,1),(14,'GSU','775 Commonwealth Ave, Boston, MA 02215','GSU.png',1,1,1,1,4.0,1,2,1),(15,'BU Fitness & Recreation Center','915 Commonwealth Ave, Boston, MA 02215','Fitrec.png',1,1,2,2,2.5,2,2,1),(16,'Cafe Landwer','900 Beacon St, Boston, MA 02215','Landwer.png',1,1,2,2,3.2,2,2,2),(17,'Tatte Bakery & Cafe','1003 Beacon St, Brookline, MA 02446','Tatte_1.png',1,1,2,2,3.9,2,2,2),(18,'Pavement Coffee Fenway','1334 Boylston St, Boston, MA 02215','Pavement_2.png',1,1,2,2,3.5,1,2,2),(19,'Tatte Bakery & Cafe Fenway','1352 Boylston St, Boston, MA 02215','Tatte_2.png',1,1,2,2,4.0,2,2,2),(20,'Starbucks Fenway','142-148 Brookline Ave, Boston, MA 02215','Starbucks_3.png',1,1,1,2,2.5,1,2,2),(21,'Caffe Nero Fenway','1375 Boylston St, Boston, MA 02215','Nero_2.png',1,1,2,2,4.2,1,2,2),(22,'Phinista','96 Peterborough St, Boston, MA 02215','Phinista.png',1,1,1,2,4.0,2,2,2),(23,'The Sipping Room','132 Jersey St, Boston, MA 02215','Sipping_Room.png',1,1,2,2,3.0,2,2,2),(24,'CAS Pickering Library','2 Silber Way, Boston, MA 02215','Pickering.png',1,2,2,2,3.5,2,1,2),(25,'Science & Engineering Library','38 Cummington Mall, Boston, MA 02215','SandE.png',1,2,2,1,3.8,1,1,1),(26,'Marsh Chapel Meditation Room','735 Commonwealth Avenue, Boston, MA 02215','Marsh_Chapel.png',2,2,2,2,4.0,2,2,1),(27,'Questrom School of Business','595 Commonwealth Avenue, Boston, MA 02215','Questrom.png',1,1,1,2,4.5,1,1,2);
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

-- Dump completed on 2025-04-20 15:43:15

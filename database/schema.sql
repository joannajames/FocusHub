-- schema.sql

-- Table structure for table `users`
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `bu_user_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `profile_img_url` varchar(500) DEFAULT NULL,
  `personal_tags` text,
  `courses` text,
  `bu_college` enum('CAS','COM','ENG','CFA','CGS','SAR','CDS','SHA','Pardee','Questrom','Kilachand','Wheelock') NOT NULL,
  `degree` varchar(255) DEFAULT NULL,
  `academic_level` enum('Undergrad','Grad','PhD') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `bu_user_id` (`bu_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `spots`
CREATE TABLE `spots` (
  `spot_id` int NOT NULL AUTO_INCREMENT,
  `spot_name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `open_early` enum('Yes','No') DEFAULT NULL,
  `open_late` enum('Yes','No') DEFAULT NULL,
  `default_img` varchar(255) DEFAULT NULL,
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

-- Table structure for table `spot_hours`
CREATE TABLE `spot_hours` (
  `id` int NOT NULL AUTO_INCREMENT,
  `spot_id` int DEFAULT NULL,
  `day_of_week` tinyint DEFAULT NULL,
  `open_time` time DEFAULT NULL,
  `close_time` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `spot_id` (`spot_id`),
  CONSTRAINT `spot_hours_ibfk_1` FOREIGN KEY (`spot_id`) REFERENCES `spots` (`spot_id`),
  CONSTRAINT `spot_hours_chk_1` CHECK ((`day_of_week` between 0 and 6))
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `reviews`
CREATE TABLE `reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `spot_id` int NOT NULL,
  `review_content` text NOT NULL,
  `rating` tinyint DEFAULT NULL,
  `review_img_url` varchar(500) DEFAULT NULL,
  `review_tags` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `user_id` (`user_id`),
  KEY `spot_id` (`spot_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`spot_id`) REFERENCES `spots` (`spot_id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `contact_us`
CREATE TABLE `contact_us` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `subject` enum('Add Study Spot','Remove Spot','Inaccurate Info','Report Bug','Feedback','Partnerships') DEFAULT NULL,
  `message` text,
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
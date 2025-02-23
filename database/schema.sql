CREATE DATABASE IF NOT EXISTS focushub;
USE focushub;

CREATE TABLE IF NOT EXISTS study_spots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    outlets ENUM('Yes', 'No') DEFAULT NULL,
    group_vs_solo ENUM('Solo', 'Group', 'Both') DEFAULT NULL,
    offers_food ENUM('Yes', 'No') DEFAULT NULL,
    seating_capacity VARCHAR(50) DEFAULT NULL,
    whiteboards ENUM('Yes', 'No') DEFAULT NULL,
    bu_affiliated ENUM('Yes', 'No') DEFAULT NULL,
    open_late ENUM('Yes', 'No') DEFAULT NULL
);

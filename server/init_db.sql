CREATE DATABASE IF NOT EXISTS `club_db`;
USE `club_db`;

SET NAMES utf8mb4;
SET time_zone = '+09:00';
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `Student`;
CREATE TABLE `Student` (
  `Student_ID` VARCHAR(20) NOT NULL,
  `Login_ID` VARCHAR(50) NOT NULL,
  `Pw` VARCHAR(255) NOT NULL,
  `Name` VARCHAR(100) NOT NULL,
  `phone_num` VARCHAR(20) NULL,
  `Email` VARCHAR(100) NULL,
  `Role` ENUM('일반', '관리자') NOT NULL DEFAULT '일반',
  PRIMARY KEY (`Student_ID`),
  UNIQUE KEY `UK_Login_ID` (`Login_ID`),
  UNIQUE KEY `UK_Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Club`;
CREATE TABLE `Club` (
  `Club_ID` INT NOT NULL AUTO_INCREMENT,
  `Club_name` VARCHAR(100) NOT NULL,
  `Club_Introduction` TEXT NULL,
  `Category` VARCHAR(50) NULL,
  `Admin` VARCHAR(20) NULL,
  PRIMARY KEY (`Club_ID`),
  UNIQUE KEY `UK_Club_name` (`Club_name`),
  KEY `IX_Category` (`Category`),
  FOREIGN KEY (`Admin`) REFERENCES `Student` (`Student_ID`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Post`;
CREATE TABLE `Post` (
  `Post_ID` INT NOT NULL AUTO_INCREMENT,
  `Club_ID` INT NOT NULL,
  `Content` TEXT NOT NULL,
  `post_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Post_ID`),
  FOREIGN KEY (`Club_ID`) REFERENCES `Club` (`Club_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Apply`;
DROP TABLE IF EXISTS `Application`;
CREATE TABLE `Apply` (
  `Application_ID` INT NOT NULL AUTO_INCREMENT,
  `Student_ID` VARCHAR(20) NOT NULL,
  `Club_ID` INT NOT NULL,
  `Self_Introduction` TEXT NULL,
  `Application_Date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Status` ENUM('대기', '승인', '거절') NOT NULL DEFAULT '대기',
  PRIMARY KEY (`Application_ID`),
  UNIQUE KEY `UK_Student_Club_Apply` (`Student_ID`, `Club_ID`),
  FOREIGN KEY (`Student_ID`) REFERENCES `Student` (`Student_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`Club_ID`) REFERENCES `Club` (`Club_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `Belong`;
DROP TABLE IF EXISTS `Membership`;
CREATE TABLE `Belong` (
  `Membership_ID` INT NOT NULL AUTO_INCREMENT,
  `Student_ID` VARCHAR(20) NOT NULL,
  `Club_ID` INT NOT NULL,
  `Position` VARCHAR(50) NOT NULL DEFAULT '일반회원',
  PRIMARY KEY (`Membership_ID`),
  UNIQUE KEY `UK_Student_Club_Member` (`Student_ID`, `Club_ID`),
  FOREIGN KEY (`Student_ID`) REFERENCES `Student` (`Student_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (`Club_ID`) REFERENCES `Club` (`Club_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

DROP TRIGGER IF EXISTS `trg_After_Application_Update`;
DROP TRIGGER IF EXISTS `trg_After_Apply_Update`;
DELIMITER $$
CREATE TRIGGER `trg_After_Apply_Update`
AFTER UPDATE ON `Apply`
FOR EACH ROW
BEGIN
  IF OLD.`Status` != '승인' AND NEW.`Status` = '승인' THEN
    INSERT IGNORE INTO `Belong` (`Student_ID`, `Club_ID`, `Position`)
    VALUES (NEW.`Student_ID`, NEW.`Club_ID`, '일반회원');
  END IF;
END$$
DELIMITER ;

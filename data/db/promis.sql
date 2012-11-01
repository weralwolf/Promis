-- phpMyAdmin SQL Dump
-- version 3.4.5deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 12, 2011 at 05:38 PM
-- Server version: 5.1.58
-- PHP Version: 5.3.6-13ubuntu3.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `promis`
--

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE IF NOT EXISTS `devices` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `friquency` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `levels`
--

CREATE TABLE IF NOT EXISTS `levels` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `measurament_points`
--

CREATE TABLE IF NOT EXISTS `measurament_points` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `satellites_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `satellites_id` (`satellites_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `measurements`
--

CREATE TABLE IF NOT EXISTS `measurements` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `units_id` int(10) unsigned NOT NULL,
  `measurement_points_id` int(10) unsigned NOT NULL,
  `satellites_id` int(10) unsigned NOT NULL,
  `devices_id` int(10) unsigned NOT NULL,
  `level_id` int(10) unsigned NOT NULL,
  `session_id` int(10) unsigned DEFAULT NULL,
  `measurement` varchar(255) NOT NULL,
  `error` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `units_id` (`units_id`,`measurement_points_id`,`satellites_id`,`devices_id`),
  KEY `measurement_points_id` (`measurement_points_id`),
  KEY `satellites_id` (`satellites_id`),
  KEY `devices_id` (`devices_id`),
  KEY `level_id` (`level_id`,`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `satellites`
--

CREATE TABLE IF NOT EXISTS `satellites` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `devices_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devices_id` (`devices_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sessions_options`
--

CREATE TABLE IF NOT EXISTS `sessions_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sessions_id` int(11) unsigned NOT NULL,
  `option` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sessions_id` (`sessions_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `units`
--

CREATE TABLE IF NOT EXISTS `units` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `measurament_points`
--
ALTER TABLE `measurament_points`
  ADD CONSTRAINT `measurament_points_ibfk_1` FOREIGN KEY (`satellites_id`) REFERENCES `satellites` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `measurements`
--
ALTER TABLE `measurements`
  ADD CONSTRAINT `measurements_ibfk_5` FOREIGN KEY (`level_id`) REFERENCES `levels` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `measurements_ibfk_1` FOREIGN KEY (`units_id`) REFERENCES `units` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `measurements_ibfk_2` FOREIGN KEY (`measurement_points_id`) REFERENCES `measurament_points` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `measurements_ibfk_3` FOREIGN KEY (`satellites_id`) REFERENCES `satellites` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `measurements_ibfk_4` FOREIGN KEY (`devices_id`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`devices_id`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `sessions_options`
--
ALTER TABLE `sessions_options`
  ADD CONSTRAINT `sessions_options_ibfk_1` FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

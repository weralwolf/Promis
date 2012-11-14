-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 14, 2012 at 05:55 PM
-- Server version: 5.5.28
-- PHP Version: 5.4.6-1ubuntu1

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
-- Table structure for table `channels`
--

CREATE TABLE IF NOT EXISTS `channels` (
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `sampling_frequency` double DEFAULT NULL,
  `devices_title` varchar(255) NOT NULL,
  `parameters_title` varchar(255) NOT NULL,
  PRIMARY KEY (`title`),
  UNIQUE KEY `title_UNIQUE` (`title`),
  KEY `fk_channels_devices1` (`devices_title`),
  KEY `fk_channels_parameters1` (`parameters_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `channels`
--

INSERT INTO `channels` (`title`, `description`, `sampling_frequency`, `devices_title`, `parameters_title`) VALUES
('efps', 'emotional flux per second', 60, 'MAM', 'efps'),
('ffps', 'field flux per second', 60, 'MAM', 'ffps'),
('gmps', 'genius minds per second', 60, 'MEM', 'gmps'),
('iqpp', 'IQ per person', 0.000278, 'IQT', 'iqpp'),
('lps', 'littres of beer pes second', 1, 'BFM', 'lps'),
('mfps', 'madness flux per second', 60, 'MAM', 'mfps'),
('pmsp', 'PMS percentage', 0.000011574, 'GIM', 'pmsp'),
('sm_mps', 'smart minds per second', 60, 'MEM', 'sm_mps'),
('st_mps', 'stupid minds per second', 60, 'MEM', 'st_mps'),
('tmps', 'total minds per second', 60, 'MEM', 'tmps'),
('uf_mps', 'useful minds persecond', 60, 'MEM', 'uf_mps'),
('ul_mps', 'useless minds per second', 60, 'MEM', 'ul_mps');

-- --------------------------------------------------------

--
-- Table structure for table `channels_has_sessions`
--

CREATE TABLE IF NOT EXISTS `channels_has_sessions` (
  `channels_title` varchar(255) NOT NULL,
  `sessions_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`channels_title`,`sessions_id`),
  KEY `fk_channels_has_sessions_sessions1` (`sessions_id`),
  KEY `fk_channels_has_sessions_channels1` (`channels_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE IF NOT EXISTS `devices` (
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `satellites_title` varchar(255) NOT NULL,
  PRIMARY KEY (`title`),
  UNIQUE KEY `title_UNIQUE` (`title`),
  KEY `fk_devices_satellites1` (`satellites_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`title`, `description`, `satellites_title`) VALUES
('BFM', 'Beer Flux Meter measure flux of beer used by mail and female parts of team', 'ww-freak'),
('GIM', 'Girls Influence Meter measure integral girls influence to a mail part of team', 'ww-freak'),
('IQT', 'IQ Tester quickly tests average IQ level', 'ww-freak'),
('MAM', 'Mental Activity Meter measure intensity of mental work', 'ww-freak'),
('MEM', 'Mental Efficiency Meter measure ration of effective mental work due to task to integral mental work including field work', 'ww-freak');

-- --------------------------------------------------------

--
-- Table structure for table `measurament_points`
--

CREATE TABLE IF NOT EXISTS `measurament_points` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time` double NOT NULL,
  `sessions_id` int(10) unsigned DEFAULT NULL,
  `lattitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `altitude` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_measurament_points_sessions1` (`sessions_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `measurements`
--

CREATE TABLE IF NOT EXISTS `measurements` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `parameters_title` varchar(255) NOT NULL,
  `parameters_units_title` varchar(255) NOT NULL,
  `channels_title` varchar(45) NOT NULL,
  `measurement_points_id` int(10) unsigned NOT NULL,
  `marker` int(10) unsigned NOT NULL,
  `measurement` blob NOT NULL,
  `rError` blob,
  `lError` blob,
  PRIMARY KEY (`id`,`parameters_title`,`parameters_units_title`),
  KEY `fk_measurements_channels1` (`channels_title`),
  KEY `fk_measurements_parameters1` (`parameters_title`,`parameters_units_title`),
  KEY `measurement_points_id` (`measurement_points_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='parent_id is presents for saving large dimensional sequences' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `parameters`
--

CREATE TABLE IF NOT EXISTS `parameters` (
  `title` varchar(255) NOT NULL,
  `units_title` varchar(255) NOT NULL,
  PRIMARY KEY (`title`,`units_title`),
  UNIQUE KEY `title_UNIQUE` (`title`),
  KEY `fk_parameters_units1` (`units_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `parameters`
--

INSERT INTO `parameters` (`title`, `units_title`) VALUES
('efps', 'ffps'),
('ffps', 'ffps'),
('gmps', 'mps'),
('iqpp', 'iqpp'),
('lps', 'lps'),
('mfps', 'ffps'),
('pmsp', 'percent'),
('sm_mps', 'mps'),
('st_mps', 'mps'),
('tmps', 'mps'),
('uf_mps', 'mps'),
('ul_mps', 'mps');

-- --------------------------------------------------------

--
-- Table structure for table `parameters_has_parameters`
--

CREATE TABLE IF NOT EXISTS `parameters_has_parameters` (
  `parent_title` varchar(255) NOT NULL,
  `child_title` varchar(255) NOT NULL,
  PRIMARY KEY (`parent_title`,`child_title`),
  KEY `fk_parameters_has_parameters_parameters2` (`child_title`),
  KEY `fk_parameters_has_parameters_parameters1` (`parent_title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `satellites`
--

CREATE TABLE IF NOT EXISTS `satellites` (
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`title`),
  UNIQUE KEY `title_UNIQUE` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `satellites`
--

INSERT INTO `satellites` (`title`, `description`) VALUES
('ww-freak', 'World wide "Freak researches" station. Main areas of interests are mental problems, complexity of logical thinking, girls influence to a men beer-activity');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `iBegin` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `iEnd` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sessions_options`
--

CREATE TABLE IF NOT EXISTS `sessions_options` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sessions_id` int(10) unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sessions_id` (`sessions_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `units`
--

CREATE TABLE IF NOT EXISTS `units` (
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `units`
--

INSERT INTO `units` (`title`) VALUES
('ffps'),
('iqpp'),
('lps'),
('mps'),
('percent');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `channels`
--
ALTER TABLE `channels`
  ADD CONSTRAINT `fk_channels_devices1` FOREIGN KEY (`devices_title`) REFERENCES `devices` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_channels_parameters1` FOREIGN KEY (`parameters_title`) REFERENCES `parameters` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `channels_has_sessions`
--
ALTER TABLE `channels_has_sessions`
  ADD CONSTRAINT `fk_channels_has_sessions_channels1` FOREIGN KEY (`channels_title`) REFERENCES `channels` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_channels_has_sessions_sessions1` FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `fk_devices_satellites1` FOREIGN KEY (`satellites_title`) REFERENCES `satellites` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `measurament_points`
--
ALTER TABLE `measurament_points`
  ADD CONSTRAINT `fk_measurament_points_sessions1` FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `measurements`
--
ALTER TABLE `measurements`
  ADD CONSTRAINT `fk_measurements_channels1` FOREIGN KEY (`channels_title`) REFERENCES `channels` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_measurements_parameters1` FOREIGN KEY (`parameters_title`, `parameters_units_title`) REFERENCES `parameters` (`title`, `units_title`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `measurements_ibfk_2` FOREIGN KEY (`measurement_points_id`) REFERENCES `measurament_points` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `parameters`
--
ALTER TABLE `parameters`
  ADD CONSTRAINT `fk_parameters_units1` FOREIGN KEY (`units_title`) REFERENCES `units` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `parameters_has_parameters`
--
ALTER TABLE `parameters_has_parameters`
  ADD CONSTRAINT `fk_parameters_has_parameters_parameters1` FOREIGN KEY (`parent_title`) REFERENCES `parameters` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_parameters_has_parameters_parameters2` FOREIGN KEY (`child_title`) REFERENCES `parameters` (`title`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `sessions_options`
--
ALTER TABLE `sessions_options`
  ADD CONSTRAINT `sessions_options_ibfk_1` FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

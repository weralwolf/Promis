SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `promis` ;
CREATE SCHEMA IF NOT EXISTS `promis` DEFAULT CHARACTER SET utf8 ;
USE `promis` ;

-- -----------------------------------------------------
-- Table `promis`.`satellites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`satellites` ;

CREATE  TABLE IF NOT EXISTS `promis`.`satellites` (
  `title` VARCHAR(255) NOT NULL ,
  `description` TEXT NOT NULL ,
  PRIMARY KEY (`title`) ,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `promis`.`devices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`devices` ;

CREATE  TABLE IF NOT EXISTS `promis`.`devices` (
  `title` VARCHAR(255) NOT NULL ,
  `description` TEXT NOT NULL ,
  `satellites_title` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`title`) ,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  INDEX `fk_devices_satellites1` (`satellites_title` ASC) ,
  CONSTRAINT `fk_devices_satellites1`
    FOREIGN KEY (`satellites_title` )
    REFERENCES `promis`.`satellites` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `promis`.`sessions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`sessions` ;

CREATE  TABLE IF NOT EXISTS `promis`.`sessions` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `iBegin` TIMESTAMP NOT NULL ,
  `iEnd` TIMESTAMP NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promis`.`measurament_points`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`measurament_points` ;

CREATE  TABLE IF NOT EXISTS `promis`.`measurament_points` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `time` DOUBLE NOT NULL ,
  `sessions_id` INT(10) UNSIGNED NULL ,
  `lattitude` DOUBLE NULL ,
  `longitude` DOUBLE NULL ,
  `altitude` DOUBLE NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_measurament_points_sessions1` (`sessions_id` ASC) ,
  CONSTRAINT `fk_measurament_points_sessions1`
    FOREIGN KEY (`sessions_id` )
    REFERENCES `promis`.`sessions` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `promis`.`units`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`units` ;

CREATE  TABLE IF NOT EXISTS `promis`.`units` (
  `title` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`title`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `promis`.`parameters`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`parameters` ;

CREATE  TABLE IF NOT EXISTS `promis`.`parameters` (
  `title` VARCHAR(255) NOT NULL ,
  `units_title` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`title`, `units_title`) ,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  INDEX `fk_parameters_units1` (`units_title` ASC) ,
  CONSTRAINT `fk_parameters_units1`
    FOREIGN KEY (`units_title` )
    REFERENCES `promis`.`units` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promis`.`channels`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`channels` ;

CREATE  TABLE IF NOT EXISTS `promis`.`channels` (
  `title` VARCHAR(255) NOT NULL ,
  `description` TEXT NOT NULL ,
  `sampling_frequency` DOUBLE NULL ,
  `devices_title` VARCHAR(255) NOT NULL ,
  `parameters_title` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`title`) ,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) ,
  INDEX `fk_channels_devices1` (`devices_title` ASC) ,
  INDEX `fk_channels_parameters1` (`parameters_title` ASC) ,
  CONSTRAINT `fk_channels_devices1`
    FOREIGN KEY (`devices_title` )
    REFERENCES `promis`.`devices` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_channels_parameters1`
    FOREIGN KEY (`parameters_title` )
    REFERENCES `promis`.`parameters` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promis`.`measurements`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`measurements` ;

CREATE  TABLE IF NOT EXISTS `promis`.`measurements` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `parameters_title` VARCHAR(255) NOT NULL ,
  `parameters_units_title` VARCHAR(255) NOT NULL ,
  `channels_title` VARCHAR(45) NOT NULL ,
  `measurement_points_id` INT(10) UNSIGNED NOT NULL ,
  `marker` INT(10) UNSIGNED NOT NULL ,
  `measurement` BLOB NOT NULL ,
  `rError` VARCHAR(255) NULL ,
  `lError` VARCHAR(255) NULL ,
  PRIMARY KEY (`id`, `parameters_title`, `parameters_units_title`) ,
  INDEX `measurement_points_id` (`measurement_points_id` ASC) ,
  INDEX `fk_measurements_parameters1` (`parameters_title` ASC, `parameters_units_title` ASC) ,
  INDEX `fk_measurements_channels1` (`channels_title` ASC) ,
  CONSTRAINT `measurements_ibfk_2`
    FOREIGN KEY (`measurement_points_id` )
    REFERENCES `promis`.`measurament_points` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_measurements_parameters1`
    FOREIGN KEY (`parameters_title` , `parameters_units_title` )
    REFERENCES `promis`.`parameters` (`title` , `units_title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_measurements_channels1`
    FOREIGN KEY (`channels_title` )
    REFERENCES `promis`.`channels` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'parent_id is presents for saving large dimensional sequences' /* comment truncated */;


-- -----------------------------------------------------
-- Table `promis`.`sessions_options`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`sessions_options` ;

CREATE  TABLE IF NOT EXISTS `promis`.`sessions_options` (
  `id` INT(10) NOT NULL AUTO_INCREMENT ,
  `sessions_id` INT(10) UNSIGNED NOT NULL ,
  `title` VARCHAR(255) NOT NULL ,
  `value` VARCHAR(255) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `sessions_id` (`sessions_id` ASC) ,
  CONSTRAINT `sessions_options_ibfk_1`
    FOREIGN KEY (`sessions_id` )
    REFERENCES `promis`.`sessions` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `promis`.`channels_has_sessions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`channels_has_sessions` ;

CREATE  TABLE IF NOT EXISTS `promis`.`channels_has_sessions` (
  `channels_title` VARCHAR(255) NOT NULL ,
  `sessions_id` INT(10) UNSIGNED NOT NULL ,
  PRIMARY KEY (`channels_title`, `sessions_id`) ,
  INDEX `fk_channels_has_sessions_sessions1` (`sessions_id` ASC) ,
  INDEX `fk_channels_has_sessions_channels1` (`channels_title` ASC) ,
  CONSTRAINT `fk_channels_has_sessions_channels1`
    FOREIGN KEY (`channels_title` )
    REFERENCES `promis`.`channels` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_channels_has_sessions_sessions1`
    FOREIGN KEY (`sessions_id` )
    REFERENCES `promis`.`sessions` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `promis`.`parameters_has_parameters`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promis`.`parameters_has_parameters` ;

CREATE  TABLE IF NOT EXISTS `promis`.`parameters_has_parameters` (
  `parent_title` VARCHAR(255) NOT NULL ,
  `child_title` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`parent_title`, `child_title`) ,
  INDEX `fk_parameters_has_parameters_parameters2` (`child_title` ASC) ,
  INDEX `fk_parameters_has_parameters_parameters1` (`parent_title` ASC) ,
  CONSTRAINT `fk_parameters_has_parameters_parameters1`
    FOREIGN KEY (`parent_title` )
    REFERENCES `promis`.`parameters` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_parameters_has_parameters_parameters2`
    FOREIGN KEY (`child_title` )
    REFERENCES `promis`.`parameters` (`title` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

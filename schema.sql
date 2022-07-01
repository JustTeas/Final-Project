CREATE SCHEMA IF NOT EXISTS `burrito_time` DEFAULT CHARACTER SET utf8 ;
USE `burrito_time` ;

drop table `users`;
drop table `orders`;
drop table `products`;

CREATE TABLE IF NOT EXISTS `burrito_time`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(255) NOT NULL,
  `lastname` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  `favorite_order` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`));


CREATE TABLE IF NOT EXISTS `burrito_time`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `method` VARCHAR(45) NOT NULL,
  `size` VARCHAR(45) NOT NULL,
  `crust` VARCHAR(45) NOT NULL,
  `quantity` INT NOT NULL,
  `toppings` TEXT NULL,
  `number_of_toppings` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`)
);


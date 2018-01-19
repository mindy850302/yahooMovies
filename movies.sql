-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 19, 2018 at 09:34 AM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 5.6.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES latin1 */;

--
-- Database: `movie`
--

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `englishName` varchar(45) DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL,
  `release` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `company` varchar(45) DEFAULT NULL,
  `director` varchar(45) DEFAULT NULL,
  `actor` varchar(45) DEFAULT NULL,
  `expectation_value` int(11) DEFAULT NULL,
  `expectation_people` varchar(45) DEFAULT NULL,
  `satisfaction_value` int(11) DEFAULT NULL,
  `satisfaction_people` varchar(45) DEFAULT NULL,
  `movie_img` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

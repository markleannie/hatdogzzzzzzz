-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2024 at 05:38 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `management`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `instructor` varchar(100) NOT NULL,
  `course_code` varchar(20) NOT NULL,
  `course_title` varchar(100) NOT NULL,
  `class_code` varchar(20) NOT NULL,
  `room` varchar(50) NOT NULL,
  `day` varchar(20) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `class_type` varchar(20) NOT NULL,
  `semester_start` date NOT NULL,
  `semester_end` date NOT NULL,
  `user_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `id` int(11) NOT NULL,
  `room_name` varchar(50) NOT NULL,
  `building` varchar(100) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`id`, `room_name`, `building`, `capacity`) VALUES
(1, 'COMLAB 1', 'IT BUILDING', 30),
(2, 'COMLAB 2', 'IT BUILDING', 30),
(3, 'COMLAB 3', 'IT BUILDING', 30),
(4, 'CISCO LAB 1', 'IT BUILDING', 30),
(5, 'CISCO LAB 2', 'IT BUILDING', 30),
(6, 'CISCO LAB 3', 'IT BUILDING', 30);

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `name` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`name`, `email`, `id`) VALUES
('hakdog', 'hakdog@gmail.com', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `department` varchar(150) DEFAULT NULL,
  `title` enum('Prof','Asst. Prof','Assoc. Prof','Lecturer','Sr. Lecturer','Instructor','Teaching Fellow','Research Fellow','Dr.','Ph.D. Candidate','Ph.D','M.A.','M.S.','M.Sc.','B.A.','B.Sc.','Engr.','CPA','RN','Attorney or Esq','Rev.','Emeritus','Visiting Professor','Honorary Professor','Distinguished Professor','Clinical Professor') DEFAULT NULL,
  `office_hours` varchar(255) DEFAULT NULL,
  `marital_status` enum('Single','Married','Divorced','Widowed') DEFAULT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `username`, `email`, `password`, `middle_name`, `last_name`, `department`, `title`, `office_hours`, `marital_status`, `contact_number`, `age`, `birthday`, `address`) VALUES
(202026, 'Loiuse Natasha', 'teacher_loiuse', 'loiusenatasha@gmail.com', 'scrypt:32768:8:1$O5572ddSfzmqFNgP$2bc52d804aad5efab8bfe1dbd0f939d889a8007bed579cd1ad0b18b0ca5c1c017006b387701a84d1f034150819e0e670094eaab933314f59a668f20a9e814994', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202028, 'bino', 'slowfarmer', 'bino@alche', 'scrypt:32768:8:1$SHJyafbjxlRr1pLn$d4f8a87db57929531e821ec4e98eec1a5bf408fdae702b56ba1928110addd130843ebb9f0cc1d539ccc46fc7aa7e4614d6ef16382d9211e6eefb434498256dea', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202029, 'GIlbert Franz ANthony R. Ormeneta', 'GIbo', 'gormeneta@gmail.com', 'scrypt:32768:8:1$GEVpyFoCdykbmorh$502d270b684dc4b85192705b05be81de97055672a8b6e4df8953bffc946d9dec50fa3dd1255b4092ded330e3b401adc7dd0d666448f1eed46f435469cacd4341', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202030, 'Jessa Mae Omen', 'marry@gmail.com', 'marry@gmail.com', 'scrypt:32768:8:1$6L7eemLLhhE8CK9M$46ad80008eee7ca1488ad218b8acac58501785a20a770857b22eec0d2fbe9da240543ac08b69722a927ae01e3a78931f7eb949a51d728c91f13e92c187dd5ccb', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202031, 'Ink Steady', 'professor_ink', 'inksteady@gmail.com', 'scrypt:32768:8:1$gtoj8n6mmn1yZGlx$a1f164dbc25cd32023ec815c04bc0fd6a9a86030131cb07971892ca9efca902c06a578e6fca45d9a8767d105decf9c56ca7cd938d22aa76e5fb369d85a08d930', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202032, 'River Maya', 'rivremaya12', 'rivermaya@gmail.com', 'scrypt:32768:8:1$AtklaJVLxxbhyLkV$25483f27a4394efc38956778ca3f1e7b772a0adf3660ef80e153f0dc52ef3568573c9b2bad242a39d072dbd98d4113db422d49c2db370ed4b2bece07e3330480', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(202033, 'Suzette', 'profzues', 'reysuzette3@gmail.com', 'scrypt:32768:8:1$R3FGanrOcrG8a66s$2f3f3761e087428e69275ea7c83ce1e6e61d957e625549e6f531b49deb1039fd0afe07c60aa757df16e7fb8b77fa4289491779e57708373c3433a419090b85dd', 'Rivera', 'Albao', 'Information Technology', 'Prof', 'Monday and Wednesday: 2:00 PM - 4:00 PM', NULL, '09752101055', 42, '1982-03-16', 'Brgy. 95-A Caibaan Tacloban City'),
(202035, 'rain melody', 'profrain', 'rainmelodyalbao@gmail.com', 'rainmelodyalbao@gmail.com...', 'rivera', 'albao', 'Information Technology', 'Instructor', 'Monday and Wednesday: 2:00 PM - 4:00 PM', NULL, '09926350296', 19, '2005-07-28', 'Brgy. 95-A Caibaan Tacloban City'),
(202036, 'lois alzette', 'teacheralzette', 'loisalzettealbao@gmail.com', 'scrypt:32768:8:1$QwNchpyjL6Oqyz1W$839dfafaa0208b920ec4f9b6f725ab3a44a9f4c3a3c8a411f45ed2ec4edeca9e9408d566f151a4cef3c5298d51e07511c589bc45fa7da50a0295b99061643218', 'Rivera', 'Albao', 'Information Technology', 'Prof', 'Monday and Wednesday: 2:00 PM - 4:00 PM', NULL, '09752101055', 20, '2004-06-13', 'Brgy. 95-A Caibaan Tacloban City'),
(202037, 'Lois Alzette', 'prof_lois', 'albaoloisalzette@gmail.com', 'scrypt:32768:8:1$IqewCAbGbTQ3nwAt$9473467c11126496b6d80df08478161c55307e69bfbec9e9afe2c0ccce9b2aa95c156eafb8f73365c0ff8ce68c2624cda21a7320dd58c95ae83cea352443e0ed', 'Rivera', 'ALBAO', 'College of Education', '', 'Monday and Wednesday: 2:00 PM - 4:00 PM', NULL, '09926350296', 20, '2004-06-13', 'BRGY. 95-A CAIBAAN, AREA-7');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`),
  ADD KEY `idx_room` (`room`),
  ADD KEY `fk_room` (`room_id`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `room_name` (`room_name`),
  ADD UNIQUE KEY `unique_room_name` (`room_name`),
  ADD KEY `idx_building` (`building`),
  ADD KEY `idx_capacity` (`capacity`),
  ADD KEY `idx_building_capacity` (`building`,`capacity`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `room`
--
ALTER TABLE `room`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=202038;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `fk_room` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

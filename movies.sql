-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 23, 2024 at 04:20 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `movies`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Action'),
(2, 'Drama'),
(5, 'Horror'),
(6, 'Thriller'),
(7, 'Romance'),
(8, 'Comedy'),
(9, 'Western'),
(10, 'Sci-fi');

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `release_date` date NOT NULL,
  `category_id` int(11) NOT NULL,
  `image_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`id`, `name`, `release_date`, `category_id`, `image_path`) VALUES
(1, 'Fight club', '2000-03-01', 6, 'images.jpeg'),
(2, 'Shawshank redemption ', '1994-10-14', 2, 'shawshank.jpeg'),
(3, 'Million dollar baby', '2005-02-23', 2, 'mdb.jpg'),
(4, 'The Dark knight', '1994-10-14', 1, 'dark_knight.jpg'),
(5, 'Green Book', '2018-09-11', 2, 'green_book.jpg'),
(6, 'About time', '2013-08-08', 7, 'about_time.jpg'),
(7, 'Interstellar', '2014-11-07', 10, 'interstellar.jpg'),
(8, 'Forrest jump', '1994-07-06', 2, 'forrest_jump.jpg'),
(9, 'Dumb and dumber', '1994-12-06', 8, 'dumb_dumber.jpg'),
(10, 'Once upon a time in hollywood', '2019-07-26', 9, 'once_upon.jpg'),
(11, 'Room', '2015-10-16', 6, 'room.jpg'),
(12, 'Mission: Impossible – Dead Reckoning Part 1', '2023-07-12', 1, 'mission_impossible.jpg'),
(13, 'The Black Demon', '2023-04-26', 5, 'black_demon.jpeg'),
(16, 'Titanic', '1997-02-26', 7, 'titanic.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ratings`
--

INSERT INTO `ratings` (`id`, `movie_id`, `user_id`, `rating`) VALUES
(19, 1, 7, 1),
(20, 2, 7, 3),
(21, 1, 4, 5),
(22, 2, 4, 5),
(23, 1, 1, 2),
(24, 2, 1, 1),
(25, 1, 2, 5),
(26, 2, 2, 5),
(27, 1, 9, 1),
(28, 2, 9, 5),
(29, 7, 9, 5),
(30, 6, 9, 3),
(31, 4, 12, 5),
(32, 1, 13, 5),
(33, 4, 13, 4),
(34, 8, 14, 4),
(35, 4, 14, 4),
(36, 1, 15, 2),
(37, 12, 16, 3),
(38, 3, 16, 1),
(39, 2, 17, 1),
(40, 4, 18, 4),
(41, 4, 19, 3),
(42, 1, 19, 5),
(43, 16, 21, 5),
(44, 3, 21, 5);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `review_text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `movie_id`, `user_id`, `review_text`) VALUES
(1, 2, 1, 'best one'),
(2, 1, 1, 'Strange'),
(3, 2, 2, 'my best movie'),
(4, 1, 2, 'tough one '),
(5, 2, 3, 'oh shawshank '),
(6, 4, 3, 'one of the best by Nolan, actually it amazed me when I first watched it in cinema   '),
(7, 2, 11, 'Amazing'),
(8, 4, 12, 'Wonderful one '),
(9, 9, 12, 'Very funny'),
(10, 9, 12, 'Nice one'),
(11, 7, 13, 'piece of magic'),
(12, 10, 13, 'good'),
(13, 4, 14, 'oh dark knight, Perfect'),
(14, 4, 18, 'review');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `isAdmin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `isAdmin`) VALUES
(1, 'salim', 'salem@s.com', '12345', NULL),
(2, 'salim', 'salim@sa.com', '12345', NULL),
(3, 'samy ', 'samy@s.com', '123321', NULL),
(4, 'saad', 'sadd@s.com', '321123', NULL),
(5, 'luis', 'luis@l.com', '123321', NULL),
(6, 'ayman', 'ayman@m.com', '123456', NULL),
(7, 'juda', 'goda@g.com', '123', NULL),
(8, 'lio', 'lio@m.com', '123123', NULL),
(9, 'samer', 'samer@sam.com', '123456', NULL),
(10, 'walter', 'walter@white.com', '123456', NULL),
(11, 'andrew', 'andrew@w.com', '123456', NULL),
(12, 'mina', 'mina@gmail.com', '123456', NULL),
(13, 'malik', 'malik@m.com', 'scrypt:32768:8:1$dSNxSrahprJa1LSU$f4e48367130781f963c853b66489d7aeba0b742e6b8de4d27c92cc1080793b980ede8f99e8b19b2df0758348c41ddcc0822d9a28e34d3b2aa731c1e8fea4d164', NULL),
(14, 'lio', 'lio@lio.com', 'scrypt:32768:8:1$FdkCZfN8AbEF7zJ6$a583bf4a9c480eff4245a7ca8f73bc0ea2da40f74fb76319afc5fe18a93b6116cb93f4313126bc35b5d37c9976a2d9c52ddb19b5a8e60c15cfa2543ab543a54c', NULL),
(15, 'Maher', 'maher@maher.com', 'scrypt:32768:8:1$FaWLjxZVZOndJlQj$b19832412f119568054316682e01bfd79510b967e677e2d2fc7179afc981eaba84ea2d1c6f406373ca8551cac1eeb674e98af1f7a310d045a12322f953180dce', NULL),
(16, 'maged', 'maged@gmail.com', 'scrypt:32768:8:1$SUededP1RhktMg1U$9f23ba5a9c682d0e16f245fb2001fed337020116c46c146f4fe2f8b9bff3c2d88c4076f805b8ba3e184534b6f768bfaeb83d1adb234754a89aca4644ad0245de', NULL),
(17, 'walter', 'walter@w.com', 'scrypt:32768:8:1$yYFPFGPVLxaHkMPy$e09c214c1432bc7054eae5fe2636c5d9a5199ca12c17297b76caaa1094e8fe893249df67eb02dbd16d3cea5cdd8d4414345b8de8b2fc0a014f1fd18c6bedb690', NULL),
(18, 'mohamed', 'mohamed@m.com', 'scrypt:32768:8:1$z2yfpH5HKKoWhXUW$f2024e19ccd52be54e80f0bdbfd1403c8a9ecebfe493369cd3d7b9ab6d5bcc3c62d3c4f5a80cc49b9ff745d9610eeffcba91a12ebd3438970ff536b9064c968f', NULL),
(19, 'maged', 'maged@m1.com', 'scrypt:32768:8:1$3p7YWwoEbXJ20CVD$d8764d1016b56baa1cb04869024d5be40f5779099af057bda2d14880b1fecde100957dc309443bc7680570bf565bfbc95222d8b9c16d471cd4163855f5668785', NULL),
(20, 'samy', 'samy@ash.com', 'scrypt:32768:8:1$4PXRAaZsO8m6bAT2$168d6d2e34af14220e711afe8b37008b1ccabbfc450cbf38441a0baa5eb80717175f98991859f9533b4f9fdc345e4eeb309edef516e3fc1595ccd19a84919af3', NULL),
(21, 'khalil ', 'khalil@m.com', 'scrypt:32768:8:1$sCKtY7ywfq8kiaQT$9c33c54a0ea5eb3d45b74f37f8f4ba7ee6c061c0eec44b423605bcf2c72352d9b477e180e59b90028543f1848a95f34587981cb247052ec5ffcc29ce1214c8ab', 1),
(22, 'sami', 'hamed@m.com', 'scrypt:32768:8:1$G5egzSUMfwV26sOr$6c7f53f11a6e8d72d25a1e19c502b845e023da06149f5e2de5b691aa38857ba3b153d09168046d8ce58b997c49018bc757c9e81017c5fed9dcbaa966b31cdff2', 0),
(23, '123', 'lionel@m12.com', 'scrypt:32768:8:1$pzbmq7ToXOBvdN8p$5549c706f9cc910bef7583ba54bb6ab330138cce36889e4aa154e399e618eb95640c83d3cc18cd913ac80aa8faf0e53942333d660f3041111867fd599d2e7098', 0),
(24, 'admin', 'admin@gmail.com', 'scrypt:32768:8:1$1hvfgETTV2ENlI56$5836f1b83c3b4dcc4bf0fe42455d6e27ff1aebacd414e60e5ed0bcec5b2310359ed10558dec844a616908bbdc3be7dca3fd681fbffbc85bd7d8614509b74d8a1', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fk_movie_id` (`movie_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `movie_id` (`movie_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `movies`
--
ALTER TABLE `movies`
  ADD CONSTRAINT `movies_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `fk_movie_id` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  ADD CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

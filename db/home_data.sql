-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 26 Mar 2020 pada 18.47
-- Versi server: 10.1.38-MariaDB
-- Versi PHP: 7.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_svm`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `home_data`
--

CREATE TABLE `home_data` (
  `id` int(11) NOT NULL,
  `no` varchar(50) DEFAULT NULL,
  `persen_ch4` varchar(50) DEFAULT NULL,
  `persen_c2h4` varchar(50) DEFAULT NULL,
  `persen_c2h2` varchar(50) DEFAULT NULL,
  `fault` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `home_data`
--

INSERT INTO `home_data` (`id`, `no`, `persen_ch4`, `persen_c2h4`, `persen_c2h2`, `fault`, `created_at`) VALUES
(5, '1', '11.53846154', '11.53846154', '76.92307692', 'D1', '2020-03-25 17:59:32.676891'),
(6, '2', '28.125', '9.375', '62.5', 'D1', '2020-03-25 18:15:59.581561'),
(7, '3', '45.45454545', '9.090909091', '45.45454545', 'D1', '2020-03-25 18:16:28.328856'),
(8, '4', '56.14035088', '8.771929825', '35.0877193', 'D1', '2020-03-25 18:19:13.013613'),
(9, '5', '71.42857143', '8.163265306', '20.40816327', 'D1', '2020-03-25 18:19:43.656636'),
(10, '6', '4.761904762', '47.61904762', '47.61904762', 'D2', '2020-03-25 18:20:09.709737'),
(11, '7', '4.761904762', '27.21088435', '68.02721088', 'D2', '2020-03-25 18:20:29.139681'),
(12, '8', '4.761904762', '63.49206349', '31.74603175', 'D2', '2020-03-25 18:20:56.810354'),
(13, '9', '33.33333333', '33.33333333', '33.33333333', 'D2', '2020-03-25 18:21:24.700863'),
(14, '10', '47.36842105', '31.57894737', '21.05263158', 'D2', '2020-03-25 18:21:47.701084');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `home_data`
--
ALTER TABLE `home_data`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `home_data`
--
ALTER TABLE `home_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

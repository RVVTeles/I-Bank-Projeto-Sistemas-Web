-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 08, 2024 at 09:48 PM
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
-- Database: `contasapagar`
--

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `cpf` varchar(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `numero_telefone` int(11) NOT NULL COMMENT 'Número de telefone do cliente',
  `endereco` varchar(255) NOT NULL,
  `numero_endereco` varchar(10) NOT NULL,
  `cidade` varchar(255) NOT NULL,
  `estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`cpf`, `nome`, `numero_telefone`, `endereco`, `numero_endereco`, `cidade`, `estado`) VALUES
('1', 'Abner', 2147483647, 'Rua Capitão Marechal Tenente', '5012', 'Fortaleza', 'Ceará'),
('12345678999', 'Joaquim', 2147483647, 'Rua tal', '82', 'Fortaleza', 'Ceará'),
('143225568-7', 'Adabervaldo Torres', 0, '', '', '', ''),
('2', 'b', 0, '', '', '', ''),
('3', 'c', 0, '', '', '', ''),
('4', 'd', 0, '', '', '', ''),
('5', 'g', 0, '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `contas`
--

CREATE TABLE `contas` (
  `id` int(11) NOT NULL,
  `cliente_cpf` varchar(11) NOT NULL,
  `valor` float NOT NULL COMMENT 'Valor da conta a ser paga',
  `juros` float NOT NULL COMMENT 'Juros a ser pago por dia de atraso',
  `data_emissao` date NOT NULL COMMENT 'Data de emissão da conta',
  `data_vencimento` date NOT NULL COMMENT 'Data de vencimento da conta',
  `data_pagamento` date DEFAULT NULL COMMENT 'Data de pagamento da conta'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contas`
--

INSERT INTO `contas` (`id`, `cliente_cpf`, `valor`, `juros`, `data_emissao`, `data_vencimento`, `data_pagamento`) VALUES
(1, '3', 200, 1, '2024-08-23', '2024-09-13', '2024-09-09'),
(2, '1', 5000, 1, '2024-08-23', '2024-09-13', '2024-09-26'),
(4, '1', 100, 1, '2024-08-23', '2024-09-13', NULL),
(5, '1', 100, 1, '2024-08-23', '2024-09-13', NULL),
(6, '1', 100, 1, '2024-08-23', '2024-08-23', '2024-09-05'),
(7, '1', 100, 1, '2024-08-23', '2024-09-13', NULL),
(8, '2', 56, 1, '2024-08-26', '2024-08-27', NULL),
(10, '143225568-7', 500, 10, '2024-09-05', '2024-09-19', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`cpf`);

--
-- Indexes for table `contas`
--
ALTER TABLE `contas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_cpf` (`cliente_cpf`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contas`
--
ALTER TABLE `contas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `contas`
--
ALTER TABLE `contas`
  ADD CONSTRAINT `contas_ibfk_1` FOREIGN KEY (`cliente_cpf`) REFERENCES `clientes` (`cpf`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

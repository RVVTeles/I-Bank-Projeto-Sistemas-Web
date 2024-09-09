-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 09, 2024 at 09:57 PM
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
  `numero_telefone` varchar(20) NOT NULL COMMENT 'Número de telefone do cliente',
  `endereco` varchar(255) NOT NULL,
  `numero_endereco` varchar(20) NOT NULL,
  `cidade` varchar(255) NOT NULL,
  `estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`cpf`, `nome`, `numero_telefone`, `endereco`, `numero_endereco`, `cidade`, `estado`) VALUES
('12345678900', 'Ana Paula Silva', '85987654321', 'Rua das Flores', '123', 'Fortaleza', 'Ceará'),
('23456789011', 'Carlos Eduardo Santos', '85976543210', 'Avenida Beira Mar', '456', 'Fortaleza', 'Ceará'),
('34567890122', 'Maria Oliveira Costa', '85965432109', 'Rua do Sol', '789', 'Fortaleza', 'Ceará'),
('45678901233', 'João Pedro Almeida', '85954321098', 'Rua das Acácias', '101', 'Fortaleza', 'Ceará');

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
(1, '12345678900', 5000, 10, '2024-09-09', '2024-09-10', NULL),
(2, '12345678900', 1500, 10, '2024-09-02', '2024-09-11', NULL),
(3, '12345678900', 2000, 30, '2024-09-02', '2024-09-03', NULL),
(4, '12345678900', 750, 10, '2024-09-02', '2024-09-04', '2024-09-06');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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

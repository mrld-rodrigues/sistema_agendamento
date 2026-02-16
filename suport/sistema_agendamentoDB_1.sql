/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.11-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: sistema_agendamento
-- ------------------------------------------------------
-- Server version	10.11.11-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `agendamentos`
--

DROP TABLE IF EXISTS `agendamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `agendamentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profissional_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `servico_id` int(11) NOT NULL,
  `data_hora` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profissional_id` (`profissional_id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `servico_id` (`servico_id`),
  CONSTRAINT `agendamentos_ibfk_1` FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`),
  CONSTRAINT `agendamentos_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  CONSTRAINT `agendamentos_ibfk_3` FOREIGN KEY (`servico_id`) REFERENCES `servicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendamentos`
--

LOCK TABLES `agendamentos` WRITE;
/*!40000 ALTER TABLE `agendamentos` DISABLE KEYS */;
INSERT INTO `agendamentos` VALUES
(2,1,2,1,'2026-02-02 19:00:00'),
(3,1,3,1,'2026-02-03 20:00:00'),
(4,1,4,1,'2026-02-04 18:00:00'),
(6,1,1,1,'2026-03-20 09:00:00'),
(7,1,1,1,'2026-03-23 09:00:00'),
(8,1,1,1,'2026-03-23 15:00:00');
/*!40000 ALTER TABLE `agendamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bloqueios_recorrentes`
--

DROP TABLE IF EXISTS `bloqueios_recorrentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloqueios_recorrentes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profissional_id` int(11) NOT NULL,
  `dia_semana` tinyint(4) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fim` time NOT NULL,
  `data_inicio` date DEFAULT NULL,
  `data_fim` date DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_profissional` (`profissional_id`),
  CONSTRAINT `bloqueios_recorrentes_ibfk_1` FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloqueios_recorrentes`
--

LOCK TABLES `bloqueios_recorrentes` WRITE;
/*!40000 ALTER TABLE `bloqueios_recorrentes` DISABLE KEYS */;
INSERT INTO `bloqueios_recorrentes` VALUES
(1,1,0,'14:00:00','16:00:00',NULL,NULL,'Reunião semanal');
/*!40000 ALTER TABLE `bloqueios_recorrentes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES
(1,'Cliente 1','c1@email.com','111'),
(2,'Cliente 2','c2@email.com','222'),
(3,'Cliente 3','c3@email.com','333'),
(4,'Cliente 4','c4@email.com','444'),
(5,'Cliente 5','c5@email.com','555'),
(6,'Cliente 6','c6@email.com','666'),
(7,'Cliente 7','c7@email.com','777'),
(8,'Cliente 8','c8@email.com','888'),
(9,'Cliente 9','c9@email.com','999'),
(10,'Cliente 10','c10@email.com','1010'),
(11,'Cliente 11','c11@email.com','1111'),
(12,'Cliente 12','c12@email.com','1212'),
(13,'Cliente 13','c13@email.com','1313'),
(14,'Cliente 14','c14@email.com','1414'),
(15,'Cliente 15','c15@email.com','1515');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dias_bloqueados`
--

DROP TABLE IF EXISTS `dias_bloqueados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `dias_bloqueados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profissional_id` int(11) NOT NULL,
  `data` date NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `profissional_id` (`profissional_id`,`data`),
  CONSTRAINT `dias_bloqueados_ibfk_1` FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dias_bloqueados`
--

LOCK TABLES `dias_bloqueados` WRITE;
/*!40000 ALTER TABLE `dias_bloqueados` DISABLE KEYS */;
INSERT INTO `dias_bloqueados` VALUES
(1,1,'2026-03-01','Férias'),
(2,1,'2026-03-02','Férias'),
(3,1,'2026-03-03','Férias'),
(4,1,'2026-03-04','Férias'),
(6,1,'2026-03-06','Férias'),
(7,1,'2026-03-07','Férias'),
(8,1,'2026-03-08','Férias'),
(9,1,'2026-03-09','Férias'),
(10,1,'2026-03-10','Férias'),
(13,1,'2026-03-11','Férias'),
(14,1,'2026-03-12','Férias'),
(15,1,'2026-03-13','Férias'),
(16,1,'2026-03-14','Férias'),
(17,1,'2026-03-15','Férias'),
(18,1,'2026-02-20','Férias'),
(19,1,'2026-02-21','Férias'),
(20,1,'2026-02-22','Férias'),
(21,1,'2026-02-23','Férias'),
(22,1,'2026-02-24','Férias'),
(23,1,'2026-02-25','Férias'),
(25,1,'2026-02-16','Feriado'),
(26,1,'2026-03-21','Feriado');
/*!40000 ALTER TABLE `dias_bloqueados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horarios_bloqueados`
--

DROP TABLE IF EXISTS `horarios_bloqueados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `horarios_bloqueados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profissional_id` int(11) NOT NULL,
  `data` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fim` time NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profissional_id` (`profissional_id`),
  CONSTRAINT `horarios_bloqueados_ibfk_1` FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horarios_bloqueados`
--

LOCK TABLES `horarios_bloqueados` WRITE;
/*!40000 ALTER TABLE `horarios_bloqueados` DISABLE KEYS */;
INSERT INTO `horarios_bloqueados` VALUES
(1,1,'2026-02-06','22:00:00','23:30:00','Descanso'),
(2,1,'2026-02-26','14:00:00','17:00:00','Folga da tarde'),
(4,1,'2026-09-15','10:00:00','12:00:00','Consulta especial');
/*!40000 ALTER TABLE `horarios_bloqueados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horarios_trabalho`
--

DROP TABLE IF EXISTS `horarios_trabalho`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `horarios_trabalho` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profissional_id` int(11) NOT NULL,
  `dia_semana` tinyint(4) NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fim` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profissional_id` (`profissional_id`),
  CONSTRAINT `horarios_trabalho_ibfk_1` FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horarios_trabalho`
--

LOCK TABLES `horarios_trabalho` WRITE;
/*!40000 ALTER TABLE `horarios_trabalho` DISABLE KEYS */;
INSERT INTO `horarios_trabalho` VALUES
(1,1,0,'18:00:00','00:00:00'),
(2,1,1,'18:00:00','00:00:00'),
(3,1,2,'18:00:00','00:00:00'),
(4,1,3,'18:00:00','00:00:00'),
(5,1,4,'18:00:00','00:00:00'),
(6,1,5,'18:00:00','00:00:00'),
(7,1,6,'18:00:00','00:00:00');
/*!40000 ALTER TABLE `horarios_trabalho` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profissionais`
--

DROP TABLE IF EXISTS `profissionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `profissionais` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `especialidade` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `intervalo_minutos` int(11) NOT NULL DEFAULT 15,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profissionais`
--

LOCK TABLES `profissionais` WRITE;
/*!40000 ALTER TABLE `profissionais` DISABLE KEYS */;
INSERT INTO `profissionais` VALUES
(1,'João Chef','Cozinheiro',NULL,NULL,15,1);
/*!40000 ALTER TABLE `profissionais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicos`
--

DROP TABLE IF EXISTS `servicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` mediumtext DEFAULT NULL,
  `duracao_minutos` int(11) NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicos`
--

LOCK TABLES `servicos` WRITE;
/*!40000 ALTER TABLE `servicos` DISABLE KEYS */;
INSERT INTO `servicos` VALUES
(1,'Jantar Particular',NULL,240,1700.00,1),
(2,'Corte de cabelo','Corte masculino com tesoura e máquina',30,45.90,1),
(3,'Corte de cabelo','Corte masculino com tesoura e máquina',30,45.90,1);
/*!40000 ALTER TABLE `servicos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-16 11:38:35

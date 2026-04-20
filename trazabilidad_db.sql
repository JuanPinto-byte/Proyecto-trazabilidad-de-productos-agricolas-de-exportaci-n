-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: trazabilidad_db
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `agricultores`
--

DROP TABLE IF EXISTS `agricultores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agricultores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `cedula` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agricultores`
--

LOCK TABLES `agricultores` WRITE;
/*!40000 ALTER TABLE `agricultores` DISABLE KEYS */;
/*!40000 ALTER TABLE `agricultores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agroquimicos`
--

DROP TABLE IF EXISTS `agroquimicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agroquimicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dosis_recomendada` decimal(10,2) DEFAULT NULL,
  `unidad_dosis` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `periodo_carencia_dias` int DEFAULT NULL,
  `ficha_tecnica_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agroquimicos`
--

LOCK TABLES `agroquimicos` WRITE;
/*!40000 ALTER TABLE `agroquimicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `agroquimicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `almacenamiento`
--

DROP TABLE IF EXISTS `almacenamiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacenamiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `bodega_id` int NOT NULL,
  `cantidad_kg` decimal(10,2) DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `fecha_salida` date DEFAULT NULL,
  `operario_id` int DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `bodega_id` (`bodega_id`),
  KEY `operario_id` (`operario_id`),
  CONSTRAINT `almacenamiento_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `almacenamiento_ibfk_2` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`),
  CONSTRAINT `almacenamiento_ibfk_3` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacenamiento`
--

LOCK TABLES `almacenamiento` WRITE;
/*!40000 ALTER TABLE `almacenamiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `almacenamiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anomalias`
--

DROP TABLE IF EXISTS `anomalias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anomalias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gravedad` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'PENDIENTE',
  `fecha_deteccion` date NOT NULL,
  `registrado_por_usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `registrado_por_usuario_id` (`registrado_por_usuario_id`),
  CONSTRAINT `anomalias_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `anomalias_ibfk_2` FOREIGN KEY (`registrado_por_usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anomalias`
--

LOCK TABLES `anomalias` WRITE;
/*!40000 ALTER TABLE `anomalias` DISABLE KEYS */;
/*!40000 ALTER TABLE `anomalias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aplicaciones_agroquimicos`
--

DROP TABLE IF EXISTS `aplicaciones_agroquimicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aplicaciones_agroquimicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `agroquimico_id` int NOT NULL,
  `fecha_aplicacion` date NOT NULL,
  `dosis_aplicada` decimal(10,2) DEFAULT NULL,
  `unidad_dosis` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `usuario_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `agroquimico_id` (`agroquimico_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_2` FOREIGN KEY (`agroquimico_id`) REFERENCES `agroquimicos` (`id`),
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aplicaciones_agroquimicos`
--

LOCK TABLES `aplicaciones_agroquimicos` WRITE;
/*!40000 ALTER TABLE `aplicaciones_agroquimicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `aplicaciones_agroquimicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auditoria`
--

DROP TABLE IF EXISTS `auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `tabla_afectada` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tipo_operacion` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `registro_id` int DEFAULT NULL,
  `datos_anteriores` json DEFAULT NULL,
  `datos_nuevos` json DEFAULT NULL,
  `fecha_operacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `direccion_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `auditoria_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria`
--

LOCK TABLES `auditoria` WRITE;
/*!40000 ALTER TABLE `auditoria` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bitacoras_cultivo`
--

DROP TABLE IF EXISTS `bitacoras_cultivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bitacoras_cultivo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `fecha` date NOT NULL,
  `actividades_realizadas` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `agronomo_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `agronomo_id` (`agronomo_id`),
  CONSTRAINT `bitacoras_cultivo_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `bitacoras_cultivo_ibfk_2` FOREIGN KEY (`agronomo_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacoras_cultivo`
--

LOCK TABLES `bitacoras_cultivo` WRITE;
/*!40000 ALTER TABLE `bitacoras_cultivo` DISABLE KEYS */;
/*!40000 ALTER TABLE `bitacoras_cultivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bodegas`
--

DROP TABLE IF EXISTS `bodegas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bodegas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capacidad_maxima_kg` decimal(10,2) DEFAULT NULL,
  `tipo_almacenamiento` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temperatura_setpoint` decimal(5,2) DEFAULT NULL,
  `humedad_setpoint` decimal(5,2) DEFAULT NULL,
  `responsable_id` int DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `responsable_id` (`responsable_id`),
  CONSTRAINT `bodegas_ibfk_1` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bodegas`
--

LOCK TABLES `bodegas` WRITE;
/*!40000 ALTER TABLE `bodegas` DISABLE KEYS */;
/*!40000 ALTER TABLE `bodegas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `condiciones_meteorologicas`
--

DROP TABLE IF EXISTS `condiciones_meteorologicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `condiciones_meteorologicas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `fecha` date NOT NULL,
  `temperatura` decimal(5,2) DEFAULT NULL,
  `humedad` decimal(5,2) DEFAULT NULL,
  `precipitacion_mm` decimal(6,2) DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  CONSTRAINT `condiciones_meteorologicas_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condiciones_meteorologicas`
--

LOCK TABLES `condiciones_meteorologicas` WRITE;
/*!40000 ALTER TABLE `condiciones_meteorologicas` DISABLE KEYS */;
/*!40000 ALTER TABLE `condiciones_meteorologicas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_temperaturas`
--

DROP TABLE IF EXISTS `control_temperaturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_temperaturas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bodega_id` int NOT NULL,
  `fecha_hora` timestamp NOT NULL,
  `temperatura` decimal(5,2) DEFAULT NULL,
  `humedad` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bodega_id` (`bodega_id`),
  CONSTRAINT `control_temperaturas_ibfk_1` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_temperaturas`
--

LOCK TABLES `control_temperaturas` WRITE;
/*!40000 ALTER TABLE `control_temperaturas` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_temperaturas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cosechas`
--

DROP TABLE IF EXISTS `cosechas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cosechas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `fecha_cosecha` date NOT NULL,
  `cantidad_total_kg` decimal(10,2) DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `usuario_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `cosechas_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `cosechas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cosechas`
--

LOCK TABLES `cosechas` WRITE;
/*!40000 ALTER TABLE `cosechas` DISABLE KEYS */;
/*!40000 ALTER TABLE `cosechas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cultivos`
--

DROP TABLE IF EXISTS `cultivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cultivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ciclo_dias` int NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cultivos`
--

LOCK TABLES `cultivos` WRITE;
/*!40000 ALTER TABLE `cultivos` DISABLE KEYS */;
/*!40000 ALTER TABLE `cultivos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cumplimiento_normativas`
--

DROP TABLE IF EXISTS `cumplimiento_normativas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cumplimiento_normativas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `normativa_id` int NOT NULL,
  `fecha_verificacion` date DEFAULT NULL,
  `cumple` tinyint(1) DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `inspector_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `normativa_id` (`normativa_id`),
  KEY `inspector_id` (`inspector_id`),
  CONSTRAINT `cumplimiento_normativas_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `cumplimiento_normativas_ibfk_2` FOREIGN KEY (`normativa_id`) REFERENCES `normativas` (`id`),
  CONSTRAINT `cumplimiento_normativas_ibfk_3` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cumplimiento_normativas`
--

LOCK TABLES `cumplimiento_normativas` WRITE;
/*!40000 ALTER TABLE `cumplimiento_normativas` DISABLE KEYS */;
/*!40000 ALTER TABLE `cumplimiento_normativas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fincas`
--

DROP TABLE IF EXISTS `fincas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fincas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_finca` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coordenadas_gps` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `area_total_hectareas` decimal(10,2) DEFAULT NULL,
  `area_cultivable_hectareas` decimal(10,2) DEFAULT NULL,
  `agricultor_id` int NOT NULL,
  `responsable_id` int DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `agricultor_id` (`agricultor_id`),
  KEY `responsable_id` (`responsable_id`),
  CONSTRAINT `fincas_ibfk_1` FOREIGN KEY (`agricultor_id`) REFERENCES `agricultores` (`id`),
  CONSTRAINT `fincas_ibfk_2` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fincas`
--

LOCK TABLES `fincas` WRITE;
/*!40000 ALTER TABLE `fincas` DISABLE KEYS */;
/*!40000 ALTER TABLE `fincas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspecciones`
--

DROP TABLE IF EXISTS `inspecciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspecciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `normativa_id` int NOT NULL,
  `fecha` date NOT NULL,
  `resultado` tinyint(1) DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `inspector_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `normativa_id` (`normativa_id`),
  KEY `inspector_id` (`inspector_id`),
  CONSTRAINT `inspecciones_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `inspecciones_ibfk_2` FOREIGN KEY (`normativa_id`) REFERENCES `normativas` (`id`),
  CONSTRAINT `inspecciones_ibfk_3` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspecciones`
--

LOCK TABLES `inspecciones` WRITE;
/*!40000 ALTER TABLE `inspecciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `inspecciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lotes`
--

DROP TABLE IF EXISTS `lotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lotes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `finca_id` int NOT NULL,
  `numero_lote` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `area_hectareas` decimal(10,2) DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT NULL,
  `usuario_creacion_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `finca_id` (`finca_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `lotes_ibfk_1` FOREIGN KEY (`finca_id`) REFERENCES `fincas` (`id`),
  CONSTRAINT `lotes_ibfk_2` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lotes`
--

LOCK TABLES `lotes` WRITE;
/*!40000 ALTER TABLE `lotes` DISABLE KEYS */;
/*!40000 ALTER TABLE `lotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `normativas`
--

DROP TABLE IF EXISTS `normativas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `normativas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `activa` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `normativas`
--

LOCK TABLES `normativas` WRITE;
/*!40000 ALTER TABLE `normativas` DISABLE KEYS */;
/*!40000 ALTER TABLE `normativas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisos`
--

DROP TABLE IF EXISTS `permisos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `accion` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recurso` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accion` (`accion`,`recurso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos`
--

LOCK TABLES `permisos` WRITE;
/*!40000 ALTER TABLE `permisos` DISABLE KEYS */;
/*!40000 ALTER TABLE `permisos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recepcion_acopio`
--

DROP TABLE IF EXISTS `recepcion_acopio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recepcion_acopio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `fecha_recepcion` date NOT NULL,
  `cantidad_kg` decimal(10,2) DEFAULT NULL,
  `temperatura_recepcion` decimal(5,2) DEFAULT NULL,
  `estado_producto` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operario_id` int DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `operario_id` (`operario_id`),
  CONSTRAINT `recepcion_acopio_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `recepcion_acopio_ibfk_2` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recepcion_acopio`
--

LOCK TABLES `recepcion_acopio` WRITE;
/*!40000 ALTER TABLE `recepcion_acopio` DISABLE KEYS */;
/*!40000 ALTER TABLE `recepcion_acopio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol_permiso`
--

DROP TABLE IF EXISTS `rol_permiso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol_permiso` (
  `rol_id` int NOT NULL,
  `permiso_id` int NOT NULL,
  PRIMARY KEY (`rol_id`,`permiso_id`),
  KEY `permiso_id` (`permiso_id`),
  CONSTRAINT `rol_permiso_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rol_permiso_ibfk_2` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol_permiso`
--

LOCK TABLES `rol_permiso` WRITE;
/*!40000 ALTER TABLE `rol_permiso` DISABLE KEYS */;
/*!40000 ALTER TABLE `rol_permiso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'COORDINADOR','Gestiona fincas, lotes, normativas y supervisa la operación general del sistema','2026-04-19 21:51:14'),(2,'AGRONOMO','Registra siembras, bitácoras de cultivo, aplicaciones de agroquímicos y consulta históricos','2026-04-19 21:51:14'),(3,'OPERARIO','Registra cosechas, recepción en acopio, almacenamiento y control de bodegas','2026-04-19 21:51:14'),(4,'INSPECTOR','Realiza inspecciones de calidad y verifica el cumplimiento de normativas','2026-04-19 21:51:14');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semillas`
--

DROP TABLE IF EXISTS `semillas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semillas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_variedad` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `especie` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `proveedor` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dias_germinacion` int DEFAULT NULL,
  `dias_cosecha` int DEFAULT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semillas`
--

LOCK TABLES `semillas` WRITE;
/*!40000 ALTER TABLE `semillas` DISABLE KEYS */;
/*!40000 ALTER TABLE `semillas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `siembras`
--

DROP TABLE IF EXISTS `siembras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `siembras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `cultivo_id` int NOT NULL,
  `semilla_id` int NOT NULL,
  `fecha_siembra` date NOT NULL,
  `fecha_cosecha_estimada` date DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `usuario_creacion_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `cultivo_id` (`cultivo_id`),
  KEY `semilla_id` (`semilla_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `siembras_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `siembras_ibfk_2` FOREIGN KEY (`cultivo_id`) REFERENCES `cultivos` (`id`),
  CONSTRAINT `siembras_ibfk_3` FOREIGN KEY (`semilla_id`) REFERENCES `semillas` (`id`),
  CONSTRAINT `siembras_ibfk_4` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `siembras`
--

LOCK TABLES `siembras` WRITE;
/*!40000 ALTER TABLE `siembras` DISABLE KEYS */;
/*!40000 ALTER TABLE `siembras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trazabilidad`
--

DROP TABLE IF EXISTS `trazabilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trazabilidad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `codigo_trazabilidad` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_generacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lote_id` (`lote_id`),
  UNIQUE KEY `codigo_trazabilidad` (`codigo_trazabilidad`),
  CONSTRAINT `trazabilidad_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trazabilidad`
--

LOCK TABLES `trazabilidad` WRITE;
/*!40000 ALTER TABLE `trazabilidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `trazabilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_completo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT NULL,
  `ultimo_acceso` timestamp NULL DEFAULT NULL,
  `rol_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_usuarios_roles` (`rol_id`),
  CONSTRAINT `fk_usuarios_roles` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','scrypt:32768:8:1$cmWD4yLi04oZG4g3$72ae99444c273ed34386dd33d9047694f79a07cac7d9f1b3947118c2182b508fc6cc4481c4aa5eb1ed8fbe94449846e0f1c75ae110d8af94d74cf8e89d6ba5d1','jesus david','123@gmail.com',NULL,1,'2026-04-20 02:53:05','2026-04-20 02:53:05',NULL,1),(2,'admin1','scrypt:32768:8:1$Q9iVtqoEv71OId7G$47cc6fb2110074ce8265cee7fd9833c4cd076a42f7c3beef495d380c85ba88a89d1875394997cf4ca1a2c78c6cfd5cf757432ec443edaa4efa4f49a101513393','jesus david','jesus@gmail.com',NULL,1,'2026-04-20 02:54:54','2026-04-20 02:54:54',NULL,1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-19 23:39:32

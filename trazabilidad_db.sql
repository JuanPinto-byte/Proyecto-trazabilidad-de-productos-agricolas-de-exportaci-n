-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: trazabilidad_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
  `departamento` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `municipio_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_agricultores_cedula` (`cedula`),
  KEY `fk_agricultor_municipio` (`municipio_id`),
  CONSTRAINT `fk_agricultor_municipio` FOREIGN KEY (`municipio_id`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agricultores`
--

LOCK TABLES `agricultores` WRITE;
/*!40000 ALTER TABLE `agricultores` DISABLE KEYS */;
INSERT INTO `agricultores` VALUES (1,'Juan Perezz','12345677','3001234567','juan@test.com','Norte de Santander','2026-04-21 04:44:50',NULL);
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
  `dosis_limite_hectarea` decimal(10,2) DEFAULT NULL,
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
  KEY `fk_alm_lote` (`lote_id`),
  KEY `fk_alm_bodega` (`bodega_id`),
  KEY `fk_alm_operario` (`operario_id`),
  CONSTRAINT `fk_alm_bodega` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`),
  CONSTRAINT `fk_alm_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_alm_operario` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`)
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
  KEY `fk_anom_lote` (`lote_id`),
  KEY `fk_anom_usuario` (`registrado_por_usuario_id`),
  CONSTRAINT `fk_anom_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_anom_usuario` FOREIGN KEY (`registrado_por_usuario_id`) REFERENCES `usuarios` (`id`)
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
  KEY `fk_aplic_lote` (`lote_id`),
  KEY `fk_aplic_agroquim` (`agroquimico_id`),
  KEY `fk_aplic_usuario` (`usuario_id`),
  CONSTRAINT `fk_aplic_agroquim` FOREIGN KEY (`agroquimico_id`) REFERENCES `agroquimicos` (`id`),
  CONSTRAINT `fk_aplic_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_aplic_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
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
  KEY `fk_aud_usuario` (`usuario_id`),
  CONSTRAINT `fk_aud_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
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
  `tipo_actividad` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actividades_realizadas` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `insumos_utilizados` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `temperatura_c` decimal(5,2) DEFAULT NULL,
  `humedad_pct` decimal(5,2) DEFAULT NULL,
  `precipitacion_mm` decimal(6,2) DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `agronomo_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_bitacora_lote` (`lote_id`),
  KEY `fk_bitacora_agronomo` (`agronomo_id`),
  CONSTRAINT `fk_bitacora_agronomo` FOREIGN KEY (`agronomo_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_bitacora_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacoras_cultivo`
--

LOCK TABLES `bitacoras_cultivo` WRITE;
/*!40000 ALTER TABLE `bitacoras_cultivo` DISABLE KEYS */;
INSERT INTO `bitacoras_cultivo` VALUES (2,16,'2026-04-25',NULL,'dada',NULL,NULL,NULL,NULL,'\n=== REGISTRO DE ACTIVIDADES AGRÍCOLAS ===\nFecha: 2026-04-25\n\n--- ACTIVIDADES REALIZADAS ---\ndada\n\n--- ACTIVIDADES ESPECÍFICAS ---\nSiembra: dada\nRiego: dadad\nFertilización: dadad\nInsumos utilizados: adad\n\n--- CONDICIONES AMBIENTALES ---\nTemperatura (°C): 1234\nHumedad (%): 30\nPrecipitación (mm): 323\n\n--- OBSERVACIONES ADICIONALES ---\ndadada\n\n=== FIN DEL REGISTRO ===\n\n--- EVIDENCIA MULTIMEDIA ---\nImágenes adjuntas: 20260425_003038_WhatsApp_Image_2026-03-27_at_6.25.33_AM.jpeg\n',2,'2026-04-25 05:30:38');
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
  `municipio` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `departamento` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capacidad_maxima_kg` decimal(10,2) DEFAULT NULL,
  `tipo_almacenamiento` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temperatura_setpoint` decimal(5,2) DEFAULT NULL,
  `humedad_setpoint` decimal(5,2) DEFAULT NULL,
  `responsable_id` int DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `departamento_id` int unsigned DEFAULT NULL,
  `municipio_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_bodegas_responsable` (`responsable_id`),
  KEY `fk_bodega_departamento` (`departamento_id`),
  KEY `fk_bodega_municipio` (`municipio_id`),
  CONSTRAINT `fk_bodega_departamento` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id`),
  CONSTRAINT `fk_bodega_municipio` FOREIGN KEY (`municipio_id`) REFERENCES `municipios` (`id`),
  CONSTRAINT `fk_bodegas_responsable` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`)
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
-- Table structure for table `certificaciones`
--

DROP TABLE IF EXISTS `certificaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `normativa_id` int NOT NULL,
  `entidad_certificadora` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_certificado` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_emision` date DEFAULT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'PENDIENTE',
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `inspector_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_cert_lote` (`lote_id`),
  KEY `fk_cert_normativa` (`normativa_id`),
  KEY `fk_cert_inspector` (`inspector_id`),
  CONSTRAINT `fk_cert_inspector` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_cert_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_cert_normativa` FOREIGN KEY (`normativa_id`) REFERENCES `normativas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificaciones`
--

LOCK TABLES `certificaciones` WRITE;
/*!40000 ALTER TABLE `certificaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificaciones` ENABLE KEYS */;
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
  KEY `fk_cond_met_lote` (`lote_id`),
  CONSTRAINT `fk_cond_met_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`)
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
  KEY `fk_ct_bodega` (`bodega_id`),
  CONSTRAINT `fk_ct_bodega` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`)
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
  KEY `fk_cosechas_lote` (`lote_id`),
  KEY `fk_cosechas_usuario` (`usuario_id`),
  CONSTRAINT `fk_cosechas_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_cosechas_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
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
  KEY `fk_cn_lote` (`lote_id`),
  KEY `fk_cn_normativa` (`normativa_id`),
  KEY `fk_cn_inspector` (`inspector_id`),
  CONSTRAINT `fk_cn_inspector` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_cn_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_cn_normativa` FOREIGN KEY (`normativa_id`) REFERENCES `normativas` (`id`)
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
-- Table structure for table `departamentos`
--

DROP TABLE IF EXISTS `departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamentos` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamentos`
--

LOCK TABLES `departamentos` WRITE;
/*!40000 ALTER TABLE `departamentos` DISABLE KEYS */;
INSERT INTO `departamentos` VALUES (1,'Amazonas'),(2,'Antioquia'),(3,'Arauca'),(4,'Atlántico'),(33,'Bogotá D.C.'),(5,'Bolívar'),(6,'Boyacá'),(7,'Caldas'),(8,'Caquetá'),(9,'Casanare'),(10,'Cauca'),(11,'Cesar'),(12,'Chocó'),(13,'Córdoba'),(14,'Cundinamarca'),(15,'Guainía'),(16,'Guaviare'),(17,'Huila'),(18,'La Guajira'),(19,'Magdalena'),(20,'Meta'),(21,'Nariño'),(22,'Norte de Santander'),(23,'Putumayo'),(24,'Quindío'),(25,'Risaralda'),(26,'San Andrés y Providencia'),(27,'Santander'),(28,'Sucre'),(29,'Tolima'),(30,'Valle del Cauca'),(31,'Vaupés'),(32,'Vichada');
/*!40000 ALTER TABLE `departamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `despachos`
--

DROP TABLE IF EXISTS `despachos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `despachos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `codigo_contenedor` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_despacho` date DEFAULT NULL,
  `puerto_destino` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pais_destino` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'PROGRAMADO',
  `ubicacion_actual` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_estimada_llegada` date DEFAULT NULL,
  `operario_id` int DEFAULT NULL,
  `observaciones` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT NULL,
  `municipio_origen_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_desp_lote` (`lote_id`),
  KEY `fk_desp_operario` (`operario_id`),
  KEY `fk_despacho_municipio` (`municipio_origen_id`),
  CONSTRAINT `fk_desp_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_desp_operario` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_despacho_municipio` FOREIGN KEY (`municipio_origen_id`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `despachos`
--

LOCK TABLES `despachos` WRITE;
/*!40000 ALTER TABLE `despachos` DISABLE KEYS */;
/*!40000 ALTER TABLE `despachos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos_trazabilidad`
--

DROP TABLE IF EXISTS `eventos_trazabilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos_trazabilidad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `etapa` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `usuario_id` int DEFAULT NULL,
  `fecha_evento` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `municipio_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_et_lote` (`lote_id`),
  KEY `fk_et_usuario` (`usuario_id`),
  KEY `fk_evento_municipio` (`municipio_id`),
  CONSTRAINT `fk_et_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_et_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_evento_municipio` FOREIGN KEY (`municipio_id`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_trazabilidad`
--

LOCK TABLES `eventos_trazabilidad` WRITE;
/*!40000 ALTER TABLE `eventos_trazabilidad` DISABLE KEYS */;
INSERT INTO `eventos_trazabilidad` VALUES (1,16,'GENERADO','{\"ubicacion_actual\": \"cucuta\", \"transportista\": \"sdada\", \"vehiculo\": \"dadada\", \"origen\": \"adada\", \"destino\": \"dada\", \"observaciones\": \"dadad\"}',6,'2026-04-25 05:34:37',NULL),(2,16,'EN_TRANSITO','{\"ubicacion_actual\": \"dada\", \"transportista\": \"dada\", \"vehiculo\": \"dada\", \"origen\": \"dada\", \"destino\": \"dada\", \"observaciones\": \"dada\"}',6,'2026-04-25 05:34:47',NULL),(3,16,'EN_PUERTO','{\"ubicacion_actual\": \"dadad\", \"transportista\": \"adada\", \"vehiculo\": \"dada\", \"origen\": \"dadada\", \"destino\": \"dada\", \"observaciones\": \"daa\"}',6,'2026-04-25 05:34:54',NULL),(4,16,'ENTREGADO','{\"ubicacion_actual\": \"dada\", \"transportista\": \"dadada\", \"vehiculo\": \"dada\", \"origen\": \"dadadada\", \"destino\": \"dada\", \"observaciones\": \"dadad\"}',6,'2026-04-25 05:35:07',NULL),(5,16,'BLOQUEADO','{\"ubicacion_actual\": \"dada\", \"transportista\": \"dada\", \"vehiculo\": \"dadad\", \"origen\": \"dada\", \"destino\": \"dada\", \"observaciones\": \"dada\"}',6,'2026-04-25 05:35:24',NULL);
/*!40000 ALTER TABLE `eventos_trazabilidad` ENABLE KEYS */;
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
  `municipio` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `departamento` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coordenadas_gps` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `area_total_hectareas` decimal(10,2) DEFAULT NULL,
  `area_cultivable_hectareas` decimal(10,2) DEFAULT NULL,
  `agricultor_id` int NOT NULL,
  `responsable_id` int DEFAULT NULL,
  `estado` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT NULL,
  `departamento_id` int unsigned DEFAULT NULL,
  `municipio_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_fincas_agricultor` (`agricultor_id`),
  KEY `fk_fincas_responsable` (`responsable_id`),
  KEY `fk_finca_departamento` (`departamento_id`),
  KEY `fk_finca_municipio` (`municipio_id`),
  CONSTRAINT `fk_finca_departamento` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id`),
  CONSTRAINT `fk_finca_municipio` FOREIGN KEY (`municipio_id`) REFERENCES `municipios` (`id`),
  CONSTRAINT `fk_fincas_agricultor` FOREIGN KEY (`agricultor_id`) REFERENCES `agricultores` (`id`),
  CONSTRAINT `fk_fincas_responsable` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fincas`
--

LOCK TABLES `fincas` WRITE;
/*!40000 ALTER TABLE `fincas` DISABLE KEYS */;
INSERT INTO `fincas` VALUES (1,'Finca bareta','Cucuta','Norte de Santander','',10.00,7.00,1,5,'ACTIVO','2026-04-23 04:25:36','2026-04-23 04:25:41',NULL,NULL),(4,'Finca Unam','Cucuta','Norte de Santander','EAEAEA',10.00,7.00,1,6,'ACTIVO','2026-04-23 09:59:49','2026-04-23 11:21:07',NULL,NULL);
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
  KEY `fk_insp_lote` (`lote_id`),
  KEY `fk_insp_normativa` (`normativa_id`),
  KEY `fk_insp_inspector` (`inspector_id`),
  CONSTRAINT `fk_insp_inspector` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_insp_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_insp_normativa` FOREIGN KEY (`normativa_id`) REFERENCES `normativas` (`id`)
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
  UNIQUE KEY `uq_lote_por_finca` (`finca_id`,`numero_lote`),
  KEY `fk_lotes_usuario` (`usuario_creacion_id`),
  CONSTRAINT `fk_lotes_finca` FOREIGN KEY (`finca_id`) REFERENCES `fincas` (`id`),
  CONSTRAINT `fk_lotes_usuario` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lotes`
--

LOCK TABLES `lotes` WRITE;
/*!40000 ALTER TABLE `lotes` DISABLE KEYS */;
INSERT INTO `lotes` VALUES (16,1,'LT-2026-001','',0.01,'ACTIVO','2026-04-23 10:06:43','2026-04-25 10:29:53',6),(19,1,'LT-2026-002','',2.00,'ACTIVO','2026-04-23 10:29:40',NULL,6),(20,4,'LT-2026-002','',3.00,'ACTIVO','2026-04-23 10:29:57','2026-04-23 11:36:25',6),(22,4,'LT-2026-004','',1.00,'ACTIVO','2026-04-23 11:47:25','2026-04-25 07:43:06',6);
/*!40000 ALTER TABLE `lotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `municipios`
--

DROP TABLE IF EXISTS `municipios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `municipios` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `departamento_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `departamento_id` (`departamento_id`),
  CONSTRAINT `municipios_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipios`
--

LOCK TABLES `municipios` WRITE;
/*!40000 ALTER TABLE `municipios` DISABLE KEYS */;
INSERT INTO `municipios` VALUES (1,'Leticia',1),(2,'Puerto Nariño',1),(3,'Medellín',2),(4,'Bello',2),(5,'Envigado',2),(6,'Rionegro',2),(7,'Arauca',3),(8,'Saravena',3),(9,'Barranquilla',4),(10,'Soledad',4),(11,'Malambo',4),(12,'Cartagena',5),(13,'Magangué',5),(14,'Mompós',5),(15,'Tunja',6),(16,'Duitama',6),(17,'Sogamoso',6),(18,'Manizales',7),(19,'Villamaría',7),(20,'La Dorada',7),(21,'Florencia',8),(22,'San Vicente del Caguán',8),(23,'Yopal',9),(24,'Aguazul',9),(25,'Popayán',10),(26,'Santander de Quilichao',10),(27,'Valledupar',11),(28,'Aguachica',11),(29,'Quibdó',12),(30,'Istmina',12),(31,'Montería',13),(32,'Lorica',13),(33,'Soacha',14),(34,'Zipaquirá',14),(35,'Fusagasugá',14),(36,'Inírida',15),(37,'San José del Guaviare',16),(38,'Neiva',17),(39,'Pitalito',17),(40,'Riohacha',18),(41,'Maicao',18),(42,'Santa Marta',19),(43,'Ciénaga',19),(44,'Villavicencio',20),(45,'Acacías',20),(46,'Pasto',21),(47,'Ipiales',21),(48,'Cúcuta',22),(49,'Ocaña',22),(50,'Pamplona',22),(51,'Mocoa',23),(52,'Puerto Asís',23),(53,'Armenia',24),(54,'Montenegro',24),(55,'Pereira',25),(56,'Dosquebradas',25),(57,'San Andrés',26),(58,'Providencia',26),(59,'Bucaramanga',27),(60,'Floridablanca',27),(61,'Barrancabermeja',27),(62,'Sincelejo',28),(63,'Corozal',28),(64,'Ibagué',29),(65,'Espinal',29),(66,'Cali',30),(67,'Palmira',30),(68,'Buenaventura',30),(69,'Mitú',31),(70,'Puerto Carreño',32),(71,'Bogotá',33);
/*!40000 ALTER TABLE `municipios` ENABLE KEYS */;
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
  `organismo_emisor` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mercado_destino` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `version` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_vigencia` date DEFAULT NULL,
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
  UNIQUE KEY `uq_permiso` (`accion`,`recurso`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos`
--

LOCK TABLES `permisos` WRITE;
/*!40000 ALTER TABLE `permisos` DISABLE KEYS */;
INSERT INTO `permisos` VALUES (17,'crear','agricultores'),(39,'crear','almacenamiento'),(28,'crear','aplicaciones_agroquimicos'),(22,'crear','bitacoras_cultivo'),(31,'crear','condiciones_meteorologicas'),(42,'crear','control_temperaturas'),(35,'crear','cosechas'),(48,'crear','cumplimiento_normativas'),(1,'crear','fincas'),(46,'crear','inspecciones'),(5,'crear','lotes'),(9,'crear','normativas'),(37,'crear','recepcion_acopio'),(25,'crear','siembras'),(33,'crear','sincronizacion_offline'),(13,'crear','usuarios'),(18,'editar','agricultores'),(40,'editar','almacenamiento'),(29,'editar','aplicaciones_agroquimicos'),(23,'editar','bitacoras_cultivo'),(43,'editar','control_temperaturas'),(2,'editar','fincas'),(6,'editar','lotes'),(10,'editar','normativas'),(26,'editar','siembras'),(14,'editar','usuarios'),(19,'eliminar','agricultores'),(3,'eliminar','fincas'),(7,'eliminar','lotes'),(11,'eliminar','normativas'),(15,'eliminar','usuarios'),(20,'ver','agricultores'),(41,'ver','almacenamiento'),(30,'ver','aplicaciones_agroquimicos'),(24,'ver','bitacoras_cultivo'),(32,'ver','condiciones_meteorologicas'),(44,'ver','control_temperaturas'),(36,'ver','cosechas'),(49,'ver','cumplimiento_normativas'),(45,'ver','despachos'),(51,'ver','eventos_trazabilidad'),(4,'ver','fincas'),(47,'ver','inspecciones'),(8,'ver','lotes'),(12,'ver','normativas'),(38,'ver','recepcion_acopio'),(21,'ver','reportes'),(27,'ver','siembras'),(34,'ver','sincronizacion_offline'),(50,'ver','trazabilidad'),(16,'ver','usuarios');
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
  KEY `fk_acopio_lote` (`lote_id`),
  KEY `fk_acopio_operario` (`operario_id`),
  CONSTRAINT `fk_acopio_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_acopio_operario` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`)
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
  KEY `fk_rp_permiso` (`permiso_id`),
  CONSTRAINT `fk_rp_permiso` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_rp_rol` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol_permiso`
--

LOCK TABLES `rol_permiso` WRITE;
/*!40000 ALTER TABLE `rol_permiso` DISABLE KEYS */;
INSERT INTO `rol_permiso` VALUES (1,1),(1,2),(1,3),(1,4),(2,4),(3,4),(1,5),(1,6),(1,7),(1,8),(2,8),(3,8),(1,9),(1,10),(1,11),(1,12),(2,12),(1,13),(1,14),(1,15),(1,16),(1,17),(1,18),(1,19),(1,20),(2,20),(1,21),(1,22),(2,22),(1,23),(2,23),(1,24),(2,24),(1,25),(2,25),(1,26),(2,26),(1,27),(2,27),(1,28),(2,28),(1,29),(2,29),(1,30),(2,30),(1,31),(2,31),(1,32),(2,32),(1,33),(2,33),(1,34),(2,34),(1,35),(3,35),(1,36),(3,36),(1,37),(3,37),(1,38),(3,38),(1,39),(3,39),(1,40),(3,40),(1,41),(3,41),(1,42),(3,42),(1,43),(3,43),(1,44),(3,44),(1,45),(3,45),(1,46),(4,46),(1,47),(4,47),(1,48),(4,48),(1,49),(4,49),(1,50),(4,50),(1,51),(4,51);
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
  UNIQUE KEY `uq_roles_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'COORDINADOR','Gestiona fincas, lotes, normativas y supervisa la operacion general del sistema','2026-04-20 02:29:11'),(2,'AGRONOMO','Registra siembras, bitacoras de cultivo, aplicaciones de agroquimicos y consulta historicos','2026-04-20 02:29:11'),(3,'OPERARIO','Registra cosechas, recepcion en acopio, almacenamiento y control de bodegas','2026-04-20 02:29:11'),(4,'INSPECTOR','Realiza inspecciones de calidad y verifica el cumplimiento de normativas','2026-04-20 02:29:11');
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
  KEY `fk_siembras_lote` (`lote_id`),
  KEY `fk_siembras_cultivo` (`cultivo_id`),
  KEY `fk_siembras_semilla` (`semilla_id`),
  KEY `fk_siembras_usuario` (`usuario_creacion_id`),
  CONSTRAINT `fk_siembras_cultivo` FOREIGN KEY (`cultivo_id`) REFERENCES `cultivos` (`id`),
  CONSTRAINT `fk_siembras_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`),
  CONSTRAINT `fk_siembras_semilla` FOREIGN KEY (`semilla_id`) REFERENCES `semillas` (`id`),
  CONSTRAINT `fk_siembras_usuario` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`)
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
-- Table structure for table `sincronizacion_offline`
--

DROP TABLE IF EXISTS `sincronizacion_offline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sincronizacion_offline` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `tipo_formulario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `referencia_id` int DEFAULT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'PENDIENTE',
  `datos_json` json DEFAULT NULL,
  `fecha_descarga` timestamp NULL DEFAULT NULL,
  `fecha_sincronizacion` timestamp NULL DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_sync_usuario` (`usuario_id`),
  CONSTRAINT `fk_sync_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sincronizacion_offline`
--

LOCK TABLES `sincronizacion_offline` WRITE;
/*!40000 ALTER TABLE `sincronizacion_offline` DISABLE KEYS */;
/*!40000 ALTER TABLE `sincronizacion_offline` ENABLE KEYS */;
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
  UNIQUE KEY `uq_traz_lote` (`lote_id`),
  UNIQUE KEY `uq_traz_codigo` (`codigo_trazabilidad`),
  CONSTRAINT `fk_traz_lote` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trazabilidad`
--

LOCK TABLES `trazabilidad` WRITE;
/*!40000 ALTER TABLE `trazabilidad` DISABLE KEYS */;
INSERT INTO `trazabilidad` VALUES (1,16,'TRZ-LT-2026-001-DED6DD','2026-04-25 05:35:24','BLOQUEADO'),(2,19,'TRZ-LT-2026-002-06D1E8','2026-04-25 02:24:30','GENERADO');
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
  UNIQUE KEY `uq_usuarios_username` (`nombre_usuario`),
  UNIQUE KEY `uq_usuarios_email` (`email`),
  KEY `fk_usuarios_rol` (`rol_id`),
  CONSTRAINT `fk_usuarios_rol` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (2,'baselessjerik','scrypt:32768:8:1$CnKcUmcSPtbtwKfR$155dd541d8a5c25afeae9fad9f251debe36b9cf268f96fa9e8bc660f949a46c722be8a5c64a5ca64208950d9b59716fbbdbc827dc894f7cd6ea19ee0cba1df4c','jerik botello','jerikbotello4@gmail.com',NULL,1,'2026-04-20 07:43:03','2026-04-23 04:27:43','2026-04-23 04:27:43',1),(3,'poyito','scrypt:32768:8:1$UxKC8hkahTAeS7tn$1cb73070f23fd80076e33be9fc778b574333f7ae2baf80e66b5b7f1726f25242e2ca10fe0f6a3adf8728f668bd563eb85ad5d336f04029bc044f903bfe25de61','jesus anaya','ayup@gmail.com',NULL,1,'2026-04-20 07:49:43','2026-04-20 07:49:43',NULL,1),(4,'Jean123','scrypt:32768:8:1$Qr5PHE4ktxV1l0Bd$97ccaf488795d19c48a58a74c57176825db21da5e204300b82dd4914ba14f97712829da8465172861b2b7d434bbbd8a296a470b854a11ed77429dc9f5f051985','Jean carlos Martinez poyo','jean4@gmail.com',NULL,1,'2026-04-20 08:21:24','2026-04-20 08:21:24',NULL,1),(5,'polo','scrypt:32768:8:1$juAajR9qVTj49386$00183c79ecc1a742bac6126a38b3b269e17e55ac1b077e97c1154d17c067051a0044d85fec7a5fe83869aa6b9b06ca8d85b95baa1560654b473e40bc1cbd6c89','polo polo','polo@gmail.com',NULL,1,'2026-04-20 08:23:57','2026-04-23 04:22:29','2026-04-23 04:22:29',3),(6,'camisa under gold','scrypt:32768:8:1$ICwvnZepJBmcJXpp$61d149f209d165c20f101da7c1ef6737100483be50e996dacb140f3c32071ab0560a56af32582dd97fab3f610fb7258ae54c9084e7f5a888ca3b7e05d73309a0','Camisa under gold blanca castellanos anaya','camisa_undergold@gmail.com','3138891500',1,'2026-04-23 04:28:59','2026-04-25 08:56:51','2026-04-25 08:56:51',1);
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

-- Dump completed on 2026-04-25 13:26:49

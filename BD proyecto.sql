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
-- Table structure for table `agroquimicos`
--

DROP TABLE IF EXISTS `agroquimicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agroquimicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` enum('Fertilizante','Pesticida','Fungicida','Herbicida','Otro') COLLATE utf8mb4_unicode_ci NOT NULL,
  `principio_activo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dosis_recomendada` decimal(10,2) DEFAULT NULL,
  `unidad_dosis` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `periodo_carencia_dias` int DEFAULT NULL,
  `limite_residuos_ppm` decimal(10,4) DEFAULT NULL,
  `ficha_tecnica_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `proveedor` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `costo_unitario` decimal(10,2) DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
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
  `bodega_id` int NOT NULL,
  `lote_id` int DEFAULT NULL,
  `numero_contenedor` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temperatura_actual` decimal(5,2) DEFAULT NULL,
  `temperatura_setpoint` decimal(5,2) DEFAULT NULL,
  `humedad_actual` decimal(5,2) DEFAULT NULL,
  `cantidad_kg` decimal(10,2) DEFAULT NULL,
  `estado_contenedor` enum('Lleno','Parcial','Vacío') COLLATE utf8mb4_unicode_ci DEFAULT 'Lleno',
  `fecha_ingreso` date DEFAULT NULL,
  `fecha_salida` date DEFAULT NULL,
  `operario_id` int DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `bodega_id` (`bodega_id`),
  KEY `lote_id` (`lote_id`),
  KEY `operario_id` (`operario_id`),
  CONSTRAINT `almacenamiento_ibfk_1` FOREIGN KEY (`bodega_id`) REFERENCES `bodegas` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `almacenamiento_ibfk_2` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE SET NULL,
  CONSTRAINT `almacenamiento_ibfk_3` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `unidad_dosis` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `razon_aplicacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `condiciones_clima` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operario_id` int DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_creacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `agroquimico_id` (`agroquimico_id`),
  KEY `operario_id` (`operario_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_2` FOREIGN KEY (`agroquimico_id`) REFERENCES `agroquimicos` (`id`),
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_3` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `aplicaciones_agroquimicos_ibfk_4` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
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
  `usuario_id` int DEFAULT NULL,
  `tabla_afectada` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tipo_operacion` enum('INSERT','UPDATE','DELETE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `registro_id` int DEFAULT NULL,
  `datos_anteriores` json DEFAULT NULL,
  `datos_nuevos` json DEFAULT NULL,
  `fecha_operacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `direccion_ip` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `auditoria_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `etapa_cultivo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actividades_realizadas` text COLLATE utf8mb4_unicode_ci,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `problemas_detectados` text COLLATE utf8mb4_unicode_ci,
  `acciones_tomadas` text COLLATE utf8mb4_unicode_ci,
  `agrónomo_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `agrónomo_id` (`agrónomo_id`),
  CONSTRAINT `bitacoras_cultivo_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bitacoras_cultivo_ibfk_2` FOREIGN KEY (`agrónomo_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `nombre_bodega` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capacidad_maxima_kg` decimal(15,2) DEFAULT NULL,
  `tipo_almacenamiento` enum('Temperatura Controlada','Temperatura Ambiente','Refrigerado') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temperatura_setpoint` decimal(5,2) DEFAULT NULL,
  `humedad_setpoint` decimal(5,2) DEFAULT NULL,
  `responsable_id` int DEFAULT NULL,
  `estado` enum('Operativa','Mantenimiento','Fuera de Servicio') COLLATE utf8mb4_unicode_ci DEFAULT 'Operativa',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `responsable_id` (`responsable_id`),
  CONSTRAINT `bodegas_ibfk_1` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `temperatura_minima` decimal(5,2) DEFAULT NULL,
  `temperatura_maxima` decimal(5,2) DEFAULT NULL,
  `temperatura_promedio` decimal(5,2) DEFAULT NULL,
  `humedad_relativa` decimal(5,2) DEFAULT NULL,
  `precipitacion_mm` decimal(10,2) DEFAULT NULL,
  `velocidad_viento_kmh` decimal(5,2) DEFAULT NULL,
  `radiacion_solar` decimal(10,2) DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `agrónomo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_meteo` (`lote_id`,`fecha`),
  KEY `agrónomo_id` (`agrónomo_id`),
  CONSTRAINT `condiciones_meteorologicas_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `condiciones_meteorologicas_ibfk_2` FOREIGN KEY (`agrónomo_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `cantidad_recibida_acopio_kg` decimal(10,2) DEFAULT NULL,
  `porcentaje_perdida` decimal(5,2) DEFAULT NULL,
  `razon_perdida` text COLLATE utf8mb4_unicode_ci,
  `calidad_cosecha` enum('Excelente','Buena','Regular','Deficiente') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `operario_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_creacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `operario_id` (`operario_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `cosechas_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cosechas_ibfk_2` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `cosechas_ibfk_3` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
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
-- Table structure for table `cumplimiento_normativas`
--

DROP TABLE IF EXISTS `cumplimiento_normativas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cumplimiento_normativas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lote_id` int NOT NULL,
  `normativa_id` int NOT NULL,
  `fecha_verificacion` date NOT NULL,
  `cumple` tinyint(1) DEFAULT NULL,
  `valor_medido` decimal(10,4) DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `inspector_id` int DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `normativa_id` (`normativa_id`),
  KEY `inspector_id` (`inspector_id`),
  CONSTRAINT `cumplimiento_normativas_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cumplimiento_normativas_ibfk_2` FOREIGN KEY (`normativa_id`) REFERENCES `normativas` (`id`),
  CONSTRAINT `cumplimiento_normativas_ibfk_3` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `nombre_finca` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coordenadas_gps` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `area_total_hectareas` decimal(10,2) DEFAULT NULL,
  `area_cultivable_hectareas` decimal(10,2) DEFAULT NULL,
  `propietario_nombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `propietario_cedula` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `propietario_telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `propietario_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `responsable_id` int DEFAULT NULL,
  `estado` enum('Activa','Inactiva','En Construcción') COLLATE utf8mb4_unicode_ci DEFAULT 'Activa',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_creacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `responsable_id` (`responsable_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `fincas_ibfk_1` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fincas_ibfk_2` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
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
  `inspector_id` int DEFAULT NULL,
  `fecha_inspeccion` date NOT NULL,
  `tipo_inspeccion` enum('Pre-Cosecha','Post-Cosecha','Almacenamiento','Pre-Despacho') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado_inspeccion` enum('Satisfactoria','Satisfactoria Con Observaciones','Insatisfactoria') COLLATE utf8mb4_unicode_ci NOT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `anomalias_detectadas` text COLLATE utf8mb4_unicode_ci,
  `recomendaciones` text COLLATE utf8mb4_unicode_ci,
  `bloquear_despacho` tinyint(1) DEFAULT '0',
  `motivo_bloqueo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `inspector_id` (`inspector_id`),
  CONSTRAINT `inspecciones_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `inspecciones_ibfk_2` FOREIGN KEY (`inspector_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
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
  `numero_lote` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `area_hectareas` decimal(10,2) DEFAULT NULL,
  `tipo_cultivo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `agrónomo_id` int DEFAULT NULL,
  `fecha_siembra` date DEFAULT NULL,
  `fecha_cosecha_estimada` date DEFAULT NULL,
  `fecha_cosecha_real` date DEFAULT NULL,
  `estado` enum('Preparación','Sembrado','Crecimiento','Cosecha','Finalizado') COLLATE utf8mb4_unicode_ci DEFAULT 'Preparación',
  `codigo_trazabilidad` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_creacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_lote` (`finca_id`,`numero_lote`),
  UNIQUE KEY `codigo_trazabilidad` (`codigo_trazabilidad`),
  KEY `agrónomo_id` (`agrónomo_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `lotes_ibfk_1` FOREIGN KEY (`finca_id`) REFERENCES `fincas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `lotes_ibfk_2` FOREIGN KEY (`agrónomo_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `lotes_ibfk_3` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
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
  `nombre_normativa` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `codigo_normativa` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `tipo` enum('Ambiental','Sanitaria','De Trazabilidad','De Agroquímicos','Otra') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `limite_minimo` decimal(10,4) DEFAULT NULL,
  `limite_maximo` decimal(10,4) DEFAULT NULL,
  `unidad_medida` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `requisitos_cumplimiento` text COLLATE utf8mb4_unicode_ci,
  `fecha_vigencia` date DEFAULT NULL,
  `activa` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
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
  `humedad_recepcion` decimal(5,2) DEFAULT NULL,
  `estado_producto` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_contenedor` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operario_id` int DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_creacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `operario_id` (`operario_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `recepcion_acopio_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `recepcion_acopio_ibfk_2` FOREIGN KEY (`operario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `recepcion_acopio_ibfk_3` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
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
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Coordinador General','Gestión general del sistema','2026-03-28 16:20:12'),(2,'Agrónomo','Registro de cultivos y condiciones','2026-03-28 16:20:12'),(3,'Operario de Acopio','Recepción y almacenamiento','2026-03-28 16:20:12'),(4,'Inspector Externo','Inspecciones de calidad','2026-03-28 16:20:12'),(5,'Administrador','Administración del sistema','2026-03-28 16:20:12');
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
  `nombre_variedad` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `especie` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proveedor` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dias_germinacion` int DEFAULT NULL,
  `dias_cosecha` int DEFAULT NULL,
  `temperatura_optima_min` decimal(5,2) DEFAULT NULL,
  `temperatura_optima_max` decimal(5,2) DEFAULT NULL,
  `humedad_optima_min` decimal(5,2) DEFAULT NULL,
  `humedad_optima_max` decimal(5,2) DEFAULT NULL,
  `rendimiento_estimado_kg_ha` decimal(10,2) DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
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
  `semilla_id` int NOT NULL,
  `cantidad_kg` decimal(10,2) DEFAULT NULL,
  `fecha_siembra` date NOT NULL,
  `densidad_siembra_kg_ha` decimal(10,2) DEFAULT NULL,
  `metodo_siembra` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_creacion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `semilla_id` (`semilla_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `siembras_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `siembras_ibfk_2` FOREIGN KEY (`semilla_id`) REFERENCES `semillas` (`id`),
  CONSTRAINT `siembras_ibfk_3` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`) ON DELETE RESTRICT
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
  `codigo_trazabilidad` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_generacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estado_codigo` enum('Activo','Cancelado','Exportado') COLLATE utf8mb4_unicode_ci DEFAULT 'Activo',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_trazabilidad` (`codigo_trazabilidad`),
  KEY `lote_id` (`lote_id`),
  CONSTRAINT `trazabilidad_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes` (`id`) ON DELETE CASCADE
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
  `nombre_usuario` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_completo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rol_id` int NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ultimo_acceso` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
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

-- Dump completed on 2026-03-28 12:24:24

-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 16-11-2023 a las 16:40:48
-- Versión del servidor: 10.4.10-MariaDB
-- Versión de PHP: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_acueducto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consumo`
--

DROP TABLE IF EXISTS `consumo`;
CREATE TABLE IF NOT EXISTS `consumo` (
  `cod_consumo` int(11) NOT NULL AUTO_INCREMENT,
  `metros_cubicos` int(11) DEFAULT NULL,
  `num_contador_punto_agua` int(11) DEFAULT NULL,
  PRIMARY KEY (`cod_consumo`),
  KEY `num_contador_punto_agua` (`num_contador_punto_agua`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Disparadores `consumo`
--
DROP TRIGGER IF EXISTS `actualizar_recibo_despues_insertar`;
DELIMITER $$
CREATE TRIGGER `actualizar_recibo_despues_insertar` AFTER INSERT ON `consumo` FOR EACH ROW BEGIN
    
    DECLARE id_propietario_val INT;
    DECLARE nombres_propietario VARCHAR(50);
    DECLARE apellidos_propietario VARCHAR(50);

    
    SELECT id, nombres, apellidos INTO id_propietario_val, nombres_propietario, apellidos_propietario
    FROM propietario
    WHERE id = (SELECT id_propietario FROM predio_propietario WHERE id_predio = (SELECT num_catastral_predio FROM punto_agua WHERE num_contador = NEW.num_contador_punto_agua));

    
    INSERT INTO recibo (id_propietario, nombres, apellidos, lectura_actual)
    VALUES (id_propietario_val, nombres_propietario, apellidos_propietario, NEW.metros_cubicos);

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gasto_acueducto`
--

DROP TABLE IF EXISTS `gasto_acueducto`;
CREATE TABLE IF NOT EXISTS `gasto_acueducto` (
  `id_tipo_gasto` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(70) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `monto` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id_tipo_gasto`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Disparadores `gasto_acueducto`
--
DROP TRIGGER IF EXISTS `eliminar_gasto_acueducto_after_delete`;
DELIMITER $$
CREATE TRIGGER `eliminar_gasto_acueducto_after_delete` AFTER DELETE ON `gasto_acueducto` FOR EACH ROW BEGIN
    DELETE FROM gasto_acueducto_contador WHERE id_tipo_gasto = OLD.id_tipo_gasto;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gasto_acueducto_contador`
--

DROP TABLE IF EXISTS `gasto_acueducto_contador`;
CREATE TABLE IF NOT EXISTS `gasto_acueducto_contador` (
  `id_tipo_gasto` int(11) DEFAULT NULL,
  `num_contador_punto_agua` int(11) DEFAULT NULL,
  KEY `id_tipo_gasto` (`id_tipo_gasto`),
  KEY `num_contador_punto_agua` (`num_contador_punto_agua`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial`
--

DROP TABLE IF EXISTS `historial`;
CREATE TABLE IF NOT EXISTS `historial` (
  `cod_historia` int(11) NOT NULL AUTO_INCREMENT,
  `consumo` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `num_contador_punto_agua` int(11) DEFAULT NULL,
  PRIMARY KEY (`cod_historia`),
  KEY `num_contador_punto_agua` (`num_contador_punto_agua`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `oficio`
--

DROP TABLE IF EXISTS `oficio`;
CREATE TABLE IF NOT EXISTS `oficio` (
  `num_oficio` int(11) NOT NULL AUTO_INCREMENT,
  `asunto` varchar(70) DEFAULT NULL,
  `descripcion` varchar(70) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`num_oficio`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `predio`
--

DROP TABLE IF EXISTS `predio`;
CREATE TABLE IF NOT EXISTS `predio` (
  `num_catastral` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_predio` varchar(30) DEFAULT NULL,
  `direccion` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`num_catastral`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `predio_propietario`
--

DROP TABLE IF EXISTS `predio_propietario`;
CREATE TABLE IF NOT EXISTS `predio_propietario` (
  `id_predio` int(11) DEFAULT NULL,
  `id_propietario` bigint(20) DEFAULT NULL,
  KEY `id_predio` (`id_predio`),
  KEY `id_propietario` (`id_propietario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propietario`
--

DROP TABLE IF EXISTS `propietario`;
CREATE TABLE IF NOT EXISTS `propietario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_cedula` bigint(20) DEFAULT NULL,
  `nombres` varchar(30) DEFAULT NULL,
  `apellidos` varchar(30) DEFAULT NULL,
  `num_telefono` bigint(20) DEFAULT NULL,
  `correo` varchar(30) DEFAULT NULL,
  `direccion` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Disparadores `propietario`
--
DROP TRIGGER IF EXISTS `eliminar_propietario_cascada`;
DELIMITER $$
CREATE TRIGGER `eliminar_propietario_cascada` BEFORE DELETE ON `propietario` FOR EACH ROW BEGIN
    
    DECLARE id_predio_val INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id_predio FROM predio_propietario WHERE id_propietario = OLD.id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    eliminar_predio:LOOP
        FETCH cur INTO id_predio_val;
        IF done THEN
            LEAVE eliminar_predio;
        END IF;

        
        DELETE FROM punto_agua WHERE num_catastral_predio = id_predio_val;

        
        DELETE FROM predio_propietario WHERE id_predio = id_predio_val;
    END LOOP;

    CLOSE cur;

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propietario_oficio`
--

DROP TABLE IF EXISTS `propietario_oficio`;
CREATE TABLE IF NOT EXISTS `propietario_oficio` (
  `id_oficio` int(11) DEFAULT NULL,
  `id_propietario` bigint(20) DEFAULT NULL,
  KEY `id_oficio` (`id_oficio`),
  KEY `id_propietario` (`id_propietario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `punto_agua`
--

DROP TABLE IF EXISTS `punto_agua`;
CREATE TABLE IF NOT EXISTS `punto_agua` (
  `num_contador` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(20) DEFAULT NULL,
  `num_catastral_predio` int(11) DEFAULT NULL,
  PRIMARY KEY (`num_contador`),
  KEY `num_catastral_predio` (`num_catastral_predio`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibo`
--

DROP TABLE IF EXISTS `recibo`;
CREATE TABLE IF NOT EXISTS `recibo` (
  `num_recibo` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_limite` date DEFAULT NULL,
  `nombres` varchar(50) DEFAULT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `servicio` varchar(10) DEFAULT NULL,
  `consumo` int(11) DEFAULT NULL,
  `lectura_anterior` bigint(20) DEFAULT 0,
  `lectura_actual` bigint(20) DEFAULT NULL,
  `costo_servicio` bigint(20) DEFAULT NULL,
  `inasistencia_asamblea` bigint(20) DEFAULT NULL,
  `contribucion` bigint(20) DEFAULT NULL,
  `otros` bigint(20) DEFAULT NULL,
  `total_pagar` bigint(20) DEFAULT NULL,
  `id_propietario` int(11) DEFAULT NULL,
  PRIMARY KEY (`num_recibo`),
  KEY `id_propietario` (`id_propietario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

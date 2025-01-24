-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-01-2025 a las 23:40:52
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `apis`
--
CREATE DATABASE IF NOT EXISTS `apis` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `apis`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `id` int(2) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(2) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `fk_grupo` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `nombre`, `fk_grupo`) VALUES
(1, 'Acceso Mis Proyectos', 1),
(2, 'Acceso Base de Tickets', 1),
(3, 'Crear Tickets', 1),
(4, 'Actualizar Estado Ticket', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyectos`
--

CREATE TABLE `proyectos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proyectos`
--

INSERT INTO `proyectos` (`id`, `nombre`, `descripcion`, `usuario_id`) VALUES
(1, 'Bancoomeva', 'Banca Xpress+', 1),
(2, 'Allianz', 'Allianz Plataforma PVI de formularios FCC', 1),
(3, 'Seguros mundial', 'Mundial pesados', 1),
(4, 'Seguro Peludo', 'Seguro Peludo', 1),
(5, 'Wiipol', 'Wiipol', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(2) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre`) VALUES
(1, 'Usuario'),
(2, 'Administrador'),
(3, 'Super Administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permisos`
--

CREATE TABLE `rol_permisos` (
  `id` int(11) NOT NULL,
  `fk_rol` int(2) NOT NULL,
  `fk_permiso` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol_permisos`
--

INSERT INTO `rol_permisos` (`id`, `fk_rol`, `fk_permiso`) VALUES
(1, 3, 1),
(2, 3, 2),
(3, 2, 1),
(7, 3, 3),
(8, 2, 3),
(9, 3, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tickets`
--

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `comentario` text DEFAULT NULL,
  `fk_usuario` int(2) NOT NULL,
  `fk_proyecto` int(11) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` enum('abierto','pendiente','atendido','devuelto','cerrado') NOT NULL DEFAULT 'abierto',
  `categoria` varchar(100) DEFAULT NULL,
  `fecha_estimada` datetime DEFAULT NULL,
  `causal_cierre` varchar(255) DEFAULT NULL,
  `comentario_cierre` text DEFAULT NULL,
  `fk_usuario_cierre` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tickets`
--

INSERT INTO `tickets` (`id`, `titulo`, `comentario`, `fk_usuario`, `fk_proyecto`, `fecha_creacion`, `estado`, `categoria`, `fecha_estimada`, `causal_cierre`, `comentario_cierre`, `fk_usuario_cierre`) VALUES
(10, 'Firma de documentos', 'Por favor firmar los documentos urgente', 1, 1, '2025-01-15 22:29:04', 'pendiente', NULL, NULL, NULL, NULL, NULL),
(11, 'Quuo Firma de documentps', 'Firmar documentos con fecha 12-03-2024', 1, 1, '2025-01-20 16:24:45', 'cerrado', NULL, NULL, 'Resuelto por cliente', 'El problema fue solucionado externamente', NULL),
(15, 'Mordecai', 'este es un ticket para mordecai', 1, 2, '2025-01-21 20:41:00', 'cerrado', 'Cliente', '2025-02-16 00:00:00', 'Resuelto por cliente', 'El problema fue solucionado externamente', 1),
(16, 'Bug', 'este es un ticket para mordecai', 1, 2, '2025-01-22 19:07:23', 'cerrado', 'Cliente', '2025-02-16 00:00:00', 'Ticket resuelto', 'Se firmó el documento solicitado', NULL),
(17, 'Bug', 'este es un ticket para mordecai', 1, 2, '2025-01-23 01:40:56', 'cerrado', 'Cliente', '2025-02-16 00:00:00', 'Ticket resuelto', 'Se arregló el bug solicitado', NULL),
(18, 'Solucionar bug en tickets', 'Por favor solucionar los bug al enviar un ticket', 1, 5, '2025-01-25 02:19:40', 'cerrado', 'Bug', '2025-01-30 00:00:00', 'Bug solucionado', 'Se arregló el bug solicitado', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ticket_archivos`
--

CREATE TABLE `ticket_archivos` (
  `id` int(11) NOT NULL,
  `fk_ticket` int(11) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `ruta_archivo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ticket_archivos`
--

INSERT INTO `ticket_archivos` (`id`, `fk_ticket`, `nombre_archivo`, `ruta_archivo`) VALUES
(6, 10, '77868.pdf', 'uploads/77868.pdf'),
(9, 15, 'apis (2).sql', 'uploads/apis (2).sql'),
(10, 16, 'apis (2).sql', 'uploads/apis (2).sql'),
(11, 17, 'apis (2).sql', 'uploads/apis (2).sql'),
(12, 18, '77912_3.pdf', 'uploads/77912_3.pdf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(2) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `fk_rol` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `nombre`, `password`, `fk_rol`) VALUES
(1, 'reddeskuser001', '1234', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_rol` (`fk_rol`),
  ADD KEY `fk_permiso` (`fk_permiso`);

--
-- Indices de la tabla `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_usuario` (`fk_usuario`),
  ADD KEY `fk_proyecto` (`fk_proyecto`),
  ADD KEY `tickets_fk_usuario_cierre` (`fk_usuario_cierre`);

--
-- Indices de la tabla `ticket_archivos`
--
ALTER TABLE `ticket_archivos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_ticket` (`fk_ticket`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_rol` (`fk_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `ticket_archivos`
--
ALTER TABLE `ticket_archivos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD CONSTRAINT `proyectos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `rol_permisos`
--
ALTER TABLE `rol_permisos`
  ADD CONSTRAINT `rol_permisos_ibfk_1` FOREIGN KEY (`fk_rol`) REFERENCES `roles` (`id`),
  ADD CONSTRAINT `rol_permisos_ibfk_2` FOREIGN KEY (`fk_permiso`) REFERENCES `permisos` (`id`);

--
-- Filtros para la tabla `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_fk_usuario_cierre` FOREIGN KEY (`fk_usuario_cierre`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`fk_usuario`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`fk_proyecto`) REFERENCES `proyectos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ticket_archivos`
--
ALTER TABLE `ticket_archivos`
  ADD CONSTRAINT `ticket_archivos_ibfk_1` FOREIGN KEY (`fk_ticket`) REFERENCES `tickets` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`fk_rol`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

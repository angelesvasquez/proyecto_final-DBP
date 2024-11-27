SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `carrito` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `fecha_agregado` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `fecha_pedido` datetime NOT NULL,
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text NOT NULL,
  `precio_base` decimal(10,2) NOT NULL,
  `activo` int(11) NOT NULL,
  `descuento` tinyint(3) NOT NULL DEFAULT 0,
  `precio_final` decimal(10,2) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio_base`, `activo`, `descuento`, `precio_final`, `imagen`) VALUES
(2, 'Chompa de lana gruesa', 'Chompa de lana gruesa, ideal para temperaturas muy frías.', 80.00, 1, 10, 72.00, 'item.png'),
(3, 'Chompa de lana', 'Chompa de lana con cuello alto para mayor calidez en climas fríos.', 90.00, 0, 12, 79.20, 'item.png'),
(4, 'Chompa bohemio', 'Chompa de lana con diseño bohemio, cómoda y cálida para cualquier ocasión.', 85.00, 0, 8, 78.20, 'item.png');

-- Trigger para calcular el precio final a partir del descuento con INSERT
DELIMITER $$
CREATE TRIGGER `calcular_precio_final_insert` BEFORE INSERT ON `productos` FOR EACH ROW BEGIN
    SET NEW.precio_final = NEW.precio_base * (1 - NEW.descuento / 100);
END
$$
DELIMITER ;


-- Trigger para calcular el precio final a partir del descuento con UPDATE
DELIMITER $$
CREATE TRIGGER `calcular_precio_final_update` BEFORE UPDATE ON `productos` FOR EACH ROW BEGIN

    SET NEW.precio_final = NEW.precio_base * (1 - NEW.descuento / 100);
END
$$
DELIMITER ;

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `roles` (`id_rol`, `descripcion`) VALUES
(1, 'admin'),
(2, 'cliente');

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombres` varchar(200) NOT NULL,
  `apellidos` varchar(200) NOT NULL,
  `email` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `usuario` varchar(30) NOT NULL,
  `password` varchar(120) NOT NULL,
  `id_rol` int(11) NOT NULL DEFAULT 2,
  `estatus` tinyint(4) NOT NULL,
  `fecha_atta` datetime NOT NULL,
  `fecha_modifica` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usuarios` (`id_usuario`, `nombres`, `apellidos`, `email`, `telefono`, `dni`, `usuario`, `password`, `id_rol`, `estatus`, `fecha_atta`, `fecha_modifica`) VALUES
(20, 'admin', 'administrador', 'admin@gmail.co', '9123451232', '29124114', 'admin', '$2b$12$mQYZd42qfVmF8RiQ6/KhOee2DMLINNFH8DqaDX7nNLJX50.SywCb.', 1, 1, '2024-10-11 00:28:20', '2024-11-27 11:16:19'),
(22, 'maria', 'sad', 'aafas@gmail.com', '912345675', '29312322', 'angeles12312', '$2b$12$/s2wtISUuCrGvRmuZFCkQumm8MpxYtTMoAatKTfsHZWDAyjmEw8Li', 2, 1, '2024-11-26 19:26:55', NULL),
(23, 'ass fgdda', 'asd ', 'asd@as.com', '52141241', '12412521', 'angeles', '$2b$12$RRgbYnL5ZIRLmzkDgsAa4OXJcWAvcIo9kcMshyWFTwO36DubTU2XS', 2, 1, '2024-11-27 11:04:14', '2024-11-27 11:23:41');


ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_producto` (`id_producto`);

ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_producto` (`id_producto`);

ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_rol` (`id_rol`);


ALTER TABLE `carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;


ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`);

ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

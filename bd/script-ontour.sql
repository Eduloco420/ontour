CREATE SCHEMA onTour;

USE onTour;

CREATE TABLE `user` (
  `id` int PRIMARY KEY auto_increment,
  `rut` varchar(10) UNIQUE NOT NULL,
  `nom` varchar(50) NOT NULL,
  `appat` varchar(50) NOT NULL,
  `apmat` varchar(50) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `isActive` boolean NOT NULL,
  `fechaCreacion` datetime NOT NULL DEFAULT NOW()
);

INSERT INTO user (rut, nom, appat, apmat, mail, password, isActive) VALUES
('98765432-1', 'María', 'López', 'Hernández', 'maria.lopez@mail.com', 'password_2', TRUE),
('11223344-5', 'Carlos', 'Martínez', 'Ríos', 'carlos.martinez@mail.com', 'password_3', TRUE),
('22334455-6', 'Sofía', 'González', 'Mendoza', 'sofia.gonzalez@mail.com', 'password_4', TRUE);

select * from user;

CREATE TABLE `alumno` (
  `id` int PRIMARY KEY auto_increment,
  `apoderado` int NOT NULL,
  `rut` varchar(10) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `appat` varchar(50) NOT NULL,
  `apmat` varchar(50) NOT NULL,
  `curso` int NOT NULL
);
INSERT INTO alumno (apoderado, rut, nom, appat, apmat, curso) VALUES
(1, '22345678-9', 'Andrés', 'López', 'Cáceres', 1), 
(1, '21765432-1', 'María', 'López', 'Hernández', 1),  
(2, '22556677-8', 'Ana', 'Martínez', 'Vargas', 1), 
(2, '22667788-9', 'Javier', 'Martínez', 'Pérez', 2),  
(3, '21778899-0', 'Laura', 'González', 'Salazar', 2),  
(3, '21889900-1', 'Diego', 'González', 'Cordero', 2); 

select * from alumno;


CREATE TABLE `curso` (
  `id` int PRIMARY KEY auto_increment,
  `nomCurso` varchar(25) NOT NULL,
  `nomColegio` varchar(50) NOT NULL,
  `cantAlumnos` int NOT NULL,
  `PaqueteTuristico` int NOT NULL,
  `seguro` int NOT NULL
);

INSERT INTO `curso` (`nomCurso`, `nomColegio`, `cantAlumnos`, `PaqueteTuristico`, `seguro`)
VALUES 
('4°A', 'Colegio Los Andes', 30, 1, 2), 
('4°B', 'Colegio Alcantara', 35, 2, 1); 

ALTER TABLE `curso`
ADD COLUMN `fechaViaje` DATE;

UPDATE `curso`
SET `fechaViaje` = '2024-12-15' 
WHERE `id` = 2;

select * from curso;

CREATE TABLE `paqueteTuristico` (
  `id` int PRIMARY KEY auto_increment,
  `nomPaquete` varchar(50) NOT NULL,
  `totalPaquete` int NOT NULL,
  `hospedaje` varchar(50) NOT NULL,
  `transporte` varchar(50) NOT NULL,
  `ciudad` varchar(255) NOT NULL,
  `fecha_ida` date NOT NULL,
  `cant_noches` int NOT NULL
);
INSERT INTO `paqueteTuristico` (`nomPaquete`, `totalPaquete`, `hospedaje`, `transporte`, `ciudad`, `fecha_ida`, `cant_noches`) 
VALUES ('Bariloche Extremo', 550000, 'Hotel 3 Estrellas', 'Bus', 'Bariloche', '2024-12-10', 5);
INSERT INTO `paqueteTuristico` (`nomPaquete`, `totalPaquete`, `hospedaje`, `transporte`, `ciudad`, `fecha_ida`, `cant_noches`) 
VALUES ('Atacama Soñado', 750000, 'Hotel 4 Estrellas', 'Avion', 'Atacama', '2025-12-06', 6);

select * from paqueteTuristico;

ALTER TABLE `paqueteTuristico`
DROP COLUMN `fecha_ida`,
DROP COLUMN `cant_noches`;


CREATE TABLE `seguro` (
  `id` int PRIMARY KEY auto_increment,
  `empresaSeguro` varchar(50) NOT NULL,
  `nomSeguro` varchar(50),
  `valorSeguro` int,
  `coberturaSeguro` int
);

INSERT INTO `seguro` (`empresaSeguro`, `nomSeguro`, `valorSeguro`, `coberturaSeguro`)
VALUES 
('Assist Card', 'Cobertura Completa', 50000, 25000),
('Metlife', 'Cobertura Básica', 20000, 5000);

select * from seguro;

CREATE TABLE `cuota` (
  `id` int PRIMARY KEY auto_increment,
  `alumnoCuota` int NOT NULL,
  `fechaCuota` datetime NOT NULL,
  `fechaVenc` datetime NOT NULL,
  `valorCuota` int NOT NULL,
  `pagado` boolean NOT NULL,
  `vencido` boolean NOT NULL
);

INSERT INTO `cuota` (`alumnoCuota`, `fechaCuota`, `fechaVenc`, `valorCuota`, `pagado`, `vencido`)
VALUES 
(1, '2024-01-10 10:00:00', '2024-02-10 10:00:00', 15000, FALSE, FALSE),
(2, '2024-01-15 10:00:00', '2024-02-15 10:00:00', 20000, TRUE, FALSE),
(3, '2024-01-20 10:00:00', '2024-02-20 10:00:00', 18000, TRUE, FALSE), 
(4, '2024-01-25 10:00:00', '2024-02-25 10:00:00', 22000, FALSE, TRUE);  
select * from cuota;

CREATE TABLE `pago` (
  `id` int PRIMARY KEY auto_increment,
  `estadoPago` varchar(255) NOT NULL,
  `montoPago` int NOT NULL,
  `nroTarjeta` BigInt NOT NULL,
  `fecVen` varchar(255) NOT NULL,
  `cvv` int NOT NULL
);
INSERT INTO `pago` (`estadoPago`, `montoPago`, `nroTarjeta`, `fecVen`, `cvv`)
VALUES
('Completado', 15000, 1234567812345678, '2026-12', 123),
('Completado', 20000, 2345678923456789, '2025-11', 456),
('Completado', 18000, 3456789034567890, '2024-12', 789),
('Pendiente', 22000, 4567890145678901, '2024-09', 321);

select * from pago;

select id as "Nro Pago", montoPago as "Monto Pagado" FROM pago;

CREATE TABLE `pagoCuota` (
  `id` int PRIMARY KEY auto_increment,
  `cuota` int,
  `pago` int
);
INSERT INTO `pagoCuota` (`cuota`, `pago`)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);


CREATE TABLE `archivo` (
  `id` int PRIMARY KEY auto_increment,
  `curso` int,
  `ruta` varchar(255)
);
 
ALTER TABLE `alumno` ADD FOREIGN KEY (`curso`) REFERENCES `curso` (`id`);

ALTER TABLE `curso` ADD FOREIGN KEY (`PaqueteTuristico`) REFERENCES `paqueteTuristico` (`id`);

ALTER TABLE `curso` ADD FOREIGN KEY (`seguro`) REFERENCES `seguro` (`id`);

ALTER TABLE `cuota` ADD FOREIGN KEY (`alumnoCuota`) REFERENCES `alumno` (`id`);

ALTER TABLE `alumno` ADD FOREIGN KEY (`apoderado`) REFERENCES `user` (`id`);

ALTER TABLE `pagoCuota` ADD FOREIGN KEY (`pago`) REFERENCES `pago` (`id`);

ALTER TABLE `pagoCuota` ADD FOREIGN KEY (`cuota`) REFERENCES `cuota` (`id`);

ALTER TABLE `archivo` ADD FOREIGN KEY (`curso`) REFERENCES `curso` (`id`);
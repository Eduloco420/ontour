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
   rol varchar(15) NOT NULL,
  `isActive` boolean NOT NULL,
  `fechaCreacion` datetime NOT NULL
);

CREATE TABLE `alumno` (
  `id` int PRIMARY KEY auto_increment,
  `apoderado` int NOT NULL,
  `rut` varchar(10) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `appat` varchar(50) NOT NULL,
  `apmat` varchar(50) NOT NULL,
  `curso` int NOT NULL
);

CREATE TABLE `curso` (
  `id` int PRIMARY KEY auto_increment,
  `nomCurso` varchar(25) NOT NULL,
  `nomColegio` varchar(50) NOT NULL,
  fechaViaje datetime NOT NULL,
  `PaqueteTuristico` int NOT NULL,
  `seguro` int NOT NULL,
  `cantAlumnos` int NOT NULL
);

CREATE TABLE `paqueteTuristico` (
  `id` int PRIMARY KEY auto_increment,
  `nomPaquete` varchar(50) NOT NULL,
  `totalPaquete` int NOT NULL,
  `hospedaje` varchar(50) NOT NULL,
  `transporte` varchar(50) NOT NULL,
  `ciudad` varchar(255) NOT NULL
);

CREATE TABLE `seguro` (
  `id` int PRIMARY KEY auto_increment,
  `empresaSeguro` varchar(50) NOT NULL,
  `nomSeguro` varchar(50),
  `valorSeguro` int,
  `coberturaSeguro` int
);

CREATE TABLE `cuota` (
  `id` int PRIMARY KEY auto_increment,
  `alumnoCuota` int NOT NULL,
  `fechaCuota` datetime NOT NULL,
  `fechaVenc` datetime NOT NULL,
  `valorCuota` int NOT NULL,
  `pagado` boolean NOT NULL,
  `vencido` boolean NOT NULL
);

CREATE TABLE `pago` (
  `id` int PRIMARY KEY auto_increment,
  `montoPago` int NOT NULL,
  `nroTarjeta` BigInt NOT NULL,
  `fecVen` varchar(255) NOT NULL,
  `cvv` int NOT NULL
);

CREATE TABLE `pagoCuota` (
  `id` int PRIMARY KEY auto_increment,
  `cuota` int,
  `pago` int
);

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

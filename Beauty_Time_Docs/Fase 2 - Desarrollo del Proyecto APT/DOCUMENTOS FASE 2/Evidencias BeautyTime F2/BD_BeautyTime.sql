-- MySQL Script generated by MySQL Workbench
-- Sun Sep 15 10:08:14 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema beautytime
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema beautytime
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `beautytime` DEFAULT CHARACTER SET utf8mb4 ;
USE `beautytime` ;

-- -----------------------------------------------------
-- Table `beautytime`.`Especialidades`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Especialidades` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Especialidades` (
  `especialidadid` INT NOT NULL,
  `especialidad` VARCHAR(45) NULL,
  PRIMARY KEY (`especialidadid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beautytime`.`Persona`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Persona` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Persona` (
  `personaid` INT NOT NULL,
  `usuario` VARCHAR(20) NULL,
  `contrasenia` VARCHAR(14) NULL,
  `nombre` VARCHAR(50) NULL,
  `apellido` VARCHAR(50) NULL,
  `email` VARCHAR(100) NULL,
  `telefono` VARCHAR(15) NULL,
  PRIMARY KEY (`personaid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beautytime`.`Empleados`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Empleados` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Empleados` (
  `empleadoid` INT(11) NOT NULL AUTO_INCREMENT,
  `fechacontrato` DATE NULL DEFAULT NULL,
  `especialidadfk` INT NOT NULL,
  `personafk` INT NOT NULL,
  PRIMARY KEY (`empleadoid`, `personafk`, `especialidadfk`),
  INDEX `fk_Empleados_Especialidades1_idx` (`especialidadfk` ASC) VISIBLE,
  INDEX `fk_Empleados_Persona1_idx` (`personafk` ASC) VISIBLE,
  CONSTRAINT `fk_Empleados_Especialidades1`
    FOREIGN KEY (`especialidadfk`)
    REFERENCES `beautytime`.`Especialidades` (`especialidadid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Empleados_Persona1`
    FOREIGN KEY (`personafk`)
    REFERENCES `beautytime`.`Persona` (`personaid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Servicios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Servicios` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Servicios` (
  `servicioid` INT(11) NOT NULL AUTO_INCREMENT,
  `nombreservicio` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `duracion` INT(11) NULL DEFAULT NULL,
  `precio` INT NULL DEFAULT NULL,
  PRIMARY KEY (`servicioid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Clientes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Clientes` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Clientes` (
  `clienteid` INT(11) NOT NULL AUTO_INCREMENT,
  `direccion` VARCHAR(255) NULL DEFAULT NULL,
  `fecharegistro` DATE NULL DEFAULT NULL,
  `personafk` INT NOT NULL,
  PRIMARY KEY (`clienteid`, `personafk`),
  INDEX `fk_Clientes_Persona1_idx` (`personafk` ASC) VISIBLE,
  CONSTRAINT `fk_Clientes_Persona1`
    FOREIGN KEY (`personafk`)
    REFERENCES `beautytime`.`Persona` (`personaid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`EstadoCita`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`EstadoCita` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`EstadoCita` (
  `estadoid` INT NOT NULL,
  `estado` ENUM('Disponible', 'Agendada', 'Completada', 'Cancelada') NULL,
  PRIMARY KEY (`estadoid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beautytime`.`Citas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Citas` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Citas` (
  `citaid` INT(11) NOT NULL,
  `empleadofk` INT(11) NOT NULL,
  `fechahora` DATETIME NOT NULL,
  `serviciofk` INT(11) NOT NULL,
  `clientefk`  INT(11) NOT NULL,
  `estadofk` INT NOT NULL,
  PRIMARY KEY (`citaid`, `estadofk`, `clientefk`, `empleadofk`, `serviciofk`),
  INDEX `EmpleadoID` (`empleadofk` ASC) VISIBLE,
  INDEX `ServicioID` (`serviciofk` ASC) VISIBLE,
  INDEX `fk_Citas_Clientes1_idx` (`clientefk` ASC) VISIBLE,
  INDEX `fk_Citas_EstadoCita1_idx` (`estadofk` ASC) VISIBLE,
  CONSTRAINT `Citas_ibfk_2`
    FOREIGN KEY (`empleadofk`)
    REFERENCES `beautytime`.`Empleados` (`empleadoid`),
  CONSTRAINT `Citas_ibfk_3`
    FOREIGN KEY (`serviciofk`)
    REFERENCES `beautytime`.`Servicios` (`servicioid`),
  CONSTRAINT `fk_Citas_Clientes1`
    FOREIGN KEY (`clientefk`)
    REFERENCES `beautytime`.`Clientes` (`clienteid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Citas_EstadoCita1`
    FOREIGN KEY (`estadofk`)
    REFERENCES `beautytime`.`EstadoCita` (`estadoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Proveedores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Proveedores` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Proveedores` (
  `proveedorid` INT(11) NOT NULL AUTO_INCREMENT,
  `nombreproveedor` VARCHAR(100) NOT NULL,
  `direccion` VARCHAR(100) NULL DEFAULT NULL,
  `telefono` VARCHAR(15) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`proveedorid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`CategoriaProducto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`CategoriaProducto` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`CategoriaProducto` (
  `categoriaprodid` INT NOT NULL,
  `categoriaprod` VARCHAR(45) NULL,
  PRIMARY KEY (`categoriaprodid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beautytime`.`Productos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Productos` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Productos` (
  `productoid` INT(11) NOT NULL AUTO_INCREMENT,
  `nombreprod` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `precio` DECIMAL(10,2) NULL DEFAULT NULL,
  `stock` INT(11) NULL DEFAULT NULL,
  `proveedorfk` INT(11) NOT NULL,
  `categoriaprodfk` INT NOT NULL,
  PRIMARY KEY (`productoid`, `proveedorfk`, `categoriaprodfk`),
  INDEX `ProveedorID` (`proveedorfk` ASC) VISIBLE,
  INDEX `fk_Productos_TipoProducto1_idx` (`categoriaprodfk` ASC) VISIBLE,
  CONSTRAINT `Productos_ibfk_1`
    FOREIGN KEY (`proveedorfk`)
    REFERENCES `beautytime`.`Proveedores` (`proveedorid`),
  CONSTRAINT `fk_Productos_TipoProducto1`
    FOREIGN KEY (`categoriaprodfk`)
    REFERENCES `beautytime`.`CategoriaProducto` (`categoriaprodid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Compras`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Compras` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Compras` (
  `compraid` INT(11) NOT NULL AUTO_INCREMENT,
  `clientefk` INT(11) NOT NULL,
  `productofk` INT(11) NOT NULL,
  `cantidad` INT(11) NOT NULL,
  `fechacompra` DATETIME NOT NULL,
  PRIMARY KEY (`compraid`, `clientefk`, `productofk`),
  INDEX `ClienteID` (`clientefk` ASC) VISIBLE,
  INDEX `ProductoID` (`productofk` ASC) VISIBLE,
  CONSTRAINT `Compras_ibfk_1`
    FOREIGN KEY (`clientefk`)
    REFERENCES `beautytime`.`Clientes` (`clienteid`),
  CONSTRAINT `Compras_ibfk_2`
    FOREIGN KEY (`productofk`)
    REFERENCES `beautytime`.`Productos` (`productoid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Venta`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Venta` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Venta` (
  `ventaid` INT(11) NOT NULL AUTO_INCREMENT,
  `clientefk` INT(11) NOT NULL,
  `monto` INT NOT NULL,
  `fechapago` DATETIME NOT NULL,
  `metodopago` ENUM('Tarjeta de Crédito', 'Tarjeta de Débito', 'Efectivo', 'Transferencia Bancaria') NOT NULL,
  PRIMARY KEY (`ventaid`, `clientefk`),
  INDEX `ClienteID` (`clientefk` ASC) VISIBLE,
  CONSTRAINT `Pagos_ibfk_1`
    FOREIGN KEY (`clientefk`)
    REFERENCES `beautytime`.`Clientes` (`clienteid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Promociones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Promociones` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Promociones` (
  `promocionid` INT(11) NOT NULL AUTO_INCREMENT,
  `nombrepromo` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `fechainicio` DATE NULL DEFAULT NULL,
  `fechafin` DATE NULL DEFAULT NULL,
  `descuento` INT NULL DEFAULT NULL,
  PRIMARY KEY (`promocionid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`AtencionCliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`AtencionCliente` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`AtencionCliente` (
  `ticketid` INT(11) NOT NULL AUTO_INCREMENT,
  `clientefk` INT(11) NOT NULL,
  `fechacreacion` DATETIME NOT NULL,
  `asunto` VARCHAR(255) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `estadosoporte` ENUM('Abierto', 'Cerrado') NOT NULL,
  PRIMARY KEY (`ticketid`, `clientefk`),
  INDEX `ClienteID` (`clientefk` ASC) VISIBLE,
  CONSTRAINT `Soporte_ibfk_1`
    FOREIGN KEY (`clientefk`)
    REFERENCES `beautytime`.`Clientes` (`clienteid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `beautytime`.`Descuento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`Descuento` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`Descuento` (
  `descuentoid` INT NOT NULL,
  `porcentaje` FLOAT NULL,
  `codigodesc` VARCHAR(45) NULL,
  PRIMARY KEY (`descuentoid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `beautytime`.`DetalleVenta`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `beautytime`.`DetalleVenta` ;

CREATE TABLE IF NOT EXISTS `beautytime`.`DetalleVenta` (
  `detalleventaid` INT NOT NULL,
  `descripcion` VARCHAR(45) NULL,
  `ventafk` INT(11) NOT NULL,
  `promocionfk` INT(11) NOT NULL,
  `descuentofk` INT NOT NULL,
  PRIMARY KEY (`detalleventaid`, `ventafk`, `promocionfk`, `descuentofk`),
  INDEX `fk_DetalleVenta_Pagos1_idx` (`ventafk` ASC) VISIBLE,
  INDEX `fk_DetalleVenta_Promociones1_idx` (`promocionfk` ASC) VISIBLE,
  INDEX `fk_DetalleVenta_Descuento1_idx` (`descuentofk` ASC) VISIBLE,
  CONSTRAINT `fk_DetalleVenta_Pagos1`
    FOREIGN KEY (`ventafk`)
    REFERENCES `beautytime`.`Venta` (`ventaid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DetalleVenta_Promociones1`
    FOREIGN KEY (`promocionfk`)
    REFERENCES `beautytime`.`Promociones` (`promocionid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DetalleVenta_Descuento1`
    FOREIGN KEY (`descuentofk`)
    REFERENCES `beautytime`.`Descuento` (`descuentoid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

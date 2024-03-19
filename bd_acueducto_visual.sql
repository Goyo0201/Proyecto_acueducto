CREATE DATABASE bd_acueducto;
USE bd_acueducto;

CREATE TABLE oficio(
    num_oficio INT AUTO_INCREMENT PRIMARY KEY,
    asunto VARCHAR (70),
    descripcion VARCHAR(70),
    fecha DATE
);

CREATE TABLE propietario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_cedula BIGINT,
    nombres VARCHAR(30),
    apellidos VARCHAR(30),
    num_telefono BIGINT,
    correo VARCHAR(30),
    direccion VARCHAR(30)
);

CREATE TABLE recibo (
    num_recibo INT AUTO_INCREMENT PRIMARY KEY,
    fecha_limite DATE,
    nombres VARCHAR(50),
    apellidos VARCHAR(50),
    servicio VARCHAR(10),
    consumo INT,
    lectura_anterior BIGINT DEFAULT 0,,
    lectura_actual BIGINT,
    costo_servicio BIGINT,
    inasistencia_asamblea BIGINT,
    contribucion BIGINT,
    otros BIGINT,
    total_pagar BIGINT,
    id_propietario INT, 
    FOREIGN KEY (id_propietario) REFERENCES propietario(id)
);

CREATE TABLE predio(
    num_catastral INT AUTO_INCREMENT PRIMARY KEY,
    nombre_predio VARCHAR(30),
    direccion VARCHAR(30)
);

CREATE TABLE punto_agua (
    num_contador INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(20),
    num_catastral_predio INT, 
    FOREIGN KEY (num_catastral_predio) REFERENCES predio(num_catastral)
);

CREATE TABLE consumo (
    cod_consumo INT AUTO_INCREMENT PRIMARY KEY,
    metros_cubicos INT,
    num_contador_punto_agua INT, 
    FOREIGN KEY (num_contador_punto_agua) REFERENCES punto_agua(num_contador)
);

CREATE TABLE gasto_acueducto(
    id_tipo_gasto INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(70),
    fecha DATE,
    monto BIGINT
);

CREATE TABLE historial (
    cod_historia INT AUTO_INCREMENT PRIMARY KEY,
    consumo INT,
    fecha DATE,
    num_contador_punto_agua INT, 
    FOREIGN KEY (num_contador_punto_agua) REFERENCES punto_agua(num_contador)
);




/*Llaves foraneas*/

CREATE TABLE propietario_oficio (
    id_oficio INT,
    id_propietario BIGINT,
    FOREIGN KEY (id_oficio) REFERENCES oficio(num_oficio),
    FOREIGN KEY (id_propietario) REFERENCES propietario(id)
);

CREATE TABLE predio_propietario (
    id_predio INT,
    id_propietario BIGINT,
    FOREIGN KEY (id_predio) REFERENCES predio(num_catastral),
    FOREIGN KEY (id_propietario) REFERENCES propietario(id)
);

CREATE TABLE gasto_acueducto_contador (
    id_tipo_gasto INT,
    num_contador_punto_agua INT,
    FOREIGN KEY (id_tipo_gasto) REFERENCES tipo_gasto_acueducto(id_tipo_gasto),
    FOREIGN KEY (num_contador_punto_agua) REFERENCES punto_agua(num_contador)
);


/*Disparadores*/

/*Disparadores*/

-- Trigger para eliminar registros en cascada al eliminar un propietario
DELIMITER //

CREATE TRIGGER eliminar_propietario_cascada
BEFORE DELETE ON propietario
FOR EACH ROW
BEGIN
    -- Obtener los id_predio asociados al propietario
    DECLARE id_predio_val INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id_predio FROM predio_propietario WHERE id_propietario = OLD.id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    eliminar_predio: LOOP
        FETCH cur INTO id_predio_val;
        IF done THEN
            LEAVE eliminar_predio;
        END IF;

        -- Eliminar registros de punto_agua
        DELETE FROM punto_agua WHERE num_catastral_predio = id_predio_val;

        -- Eliminar registros de predio_propietario
        DELETE FROM predio_propietario WHERE id_predio = id_predio_val;
    END LOOP;

    CLOSE cur;

END;
//

DELIMITER ;



-- Trigger para actualizar la tabla recibo después de insertar en la tabla consumo
DELIMITER //

CREATE TRIGGER actualizar_recibo_despues_insertar
AFTER INSERT ON consumo
FOR EACH ROW
BEGIN
    -- Variables para almacenar información del propietario
    DECLARE id_propietario_val INT;
    DECLARE nombres_propietario VARCHAR(50);
    DECLARE apellidos_propietario VARCHAR(50);

    -- Obtener id, nombres y apellidos del propietario
    SELECT id, nombres, apellidos INTO id_propietario_val, nombres_propietario, apellidos_propietario
    FROM propietario
    WHERE id = (SELECT id_propietario FROM predio_propietario WHERE id_predio = (SELECT num_catastral_predio FROM punto_agua WHERE num_contador = NEW.num_contador_punto_agua));

    -- Insertar información en la tabla recibo
    INSERT INTO recibo (id_propietario, nombres, apellidos, lectura_actual)
    VALUES (id_propietario_val, nombres_propietario, apellidos_propietario, NEW.metros_cubicos);

END;
//

DELIMITER ;







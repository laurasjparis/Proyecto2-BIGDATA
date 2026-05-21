
-- Crear tabla de estaciones
CREATE TABLE estaciones (
    id_estacion INT,
    autoridad_ambiental VARCHAR(100),
    estacion VARCHAR(200),
    latitud DOUBLE,
    longitud DOUBLE,
    variable VARCHAR(100),
    unidades VARCHAR(50),
    anio INT,
    codigo_departamento INT,
    nombre_departamento VARCHAR(100),
    codigo_municipio VARCHAR(20),
    nombre_municipio VARCHAR(100),
    tipo_estacion VARCHAR(50)
);

-- Cargar datos desde CSV
LOAD DATA LOCAL INFILE '/home/ec2-user/Calidad_del_Aire_en_Colombia_(Promedio_Anual)_20260520.csv'
INTO TABLE estaciones
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_estacion, autoridad_ambiental, estacion, latitud, longitud, variable, unidades, @dummy, anio, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, codigo_departamento, nombre_departamento, codigo_municipio, nombre_municipio, tipo_estacion, @dummy);

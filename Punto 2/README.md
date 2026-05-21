# PUNTO 2 — Fuentes de Datos

## Instrucciones

---

# RDS MariaDB

```bash
# 1. Crear instancia RDS MariaDB en AWS (db.t3.micro, Free Tier)

# 2. Abrir puerto 3306 en Security Group (0.0.0.0/0)

# 3. Descargar certificado SSL
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

# 4. Conectarse al RDS
mysql -h <RDS_ENDPOINT> -P 3306 -u admin -pAdmin1234! --ssl-ca=global-bundle.pem calidad_aire

# 5. Crear tabla
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

# 6. Cargar datos
LOAD DATA LOCAL INFILE '/home/ec2-user/Calidad_del_Aire_en_Colombia_(Promedio_Anual)_20260520.csv'
INTO TABLE estaciones
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_estacion, autoridad_ambiental, estacion, latitud, longitud, variable, unidades, @dummy, anio, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, codigo_departamento, nombre_departamento, codigo_municipio, nombre_municipio, tipo_estacion, @dummy);
```

---

# EC2 — Subir CSV

```bash
# Desde PowerShell en Windows (estando en el Desktop)

scp -i "proyecto2-key.pem" "Calidad_del_Aire_en_Colombia_(Promedio_Anual)_20260520.csv" ec2-user@<EC2_IP>:/home/ec2-user/

# Si hay error de permisos con el .pem en Windows:

icacls "proyecto2-key.pem" /inheritance:r
icacls "proyecto2-key.pem" /grant:r "MI PC:R"
```

---

# URL Pública (Servidor HTTP)

```bash
# En la EC2, correr servidor HTTP en background

nohup python3 -m http.server 8080 &

# URL resultante:

http://<EC2_IP>:8080/Calidad_del_Aire_en_Colombia_(Promedio_Anual)_20260520.csv

# IMPORTANTE:
# Abrir puerto 8080 en Security Group de la EC2 (launch-wizard-X)
```
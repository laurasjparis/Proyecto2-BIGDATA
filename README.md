# Proyecto 2 - Big Data con AWS

## Universidad EAFIT
### ST0263 - Topicos Especiales en Telematica 2026-1

## Integrantes
- William Andres Henao Lopez - wahenaol@eafit.edu.co
- Samuel Cadavid Zapata - scadavidz@eafit.edu.co
- Laura Sofia Jimenez Paris - lsjimenezp@eafit.edu.co

---

## Descripcion del proyecto

Caso de estudio de procesamiento de Big Data usando servicios de AWS.
Se analizan datos de calidad del aire en Colombia provenientes del IDEAM
y disponibles en el portal de datos abiertos datos.gov.co.

El pipeline completo cubre desde la ingesta de datos en multiples fuentes,
pasando por procesamiento y catalogacion, hasta visualizacion interactiva.

---

## Dataset

- Nombre: Calidad del Aire en Colombia (Promedio Anual)
- Fuente: https://www.datos.gov.co
- Registros: 29,683
- Columnas: 28
- Periodo: 2011 - 2024

---

## Preguntas de negocio

1. Que ciudad colombiana tuvo el mayor promedio de contaminacion anual?
2. Que departamentos superaron mas dias el limite permisible de contaminacion?
3. Cuales son las 5 estaciones de monitoreo mas contaminadas del pais?
4. Como ha evolucionado el promedio de contaminacion anual en Antioquia?
5. Cuales son los contaminantes mas frecuentes por departamento?

---

## Arquitectura del proyecto

Fuentes de datos:
- RDS MariaDB: catalogo de estaciones de monitoreo
- EC2: archivo CSV con mediciones historicas
- URL publica: servidor HTTP en EC2 exponiendo el dataset

Datalake S3 (proyecto2-datalake-calidad-aire):
- raw/: datos crudos ingestados desde las 3 fuentes
- trusted/: datos limpios en formato Parquet
- refined/: resultados de analisis

Procesamiento:
- AWS Glue + Spark: limpieza y transformacion de raw a trusted
- AWS Glue Crawler: catalogacion automatica de tablas
- AWS Athena: consultas SQL analiticas
- AWS Glue Notebook: analisis con PySpark

Visualizacion:
- Streamlit: dashboard interactivo desplegado en EC2

---

## Estructura del repositorio

Proyecto2-BIGDATA/
├── README.md
├── punto1/
│   ├── README.md
│   └── evidencias/
├── punto2/
│   ├── README.md
│   ├── crear_tabla.sql
│   ├── cargar_datos.sql
│   └── evidencias/
├── punto3/
│   ├── README.md
│   ├── ingest.py
│   └── evidencias/
├── punto4/
│   ├── README.md
│   ├── glue_job.py
│   └── evidencias/
├── punto5/
│   ├── README.md
│   └── evidencias/
├── punto6/
│   ├── README.md
│   ├── consultas.sql
│   └── evidencias/
├── punto7/
│   ├── README.md
│   ├── pyspark_analysis.py
│   └── evidencias/
└── punto8/
├── README.md
├── app.py
└── evidencias/

---

## Requisitos previos

- Cuenta de AWS Academy con Learner Lab activo
- Python 3.9 o superior
- Credenciales de AWS configuradas (aws configure)
- Par de claves .pem para acceso a EC2

---

## Servicios AWS utilizados

- Amazon EC2 (t2.micro - Amazon Linux 2023)
- Amazon RDS (MariaDB 11.8 - db.t3.micro)
- Amazon S3
- AWS Glue (ETL Jobs, Crawlers, Notebooks)
- Amazon Athena

---

## Notas importantes

- Las credenciales de AWS Academy expiran cada 4 horas.
  Renovar con aws configure y aws configure set aws_session_token antes
  de ejecutar cualquier script.
- La IP publica de la EC2 cambia cada vez que se reinicia el lab.
  Actualizar la IP en los scripts correspondientes.
- El servidor HTTP de la EC2 debe estar corriendo para que la ingesta
  desde URL funcione: nohup python3 -m http.server 8080 and
- El dashboard Streamlit es accesible en http://<EC2_IP>:8501
  siempre que la EC2 este corriendo y el lab este activo.
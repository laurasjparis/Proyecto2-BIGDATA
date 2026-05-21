# PUNTO 4 — Procesamiento con AWS Glue y Spark

## Instrucciones

1. Ir a **AWS Glue → ETL Jobs → Script editor**
2. Seleccionar:
   - **Motor:** Spark
   - **Opción:** Start fresh
3. Configurar los detalles del Job:
   - **Name:** proyecto2-raw-to-trusted
   - **IAM Role:** LabRole
   - **Glue version:** 4.0
   - **Worker type:** G.1X
   - **Number of workers:** 2
   - **Timeout:** 10 minutos
4. Pegar el script `glue_job.py`
5. Hacer clic en **Save → Run**

---

# Script glue_job.py

```python
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, trim, upper
from pyspark.sql.types import DoubleType, IntegerType

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("proyecto2-raw-to-trusted", {})

BUCKET = "proyecto2-datalake-calidad-aire"

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("multiLine", "true") \
    .csv(f"s3://{BUCKET}/raw/mediciones.csv")

df2 = df.dropDuplicates().dropna(subset=["ID Estacion"])

df3 = df2.select(
    col("ID Estacion").alias("id_estacion"),
    col("Estación").alias("estacion"),
    col("Autoridad Ambiental").alias("autoridad_ambiental"),
    col("Latitud").cast(DoubleType()).alias("latitud"),
    col("Longitud").cast(DoubleType()).alias("longitud"),
    col("Variable").alias("variable"),
    col("Unidades").alias("unidades"),
    col("Año").cast(IntegerType()).alias("anio"),
    col("Promedio").cast(DoubleType()).alias("promedio"),
    col("Máximo").cast(DoubleType()).alias("maximo"),
    col("Mínimo").cast(DoubleType()).alias("minimo"),
    col("Días de excedencias").cast(IntegerType()).alias("dias_excedencias"),
    col("Nombre del Departamento").alias("departamento"),
    col("Nombre del Municipio").alias("municipio"),
    col("Tipo de Estación").alias("tipo_estacion")
)

df3.write.mode("overwrite").parquet(f"s3://{BUCKET}/trusted/mediciones/")

print("Completado!")

job.commit()
```

---

# Solución de Problemas

```bash
# Si el job dice Succeeded pero trusted/ está vacío:
# el script anterior tenía un bug, usar esta versión del script

# Si da error de permisos S3:
# verificar que el IAM Role sea LabRole
```

---

# Archivos para el Repo

```bash
punto4/
├── README.md
├── glue_job.py
└── evidencias/
```

---
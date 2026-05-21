# PUNTO 5 — Catalogación con Glue Crawler

## Instrucciones

1. Ir a **AWS Glue → Crawlers → Create crawler**
2. Configurar:
   - **Nombre:** proyecto2-crawler
   - **Data source:** S3
   - **Ruta:** s3://proyecto2-datalake-calidad-aire/trusted/mediciones/
   - **IAM Role:** LabRole
   - **Target database:** calidad_aire_db
   - **Acción:** crear nueva base de datos
   - **Table name prefix:** trusted_
   - **Frequency:** On demand
3. Hacer clic en **Create crawler**
4. Ejecutar con **Run**

---

# Solución de Problemas

```bash
# Si la base de datos no aparece en el dropdown:
# refrescar con el botón 🔄

# Si el crawler no crea tablas:
# verificar que trusted/mediciones/ tenga archivos .parquet
```
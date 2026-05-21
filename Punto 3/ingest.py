import boto3
import pymysql
import requests

S3_BUCKET = 'proyecto2-datalake-calidad-aire'

RDS_HOST = '<RDS_ENDPOINT>'
RDS_USER = 'admin'
RDS_PASS = 'Admin1234!'
RDS_DB = 'calidad_aire'

EC2_CSV = '/home/ec2-user/Calidad_del_Aire_en_Colombia_(Promedio_Anual)_20260520.csv'

URL_CSV = 'http://<EC2_IP>:8080/Calidad_del_Aire_en_Colombia_(Promedio_Anual)_20260520.csv'

s3 = boto3.client('s3', region_name='us-east-1')

# Fuente 1: CSV desde EC2

s3.upload_file(
    EC2_CSV,
    S3_BUCKET,
    'raw/mediciones.csv'
)

# Fuente 2: RDS MariaDB

conn = pymysql.connect(
    host=RDS_HOST,
    user=RDS_USER,
    password=RDS_PASS,
    database=RDS_DB,
    ssl={'ca': '/home/ec2-user/global-bundle.pem'}
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM estaciones")

rows = cursor.fetchall()

cols = [d[0] for d in cursor.description]

csv_content = ','.join(cols) + '\n'

for row in rows:
    csv_content += ','.join(
        [str(x) if x is not None else '' for x in row]
    ) + '\n'

s3.put_object(
    Bucket=S3_BUCKET,
    Key='raw/estaciones_rds.csv',
    Body=csv_content.encode('utf-8')
)

conn.close()

# Fuente 3: URL pública

response = requests.get(URL_CSV)

s3.put_object(
    Bucket=S3_BUCKET,
    Key='raw/mediciones_url.csv',
    Body=response.content
)

print("Ingestion completada!")

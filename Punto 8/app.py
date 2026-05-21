import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import boto3
import io

st.set_page_config(page_title="Calidad del Aire en Colombia", layout="wide")
st.title("Dashboard - Calidad del Aire en Colombia")
st.markdown("Analisis de datos del IDEAM procesados con AWS Big Data")

@st.cache_data
def cargar_datos():
    s3 = boto3.client('s3', region_name='us-east-1')
    obj = s3.get_object(Bucket='proyecto2-datalake-calidad-aire', Key='raw/mediciones.csv')
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    df['Promedio'] = pd.to_numeric(df['Promedio'], errors='coerce')
    df['Dias de excedencias'] = pd.to_numeric(df['Días de excedencias'], errors='coerce')
    df['Anio'] = pd.to_numeric(df['Año'].astype(str).str.replace(',', ''), errors='coerce')
    return df

df = cargar_datos()

st.sidebar.header("Filtros")
departamentos = ['Todos'] + sorted(df['Nombre del Departamento'].dropna().unique().tolist())
depto_sel = st.sidebar.selectbox("Departamento", departamentos)

variables = ['Todos'] + sorted(df['Variable'].dropna().unique().tolist())
var_sel = st.sidebar.selectbox("Contaminante", variables)

df_fil = df.copy()
if depto_sel != 'Todos':
    df_fil = df_fil[df_fil['Nombre del Departamento'] == depto_sel]
if var_sel != 'Todos':
    df_fil = df_fil[df_fil['Variable'] == var_sel]

col1, col2, col3 = st.columns(3)
col1.metric("Total registros", f"{len(df_fil):,}")
col2.metric("Departamentos", df_fil['Nombre del Departamento'].nunique())
col3.metric("Estaciones", df_fil['Estación'].nunique())

st.markdown("---")

st.subheader("Top 10 municipios con mayor contaminacion promedio")
top_mun = df_fil.groupby('Nombre del Municipio')['Promedio'].mean().nlargest(10).reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.barh(top_mun['Nombre del Municipio'], top_mun['Promedio'], color='steelblue')
ax1.set_xlabel("Promedio de contaminacion")
ax1.invert_yaxis()
st.pyplot(fig1)

st.subheader("Dias de excedencia por departamento")
exc_depto = df_fil.groupby('Nombre del Departamento')['Dias de excedencias'].sum().nlargest(10).reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(exc_depto['Nombre del Departamento'], exc_depto['Dias de excedencias'], color='tomato')
ax2.set_xticklabels(exc_depto['Nombre del Departamento'], rotation=45, ha='right')
ax2.set_ylabel("Total dias excedencia")
st.pyplot(fig2)

st.subheader("Evolucion anual del promedio de contaminacion")
evol = df_fil.groupby('Anio')['Promedio'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(evol['Anio'], evol['Promedio'], marker='o', color='green')
ax3.set_xlabel("Anio")
ax3.set_ylabel("Promedio")
ax3.grid(True)
st.pyplot(fig3)

st.subheader("Datos filtrados")
st.dataframe(df_fil.head(100))
-- Pregunta 1 — Ciudad con mayor promedio de PM2.5
SELECT 
    municipio,
    variable,
    ROUND(AVG(promedio), 2) AS promedio_contaminacion
FROM trusted_mediciones
WHERE variable = 'PM2.5'
GROUP BY municipio, variable
ORDER BY promedio_contaminacion DESC
LIMIT 10;

-- Pregunta 2 — Departamentos con más días de excedencia
SELECT 
    departamento,
    SUM(dias_excedencias) AS total_dias_excedencia
FROM trusted_mediciones
GROUP BY departamento
ORDER BY total_dias_excedencia DESC
LIMIT 10;

-- Pregunta 3 — 5 estaciones más contaminadas
SELECT 
    estacion,
    municipio,
    departamento,
    ROUND(MAX(maximo), 2) AS max_contaminacion
FROM trusted_mediciones
GROUP BY estacion, municipio, departamento
ORDER BY max_contaminacion DESC
LIMIT 5;

-- Pregunta 4 — Evolución anual en Antioquia
SELECT 
    anio,
    ROUND(AVG(promedio), 2) AS promedio_anual
FROM trusted_mediciones
WHERE departamento = 'ANTIOQUIA'
GROUP BY anio
ORDER BY anio;

-- Pregunta 5 — Contaminantes más frecuentes por departamento
SELECT 
    departamento,
    variable,
    COUNT(*) AS mediciones
FROM trusted_mediciones
GROUP BY departamento, variable
ORDER BY mediciones DESC
LIMIT 10;

# Práctica 1: Analizador de Leads / Campañas en Python

## Objetivo
Aprender a crear un script Python que lea datos de un CSV, calcule métricas básicas y genere un resumen de campaña.  
Esta práctica sirve como base para analizar **datos reales de marketing**.

---

## Carpeta relacionada
~/proyectos/nextia/marketing/
│
├── datasets/leads.csv # CSV de ejemplo con leads/campañas
├── scripts/analizador_leads.py # Script Python que analiza los datos
├── reports/ # Carpeta donde se guardarán reportes futuros

python
Copiar código

---

## Código del script

```python
import csv

# Cargar datos del CSV
with open("../datasets/leads.csv", newline='', encoding="utf-8") as csvfile:
    lector = csv.DictReader(csvfile)
    leads = list(lector)

# Calcular métricas
total_clicks = sum(int(lead["clicks"]) for lead in leads)
total_conversiones = sum(int(lead["conversiones"]) for lead in leads)
total_gasto = sum(float(lead["gasto"]) for lead in leads)

# Costo por conversión (CPC)
if total_conversiones > 0:
    cpc = total_gasto / total_conversiones
else:
    cpc = 0

# Mostrar resultados
print("📊 Resumen de Campaña")
print(f"Total de Clicks: {total_clicks}")
print(f"Total de Conversiones: {total_conversiones}")
print(f"Gasto Total: ${total_gasto}")
print(f"Costo por Conversión (CPC): ${cpc:.2f}")
Explicación del código
import csv: importa la librería estándar de Python para trabajar con CSV.

csv.DictReader(...): convierte cada fila del CSV en un diccionario con nombres de columna como claves.

leads = list(lector): guarda todas las filas en una lista para poder manipularlas.

sum(int(...)) / sum(float(...)): suma los valores numéricos de cada columna (clicks, conversiones, gasto).

if total_conversiones > 0: cpc = total_gasto / total_conversiones: evita división entre cero.

print(...): muestra un resumen en la terminal.

Uso con datos reales
Reemplaza leads.csv con tus datos reales (mismo formato de columnas: nombre,email,fuente,clicks,conversiones,gasto).

Ejecuta el script:

bash
Copiar código
cd ~/proyectos/nextia/marketing/scripts
python3 analizador_leads.py
Obtendrás métricas actualizadas automáticamente.

Cómo agregar más datos o métricas
Para agregar más filas en el CSV: simplemente abre datasets/leads.csv y añade nuevos leads.

Para nuevas métricas (ejemplo: CTR, ROI, tasa de conversión por fuente): edita analizador_leads.py y añade nuevas operaciones sobre la lista leads.

Puedes generar reportes automáticos guardando el resultado en un archivo .txt o .csv dentro de reports/:

python
Copiar código
with open("../reports/resumen_campaña.txt", "w", encoding="utf-8") as f:
    f.write("Total Clicks: {}\n".format(total_clicks))
    f.write("Total Conversiones: {}\n".format(total_conversiones))
    f.write("Gasto Total: ${}\n".format(total_gasto))
    f.write("Costo por Conversión (CPC): ${:.2f}\n".format(cpc))
Resumen de la práctica
Creamos un dataset de ejemplo (leads.csv).

Creamos un script Python (analizador_leads.py) que calcula métricas básicas: Clicks totales, Conversiones, Gasto y CPC.

Ejecutamos y validamos resultados.

Guardamos la enseñanza en Markdown para consultar en cualquier momento.

La práctica es escalable: puedes usar datos reales, agregar filas, nuevas métricas y generar reportes automáticos en reports/.

yaml
Copiar código

Guarda con `CTRL + O` y sal de nano con `CTRL + X`.

---

### 🔹 Mini-resumen bro

- Tienes **documentación completa** de la práctica dentro de Nextia Marketing.  
- Ahora sabes cómo **reanudar el análisis** con nuevos datos y métricas sin romper nada.  
- Todo queda **centralizado** en `marketing/docs/` para futuras consultas.  

---

Si quieres, bro, el **siguiente paso** sería:  
1. **Mejorar el script** para generar reportes automáticos por **fuente** (Google, Facebook, SEO…) y otras métricas avanzadas.  
2. Crear un **archivo final CSV o Excel** que se vaya actualizando con cada ejecución.  

¿Quieres que hagamos esa versión mejorada de inmediato?

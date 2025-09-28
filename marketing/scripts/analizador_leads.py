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

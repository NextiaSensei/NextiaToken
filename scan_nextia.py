#!/usr/bin/env python3
"""
scan_nextia.py
Escanea ~/proyectos/nextia y genera:
 - project_index.csv
 - project_index.md
 - project_index.html (opcional)
Uso:
 python3 scan_nextia.py
"""
import os, csv, datetime, pathlib, html

ROOT = os.path.expanduser("~/proyectos/nextia")
CSV_OUT = os.path.join(ROOT, "project_index.csv")
MD_OUT = os.path.join(ROOT, "project_index.md")
HTML_OUT = os.path.join(ROOT, "project_index.html")

rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    # registrar carpeta
    stat = os.stat(dirpath)
    rows.append({
        "type":"dir",
        "path": rel,
        "name": os.path.basename(dirpath),
        "size": 0,
        "mtime": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
    })
    for f in filenames:
        fp = os.path.join(dirpath, f)
        try:
            st = os.stat(fp)
            rows.append({
                "type":"file",
                "path": os.path.relpath(fp, ROOT),
                "name": f,
                "size": st.st_size,
                "mtime": datetime.datetime.fromtimestamp(st.st_mtime).isoformat()
            })
        except FileNotFoundError:
            continue

# escribir CSV
with open(CSV_OUT, "w", newline="", encoding="utf-8") as csvf:
    w = csv.DictWriter(csvf, fieldnames=["type","path","name","size","mtime"])
    w.writeheader()
    for r in rows:
        w.writerow(r)

# escribir MD
with open(MD_OUT, "w", encoding="utf-8") as md:
    md.write("# Índice del proyecto Nextia\n\n")
    md.write(f"_Generado: {datetime.datetime.now().isoformat()}_\n\n")
    md.write("|Tipo|Ruta|Nombre|Tamaño(bytes)|Modificado|\n")
    md.write("|---|---|---:|---:|---|\n")
    for r in rows:
        md.write(f"|{r['type']}|`{r['path']}`|{r['name']}|{r['size']}|{r['mtime']}|\n")

# escribir HTML (simple)
with open(HTML_OUT, "w", encoding="utf-8") as h:
    h.write("<!doctype html><html><head><meta charset='utf-8'><title>Nextia Index</title></head><body>")
    h.write(f"<h1>Índice Nextia — Generado: {html.escape(datetime.datetime.now().isoformat())}</h1>")
    h.write("<table border='1' cellpadding='4'><tr><th>Tipo</th><th>Ruta</th><th>Nombre</th><th>Tamaño</th><th>Modificado</th></tr>")
    for r in rows:
        h.write("<tr>")
        h.write(f"<td>{html.escape(r['type'])}</td>")
        h.write(f"<td>{html.escape(r['path'])}</td>")
        h.write(f"<td>{html.escape(r['name'])}</td>")
        h.write(f"<td>{r['size']}</td>")
        h.write(f"<td>{html.escape(r['mtime'])}</td>")
        h.write("</tr>")
    h.write("</table></body></html>")

print("Generados:", CSV_OUT, MD_OUT, HTML_OUT)

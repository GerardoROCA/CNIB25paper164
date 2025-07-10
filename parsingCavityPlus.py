#!/usr/bin/env python

import pandas as pd
from bs4 import BeautifulSoup

# ----------------------------------------------------------
# Documento HTML de ejemplo: tabla con datos de cavidades
# ----------------------------------------------------------
html_doc = """<table data-v-92dc5b31="" class="table align-center text-center" ... >... </table>"""

# ----------------------------------------------------------
# Parseo del HTML con BeautifulSoup
# ----------------------------------------------------------
# Creamos el objeto BeautifulSoup para navegar la estructura HTML
soup = BeautifulSoup(html_doc, 'html.parser')
# Buscamos el primer <tbody> que contiene las filas de datos principales
tbody = soup.find('tbody')
if tbody is None:
    # Si no existe <tbody>, alertamos al usuario
    raise RuntimeError("No se encontró <tbody>. ¿Pegaste bien tu HTML?")

# ----------------------------------------------------------
# Extracción de datos: filas principales y detalles colapsables
# ----------------------------------------------------------
rows = []  # Lista para almacenar cada entrada como diccionario
for row in tbody.find_all('tr', recursive=False):
    # Saltamos filas de detalle (tienen atributo 'id')
    if row.get('id'):
        continue

    # Extraemos celdas de la fila principal
    cells = row.find_all('td', recursive=False)
    entry = {
        'Index':        cells[0].get_text(strip=True),
        'Pred Max pKd': cells[1].get_text(strip=True),
        'Pred Ave pKd': cells[2].get_text(strip=True),
        'DrugScore':    cells[3].get_text(strip=True),
        'Druggability': cells[4].get_text(strip=True),
    }

    # La siguiente fila contiene la tabla de detalles colapsables
    det = row.find_next_sibling('tr')
    tbl = det.find('table')
    # Iteramos por cada fila de detalle (clave: <th>, valor: <td>)
    for dtr in tbl.find_all('tr'):
        key = dtr.find('th').get_text(strip=True)
        val = dtr.find('td').get_text(strip=True)
        entry[key] = val

    # Añadimos la entrada completa a la lista
    rows.append(entry)

# ----------------------------------------------------------
# Creación de DataFrame y exportación a Excel
# ----------------------------------------------------------
df = pd.DataFrame(rows)
output_file = "SM-NCCHUMANO-RELAXED03-03.xlsx"
# Guardamos los datos en un archivo .xlsx sin incluir índice
df.to_excel(output_file, index=False)

print(f"ok {output_file}")  # Confirmación de generación del archivo

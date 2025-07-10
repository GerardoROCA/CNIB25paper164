#!/usr/bin/env python

import pandas as pd
from glob import glob
import os

# -----------------------------
# Configuración de parámetros
# -----------------------------
# Mapeo para convertir niveles de druggability a valores numéricos
drugg_map = {'Medium': 2, 'Strong': 3}

# Rutas de las carpetas que contienen los archivos .xlsx a procesar
FOLDERS = [
    r".\TopModels\Dimer\Anguila",
    r".\TopModels\Dimer\Human",
    r".\TopModels\Monomer\Anguila",
    r".\TopModels\Monomer\Human"
]

# ----------------------------------------------------------------
# Procesamiento de cada carpeta: lectura, filtrado y cálculo de métricas
# ----------------------------------------------------------------
for folder in FOLDERS:
    # Patrón para encontrar todos los archivos .xlsx en la carpeta
    pattern = os.path.join(folder, '*.xlsx')
    # Ruta para el archivo de resumen de esta carpeta
    resumen_path = os.path.join(folder, 'resumen.txt')
    resultados = []  # Lista para almacenar resultados por archivo

    # Abrimos el archivo de resumen en modo escritura
    with open(resumen_path, 'w', encoding='utf-8') as resumen:
        # Iteramos sobre cada archivo que cumpla el patrón
        for filepath in glob(pattern):
            # Leemos el Excel y obtenemos el nombre de archivo
            df = pd.read_excel(filepath)
            name = os.path.basename(filepath)

            # --------------------------------------------------
            # Validación: comprobamos columnas mínimas requeridas
            # --------------------------------------------------
            required_cols = {'Index', 'Druggability', 'DrugScore', 'Surface Area (Å2)'}
            if not required_cols.issubset(df.columns):
                linea = f"Omitido (faltan columnas): {name}"
                resumen.write(linea + '\n')
                print(linea)
                continue  # Pasamos al siguiente archivo

            # --------------------------------------------------
            # Filtrado: descartamos cavidades débilmente drogas y puntuaciones negativas
            # --------------------------------------------------
            df_f = df[(df['DrugScore'] >= 0) & (df['Druggability'] != 'Weak')].copy()
            if df_f.empty:
                linea = f"Sin datos válidos tras filtrar: {name}"
                resumen.write(linea + '\n')
                print(linea)
                continue

            # --------------------------------------------------
            # Cálculo de métricas por archivo
            # - Convertimos Druggability a valor numérico
            # - Obtenemos los top 3 índices según DrugScore
            # - Calculamos superficie máxima y su índice
            # --------------------------------------------------
            df_f['drugg_score'] = df_f['Druggability'].map(drugg_map)
            top3 = df_f.nlargest(3, 'DrugScore')['Index'].tolist()
            max_surface = df_f['Surface Area (Å2)'].max()
            idx_surface = int(df_f.loc[df_f['Surface Area (Å2)'].idxmax(), 'Index'])

            # Guardamos los resultados en la lista
            resultados.append({
                'archivo': name,
                'promedio_druggability': df_f['drugg_score'].mean(),
                'conteo_strong': int((df_f['Druggability'] == 'Strong').sum()),
                'max_drugscore': df_f['DrugScore'].max(),
                'avg_drugscore': df_f['DrugScore'].mean(),
                'max_surface_area': max_surface,
                'index_max_surface': idx_surface,
                'top3_indices': top3
            })

            # Escribimos en el resumen una línea con los datos clave
            linea = (
                f"{name}: Top 3 índices por DrugScore = {top3}; "
                f"Superficie máxima = {max_surface:.2f} (Index {idx_surface})"
            )
            resumen.write(linea + '\n')
            print(linea)

        # --------------------------------
        # Generación del resumen final
        # --------------------------------
        if not resultados:
            mensaje = "No se encontraron datos válidos en ningún archivo."
            resumen.write(mensaje + '\n')
            print(mensaje)
        else:
            # Convertimos a DataFrame para análisis global
            res_df = pd.DataFrame(resultados)
            # Seleccionamos los mejores por cada métrica
            gan_prom = res_df.loc[res_df['promedio_druggability'].idxmax()]
            gan_strong = res_df.loc[res_df['conteo_strong'].idxmax()]
            gan_maxds = res_df.loc[res_df['max_drugscore'].idxmax()]
            gan_avgds = res_df.loc[res_df['avg_drugscore'].idxmax()]
            gan_surf = res_df.loc[res_df['max_surface_area'].idxmax()]

            # Escribimos tabla de resultados por archivo
            resumen.write("\nResumen por archivo:\n")
            resumen.write(
                res_df[
                    ['archivo', 'promedio_druggability', 'conteo_strong',
                     'max_drugscore', 'avg_drugscore', 'max_surface_area']
                ].to_string(index=False) + '\n\n'
            )
            print("\nResumen por archivo:")
            print(
                res_df[
                    ['archivo', 'promedio_druggability', 'conteo_strong',
                     'max_drugscore', 'avg_drugscore', 'max_surface_area']
                ].to_string(index=False), '\n'
            )

            # Escribimos cuáles archivos lideran cada métrica
            resumen.write(
                f"Mejor promedio de Druggability: {gan_prom['archivo']}"
                f" ({gan_prom['promedio_druggability']:.2f})\n"
            )
            resumen.write(
                f"Mayor número de Strong:       {gan_strong['archivo']}"
                f" ({gan_strong['conteo_strong']})\n"
            )
            resumen.write(
                f"DrugScore máximo:            {gan_maxds['archivo']}"
                f" ({gan_maxds['max_drugscore']})\n"
            )
            resumen.write(
                f"DrugScore promedio:          {gan_avgds['archivo']}"
                f" ({gan_avgds['avg_drugscore']:.2f})\n"
            )
            resumen.write(
                f"Superficie máxima:           {gan_surf['archivo']}"
                f" ({gan_surf['max_surface_area']:.2f}, "
                f"Index {gan_surf['index_max_surface']})\n"
            )

            # Mostramos por consola los líderes de cada métrica
            print(f"Mejor promedio de Druggability: {gan_prom['archivo']} ({gan_prom['promedio_druggability']:.2f})")
            print(f"Mayor número de Strong:       {gan_strong['archivo']} ({gan_strong['conteo_strong']})")
            print(f"DrugScore máximo:            {gan_maxds['archivo']} ({gan_maxds['max_drugscore']})")
            print(f"DrugScore promedio:          {gan_avgds['archivo']} ({gan_avgds['avg_drugscore']:.2f})")
            print(f"Superficie máxima:           {gan_surf['archivo']} ({gan_surf['max_surface_area']:.2f}, "
                  f"Index {gan_surf['index_max_surface']})\n")

    # Mensaje final indicando la ubicación del archivo resumen
    print(f"Archivo de resumen generado en: {resumen_path}\n")

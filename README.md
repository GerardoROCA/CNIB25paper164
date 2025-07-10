# CNIB25paper164

Este repositorio contiene scripts comentados para:

- **Resumen de métricas de Druggability** (`scoresResume.py`)
- **Generación de heatmaps de RMSD** (`heatMaps.py`)
- **Parseo de tablas HTML y exportación a Excel** (`parsingCavityPlus.py`)
- **Visualización interactiva de Ramachandran Favored** (`scoresDashboard.py`)

## Requisitos

Instalación rápida:

```bash
pip install -r requirements.txt
```

## Uso de los scripts

### 1. Generar resúmenes de Druggability

```bash
python scoresResume.py
```

- Lee archivos `.xlsx` organizados en carpetas.
- Filtra cavidades según `DrugScore` y `Druggability`.
- Produce un `resumen.txt` con métricas (promedios, top3, superficies).

### 2. Heatmaps de RMSD

```bash
python heatMaps.py
```

- Define matrices de RMSD para monómeros y dímeros.
- Genera y guarda figuras PNG con valores en cada celda.

### 3. Parseo HTML a Excel

```bash
python parsingCavityPlus.py
```

- Extrae datos de una tabla HTML colapsable.
- Crea un DataFrame y exporta a `SM-NCCHUMANO-RELAXED03-03.xlsx`.

### 4. Dash App para Ramachandran

```bash
python scoresDashboard.py
```

- Inicia un servidor web en `http://127.0.0.1:8050`.
- Filtros dinámicos para estructura, software, proteína, modelos y relajación.
- Gráficas interactivas: barras y boxplots de Ramachandran Favored.


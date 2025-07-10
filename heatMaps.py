#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Configuración global para renderizado de texto matemático
# ----------------------------------------------------------
plt.rcParams['mathtext.fontset'] = 'dejavusans'  # Fuente para símbolos LaTeX

# ----------------------------------------------------------
# Función para graficar heatmap con valores en cada celda
# ----------------------------------------------------------
def plot_heatmap_with_values(matrix, labels, title, filename):
    """
    Dibuja y guarda un heatmap de RMSD con valores numéricos overlay.

    Parámetros:
    - matrix: numpy array cuadrada con valores RMSD.
    - labels: lista de etiquetas para ejes x e y.
    - title: título de la figura (puede contener LaTeX).
    - filename: ruta de archivo PNG para guardar la figura.
    """
    # Configuración de figura y ejes
    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, cmap='coolwarm', interpolation='nearest')  # Mapa de calor
    plt.colorbar(label='RMSD (Å)')                            # Barra de color con etiqueta
    
    # Etiquetas de los ejes X e Y con rotación para evitar solapamiento
    plt.xticks(ticks=np.arange(len(labels)), labels=labels, rotation=45, ha='right')
    plt.yticks(ticks=np.arange(len(labels)), labels=labels)

    # Iteramos sobre cada celda para colocar el valor numérico
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            plt.text(j, i, f"{value:.2f}", ha='center', va='center', color='black')

    # Ajustes finales antes de guardar y mostrar
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)  # Guardado en alta resolución
    plt.show()

# ----------------------------------------------------------
# Datos de RMSD: matrices para monómeros y dímeros
# ----------------------------------------------------------
# RMSD para monómero de βNCC en anguila
rmsd_pez = np.array([
    [0.000, 1.182, 1.029, 0.862],
    [1.182, 0.000, 0.877, 1.177],
    [1.029, 0.877, 0.000, 1.013],
    [0.862, 1.177, 1.013, 0.000]
])
# RMSD para monómero de humanNCC
rmsd_hum = np.array([
    [0.000, 1.022, 1.208, 0.908],
    [1.022, 0.000, 1.038, 1.018],
    [1.208, 1.038, 0.000, 0.809],
    [0.908, 1.018, 0.809, 0.000]
])

# Etiquetas en LaTeX para los ensayos comparativos
labels_pez = [
    r"AF $\beta\mathrm{NCC}$", r"RF $\beta\mathrm{NCC}$",
    r"SM $\beta\mathrm{NCC}$", r"MD $\beta\mathrm{NCC}$"
]
labels_hum = [
    r"AF $\mathrm{humanNCC}$", r"MD $\mathrm{humanNCC}$",
    r"RB $\mathrm{humanNCC}$", r"SM $\mathrm{humanNCC}$"
]

# Graficar heatmaps de RMSD para monómeros
plot_heatmap_with_values(
    rmsd_pez,
    labels_pez,
    r"Figure 1 – Heatmap RMSD $\beta\mathrm{NCC}$ Monomer",
    "heatmap_monomeros_pez.png"
)
plot_heatmap_with_values(
    rmsd_hum,
    labels_hum,
    r"Figure 2 – Heatmap RMSD $\mathrm{humanNCC}$ Monomer",
    "heatmap_monomeros_humano.png"
)

# RMSD para dímero de βNCC y humanNCC combinados
rmsd_dimers = np.array([
    [0.000, 1.093, 1.288, 1.122],
    [1.093, 0.000, 1.194, 0.987],
    [1.288, 1.194, 0.000, 1.277],
    [1.122, 0.987, 1.277, 0.000]
])
labels_dimers = [
    r"SM $\beta\mathrm{NCC}$", r"AF $\beta\mathrm{NCC}$",
    r"SM $\mathrm{humanNCC}$", r"AF $\mathrm{humanNCC}$"
]

# Graficar heatmap de RMSD para dímeros
plot_heatmap_with_values(
    rmsd_dimers,
    labels_dimers,
    "Figure 3 – Heatmap RMSD dimer models",
    "heatmap_dimers.png"
)

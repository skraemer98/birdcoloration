import os
import numpy as np
import cv2


#    Genera máscaras rellenando la región delimitada por las coordenadas.
#
#    Parámetros:
#        imagenes_dir (str): carpeta con las imágenes originales
#        coords_dirs (dict): carpeta con las coordenadas para las mascaras en cada imagen
#        output_dir (str): carpeta donde guardar las máscaras

# El codigo recorre la carpeta de coordenadas (si no tiene coordenadas asignadas la imagen, no genera la mascara). 
# Se emparejan las coordenadas con la imagen correspondiente. Obtenemos dimensiones de la imagen para crear la mascara del mismo tamaño. 
# Se genera la mascara poniendo unos en el centro de la region y ceros por fuera


def generar_mascaras(imagenes_dir, coords_dir, output_dir="mascaras"):

    os.makedirs(output_dir, exist_ok=True)

    for archivo in os.listdir(coords_dir):

        if not archivo.endswith(".txt"):
            continue
        numero_imagen = archivo.replace("_COORDINATES.txt", "")
        img_nombre = f"{numero_imagen}.jpg"
        img_path = os.path.join(imagenes_dir, img_nombre)
        coords_path = os.path.join(coords_dir, archivo)

        if not os.path.exists(img_path):
            continue
        
        img = cv2.imread(img_path)
        height, width = img.shape[:2]
        
        mask = np.zeros((height, width), dtype=np.uint8)

        with open(coords_path, "r") as f:
            coords = [tuple(map(int, line.strip().split())) for line in f if line.strip()]
        if len(coords) >= 3:
            pts = np.array([coords], dtype=np.int32)
            cv2.fillPoly(mask, pts, 255)
        mask_path = os.path.join(output_dir, f"{numero_imagen}_mask.png")
        cv2.imwrite(mask_path, mask)


if __name__ == "__main__":
    
    generar_mascaras("Photos_resized", "Meassurements_Belly", "mascaras_panza")
    generar_mascaras("Photos_resized", "Meassurements_Throat", "mascaras_garganta")

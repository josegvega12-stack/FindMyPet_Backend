import base64
import io
from typing import List, Tuple

from PIL import Image
import numpy as np


# Convierte una imagen (en bytes) a un vector numérico sencillo
def simple_embedding(image_bytes: bytes) -> List[float]:
    # Abrir la imagen con PIL
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Redimensionar para que sea pequeña (más rápido)
    image = image.resize((64, 64))
    # Convertir a array de numpy
    arr = np.asarray(image).astype("float32") / 255.0
    # Aplanar a un vector
    embedding = arr.flatten()
    return embedding.tolist()


# Extrae un color promedio desde una imagen en base64
def extract_colors_from_base64(image_base64: str) -> Tuple[int, int, int]:
    """
    Recibe una imagen en base64 y devuelve un color promedio (R, G, B).
    Esto es una versión sencilla para tener algo funcional.
    """
    # Quitar prefijo si viene como "data:image/jpeg;base64,...."
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((32, 32))

    arr = np.asarray(image).astype("float32")
    # Promedio de todos los píxeles
    mean_color = arr.mean(axis=(0, 1))
    r, g, b = mean_color
    return int(r), int(g), int(b)

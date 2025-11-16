from typing import Tuple


def grid_cell(latitude: float, longitude: float, cell_size: float = 0.01) -> Tuple[int, int]:
    """
    Agrupa coordenadas (lat, lon) en una celda de una grilla.
    Sirve para aproximar áreas y reducir búsquedas.

    cell_size = tamaño de la celda en grados.
    Por ejemplo, 0.01 ~ aprox. 1 km dependiendo de la zona.
    """
    lat_index = int(latitude / cell_size)
    lon_index = int(longitude / cell_size)
    return lat_index, lon_index
# --- Compatibilidad con server.py ---
def load_grid_cell(lat: float, lon: float, cell_size: float = 0.01) -> str:
    """
    Convierte lat/lon en una celda aproximada en formato string "lat_lon".
    Sirve como reemplazo directo de la función que esperaba server.py.
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return "0_0"

    lat_cell = round(lat / cell_size) * cell_size
    lon_cell = round(lon / cell_size) * cell_size
    return f"{lat_cell:.4f}_{lon_cell:.4f}"

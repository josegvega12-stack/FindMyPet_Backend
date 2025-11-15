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

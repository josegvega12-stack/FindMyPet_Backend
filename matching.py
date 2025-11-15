import numpy as np
from typing import List, Dict, Any


# 🔍 Calcula la similitud entre dos embeddings (vectores)
def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


# 🧠 Procesa una lista de reportes y devuelve las coincidencias más parecidas
def process_sighting_matches(lost_embeddings: List[Dict[str, Any]], sighting_embeddings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    matches = []

    for lost in lost_embeddings:
        best_score = 0.0
        best_match = None

        for sighting in sighting_embeddings:
            score = cosine_similarity(lost["embedding"], sighting["embedding"])
            if score > best_score:
                best_score = score
                best_match = sighting

        if best_match and best_score > 0.75:  # umbral de similitud (ajustable)
            matches.append({
                "lost_id": lost["id"],
                "sighting_id": best_match["id"],
                "similarity": round(best_score, 3)
            })

    return matches
# Wrapper para compatibilidad: mantiene la firma esperada por server.py
def matcher(lost_embeddings, sighting_embeddings):
    return process_sighting_matches(lost_embeddings, sighting_embeddings)

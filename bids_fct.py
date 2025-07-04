"""
Crear etiqueta como variable, así editamos en un único lugar la pasada que estamos dando a la evaluación
- el Id se mantiene como el identificador del equipo.
- Añadir una nueva columna para identificar el Factor evaluado y la discilplina "Coordenação. F1A
- Obra mantiene el "Nombre del edifício"

Evaluamos a todos los concorrentes a la vez en cada de las disciplinas y de los factores: 24 en total.
------> ¿ O evaluamos a cada concorrente en cada una de las disciplinas (como si fusesen los old_concorrentes)
donde el actual Work corresponde a cada factor? <----------
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Work:
    label: str
    cost: float

@dataclass
class Competitor:
    id: int
    works: List[Work]

competitors: List[Competitor] = [
    Competitor(1, [Work("1A", 14_000_000.0),
                   Work("1B", 10_200_000.0)]),
    
    Competitor(2, [Work("2A", 25_800_000.0)]),
    
    Competitor(3, [Work("3A",  3_100_000.0),
                   Work("3B",  21_900_000.0),
                   Work("3C",  10_700_000.0),
                   Work("3D",  4_000_000.0)]),
]


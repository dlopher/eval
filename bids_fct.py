"""
ABSTRACT STRUCTURE FOR A NEW CONCORRENTE:
Concorrente(
    id=...,
    factors=[
        Factor(
            name="A1. Obras de edifícios de UC na UE",
            disciplinas=[
                Disciplina(name="Coordenação", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ARQ", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ArqPAIS", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="Estruturas", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="AVACR", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="SCIE", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="IESE", projetos=[Projeto("Projeto 1", ...), ...]),
            ]
        ),
        Factor(
            name="A2. Obras de edifícios escolares na UE",
            disciplinas=[
                Disciplina(name="Coordenação", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ARQ", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ArqPAIS", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="Estruturas", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="AVACR", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="SCIE", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="IESE", projetos=[Projeto("Projeto 1", ...), ...]),
            ]
        ),
        Factor(
            name="A3. Obras de reabilitação com reforço sísmico na UE",
            disciplinas=[
                Disciplina(name="Coordenação", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ARQ", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="Estruturas", projetos=[Projeto("Projeto 1", ...), ...]),
            ]
        ),
        Factor(
            name="A4. NZEB + 20, LEAD, BREAM na UE",
            disciplinas=[
                Disciplina(name="Coordenação", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ARQ", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ECT", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="AVACR", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="IESE", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="IESA", projetos=[Projeto("Projeto 1", ...), ...]),
            ]
        ),
    ]
)
"""

from dataclasses import dataclass
from typing import List

# Estructura de datos
@dataclass
class Projeto:
    name: str
    cost: float

@dataclass
class Disciplina:
    name: str
    projetos: List[Projeto]

@dataclass
class Factor:
    name: str
    disciplinas: List[Disciplina]

@dataclass
class Concorrente:
    id: int
    factors: List[Factor]

# --- COMPETITION DATA ---

competitors: List[Concorrente] = [
    Concorrente(
        id=1,
        factors=[
            Factor(
                name="A1. Obras de edifícios de UC na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto CP1", 12_000_000.0),
                            Projeto("Projeto CP2", 9_500_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto ARQ1", 7_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "ArqPAIS",
                        [
                            Projeto("Projeto Pais1", 16_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto Estrut1", 18_000_000.0),
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto AVACR1", 16_900_000.0),
                        ]
                    ),
                    Disciplina(
                        "SCIE",
                        [
                            Projeto("Projeto SCIE1", 6_500_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESE",
                        [
                            Projeto("Projeto IESE1", 4_200_000.0),
                        ]
                    ),
                ]
            ),
            Factor(
                name="A2. Obras de edifícios escolares na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto ESC1", 10_000_000.0),
                            Projeto("Projeto ESC2", 6_500_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto ARQ2", 13_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "ArqPAIS",
                        [
                            # Empty
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto Estrut2", 17_000_000.0),
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto AVACR2", 19_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "SCIE",
                        [
                            # Empty
                        ]
                    ),
                    Disciplina(
                        "IESE",
                        [
                            Projeto("Projeto IESE2", 5_000_000.0),
                        ]
                    ),
                ]
            ),
            Factor(
                name="A3. Obras de reabilitação com reforço sísmico na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto REAB1", 6_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto ARQ3", 2_900_000.0),
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto Estrut3", 9_500_000.0),
                        ]
                    ),
                ]
            ),
            Factor(
                name="A4. NZEB + 20, LEAD, BREAM na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto NZEB1", 21_000_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto ARQ4", 8_400_000.0),
                        ]
                    ),
                    Disciplina(
                        "ECT",
                        [
                            Projeto("Projeto ECT1", 3_100_000.0),
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto AVACR3", 2_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESE",
                        [
                            Projeto("Projeto IESE3", 7_700_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESA",
                        [
                            # Empty
                        ]
                    ),
                ]
            ),
        ]
    ),
    
    # ---> INSERT CONCORRENTE HERE
]


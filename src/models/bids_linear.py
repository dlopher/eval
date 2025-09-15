"""
ABSTRACT STRUCTURE FOR A NEW CONCORRENTE:
Concorrente(
    id=...,
    factors=[
        Factor(
            id = "A1",
            name="Obras de edifícios de UC na UE",
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
            id="A2",
            name="Obras de edifícios escolares na UE",
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
            id="A3",
            name="Obras de reabilitação com reforço sísmico na UE",
            disciplinas=[
                Disciplina(name="Coordenação", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="ARQ", projetos=[Projeto("Projeto 1", ...), ...]),
                Disciplina(name="Estruturas", projetos=[Projeto("Projeto 1", ...), ...]),
            ]
        ),
        Factor(
            id="A4",
            name="Edifícios NZEB + 20, LEAD ou BREAM na UE",
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
    observations: str = ""
    status: str = ""

@dataclass
class Disciplina:
    name: str
    projetos: List[Projeto]

@dataclass
class Factor:
    id: str
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
                id ="A1",
                name="Obras de edifícios de Ut. Colectiva na UE",
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
                id="A2",
                name="Obras de edifícios escolares na UE",
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
                id="A3",
                name="Obras de reabilitação com reforço sísmico na UE",
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
                id="A4",
                name="Edifícios NZEB + 20, LEAD ou BREAM na UE",
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
    Concorrente(
        id=2,
        factors=[
            Factor(
                id ="A1",
                name="Obras de edifícios de Ut. Colectiva na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto ert", 16_000_000.0),
                            Projeto("Projeto POIHG", 19_500_000.0),
                            Projeto("Projeto CP2", 9_500_000.0),
                            Projeto("Projeto CP3", 8_000_000.0),
                            Projeto("Projeto CP4", 12_000_000.0),

                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto rt87", 17_200_000.0),
                            Projeto("Projeto rt845", 15_500_000.0),
                            Projeto("Projeto rrty67", 11_900_000.0),
                            Projeto("Projeto rfhfgh897", 19_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "ArqPAIS",
                        [
                            Projeto("Projeto 98rjwhnb", 13_860_000.0),
                            Projeto("Projeto rt87", 10_200_000.0),
                            Projeto("Projeto rt87", 5_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto Estrut1", 28_000_000.0),
                            Projeto("Projeto rt87", 17_200_000.0),
                            Projeto("Projeto rt87", 17_200_000.0)
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto AVACR1", 17_900_000.0),
                            Projeto("Projeto AVACR1", 6_300_000.0),
                            Projeto("Projeto AVACR1", 8_900_000.0),
                        ]
                    ),
                    Disciplina(
                        "SCIE",
                        [
                            Projeto("Projeto TRFGTRE", 12_500_000.0),
                            Projeto("Projeto 4543dfg", 23_500_000.0),
                            Projeto("Projeto fdgfgfdg", 18_600_000.0),
                            Projeto("Projeto nbnbgfew", 8_980_000.0),
                            Projeto("Projeto RETUY76", 15_589_000.0),
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
                id="A2",
                name="Obras de edifícios escolares na UE",
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
                            Projeto("Projeto ARQ2", 3_200_000.0),
                            Projeto("Projeto ARQ2", 27_800_000.0),
                            Projeto("Projeto ARQ2", 12_400_000.0),
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
                            Projeto("Projeto 4543dfg", 23_500_000.0),
                            Projeto("Projeto fdgfgfdg", 18_600_000.0),
                            Projeto("Projeto nbnbgfew", 8_980_000.0),
                            Projeto("Projeto RETUY76", 15_589_000.0),
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
                id="A3",
                name="Obras de reabilitação com reforço sísmico na UE",
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
                            Projeto("Projeto ARQ)/%", 4_450_000.0),
                            Projeto("Projeto AR34", 12_800_000.0),
                            Projeto("Projeto AR764", 16_890_000.0),
                            Projeto("Projeto ARiuytgvd", 19_976_000.0),
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
                id="A4",
                name="Edifícios NZEB + 20, LEAD ou BREAM na UE",
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
                            Projeto("Projeto IESE3", 17_700_000.0),
                            Projeto("Projeto IESE5", 9_780_000.0),
                        ]
                    ),
                ]
            ),
        ]
    ),

    Concorrente(
        id=3,
        factors=[
            Factor(
                id="A1",
                name="Obras de edifícios de Ut. Colectiva na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto A1C1", 10_500_000.0),
                            Projeto("Projeto A1C2", 8_200_000.0),
                            Projeto("Projeto A1C3", 9_300_000.0),
                            Projeto("Projeto A1C4", 11_400_000.0),
                            Projeto("Projeto A1C5", 7_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto A1ARQ1", 12_300_000.0),
                            Projeto("Projeto A1ARQ2", 10_200_000.0),
                            Projeto("Projeto A1ARQ3", 9_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "ArqPAIS",
                        [
                            Projeto("Projeto A1Pais1", 15_400_000.0),
                            Projeto("Projeto A1Pais2", 13_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto A1Estrut1", 18_700_000.0),
                            Projeto("Projeto A1Estrut2", 16_500_000.0),
                            Projeto("Projeto A1Estrut3", 14_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto A1AVACR1", 9_800_000.0),
                            Projeto("Projeto A1AVACR2", 8_700_000.0),
                        ]
                    ),
                    Disciplina(
                        "SCIE",
                        [
                            Projeto("Projeto A1SCIE1", 6_300_000.0),
                            Projeto("Projeto A1SCIE2", 5_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESE",
                        [
                            Projeto("Projeto A1IESE1", 4_500_000.0),
                            Projeto("Projeto A1IESE2", 3_800_000.0),
                        ]
                    ),
                ]
            ),
            Factor(
                id="A2",
                name="Obras de edifícios escolares na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto A2C1", 11_000_000.0),
                            Projeto("Projeto A2C2", 7_500_000.0),
                            Projeto("Projeto A2C3", 9_200_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto A2ARQ1", 13_800_000.0),
                            Projeto("Projeto A2ARQ2", 12_400_000.0),
                        ]
                    ),
                    Disciplina(
                        "ArqPAIS",
                        [
                            Projeto("Projeto A2Pais1", 9_200_000.0),
                            Projeto("Projeto A2Pais2", 8_100_000.0),
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto A2Estrut1", 16_500_000.0),
                            Projeto("Projeto A2Estrut2", 14_300_000.0),
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto A2AVACR1", 14_800_000.0),
                            Projeto("Projeto A2AVACR2", 13_600_000.0),
                        ]
                    ),
                    Disciplina(
                        "SCIE",
                        [
                            Projeto("Projeto A2SCIE1", 5_600_000.0),
                            Projeto("Projeto A2SCIE2", 4_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESE",
                        [
                            Projeto("Projeto A2IESE1", 3_900_000.0),
                            Projeto("Projeto A2IESE2", 3_200_000.0),
                        ]
                    ),
                ]
            ),
            Factor(
                id="A3",
                name="Obras de reabilitação com reforço sísmico na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto A3C1", 7_800_000.0),
                            Projeto("Projeto A3C2", 6_500_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto A3ARQ1", 3_200_000.0),
                            Projeto("Projeto A3ARQ2", 5_400_000.0),
                            Projeto("Projeto A3ARQ3", 4_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "Estruturas",
                        [
                            Projeto("Projeto A3Estrut1", 10_500_000.0),
                            Projeto("Projeto A3Estrut2", 9_200_000.0),
                        ]
                    ),
                ]
            ),
            Factor(
                id="A4",
                name="Edifícios NZEB + 20, LEAD ou BREAM na UE",
                disciplinas=[
                    Disciplina(
                        "Coordenação",
                        [
                            Projeto("Projeto A4C1", 20_000_000.0),
                            Projeto("Projeto A4C2", 18_500_000.0),
                        ]
                    ),
                    Disciplina(
                        "ARQ",
                        [
                            Projeto("Projeto A4ARQ1", 9_400_000.0),
                            Projeto("Projeto A4ARQ2", 8_700_000.0),
                        ]
                    ),
                    Disciplina(
                        "ECT",
                        [
                            Projeto("Projeto A4ECT1", 4_100_000.0),
                            Projeto("Projeto A4ECT2", 3_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "AVACR",
                        [
                            Projeto("Projeto A4AVACR1", 3_200_000.0),
                            Projeto("Projeto A4AVACR2", 2_900_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESE",
                        [
                            Projeto("Projeto A4IESE1", 6_700_000.0),
                            Projeto("Projeto A4IESE2", 5_800_000.0),
                        ]
                    ),
                    Disciplina(
                        "IESA",
                        [
                            Projeto("Projeto A4IESA1", 8_900_000.0),
                            Projeto("Projeto A4IESA2", 7_600_000.0),
                        ]
                    ),
                ]
            ),
        ]
    ),

    # ---> INSERT CONCORRENTE HERE
]


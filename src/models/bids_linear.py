from dataclasses import dataclass
from typing import List
from datetime import datetime

# --- DATA STRUCTURE ---
@dataclass
class Projeto:
    name: str
    cost: float
    date: datetime = None
    observations: str = ""
    status: str = ""

@dataclass
class Formação:
    name: str
    hours: float
    # date: datetime = None
    observations: str = ""
    status: str = ""

@dataclass
class Disciplina:
    name: str
    projetos: List[Projeto] = None
    formacoes: List[Formação] = None

    def __post_init__(self):
        if self.projetos is None:
            self.projetos = []
        if self.formacoes is None:
            self.formacoes = []

@dataclass
class Factor:
    id: str
    name: str
    disciplinas: List[Disciplina]

@dataclass
class Concorrente:
    id: int
    factors: List[Factor]


# --- COMPETITION DATA --- (no longer used in linear mode as we will be reading from excel files)

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
   
    # ---> INSERT CONCORRENTE HERE
]


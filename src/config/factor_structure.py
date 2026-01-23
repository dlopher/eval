from typing import Dict, List


# Define factor structure
FACTOR_STRUCTURE = {
    "A1": {
        "name": "Projetos de obras executadas de edifícios de utilização coletiva na UE",
        "type": "projeto",
        "require_date": True,
        "require_owner": True,
        "disciplinas": [
            "Coordenação", 
            "ARQ", 
            "ArqPAIS", 
            "Estruturas", 
            "AVACR",
            "BIM"
        ]
    },
    "A2": {
        "name": "Projetos de obras executadas de edifícios escolares na UE",
        "type": "projeto",
        "require_date": True,
        "require_owner": True,
        "disciplinas": [
            "Coordenação", 
            "ARQ", 
            "ArqPAIS", 
            "Estruturas", 
            "AVACR",
            "BIM"
        ]
    },
    "A3": {
        "name": "Projetos de obras públicas executadas na UE",
        "type": "projeto",
        "require_date": True,
        "require_owner": True,
        "disciplinas": [
            "Coordenação", 
            "ARQ", 
            "ArqPAIS", 
            "Estruturas", 
            "AVACR",
            "BIM"
        ]
    },
    "A4": {
        "name": "Projetos de obras executadas de reabilitação de edifícios (com reforço sísmico) na UE",
        "type": "projeto",
        "require_date": True,
        "require_owner": True,
        "disciplinas": [
            "Coordenação", 
            "ARQ", 
            "ArqPAIS", 
            "Estruturas", 
            "AVACR",
            "BIM"
        ]
    },
    "A5": {
        "name": "Horas de formação para a gestão BIM",
        "type": "formação",
        "require_date": False,
        "require_owner": False,
        "disciplinas": [
            "formação BIM"
        ]
    }
}
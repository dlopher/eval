import os

# PDF folder path
PDF_FOLDER = "data/input/equipa_tecnica"

# Define expected table columns
COLUMNS = [
    "PROJETO ORDENADOR E DE ESPECIALIDADE",
    "NOME DO AUTOR DO PROJETO", 
    "Nº INSCRIÇÃO NA ORDEM PROFISSIONAL"
]

ESPECIALIDADES = [
    "Projeto de Arquitetura, incluindo Plano de Acessibilidades",
    "Projeto de Demolições, Escavação e Contenção Periférica, Fundações e Estruturas",
    "Projeto de Instalações, Equipamentos e Sistemas de Águas",
    "Projeto de Instalações, Equipamentos e Sistemas de Esgotos",
    "Projeto de Instalações, Equipamentos e Sistemas Elétricos",
    "Projeto de Instalações, Equipamentos e Sistemas de Comunicações",
    "Projeto de Instalações, Equipamentos e Sistemas de Gás",
    "Projeto de Instalações, Equipamentos e Sistemas de Aquecimento, Ventilação, Ar Condicionado e Refrigeração (AVACR)",
    "Projeto de Instalações, Equipamentos e Sistemas de Transporte Pessoas e Cargas",
    "Projeto de Segurança Contra Incêndio em Edifícios (SCIE)",
    "Projeto de Sistemas de Segurança Integrada",
    "Projeto de Gestão Técnica Centralizada",
    "Projeto de Condicionamento Acústico",
    "Estudo de Comportamento Térmico",
    "Projeto de Arquitetura Paisagista" 
]

# Map filenames to identifiers
FILE_MAPPING = {
    "11003.pdf": "11003",
    "11115.pdf": "11115",
    "11151.pdf": "11151",
    "11161.pdf": "11161",
    "11163.pdf": "11163",
    "11178.pdf": "11178",
    "11180.pdf": "11180",
    "11192.pdf": "11192",
    "11196.pdf": "11196",
}
# -*- coding: latin-1 -*-
"""
IndexarTextos.py

Indexa textos utilizando:
- Normalização forte
- Remoção de acentos
- Detecção por radical
- Ativação proporcional de tríades
- Score final = positivo - negativo
"""

import os
import csv
import json
import re
import unicodedata
from collections import defaultdict

ARQUIVO_TRIADE_POS = "Tabela_Categorias_Tríades_POSITIVAS.csv"
ARQUIVO_TRIADE_NEG = "Tabela_Categorias_Tríades_NEGATIVAS.csv"

PASTA_TEXTOS = "textos"
ARQUIVO_SAIDA = "indice_textos.json"


# ==============================
# NORMALIZAÇÃO FORTE
# ==============================

def normalizar(texto):
    texto = texto.lower()

    # remover acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    # remover pontuação
    texto = re.sub(r'[^\w\s]', ' ', texto)

    # normalizar espaços
    texto = re.sub(r'\s+', ' ', texto)

    return texto.strip()


# ==============================
# RADICAL SIMPLES
# ==============================

def radical(palavra):
    if len(palavra) > 5:
        return palavra[:6]
    return palavra


def contar_termos_encontrados(texto_norm, termos):
    palavras = texto_norm.split()
    encontrados = 0

    for termo in termos:
        termo_r = radical(termo)

        for palavra in palavras:
            if radical(palavra).startswith(termo_r):
                encontrados += 1
                break

    return encontrados


# ==============================
# CARREGAR TRÍADES
# ==============================

def carregar_triades(arquivo):
    triades = defaultdict(list)

    with open(arquivo, encoding="latin-1") as f:
        reader = csv.reader(f)
        next(reader, None)

        for linha in reader:
            if not linha or len(linha) < 3:
                continue

            categoria = linha[0].strip()
            triade_str = linha[1].strip()
            peso = float(linha[2])

            termos = [t.strip().lower() for t in triade_str.split(";") if t.strip()]

            if len(termos) == 3:
                triades[categoria].append((termos, peso))

    return triades


# ==============================
# CLASSIFICAR TEXTO
# ==============================

def classificar_texto(texto, triades_pos, triades_neg):

    texto_norm = normalizar(texto)
    resultados = {}

    categorias = set(list(triades_pos.keys()) + list(triades_neg.keys()))

    for categoria in categorias:

        score_pos = 0.0
        score_neg = 0.0

        # POSITIVAS
        for termos, peso in triades_pos.get(categoria, []):

            encontrados = contar_termos_encontrados(texto_norm, termos)

            if encontrados > 0:
                fator = encontrados / 3.0
                score_pos += peso * fator

        # NEGATIVAS
        for termos, peso in triades_neg.get(categoria, []):

            encontrados = contar_termos_encontrados(texto_norm, termos)

            if encontrados > 0:
                fator = encontrados / 3.0
                score_neg += peso * fator

        score_final = round(score_pos - score_neg, 4)

        if score_pos > 0 or score_neg > 0:
            resultados[categoria] = {
                "positivo": round(score_pos, 4),
                "negativo": round(score_neg, 4),
                "final": score_final
            }

    return resultados


# ==============================
# INDEXAÇÃO COMPLETA
# ==============================

def indexar_textos():

    print("Carregando tríades positivas...")
    triades_pos = carregar_triades(ARQUIVO_TRIADE_POS)

    print("Carregando tríades negativas...")
    triades_neg = carregar_triades(ARQUIVO_TRIADE_NEG)

    indice = {}

    for nome_arquivo in os.listdir(PASTA_TEXTOS):

        caminho = os.path.join(PASTA_TEXTOS, nome_arquivo)

        if not os.path.isfile(caminho):
            continue

        if not nome_arquivo.lower().endswith(".txt"):
            continue

        print(f"Indexando: {nome_arquivo}")

        with open(caminho, encoding="latin-1") as f:
            conteudo = f.read()

        classificacao = classificar_texto(conteudo, triades_pos, triades_neg)

        indice[nome_arquivo] = classificacao

    print("Salvando índice...")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(indice, f, indent=2, ensure_ascii=False)

    print("Indexação concluída com sucesso.")


# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":
    indexar_textos()

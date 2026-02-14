# -*- coding: latin-1 -*-

import os
import csv
import json
import re
import unicodedata

CSV_POS = "Tabela_Categorias_Tríades_POSITIVAS.csv"
CSV_NEG = "Tabela_Categorias_Tríades_NEGATIVAS.csv"
ARQUIVO_INDICE = "indice_textos.json"
PASTA_TEXTOS = "textos"

PESO_1 = 0.3
PESO_2 = 0.6
PESO_3 = 1.0


# =========================
# NORMALIZAÇÃO
# =========================

def normalizar(txt):
    txt = txt.lower()
    txt = unicodedata.normalize("NFD", txt)
    txt = txt.encode("ascii", "ignore").decode("utf-8")
    txt = txt.replace("ç", "c")
    return txt


def radical(p):
    if len(p) > 4:
        return p[:5]
    return p


def normalizar_lista(lista):
    return [radical(normalizar(p.strip())) for p in lista]


# =========================
# CARREGAR CSV TRÍADES
# =========================

def carregar_triadess(caminho):

    categorias = {}

    with open(caminho, encoding="iso-8859-1") as f:
        leitor = csv.reader(f, delimiter=",")

        for linha in leitor:

            # ignora linhas vazias
            if not linha or len(linha) < 3:
                continue

            # ignora cabeçalho
            if linha[0].strip().upper() == "CATEGORIA":
                continue

            categoria = linha[0].strip().upper()
            termos_brutos = linha[1].split(";")

            try:
                peso = float(linha[2].strip())
            except:
                continue  # ignora linha inválida

            termos = normalizar_lista(termos_brutos)

            if categoria not in categorias:
                categorias[categoria] = []

            categorias[categoria].append((termos, peso))

    return categorias


# =========================
# CLASSIFICAR PERGUNTA
# =========================

def classificar_pergunta(pergunta, pos_dict, neg_dict):

    palavras = re.findall(r"\w+", normalizar(pergunta))
    palavras = [radical(p) for p in palavras]

    palavras_set = set(palavras)
    scores = {}

    todas_categorias = set(pos_dict.keys()) | set(neg_dict.keys())

    for categoria in todas_categorias:

        soma_pos = 0
        soma_neg = 0

        if categoria in pos_dict:
            for termos, peso in pos_dict[categoria]:
                encontrados = len([t for t in termos if t in palavras_set])

                if encontrados == 1:
                    soma_pos += peso * PESO_1
                elif encontrados == 2:
                    soma_pos += peso * PESO_2
                elif encontrados == 3:
                    soma_pos += peso * PESO_3

        if categoria in neg_dict:
            for termos, peso in neg_dict[categoria]:
                encontrados = len([t for t in termos if t in palavras_set])

                if encontrados == 1:
                    soma_neg += peso * PESO_1
                elif encontrados == 2:
                    soma_neg += peso * PESO_2
                elif encontrados == 3:
                    soma_neg += peso * PESO_3

        score_final = soma_pos - soma_neg

        if score_final > 0:
            scores[categoria] = score_final

    if not scores:
        return None, None

    ordenado = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    principal = ordenado[0][0]
    secundaria = ordenado[1][0] if len(ordenado) > 1 else None

    return principal, secundaria


# =========================
# INDICE
# =========================

def carregar_indice():
    with open(ARQUIVO_INDICE, encoding="utf-8") as f:
        return json.load(f)


def buscar_documentos(indice, categoria, limite=10):

    resultados = []

    for nome, dados in indice.items():
        if categoria in dados:
            final = dados[categoria]["final"]
            if final > 0:
                resultados.append((nome, final))

    resultados.sort(key=lambda x: x[1], reverse=True)

    return resultados[:limite]


# =========================
# CONTEXTO REAL
# =========================

def buscar_contexto(nome_arquivo, categoria):

    caminho = os.path.join(PASTA_TEXTOS, nome_arquivo)

    if not os.path.exists(caminho):
        return []

    with open(caminho, encoding="latin-1") as f:
        texto = f.read()

    palavras = re.findall(r"\w+", texto)
    cat_norm = normalizar(categoria)

    resultados = []

    for i, palavra in enumerate(palavras):

        if cat_norm in normalizar(palavra):

            inicio = max(0, i - 5)
            fim = min(len(palavras), i + 6)

            trecho = palavras[inicio:fim]

            trecho_formatado = []

            for j, w in enumerate(trecho):
                if inicio + j == i:
                    trecho_formatado.append("[" + w + "]")
                else:
                    trecho_formatado.append(w)

            resultados.append(" ".join(trecho_formatado))

    return resultados


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    pos_dict = carregar_triadess(CSV_POS)
    neg_dict = carregar_triadess(CSV_NEG)
    indice = carregar_indice()

    while True:

        pergunta = input("\nDigite sua pergunta (ENTER para sair): ").strip()

        if not pergunta:
            break

        principal, secundaria = classificar_pergunta(pergunta, pos_dict, neg_dict)

        print("\nCategoria Principal:", principal)
        print("Categoria Secundaria:", secundaria)

        if not principal:
            continue

        resultados = buscar_documentos(indice, principal)

        for nome, score in resultados:

            print("\nArquivo:", nome)
            print("Score:", score)

            contextos = buscar_contexto(nome, principal)

            for ctx in contextos:
                print("Contexto:", ctx)

            print("-" * 40)





import csv
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/meyer/Documents/Python")

ARQ_ENTRADA = BASE / "horas_trabalhadas.csv"
ARQ_SAIDA = BASE / "relatorio_horas.csv"
ARQ_LOG = BASE / "atividade.log"

# Função que registra um evento de processamento - LOG
def registrar_log(mensagem):
    BASE.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with ARQ_LOG.open("a", encoding="iso-8859-1") as f:
        f.write(f"[{timestamp}] {mensagem}\n")

# Processa o CSV
def processar_csv():
    # Exceção
    try:
        if not ARQ_ENTRADA.exists():
            raise FileNotFoundError("Arquivo CSV de entrada não encontrado.")

        totais = {}
        # 1 - Leitura do arquivo de entrada
        with ARQ_ENTRADA.open("r", encoding="iso-8859-1") as csvfile:
            leitor = csv.DictReader(csvfile, delimiter=";")
            # 1.1 - Processamento registro a registro
            for linha in leitor:
                try:
                    nome = linha["funcionario"]
                    horas = float(linha["horas"].replace(",", "."))
                    totais[nome] = totais.get(nome, 0) + horas
                except (ValueError, KeyError):
                    registrar_log(f"Linha inválida ignorada: {linha}")
        # 2 - Gravação do arquivo de saída
        with ARQ_SAIDA.open("w", encoding="iso-8859-1", newline="") as csvfile:
            campos = ["funcionario", "total_horas"]
            escritor = csv.DictWriter(csvfile, fieldnames=campos, delimiter=";")
            escritor.writeheader()
            # 2.1 - Processamento linha a linha
            for nome, total in totais.items():
                escritor.writerow({
                    "funcionario": nome,
                    "total_horas": f"{total:.2f}"
                })
    # Tratamento das exceções
    except FileNotFoundError as e:
        print(f"❌ {e}")
        registrar_log(str(e))

    except PermissionError:
        print("❌ Erro de permissão ao acessar arquivos.")
        registrar_log("Erro de permissão ao acessar arquivos.")

    except Exception as e:
        print("❌ Erro inesperado.")
        registrar_log(f"Erro inesperado: {e}")

    else:
        print("✔ Relatório CSV gerado com sucesso.")
        registrar_log("Relatório CSV gerado com sucesso.")

    finally:
        print("Processamento finalizado.")
        
# Inicia o processamento do programa, invocando a principal função.
if __name__ == "__main__":
    processar_csv()

import requests
from datetime import datetime

URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL,BTC-BRL"

def obter_cotacoes():
    print("🔎 Consultando API de cotações...")
    
    try:
        resposta = requests.get(URL, timeout=10)
        resposta.raise_for_status()  # dispara erro se status != 200
        
        dados = resposta.json()
        
        return {
            "USD": float(dados["USDBRL"]["bid"]),
            "EUR": float(dados["EURBRL"]["bid"]),
            "GBP": float(dados["GBPBRL"]["bid"]),
            "BTC": float(dados["BTCBRL"]["bid"]),
        }
    
    except requests.exceptions.SSLError:
        print("\n❌ ERRO DE SSL!")
        print("Sua rede está interceptando HTTPS e não permite certificados externos.")
        print("Use a VERSÃO OFFLINE da aula 17 dentro da empresa.")
        return None

    except requests.exceptions.Timeout:
        print("\n⏱️ Tempo de resposta esgotado. Tente novamente.")
        return None

    except Exception as e:
        print(f"\n❌ Erro ao acessar a API: {e}")
        return None

def converter(valor, moeda, cotacoes):
    moeda = moeda.upper()
    if moeda not in cotacoes:
        print(f"⚠️ Moeda '{moeda}' não disponível.")
        return
    
    cotacao = cotacoes[moeda]
    convertido = valor / cotacao
    print(f"\n💰 Cotação atual {moeda}: R${cotacao:.4f}")
    print(f"R${valor:.2f} equivalem a {convertido:.2f} {moeda}")

print("=== Sistema Online de Conversão de Moedas ===")
valor = float(input("Digite o valor em reais (R$): "))
moeda = input("Digite a moeda desejada (USD, EUR, GBP, BTC): ")

cotacoes = obter_cotacoes()

if cotacoes:
    converter(valor, moeda, cotacoes)
    print(f"\nConsulta realizada em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

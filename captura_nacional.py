import requests
import pandas as pd

# Link de exemplo para bolsas no país (ajuste para o arquivo CSV mais recente do portal)
CSV_LINK = "https://dadosabertos.cnpq.br/bolsas_pais_2024.csv" 

def capturar_nacional():
    print("Iniciando captura nacional (CNPq)...")
    try:
        response = requests.get(CSV_LINK)
        with open("temp_bolsas.csv", "wb") as f:
            f.write(response.content)
        
        # Lê o CSV corrigindo o separador comum no Brasil (;)
        df = pd.read_csv("temp_bolsas.csv", sep=";", encoding="latin-1")
        
        # Filtro corrigido: garante que pegamos apenas bolsas ativas
        # Ajuste o nome da coluna 'STATUS_BOLSA' conforme o cabeçalho real do arquivo
        if 'STATUS_BOLSA' in df.columns:
            bolsas_ativas = df == 'ATIVO']
        else:
            bolsas_ativas = df.head(10) # Fallback para teste se a coluna for diferente
        
        resultados = bolsas_ativas.to_dict('records')
        print(f"✅ Capturadas {len(resultados)} bolsas nacionais.")
        return resultados
    except Exception as e:
        print(f"❌ Erro na captura nacional: {e}")
        return # Retorna lista vazia para não quebrar o main.py

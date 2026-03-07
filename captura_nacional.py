import requests
import pandas as pd
import io

# Link oficial de dados abertos do CNPq
CSV_LINK = "https://dadosabertos.cnpq.br/bolsas_pais_2024.csv" 

def capturar_nacional():
    print("Iniciando captura nacional (CNPq)...")
    try:
        response = requests.get(CSV_LINK)
        # Lê o CSV diretamente da memória para ser mais rápido
        df = pd.read_csv(io.BytesIO(response.content), sep=";", encoding="latin-1")
        
        # Filtro corrigido: seleciona as linhas onde o status é ATIVO
        if 'STATUS_BOLSA' in df.columns:
            bolsas_ativas = df == 'ATIVO']
        else:
            # Caso o cabeçalho mude, pegamos uma amostra para teste
            bolsas_ativas = df.head(10)
        
        resultados =
        for _, row in bolsas_ativas.iterrows():
            resultados.append({
                "title": f"Bolsa {row.get('MODALIDADE_BOLSA', 'CNPq')}",
                "provider": "CNPq",
                "link": "https://www.gov.br/cnpq/pt-br",
                "description": f"Instituição: {row.get('NOME_INSTITUICAO', 'N/A')}",
                "deadline": None
            })
        print(f"✅ Capturadas {len(resultados)} bolsas nacionais.")
        return resultados
    except Exception as e:
        print(f"❌ Erro na captura nacional: {e}")
        return

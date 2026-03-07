import requests
import pandas as pd
import io

def capturar_nacional():
    print("Iniciando captura nacional (CNPq)...")
    
    CSV_LINK = "https://dadosabertos.cnpq.br/bolsas_pais_2024.csv"

    try:
        response = requests.get(CSV_LINK, timeout=30)
        response.raise_for_status()

        df = pd.read_csv(
            io.BytesIO(response.content),
            sep=";",
            encoding="latin-1",
            on_bad_lines='skip'
        )

        df.columns = [c.upper() for c in df.columns]

        if 'STATUS_BOLSA' in df.columns:
            bolsas_ativas = df[df['STATUS_BOLSA'] == 'ATIVO']
        else:
            bolsas_ativas = df.head(20)

        resultados = []

        for _, row in bolsas_ativas.iterrows():
            resultados.append({
                "title": f"Bolsa {row.get('MODALIDADE_BOLSA', 'Pesquisa')}",
                "provider": "CNPq",
                "link": "https://www.gov.br/cnpq/pt-br",
                "description": f"Instituição: {row.get('NOME_INSTITUICAO', 'N/A')} | Área: {row.get('NOME_GRANDE_AREA', 'N/A')}",
                "deadline": None
            })

        print(f"✅ Capturadas {len(resultados)} bolsas nacionais.")
        return resultados

    except Exception as e:
        print(f"❌ Erro na captura nacional: {e}")
        return []

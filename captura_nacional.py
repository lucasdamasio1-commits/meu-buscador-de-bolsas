import pandas as pd
import io
import requests
import time

def captura_nacional():

    print("Capturando bolsas CNPq...")

    url = "https://dadosabertos.cnpq.br/bolsas_pais_2024.csv"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/csv"
    }

    for tentativa in range(3):

        try:

            r = requests.get(url, headers=headers, timeout=60)

            r.raise_for_status()

            df = pd.read_csv(
                io.BytesIO(r.content),
                sep=";",
                encoding="latin-1",
                on_bad_lines="skip"
            )

            df.columns = [c.upper() for c in df.columns]

            bolsas = df.head(30)

            resultados = []

            for _, row in bolsas.iterrows():

                resultados.append({
                    "title": f"Bolsa {row.get('MODALIDADE_BOLSA','Pesquisa')}",
                    "provider": "CNPq",
                    "link": "https://www.gov.br/cnpq",
                    "description": row.get("NOME_GRANDE_AREA","Pesquisa científica"),
                    "deadline": None
                })

            print("CNPq:", len(resultados))

            return resultados

        except Exception as e:

            print("Tentativa CNPq falhou:", tentativa + 1)
            time.sleep(5)

    print("CNPq indisponível")

    return []

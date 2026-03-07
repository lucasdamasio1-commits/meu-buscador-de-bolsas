import pandas as pd
import io
from utils import get_request

def captura_nacional():

    print("Capturando bolsas CNPq...")

    CSV_LINK = "https://dadosabertos.cnpq.br/bolsas_pais_2024.csv"

    try:

        response = get_request(CSV_LINK)

        df = pd.read_csv(
            io.BytesIO(response.content),
            sep=";",
            encoding="latin-1",
            on_bad_lines="skip"
        )

        df.columns = [c.upper() for c in df.columns]

        if "STATUS_BOLSA" in df.columns:
            bolsas = df[df["STATUS_BOLSA"] == "ATIVO"]
        else:
            bolsas = df.head(20)

        resultados = []

        for _, row in bolsas.head(30).iterrows():

            resultados.append({
                "title": f"Bolsa {row.get('MODALIDADE_BOLSA','Pesquisa')}",
                "provider": "CNPq",
                "link": "https://www.gov.br/cnpq",
                "description": f"{row.get('NOME_INSTITUICAO','')} - {row.get('NOME_GRANDE_AREA','')}",
                "deadline": None
            })

        print("CNPq:", len(resultados))
        return resultados

    except Exception as e:
        print("Erro CNPq:", e)
        return []

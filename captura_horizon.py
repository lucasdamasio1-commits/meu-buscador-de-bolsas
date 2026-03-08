import requests


def captura_horizon():

    print("Consultando Horizon Europe...")

    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"

    params = {
        "apiKey": "SEDIA",
        "pageSize": 50,
        "pageNumber": 1
    }

    payload = {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"type": ["1"]}},
                    {"terms": {"status": ["31094501"]}}
                ]
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(
        url,
        params=params,
        json=payload,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        print("Erro Horizon:", response.text)
        return []

    data = response.json()

    oportunidades = []

    try:

        resultados = data["hits"]["hits"]

        for item in resultados:

            fonte = item["_source"]

            titulo = fonte.get("title", "Sem título")
            descricao = fonte.get("description", "")

            oportunidades.append({
                "titulo": titulo,
                "instituicao": "Horizon Europe",
                "area": "Pesquisa",
                "pais": "Europa",
                "link": "https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
                "descricao": descricao
            })

    except Exception as e:

        print("Erro ao processar Horizon:", e)

    print("Horizon encontrados:", len(resultados))

    return resultados

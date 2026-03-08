import requests

def capturar_horizon():
    print("Consultando Horizon Europe...")

    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"

    payload = {
        "bool": {
            "must": [
                {"terms": {"type": ["1"]}},
                {"terms": {"status": ["31094501"]}}
            ]
        }
    }

    params = {
        "apiKey": "SEDIA",
        "pageSize": 50,
        "pageNumber": 1
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, params=params, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()

    oportunidades = []

    for item in data.get("results", []):
        oportunidades.append({
            "titulo": item.get("title"),
            "instituicao": "Horizon Europe",
            "area": "Pesquisa",
            "pais": "Europa",
            "link": item.get("url"),
            "descricao": item.get("description", "")
        })

    print("Horizon encontrados:", len(oportunidades))

    return oportunidades

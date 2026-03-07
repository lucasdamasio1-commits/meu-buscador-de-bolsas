import requests

def captura_horizon():

    print("Consultando Horizon Europe...")

    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"

    payload = {
        "query": "*",
        "page": 0,
        "size": 20
    }

    try:

        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()

        dados = r.json()

        resultados = []

        chamadas = dados.get("results", [])

        for call in chamadas:

            identifier = call.get("identifier")

            resultados.append({
                "title": call.get("title"),
                "provider": "Horizon Europe",
                "deadline": call.get("deadline"),
                "link": f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/{identifier}",
                "description": call.get("description","EU research funding call")
            })

        print("Horizon:", len(resultados))

        return resultados

    except Exception as e:

        print("Erro Horizon:", e)
        return []

import requests

def captura_horizon():

    print("Consultando Horizon Europe...")

    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"

    payload = {
        "query": "*",
        "page": 0,
        "size": 20,
        "sort": "deadline"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:

        r = requests.post(url, json=payload, headers=headers, timeout=30)

        r.raise_for_status()

        data = r.json()

        resultados = []

        chamadas = data.get("results", [])

        for call in chamadas:

            identifier = call.get("identifier")

            resultados.append({
                "title": call.get("title"),
                "provider": "Horizon Europe",
                "deadline": call.get("deadline"),
                "link": f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/{identifier}",
                "description": call.get("description","EU research funding")
            })

        print("Horizon:", len(resultados))

        return resultados

    except Exception as e:

        print("Erro Horizon:", e)

        return []

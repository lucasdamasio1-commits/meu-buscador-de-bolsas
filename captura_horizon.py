import requests


def captura_horizon():

    print("Consultando Horizon Europe...")

    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA"

    payload = {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"type": ["1"]}},
                    {"terms": {"status": ["31094501"]}}
                ]
            }
        },
        "from": 0,
        "size": 50
    }

    headers = {
        "Content-Type": "application/json"
    }

    resultados = []

    try:

        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()

        data = response.json()

        for item in data.get("results", []):

            resultados.append({
                "title": item.get("title", ""),
                "description": item.get("content", ""),
                "provider": "Horizon Europe",
                "link": item.get("url", ""),
                "deadline": None
            })

        print("Horizon capturado:", len(resultados))

    except Exception as e:

        print("Erro Horizon:", e)

    return resultados

import requests

def captura_horizon():

    print("Consultando Horizon Europe...")

    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA"

    payload = {
        "bool": {
            "must": [
                {"terms": {"type": ["1"]}},
                {"terms": {"status": ["31094501"]}}
            ]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    resultados = []

    try:

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        response.raise_for_status()

        data = response.json()

        documentos = data.get("results", [])

        for item in documentos:

            titulo = item.get("title", "Sem título")

            descricao = item.get("content", "")

            link = item.get("url", "")

            resultados.append({
                "title": titulo,
                "description": descricao,
                "provider": "Horizon Europe",
                "link": link,
                "deadline": None
            })

        print("Horizon capturado:", len(resultados))

    except Exception as e:

        print("Erro Horizon:", e)

    return resultados

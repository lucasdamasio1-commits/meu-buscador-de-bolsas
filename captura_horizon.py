import requests

def capturar_horizon():
    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA"

    payload = {
        "bool": {
            "must": [
                {"terms": {"type": ["1"]}},        # Grants
                {"terms": {"status": ["31094501"]}} # Open calls
            ]
        }
    }

    print("Consultando API Horizon Europe...")

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()

        dados = response.json()
        chamadas = dados.get("results", [])

        resultados = []

        for call in chamadas:
            resultados.append({
                "title": call.get("title"),
                "deadline": call.get("deadline"),
                "link": f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/{call.get('identifier')}",
                "provider": "Horizon Europe",
                "description": call.get(
                    "description",
                    "Edital de pesquisa e inovação da União Europeia."
                )
            })

        print(f"✅ Recuperadas {len(resultados)} chamadas internacionais.")
        return resultados

    except Exception as e:
        print(f"❌ Erro Horizon: {e}")
        return []

import requests

def captura_horizon():
    print("Consultando Horizon Europe...")
    # A API exige o parâmetro 'text'. Usamos '***' para trazer todos os resultados
    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"
    params = {'apiKey': 'SEDIA', 'text': '***'}
    
    payload = {
        "bool": {
            "must": [
                { "terms": { "type": ["1"] } },
                { "terms": { "status": ["31094501"] } }
            ]
        }
    }
    
    try:
        response = requests.post(url, params=params, json=payload, timeout=30)
        response.raise_for_status()
        
        dados = response.json()
        chamadas = dados.get('results',)
        
        oportunidades =
        for call in chamadas:
            resultados.append({
                "titulo": call.get('title'), # Padronizado para seu script de embeddings
                "descricao": call.get('description', 'Edital internacional.'),
                "prazo": call.get('deadline'),
                "link": f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/{call.get('identifier')}",
                "origem": "Horizon Europe"
            })
        print(f"✅ Horizon Europe: {len(resultados)} recuperadas.")
        return resultados
    except Exception as e:
        print(f"⚠️ Erro Horizon: {e}")
        return

    return resultados



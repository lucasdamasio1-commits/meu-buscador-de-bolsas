import requests
import json

def capturar_horizon():
    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA"
    
    # Filtro para buscar apenas chamadas (Grants) de 2021-2027 que estão abertas [6]
    payload = {
        "bool": {
            "must": [
                { "terms": { "type": ["1"] } }, # Tipo 1 = Grants
                { "terms": { "status": ["31094501"] } } # Status 31094501 = Open
            ]
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    print("Consultando API Horizon Europe...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        dados = response.json()
        chamadas = dados.get('results',)
        
        resultados =
        for call in chamadas:
            resultados.append({
                "title": call.get('title'),
                "deadline": call.get('deadline'),
                "link": f"https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/{call.get('identifier')}",
                "provider": "Horizon Europe"
            })
        
        print(f"Recuperadas {len(resultados)} chamadas internacionais abertas.")
        return resultados
    else:
        print(f"Erro na API: {response.status_code}")
        return

if __name__ == "__main__":
    capturar_horizon()
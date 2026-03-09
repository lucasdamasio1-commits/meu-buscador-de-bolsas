import requests

def captura_horizon():
    print("Consultando Horizon Europe (API SEDIA)...")
    url = "https://api.tech.ec.europa.eu/search-api/prod/rest/search"
    
    # Adicionamos 'text': '***' para evitar o erro de 'parameter text is not present'
    params = {
        "apiKey": "SEDIA",
        "text": "***",
        "pageSize": 50,
        "pageNumber": 1
    }

    payload = {
        "bool": {
            "must": [
                { "terms": { "type": ["1"] } },        # Filtra apenas por Grants (Bolsas) [3, 1]
                { "terms": { "status": ["31094501", "31094502"] } } # Abertas e Em Breve
            ]
        }
    }

    try:
        response = requests.post(url, params=params, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        itens = data.get('results',)
        oportunidades =

        for item in itens:
            # Pegamos o código legível (ex: HORIZON-CL2-2024-...) [3, 4]
            identificador = item.get('identifier')
            if not identificador:
                continue
            
            # CONSTRUÇÃO DO LINK REAL:
            # Usamos a página de 'calls-for-proposals' filtrando pelo identificador exato
            link_oficial = (
                "https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/"
                f"calls-for-proposals?isExactMatch=true&keywords={identificador}"
            )

            oportunidades.append({
                "titulo": item.get("title", "Sem título"),
                "descricao": item.get("description", "Edital oficial de fomento à pesquisa da União Europeia."),
                "prazo": item.get("deadline"),
                "link": link_oficial,
                "origem": "Horizon Europe",
                "area": "Internacional / Europa"
            })

        print(f"✅ Horizon: {len(oportunidades)} oportunidades reais vinculadas.")
        return oportunidades

    except Exception as e:
        print(f"⚠️ Erro Horizon: {e}")
        return





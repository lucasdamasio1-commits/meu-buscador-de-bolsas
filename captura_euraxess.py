import requests
from bs4 import BeautifulSoup

def captura_euraxess():
    print("Capturando oportunidades globais (EURAXESS)...")
    # Filtro para jobs/funding em todas as áreas e países
    url = "https://euraxess.ec.europa.eu/jobs/search"
    oportunidades =
    
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        # Nota: O EURAXESS pode exigir Playwright se a página for muito dinâmica
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Localiza os blocos de resultados (ajustar conforme a estrutura atual)
        cards = soup.find_all('div', class_='views-row')
        
        for card in cards:
            titulo = card.find('h3').get_text().strip() if card.find('h3') else "Sem título"
            link = card.find('a')['href']
            
            oportunidades.append({
                "titulo": titulo,
                "descricao": "Oportunidade de pesquisa/fomento via rede EURAXESS (Pan-Europeia e Global).",
                "prazo": "Verificar no portal",
                "link": f"https://euraxess.ec.europa.eu{link}" if link.startswith('/') else link,
                "origem": "EURAXESS",
                "area": "Internacional"
            })
    except Exception as e:
        print(f"⚠️ Falha no EURAXESS: {e}")
        
    return oportunidades

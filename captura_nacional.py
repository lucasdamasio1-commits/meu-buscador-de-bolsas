import requests
from bs4 import BeautifulSoup

def captura_nacional():
    print("Capturando chamadas abertas do CNPq...")
    url = "https://www.gov.br/cnpq/pt-br/chamadas/abertas-para-submissao"
    
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        oportunidades = []
        # Procura pelos blocos de chamadas na página oficial
        links = soup.find_all('a', class_='internal-link')
        
        for link in links:
            titulo = link.get_text().strip()
            if "Chamada" in titulo or "Edital" in titulo:
                oportunidades.append({
                    "titulo": titulo,
                    "descricao": "Edital aberto para submissão de propostas.",
                    "prazo": "Veja no edital",
                    "link": link.get('href'),
                    "origem": "CNPq"
                })
        
        print(f"✅ CNPq: {len(resultados)} chamadas encontradas.")
        return oportunidades
    except Exception as e:
        print(f"⚠️ Erro ao acessar portal CNPq: {e}")
        return



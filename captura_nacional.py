import requests
from bs4 import BeautifulSoup

def captura_nacional():
    print("Capturando chamadas abertas do CNPq...")
    url = "https://www.gov.br/cnpq/pt-br/chamadas/abertas-para-submissao"
    
    # Trocamos 'resultados' por 'oportunidades' aqui
    oportunidades = 
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Procura pelos links de chamadas na página oficial
        links = soup.find_all('a', class_='internal-link')
        
        for link in links:
            titulo = link.get_text().strip()
            # Filtra para pegar apenas links que pareçam editais/chamadas
            if any(palavra in titulo.lower() for palavra in ["chamada", "edital", "bolsa"]):
                # Adicionamos à lista com o novo nome
                oportunidades.append({
                    "titulo": titulo,
                    "descricao": "Edital aberto para submissão de propostas no CNPq.",
                    "prazo": "Consultar edital",
                    "link": link.get('href'),
                    "origem": "CNPq"
                })
        
        print(f"✅ CNPq: {len(oportunidades)} chamadas encontradas.")
        
    except Exception as e:
        print(f"⚠️ Erro ao acessar portal CNPq: {e}")
    
    # Retornamos a lista com o novo nome
    return oportunidades

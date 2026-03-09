import requests
from bs4 import BeautifulSoup

def captura_fulbright():
    print("Capturando oportunidades da Fulbright Brasil...")
    url = "https://fulbright.org.br/bolsas-para-brasileiros/"
    oportunidades = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # O site organiza os itens em colunas de cards
        cards = soup.find_all('div', class_='col-md-4')

        for card in cards:
            try:
                # Localiza o título (geralmente em tags h3 ou h4)
                titulo_tag = card.find(['h3', 'h4'])
                if not titulo_tag:
                    continue

                titulo = titulo_tag.get_text().strip()
                link = card.find('a')['href'] if card.find('a') else url
                texto_card = card.get_text().strip()

                # Extrai a data prevista informada no texto
                prazo = "Consultar edital"
                if "Previsto para" in texto_card:
                    # Isola apenas a parte após "Previsto para"
                    partes = texto_card.split("Previsto para")
                    prazo = partes[-1].strip().split(".") # Pega o mês/ano antes do ponto final

                oportunidades.append({
                    "titulo": titulo,
                    "descricao": "Oportunidade Fulbright para brasileiros nos EUA (Cátedra, Pesquisa ou Ensino).",
                    "prazo": prazo,
                    "link": link,
                    "origem": "Fulbright Brasil",
                    "area": "Multidisciplinar"
                })
            except Exception:
                continue

        print(f"✅ Fulbright: {len(oportunidades)} itens (previstos/abertos) encontrados.")

    except Exception as e:
        print(f"⚠️ Erro ao acessar portal Fulbright: {e}")

    return oportunidades

if __name__ == "__main__":
    # Teste rápido de funcionamento
    res = captura_fulbright()
    for o in res:
        print(f"- {o['titulo']} ({o['prazo']})")

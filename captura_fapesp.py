from playwright.sync_api import sync_playwright

def capturar_fapesp():
    with sync_playwright() as p:
        # 1. Inicia o navegador (headless=True para rodar em segundo plano)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Acessando portal de oportunidades FAPESP...")
        page.goto("https://fapesp.br/oportunidades/")
        
        # 2. Aguarda o carregamento da lista de editais
        page.wait_for_selector(".oportunidade-item") # Seletor exemplo da lista
        
        # 3. Extrai dados de todos os blocos de oportunidade
        oportunidades =
        itens = page.query_selector_all(".oportunidade-item")
        
        for item in itens:
            titulo = item.query_selector("h2").inner_text()
            prazo = item.query_selector(".prazo").inner_text()
            link = item.query_selector("a").get_attribute("href")
            
            oportunidades.append({
                "title": titulo,
                "deadline": prazo,
                "link": f"https://fapesp.br{link}",
                "provider": "FAPESP"
            })
        
        browser.close()
        print(f"Encontradas {len(oportunidades)} novas oportunidades na FAPESP.")
        return oportunidades

if __name__ == "__main__":
    capturar_fapesp()
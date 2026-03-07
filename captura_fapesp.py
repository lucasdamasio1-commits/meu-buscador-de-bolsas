from playwright.sync_api import sync_playwright

def capturar_fapesp():
    oportunidades = # Inicialização corrigida
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            print("Acessando portal de oportunidades FAPESP...")
            page.goto("https://fapesp.br/oportunidades/", timeout=60000)
            
            # Aguarda carregar os itens dinâmicos 
            page.wait_for_selector(".oportunidade-item", timeout=10000)
            itens = page.query_selector_all(".oportunidade-item")
            
            for item in itens:
                titulo = item.query_selector("h2").inner_text()
                link = item.query_selector("a").get_attribute("href")
                oportunidades.append({
                    "title": titulo,
                    "provider": "FAPESP",
                    "link": f"https://fapesp.br{link}",
                    "description": "Bolsa vinculada a projeto de auxílio à pesquisa FAPESP."
                })
            browser.close()
        print(f"✅ Encontradas {len(oportunidades)} vagas na FAPESP.")
    except Exception as e:
        print(f"❌ Erro ao ler FAPESP: {e}")
    return oportunidades

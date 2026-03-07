from playwright.sync_api import sync_playwright

def capturar_fapesp():
    oportunidades = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            print("Acessando portal de oportunidades FAPESP...")
            page.goto("https://fapesp.br/oportunidades/", timeout=60000)

            page.wait_for_load_state("networkidle")
            page.wait_for_selector(".oportunidade", timeout=15000)

            itens = page.query_selector_all(".oportunidade")

            for item in itens:
                titulo_el = item.query_selector("h2")
                link_el = item.query_selector("a")

                titulo = titulo_el.inner_text().strip() if titulo_el else "Oportunidade FAPESP"
                link = link_el.get_attribute("href") if link_el else ""

                oportunidades.append({
                    "title": titulo,
                    "provider": "FAPESP",
                    "link": f"https://fapesp.br{link}" if link.startswith("/") else link,
                    "description": "Bolsa vinculada a projeto de auxílio à pesquisa FAPESP."
                })

            browser.close()

        print(f"✅ Encontradas {len(oportunidades)} vagas na FAPESP.")

    except Exception as e:
        print(f"❌ Erro ao ler FAPESP: {e}")

    return oportunidades

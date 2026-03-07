from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def captura_fapesp():

    print("Capturando FAPESP...")

    oportunidades = []

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://fapesp.br/oportunidades/", timeout=60000)
            page.wait_for_load_state("networkidle")

            html = page.content()

            soup = BeautifulSoup(html, "lxml")

            links = soup.find_all("a")

            for link in links:

                texto = link.get_text().lower()

                if any(p in texto for p in ["bolsa", "fellowship", "phd", "postdoc"]):

                    href = link.get("href")

                    if href:

                        oportunidades.append({
                            "title": link.get_text().strip(),
                            "provider": "FAPESP",
                            "link": href,
                            "description": "Oportunidade vinculada a projeto financiado pela FAPESP",
                            "deadline": None
                        })

            browser.close()

        print("FAPESP:", len(oportunidades))
        return oportunidades[:20]

    except Exception as e:

        print("Erro FAPESP:", e)
        return []

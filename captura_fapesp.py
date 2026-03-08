from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import time


# ------------------------------
# CARREGAMENTO DO MODELO DE IA
# ------------------------------

def carregar_modelo_ia():

    print("Carregando modelo de Inteligência Artificial...")

    modelo = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    print("Modelo carregado com sucesso.")

    return modelo


# ------------------------------
# CAPTURA DE OPORTUNIDADES FAPESP
# ------------------------------

def captura_fapesp(max_resultados=100):

    print("Capturando oportunidades da FAPESP...")

    oportunidades = []

    keywords = [
        "bolsa",
        "fellowship",
        "phd",
        "doutorado",
        "postdoc",
        "pesquisa"
    ]

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(
                "https://fapesp.br/oportunidades/",
                timeout=60000
            )

            page.wait_for_load_state("networkidle")

            html = page.content()

            soup = BeautifulSoup(html, "lxml")

            links = soup.find_all("a")

            for link in links:

                texto = link.get_text().strip()

                if not texto:
                    continue

                texto_lower = texto.lower()

                if any(k in texto_lower for k in keywords):

                    href = link.get("href")

                    if not href:
                        continue

                    if href.startswith("/"):
                        href = "https://fapesp.br" + href

                    oportunidades.append({
                        "title": texto,
                        "provider": "FAPESP",
                        "link": href,
                        "description": "Oportunidade vinculada a projeto financiado pela FAPESP.",
                        "deadline": None
                    })

            browser.close()

        # remover duplicatas simples
        vistos = set()
        oportunidades_unicas = []

        for o in oportunidades:

            if o["link"] not in vistos:
                vistos.add(o["link"])
                oportunidades_unicas.append(o)

        print(f"Total encontrado: {len(oportunidades_unicas)}")

        return oportunidades_unicas[:max_resultados]

    except Exception as e:

        print("Erro ao capturar FAPESP:", e)

        return []


# ------------------------------
# REMOVER DUPLICATAS COM IA
# ------------------------------

def remover_duplicatas_semanticas(oportunidades, modelo, threshold=0.85):

    print("Removendo duplicatas semânticas com IA...")

    titulos = [o["title"] for o in oportunidades]

    embeddings = modelo.encode(titulos)

    filtrados = []

    usados = set()

    for i in range(len(titulos)):

        if i in usados:
            continue

        filtrados.append(oportunidades[i])

        for j in range(i + 1, len(titulos)):

            similaridade = util.cos_sim(
                embeddings[i],
                embeddings[j]
            ).item()

            if similaridade > threshold:
                usados.add(j)

    print("Após filtragem IA:", len(filtrados))

    return filtrados


# ------------------------------
# EXECUÇÃO PRINCIPAL
# ------------------------------

if __name__ == "__main__":

    inicio = time.time()

    modelo = carregar_modelo_ia()

    oportunidades = captura_fapesp()

    oportunidades = remover_duplicatas_semanticas(
        oportunidades,
        modelo
    )

    print("\nExemplo de oportunidades:\n")

    for op in oportunidades[:10]:

        print(op["title"])
        print(op["link"])
        print()

    print("Tempo total:", round(time.time() - inicio, 2), "segundos")



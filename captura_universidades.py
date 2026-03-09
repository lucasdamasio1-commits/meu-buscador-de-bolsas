import requests
from bs4 import BeautifulSoup


def captura_universidades():

    print("Buscando oportunidades em universidades globais...")

    oportunidades = []

    urls = [

        "https://www.jobs.ac.uk/phd",
        "https://www.jobs.ac.uk/research",
        "https://academicpositions.com/jobs/phd",
        "https://academicpositions.com/jobs/postdoc",

    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:

        try:

            response = requests.get(url, headers=headers, timeout=30)

            soup = BeautifulSoup(response.content, "html.parser")

            for item in soup.find_all("h2"):

                titulo = item.get_text(strip=True)

                oportunidades.append({

                    "titulo": titulo,
                    "descricao": "Oportunidade acadêmica internacional",
                    "prazo": "Verificar portal",
                    "link": url,
                    "origem": "Universidades Globais",
                    "area": "Pesquisa"

                })

        except Exception as e:

            print("Erro ao consultar:", url, e)

    print("Universidades encontradas:", len(oportunidades))

    return oportunidades

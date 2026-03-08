import requests


def capturar_daad():

    print("Consultando DAAD...")

    url = "https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/"

    oportunidades = [{
        "titulo": "DAAD Scholarships Database",
        "instituicao": "DAAD",
        "area": "Diversas",
        "pais": "Alemanha",
        "link": url,
        "descricao": "Banco oficial de bolsas DAAD"
    }]

    return oportunidades

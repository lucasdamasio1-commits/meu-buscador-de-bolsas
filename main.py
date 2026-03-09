from captura_nacional import captura_nacional
from captura_fapesp import captura_fapesp
from captura_horizon import captura_horizon
from captura_daad import captura_daad
from captura_euraxess import captura_euraxess
from captura_fulbright import captura_fulbright

from salvar_scholarships import salvar_scholarships
from embeddings import gerar_embeddings

import datetime
import json


def executar():

    print("Iniciando coleta:", datetime.datetime.now())

    oportunidades = []

    # -------- FONTES NACIONAIS --------
    try:
        oportunidades.extend(captura_nacional() or [])
    except Exception as e:
        print("Erro captura_nacional:", e)

    try:
        oportunidades.extend(captura_fapesp() or [])
    except Exception as e:
        print("Erro FAPESP:", e)

    try:
        oportunidades.extend(captura_fulbright() or [])
    except Exception as e:
        print("Erro Fulbright:", e)

    # -------- FONTES INTERNACIONAIS --------
    try:
        oportunidades.extend(captura_horizon() or [])
    except Exception as e:
        print("Erro Horizon:", e)

    try:
        oportunidades.extend(captura_euraxess() or [])
    except Exception as e:
        print("Erro EURAXESS:", e)

    try:
        oportunidades.extend(captura_daad() or [])
    except Exception as e:
        print("Erro DAAD:", e)

    # -------- SALVAR RESULTADOS --------
    if oportunidades:

        salvar_scholarships(oportunidades)

        print("Dados enviados ao Supabase")
        print("Total capturado:", len(oportunidades))

        gerar_embeddings()

        with open("oportunidades.json", "w", encoding="utf-8") as f:
            json.dump(oportunidades, f, indent=2, ensure_ascii=False)

        print("Arquivo JSON salvo.")

    else:

        print("Nenhuma oportunidade encontrada.")


if __name__ == "__main__":
    executar()

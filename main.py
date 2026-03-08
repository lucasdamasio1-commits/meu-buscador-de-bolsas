from captura_nacional import captura_nacional
from captura_fapesp import captura_fapesp
from captura_horizon import captura_horizon
from captura_daad import captura_daad
from salvar_scholarships import salvar_scholarships
from embeddings import gerar_embeddings
import datetime

import datetime
import json

def executar():

    print("Iniciando coleta:", datetime.datetime.now())

    oportunidades = []

    oportunidades += captura_nacional()
    oportunidades += captura_fapesp()
    oportunidades += captura_horizon()
    oportunidades += captura_daad()
    
    salvar_scholarships(resultados)

    print("Dados enviados ao Supabase")
    print("Total capturado:", len(resultados))

    gerar_embeddings()

    with open("oportunidades.json","w",encoding="utf-8") as f:
        json.dump(oportunidades,f,indent=2,ensure_ascii=False)

    print("Arquivo salvo.")

if __name__ == "__main__":
    executar()









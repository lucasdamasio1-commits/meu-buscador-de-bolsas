from supabase_client import supabase
from embeddings import gerar_embedding


def salvar_scholarships(lista):

    for item in lista:

        titulo = item.get("title")
        descricao = item.get("description")

        embedding = gerar_embedding(titulo, descricao)

        data = {
            "title": titulo,
            "description": descricao,
            "provider": item.get("provider"),
            "link": item.get("link"),
            "deadline": item.get("deadline"),
            "embedding": embedding
        }

        supabase.table("scholarships").upsert(data).execute()

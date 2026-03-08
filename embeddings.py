from supabase import create_client
from sentence_transformers import SentenceTransformer
import os


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def gerar_embeddings():

    print("Gerando embeddings...")

    response = supabase.table("scholarships").select("*").execute()

    bolsas = response.data

    for bolsa in bolsas:

        texto = f"{bolsa['titulo']} {bolsa['descricao']}"

        embedding = model.encode(texto).tolist()

        supabase.table("scholarships") \
            .update({"embedding": embedding}) \
            .eq("id", bolsa["id"]) \
            .execute()

    print("Embeddings atualizados:", len(bolsas))

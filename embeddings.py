from sentence_transformers import SentenceTransformer

# modelo usado no dashboard
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def gerar_embedding(titulo, descricao):

    texto = f"{titulo} {descricao}"

    vetor = model.encode(texto)

    return vetor.tolist()

import os
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Inicializa o modelo de IA (384 dimensões)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def salvar_scholarships(oportunidades):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)

    print(f"Iniciando gravação de {len(oportunidades)} itens no banco...")

    for o in oportunidades:
        try:
            # Gerar embedding para busca semântica
            texto_para_ia = f"{o.get('titulo', '')} {o.get('descricao', '')}"
            vetor = model.encode(texto_para_ia).tolist()

            # MAPEAMENTO: De chaves Python para colunas do Banco
            dados_banco = {
                "title": o.get('titulo'),
                "description": o.get('descricao'),
                "deadline": o.get('prazo') if o.get('prazo') else None,
                "link": o.get('link'),
                "provider": o.get('origem'),
                "area": o.get('area'), # Agora a coluna existe no banco!
                "embedding": vetor
            }

            # Upsert usa o link como chave para não duplicar
            supabase.table("scholarships").upsert(dados_banco, on_conflict="link").execute()
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar item {o.get('titulo')}: {e}")

    print("✅ Processo de salvamento concluído.")

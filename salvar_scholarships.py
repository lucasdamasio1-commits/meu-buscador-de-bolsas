import os
import re
from supabase import create_client
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def salvar_scholarships(oportunidades):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)

    print(f"Iniciando gravação de {len(oportunidades)} itens no banco...")

    for o in oportunidades:
        titulo = o.get('titulo')
        link = o.get('link')
        
        # Filtro de segurança: ignora itens sem título ou links quebrados
        if not titulo or titulo == "None" or not link or "fapesp.br/Control/" in link:
            continue

        try:
            prazo_original = o.get('prazo', '')
            descricao = o.get('descricao', '')

            # Tratamento de Data: Se não for AAAA-MM-DD, move o texto para a descrição
            data_db = None
            if prazo_original and re.match(r'^\d{4}-\d{2}-\d{2}$', str(prazo_original)):
                data_db = prazo_original
            elif prazo_original:
                descricao = f"{descricao} | Prazo: {prazo_original}"

            # Gera inteligência para o dashboard
            texto_para_ia = f"{titulo} {descricao}"
            vetor = model.encode(texto_para_ia).tolist()

            dados_banco = {
                "title": titulo,
                "description": descricao,
                "deadline": data_db,
                "link": link,
                "provider": o.get('origem'),
                "area": o.get('area'),
                "embedding": vetor
            }

            # Upsert evita duplicados usando o link como chave única [5]
            supabase.table("scholarships").upsert(dados_banco, on_conflict="link").execute()
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar item '{titulo}': {e}")

    print("✅ Processo de salvamento concluído.")

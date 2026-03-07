import os
import re
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Importa as funções que você criou nos passos anteriores
from captura_nacional import capturar_nacional
from captura_fapesp import capturar_fapesp
from captura_horizon import capturar_horizon

load_dotenv()

# Inicializa o banco e o modelo de IA
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # Modelo leve e multilíngue 

def limpar_texto(texto):
    if not texto: return ""
    # Remove tags HTML (ex: <p>, <br>) [1]
    texto_limpo = re.sub(r'<[^>]+>', '', texto)
    return texto_limpo.strip()

def processar_e_salvar(lista_oportunidades):
    for item in lista_oportunidades:
        # 1. Limpeza e Padronização
        titulo = limpar_texto(item.get('title'))
        descricao = limpar_texto(item.get('description', ''))
        
        # 2. Geração do Embedding (Vetor para busca semântica) 
        texto_para_ia = f"{titulo} {descricao}"
        vetor = model.encode(texto_para_ia).tolist()
        
        # 3. Envio para o Supabase (Upsert evita duplicados usando o Link como chave) 
        dados = {
            "title": titulo,
            "description": descricao,
            "deadline": item.get('deadline'),
            "provider": item.get('provider'),
            "link": item.get('link'),
            "embedding": vetor
        }
        supabase.table("scholarships").upsert(dados, on_conflict="link").execute()

def executar_tudo():
    print(f"--- Início do processamento: {datetime.now()} ---")
    
    # Executa cada capturador
    dados_nacionais = capturar_nacional()
    processar_e_salvar(dados_nacionais)
    
    dados_fapesp = capturar_fapesp()
    processar_e_salvar(dados_fapesp)
    
    dados_horizon = capturar_horizon()
    processar_e_salvar(dados_horizon)
    
    print("--- Processamento concluído com sucesso! ---")

if __name__ == "__main__":
    executar_tudo()
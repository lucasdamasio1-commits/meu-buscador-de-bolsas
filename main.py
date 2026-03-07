import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

# 1. Ajuste de Caminho (Garante que o Python encontre seus outros arquivos.py)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa as funções dos seus outros arquivos
from captura_nacional import capturar_nacional
from captura_fapesp import capturar_fapesp
from captura_horizon import capturar_horizon

# Carrega as chaves do arquivo.env (local) ou do ambiente (GitHub)
load_dotenv()

# 2. Configurações Iniciais
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY") # Lembre-se: use a 'service_role key' aqui

if not URL or not KEY:
    print("❌ Erro: Chaves do Supabase não encontradas!")
    sys.exit(1)

supabase = create_client(URL, KEY)

# Inicializa o modelo de IA (384 dimensões)
print("Carregando modelo de Inteligência Artificial...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def limpar_texto(texto):
    """Remove tags HTML e espaços extras para melhorar a busca da IA."""
    if not texto:
        return ""
    # Remove tags como <p>, <br>, etc 
    texto_limpo = re.sub(r'<[^>]+>', '', str(texto))
    return texto_limpo.strip()

def processar_e_salvar(oportunidades, agência_nome):
    """Gera vetores e salva os dados na tabela 'scholarships'."""
    if not oportunidades:
        print(f"⚠️ Nenhuma oportunidade nova para {agência_nome}.")
        return

    print(f"Processando {len(oportunidades)} itens de {agência_nome}...")
    
    for item in oportunidades:
        try:
            # Limpeza
            titulo = limpar_texto(item.get('title', 'Sem título'))
            descricao = limpar_texto(item.get('description', 'Sem descrição'))
            link = item.get('link')
            prazo = item.get('deadline')

            # Geração do Embedding (Vetor numérico que a IA usa para 'entender' o contexto)
            texto_para_ia = f"{titulo}. {descricao}"
            vetor = model.encode(texto_para_ia).tolist()

            # Montagem do dado para o banco
            payload = {
                "title": titulo,
                "description": descricao,
                "deadline": prazo if prazo else None,
                "provider": item.get('provider', agência_nome),
                "link": link,
                "embedding": vetor
            }

            # Envio (Upsert: insere se for novo, atualiza se o link já existir) 
            supabase.table("scholarships").upsert(payload, on_conflict="link").execute()
            
        except Exception as e:
            print(f"❌ Erro ao salvar item '{item.get('title')}': {e}")

def executar_sistema():
    start_time = datetime.now()
    print(f"\n--- Início do Ciclo de Atualização: {start_time.strftime('%d/%m/%Y %H:%M:%S')} ---")

    # Executa cada capturador individualmente
    try:
        dados_br = capturar_nacional()
        processar_e_salvar(dados_br, "Nacional (CNPq/CAPES)")

        dados_fapesp = capturar_fapesp()
        processar_e_salvar(dados_fapesp, "FAPESP")

        dados_eu = capturar_horizon()
        processar_e_salvar(dados_eu, "Horizon Europe")

    except Exception as e:
        print(f"💥 Erro crítico durante a execução: {e}")

    end_time = datetime.now()
    print(f"--- Ciclo Finalizado com sucesso em {end_time - start_time} ---")

if __name__ == "__main__":
    executar_sistema()

import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer
import os

# 1. Configuração Inicial
st.set_page_config(page_title="Buscador de Bolsas", layout="wide", page_icon="🎓")

# 2. Conexão Segura com Supabase
@st.cache_resource
def init_connection():
    # Tenta buscar primeiro no Streamlit Cloud (Secrets)
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    
    # Se não encontrar, tenta buscar localmente no.env
    if not url or not key:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
    if not url or not key:
        st.error("Credenciais do Supabase não encontradas. Configure os 'Secrets' no Streamlit.")
        st.stop()
        
    return create_client(url, key)

supabase = init_connection()

# 3. Modelo de IA
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()

# 4. Interface do Usuário
st.title("🎓 Oportunidades de Bolsa de Pesquisa")

query = st.text_input("Descreva o que você procura (ex: Doutorado em Administração na Europa)")

if query:
    # Busca Semântica via IA
    query_vector = model.encode(query).tolist()
    res = supabase.rpc('match_documents', {
        'query_embedding': query_vector,
        'match_threshold': 0.4,
        'match_count': 10
    }).execute()
    dados = res.data
else:
    # Mostra as mais recentes por padrão
    res = supabase.table("scholarships").select("*").order("deadline", desc=False).limit(15).execute()
    dados = res.data

# 5. Exibição
if not dados:
    st.info("Nenhuma bolsa encontrada para esta busca.")
else:
    for item in dados:
        with st.expander(f"{item['title']} - {item['provider']}"):
            st.write(f"**Prazo:** {item['deadline']}")
            st.write(item['description'])
            st.link_button("Ver Edital", item['link'])


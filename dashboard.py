import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer
import os

# 1. Configuração da Página
st.set_page_config(page_title="Buscador de Bolsas", layout="wide", page_icon="🎓")

# 2. Conexão com o Supabase
@st.cache_resource
def init_connection():
    # Tenta carregar do Render/Streamlit Cloud (Secrets)
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    
    # Fallback para local
    if not url or not key:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
    return create_client(url, key)

supabase = init_connection()

# 3. Carregar Modelo de IA
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()

# 4. Interface Principal
st.title("🎓 Oportunidades de Bolsa de Pesquisa")

# Barra lateral com métrica de total
res_count = supabase.table("scholarships").select("id", count="exact").execute()
total_no_banco = res_count.count if res_count.count else 0
st.sidebar.metric("Total de Bolsas no Banco", total_no_banco)

query = st.text_input("Busca por Perfil (ex: Doutorado em IA ou Biotecnologia)")

# 5. Lógica de busca e exibição
if query:
    # Busca Semântica
    query_vector = model.encode(query).tolist()
    res = supabase.rpc('match_documents', {
        'query_embedding': query_vector,
        'match_threshold': 0.1, # Menor rigidez para mostrar mais resultados 
        'match_count': 200      # Aumentamos o limite para 200 itens
    }).execute()
    dados = res.data
else:
    # MOSTRA TUDO (Removido o.limit(15))
    res = supabase.table("scholarships").select("*").order("deadline", desc=False).execute()
    dados = res.data

# 6. Exibição dos resultados
if not dados:
    st.info("Nenhuma bolsa encontrada.")
else:
    st.write(f"Exibindo **{len(dados)}** resultados:")
    for item in dados:
        with st.expander(f"📌 {item['title']} | {item.get('provider', item.get('origem', 'N/A'))}"):
            st.write(f"**Área:** {item.get('area', 'Não informada')}")
            st.write(f"**Prazo:** {item['deadline'] or 'Consultar edital'}")
            st.write(item['description'])
            st.link_button("Ver Edital Completo", item['link'])

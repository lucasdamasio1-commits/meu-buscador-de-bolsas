import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Configuração da página
st.set_page_config(page_title="Buscador de Bolsas", layout="wide")
st.title("🎓 Oportunidades de Bolsa de Pesquisa")

# Conexão com banco
@st.cache_resource
def init_connection():
    return create_client(st.secrets, st.secrets)

supabase = init_connection()
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Barra lateral para filtros tradicionais
st.sidebar.header("Filtros")
provider = st.sidebar.multiselect("Agência",)

# Busca Semântica (A "Inteligência" do projeto)
query = st.text_input("Descreva seu perfil (ex: Doutorado em Genética ou IA aplicada à saúde)")

if query:
    # Gera o vetor da pergunta do usuário
    query_vector = model.encode(query).tolist()
    
    # Chama a função de busca no banco (RPC)
    res = supabase.rpc('match_documents', {
        'query_embedding': query_vector,
        'match_threshold': 0.5,
        'match_count': 10
    }).execute()
    dados = res.data
else:
    # Mostra as mais recentes se não houver busca
    res = supabase.table("scholarships").select("*").order("deadline").limit(20).execute()
    dados = res.data

# Exibição dos resultados
for item in dados:
    with st.expander(f"{item['title']} - Prazo: {item['deadline']}"):
        st.write(item['description'])
        st.link_button("Ver Edital Completo", item['link'])
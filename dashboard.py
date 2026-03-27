import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer
import os

st.set_page_config(page_title="Buscador de Bolsas", layout="wide", page_icon="🎓")

@st.cache_resource
def init_connection():
    url = None
    key = None

    if "SUPABASE_URL" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

    if not url or not key:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("Supabase não configurado.")
        st.stop()

    return create_client(url, key)

supabase = init_connection()

@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()

st.title("🎓 Oportunidades de Bolsa de Pesquisa")

query = st.text_input("Descreva o que você procura")

if query:
    query_vector = model.encode(query).tolist()

    res = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_vector,
            'match_threshold': 0.4,
            'match_count': 10
        }
    ).execute()

    dados = res.data
else:
    res = supabase.table("scholarships").select("*").limit(10).execute()
    dados = res.data

if not dados:
    st.info("Nenhum resultado encontrado.")
else:
    for item in dados:
        with st.expander(item["title"]):
            st.write(item["description"])

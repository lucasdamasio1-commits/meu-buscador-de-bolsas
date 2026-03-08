import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer
import os

# ------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ------------------------------------------------

st.set_page_config(
    page_title="Buscador de Bolsas",
    layout="wide",
    page_icon="🎓"
)

# ------------------------------------------------
# 2. CONEXÃO SEGURA COM SUPABASE
# ------------------------------------------------

@st.cache_resource
def init_connection():

    url = None
    key = None

    # tenta pegar primeiro dos Secrets do Streamlit
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
    except:
        pass

    # fallback para .env local
    if not url or not key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
        except:
            pass

    if not url or not key:
        st.error(
            "Credenciais do Supabase não encontradas. "
            "Configure SUPABASE_URL e SUPABASE_KEY nos Secrets do Streamlit."
        )
        st.stop()

    return create_client(url, key)


supabase = init_connection()

# ------------------------------------------------
# 3. MODELO DE IA PARA BUSCA SEMÂNTICA
# ------------------------------------------------

@st.cache_resource
def load_model():

    model = SentenceTransformer(
        "paraphrase-multilingual-MiniLM-L12-v2"
    )

    return model


model = load_model()

# ------------------------------------------------
# 4. INTERFACE DO USUÁRIO
# ------------------------------------------------

st.title("🎓 Oportunidades de Bolsa de Pesquisa")

st.write(
    "Pesquise oportunidades acadêmicas usando linguagem natural."
)

query = st.text_input(
    "Descreva o que você procura (ex: Doutorado em Biologia na Europa)"
)

# ------------------------------------------------
# 5. BUSCA
# ------------------------------------------------

dados = []

try:

    if query:

        # vetor da consulta
        query_vector = model.encode(query).tolist()

        # busca semântica
        res = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_vector,
                "match_threshold": 0.4,
                "match_count": 10
            }
        ).execute()

        dados = res.data

    else:

        # mostra bolsas mais próximas do deadline
        res = (
            supabase
            .table("scholarship")
            .select("*")
            .order("deadline", desc=False)
            .limit(15)
            .execute()
        )

        dados = res.data

except Exception as e:

    st.error("Erro ao consultar o banco de dados.")
    st.exception(e)

# ------------------------------------------------
# 6. EXIBIÇÃO DOS RESULTADOS
# ------------------------------------------------

if not dados:

    st.info("Nenhuma bolsa encontrada para esta busca.")

else:

    st.write(f"🔎 {len(dados)} oportunidades encontradas")

    for item in dados:

        titulo = item.get("title", "Sem título")
        provider = item.get("provider", "Instituição desconhecida")

        with st.expander(f"{titulo} — {provider}"):

            deadline = item.get("deadline", "Não informado")
            description = item.get("description", "")
            link = item.get("link", "")

            st.write(f"**Prazo:** {deadline}")

            if description:
                st.write(description)

            if link:
                st.link_button("Ver Edital", link)

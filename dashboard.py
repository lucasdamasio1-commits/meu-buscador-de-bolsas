import streamlit as st
from supabase import create_client
import os
import pandas as pd

# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------

st.set_page_config(
    page_title="Buscador de Bolsas",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Encontre oportunidades de bolsas de pesquisa")

st.write("Oportunidades coletadas automaticamente de agências de fomento.")

# -----------------------------
# CONEXÃO COM SUPABASE
# -----------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# BUSCAR DADOS
# -----------------------------

@st.cache_data
def carregar_dados():

    response = supabase.table("scholarship").select("*").execute()

    if response.data:
        return pd.DataFrame(response.data)
    else:
        return pd.DataFrame()

df = carregar_dados()

# -----------------------------
# SE NÃO HOUVER DADOS
# -----------------------------

if df.empty:
    st.warning("Nenhuma oportunidade encontrada no banco de dados.")
    st.stop()

# -----------------------------
# FILTRO DE BUSCA
# -----------------------------

busca = st.text_input("🔎 Buscar por palavra-chave")

if busca:
    df = df[
        df["title"].str.contains(busca, case=False, na=False) |
        df["description"].str.contains(busca, case=False, na=False)
    ]

# -----------------------------
# FILTRO POR PROVEDOR
# -----------------------------

provedores = df["provider"].dropna().unique()

filtro_provedor = st.selectbox(
    "Filtrar por instituição",
    ["Todos"] + list(provedores)
)

if filtro_provedor != "Todos":
    df = df[df["provider"] == filtro_provedor]

# -----------------------------
# ORDENAR POR DEADLINE
# -----------------------------

if "deadline" in df.columns:
    df = df.sort_values("deadline")

# -----------------------------
# MOSTRAR RESULTADOS
# -----------------------------

st.write(f"📊 {len(df)} oportunidades encontradas")

for _, row in df.iterrows():

    with st.container():

        st.subheader(row["title"])

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"🏛 **Instituição:** {row['provider']}")

        with col2:
            st.write(f"📅 **Deadline:** {row['deadline']}")

        st.write(row["description"])

        if row["link"]:
            st.link_button("Abrir edital", row["link"])

        st.divider()


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
# ==========================
# 📥 Leitura do CSV otimizado
# ==========================
df = pd.read_csv("planilha_cassino.csv", parse_dates=["data"])
df["dia_da_semana"] = df["data"].dt.day_name(locale='pt_BR')
df["fim_de_semana"] = df["data"].dt.weekday >= 5

# ==========================
# 🎛️ Filtros laterais
# ==========================
st.sidebar.header("🎯 Filtros")

# Filtro por intervalo de data
data_min = df["data"].min()
data_max = df["data"].max()
data_range = st.sidebar.date_input("📅 Intervalo de Datas", [data_min, data_max], min_value=data_min, max_value=data_max)

# Filtros suspensos (todos selecionados por padrão)
todos_fornecedores = df["fornecedor"].dropna().unique().tolist()
fornecedores = st.sidebar.multiselect("🧪 Provedor", todos_fornecedores, default=todos_fornecedores)

todos_tipos = df["tipo"].dropna().unique().tolist()
tipos = st.sidebar.multiselect("🎲 Tipo de Jogo", todos_tipos, default=todos_tipos)

todos_jogos = df["jogo"].dropna().unique().tolist()
jogos = st.sidebar.multiselect("🕹️ Jogo", todos_jogos, default=todos_jogos)



# ==========================
# 🔍 Aplicação de filtros
# ==========================
df_filtrado = df[
    (df["data"] >= pd.to_datetime(data_range[0])) &
    (df["data"] <= pd.to_datetime(data_range[1])) &
    (df["fornecedor"].isin(fornecedores)) &
    (df["tipo"].isin(tipos)) &
    (df["jogo"].isin(jogos))
]

# ==========================
# 🎯 KPIs principais
# ==========================
st.markdown("""
    <h1 style='text-align: center;'>🎰 Painel de Análise de GGR - Cassino</h1>
""", unsafe_allow_html=True)



ggr_por_data = df_filtrado.groupby("data")["ggr"].sum().reset_index()

if not ggr_por_data.empty:
    melhor_dia = ggr_por_data.loc[ggr_por_data["ggr"].idxmax()]
    pior_dia = ggr_por_data.loc[ggr_por_data["ggr"].idxmin()]
else:
    melhor_dia = {"data": "-", "ggr": 0}
    pior_dia = {"data": "-", "ggr": 0}
import streamlit as st

import streamlit as st
import pandas as pd

# Exemplo: definindo df_filtrado
# df_filtrado = pd.read_csv('seu_arquivo.csv') # ou seu dataframe já filtrado

total_jogadores = df_filtrado["jogador_id"].nunique()
ggr_total = df_filtrado["ggr"].sum()
total_apostado = df_filtrado["aposta"].sum()
total_ganho = df_filtrado["ganho"].sum()

# CSS para os cartões
st.markdown(
    """
    <style>
    .card-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        background: #fff;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgb(0 0 0 / 0.1);
        flex: 1;
        min-width: 200px;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .card-icon {
        flex-shrink: 0;
        width: 40px;
        height: 40px;
        color: #1a237e; /* azul escuro */
    }
    .card-content {
        display: flex;
        flex-direction: column;
    }
    .card-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a237e;
    }
    .card-label {
        font-size: 0.85rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Ícones SVG atualizados conforme pedido
icon_players = """
<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
  <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2 0-6 1-6 3v2h12v-2c0-2-4-3-6-3zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 2.02 1.97 3.45v2h6v-2c0-2-4-3-6-3z"/>
</svg>
"""

icon_cofre = """
<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
  <path d="M20 7h-1V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v2H4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zM7 5h10v2H7V5zm13 10H4v-6h16v6zM12 9a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/>
</svg>
"""

icon_notas = """
<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
  <path d="M20 6H4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zm0 10H4v-8h16v8zm-7-7h-2v2h2v-2zm0 4h-2v2h2v-2z"/>
</svg>
"""

icon_seta_baixo = """
<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
  <path d="M7 10l5 5 5-5H7z"/>
</svg>
"""

def format_brl(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

cards_html = f"""
<div class="card-container">
  <div class="card">
    <div class="card-icon">{icon_players}</div>
    <div class="card-content">
      <div class="card-value">{total_jogadores:,}</div>
      <div class="card-label">TOTAL JOGADORES</div>
    </div>
  </div>
  <div class="card">
    <div class="card-icon">{icon_cofre}</div>
    <div class="card-content">
      <div class="card-value">R$ {format_brl(ggr_total)}</div>
      <div class="card-label">GGR - RECEITA BRUTA</div>
    </div>
  </div>
  <div class="card">
    <div class="card-icon">{icon_notas}</div>
    <div class="card-content">
      <div class="card-value">R$ {format_brl(total_apostado)}</div>
      <div class="card-label">TOTAL APOSTADO</div>
    </div>
  </div>
  <div class="card">
    <div class="card-icon">{icon_seta_baixo}</div>
    <div class="card-content">
      <div class="card-value">R$ {format_brl(total_ganho)}</div>
      <div class="card-label">GANHO DOS JOGADORES</div>
    </div>
  </div>
</div>
"""

st.markdown(cards_html, unsafe_allow_html=True)





# ==========================
# 📈 Gráficos
# ==========================

# Evolução diária do GGR
st.subheader("📆 Evolução Diária do GGR")
fig = px.line(ggr_por_data, x="data", y="ggr", title="GGR Diário", markers=True)
fig.update_layout(xaxis_title="Data", yaxis_title="GGR (R$)", height=400)
st.plotly_chart(fig, use_container_width=True)


import plotly.express as px

# ==========================
# 🧾 Tabelas de insights em Plotly com valores
# ==========================

import plotly.express as px

# ==========================
# 🧾 Tabelas de insights em Plotly com valores
# ==========================

col1, col2, col3 = st.columns(3)

# ❌ 10 Piores Fornecedores (menor GGR)
piores_provedores = df_filtrado.groupby("fornecedor")["ggr"].sum().sort_values().head(10).reset_index()
fig_piores = px.bar(
    piores_provedores,
    x="ggr",
    y="fornecedor",
    orientation="h",
    text="ggr",
    title="❌ 10 Piores Fornecedores (GGR)",
    labels={"ggr": "GGR", "fornecedor": "Fornecedor"},
    template="simple_white"
)
fig_piores.update_traces(marker_color="#e53935", texttemplate='R$ %{text:,.2f}', textposition='outside')
fig_piores.update_layout(height=400, yaxis_title=None)

with col1:
    st.plotly_chart(fig_piores, use_container_width=True)

# 🎮 Top 5 Jogos no Fim de Semana
top_jogos_fds = df_filtrado[df_filtrado["fim_de_semana"]].groupby("jogo").size().sort_values(ascending=False).head(5).reset_index(name="qtd_jogadas")
fig_jogos = px.bar(
    top_jogos_fds,
    x="jogo",
    y="qtd_jogadas",
    text="qtd_jogadas",
    title="🎮 Top 5 Jogos no Fim de Semana",
    labels={"jogo": "Jogo", "qtd_jogadas": "Qtd. Jogadas"},
    template="simple_white"
)
fig_jogos.update_traces(marker_color="#1e88e5", texttemplate='%{text}', textposition='outside')
fig_jogos.update_layout(height=400, xaxis_tickangle=-45)

with col3:
    st.plotly_chart(fig_jogos, use_container_width=True)

# ✅ Top 10 Melhores Fornecedores (maior GGR - ordem decrescente de cima pra baixo)
melhores_provedores = df_filtrado.groupby("fornecedor")["ggr"].sum().sort_values(ascending=False).head(10).reset_index()
fig_melhores = px.bar(
    melhores_provedores,
    x="ggr",
    y="fornecedor",
    orientation="h",
    text="ggr",
    title="✅ Top 10 Melhores Fornecedores (GGR)",
    labels={"ggr": "GGR", "fornecedor": "Fornecedor"},
    template="simple_white"
)
fig_melhores.update_traces(marker_color="#43a047", texttemplate='R$ %{text:,.2f}', textposition='outside')
fig_melhores.update_layout(
    height=400,
    yaxis=dict(categoryorder="total ascending"),  # inverte para cima = maior
    yaxis_title=None
)

with col2:
    st.plotly_chart(fig_melhores, use_container_width=True)



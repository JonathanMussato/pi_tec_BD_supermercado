
import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def formatar_moeda(valor):
    numero = f"{valor:,.2f}"
    numero = numero.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"US$ {numero}"

# --------------------------------------------------
# CONFIGURAÇÕES DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# CARREGAMENTO DOS DADOS
# --------------------------------------------------

caminho_csv = (
    Path(__file__).parent
    / "dataset"
    / "SuperMarket Analysis.csv"
)

@st.cache_data
def carregar_dados():
    dados = pd.read_csv(caminho_csv)

    dados['Date'] = pd.to_datetime(
        dados['Date'],
        errors='coerce'
    )

    dados['Hour'] = pd.to_datetime(
        dados['Time'],
        format='%I:%M:%S %p',
        errors='coerce'
    ).dt.hour

    return dados


df = carregar_dados()

# --------------------------------------------------
# TREINAMENTO DO K-MEANS
# --------------------------------------------------

X = df[['Quantity', 'Sales']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

modelo = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

df['Cluster'] = modelo.fit_predict(X_scaled).astype(str)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("📊 Dashboard de Vendas")
st.caption("Análise de dados do supermercado")

st.divider()


# --------------------------------------------------
# FILTROS LATERAIS
# --------------------------------------------------

st.sidebar.header("Filtros")

# Período
data_inicial = df['Date'].min().date()
data_final = df['Date'].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)

# Filial
filiais = sorted(df['Branch'].dropna().unique())

filiais_selecionadas = st.sidebar.multiselect(
    "Filial",
    options=filiais,
    default=filiais
)

# Categoria
categorias = sorted(df['Product line'].dropna().unique())

categorias_selecionadas = st.sidebar.multiselect(
    "Categoria",
    options=categorias,
    default=categorias
)

# Forma de pagamento
pagamentos = sorted(df['Payment'].dropna().unique())

pagamentos_selecionados = st.sidebar.multiselect(
    "Forma de pagamento",
    options=pagamentos,
    default=pagamentos
)


# --------------------------------------------------
# APLICAÇÃO DOS FILTROS
# --------------------------------------------------

df_filtrado = df.copy()

if len(periodo) == 2:

    df_filtrado = df_filtrado[
        (df_filtrado['Date'].dt.date >= periodo[0]) &
        (df_filtrado['Date'].dt.date <= periodo[1])
    ]

df_filtrado = df_filtrado[
    df_filtrado['Branch'].isin(filiais_selecionadas)
]

df_filtrado = df_filtrado[
    df_filtrado['Product line'].isin(categorias_selecionadas)
]

df_filtrado = df_filtrado[
    df_filtrado['Payment'].isin(pagamentos_selecionados)
]


# --------------------------------------------------
# INDICADORES
# --------------------------------------------------

if df_filtrado.empty:

    st.warning("Não existem dados para os filtros selecionados.")

    st.stop()


faturamento = df_filtrado['Sales'].sum()

transacoes = df_filtrado['Invoice ID'].nunique()

ticket_medio = df_filtrado['Sales'].mean()

avaliacao = df_filtrado['Rating'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Faturamento total",
    formatar_moeda(faturamento)
)

col2.metric(
    "Transações",
    f"{transacoes:,}"
)

col3.metric(
    "Ticket médio",
    formatar_moeda(ticket_medio)
)

col4.metric(
    "Avaliação média",
    f"{avaliacao:.2f}"
)


st.divider()


# --------------------------------------------------
# GRÁFICOS - VENDAS
# --------------------------------------------------

st.subheader("Análise de vendas")

col1, col2 = st.columns(2)


# Faturamento por categoria
with col1:

    vendas_categoria = (
        df_filtrado
        .groupby('Product line', as_index=False)['Sales']
        .sum()
        .sort_values('Sales', ascending=False)
    )

    fig1 = px.bar(
        vendas_categoria,
        x='Product line',
        y='Sales',
        title='Faturamento por categoria',
        labels={
            'Product line': 'Categoria',
            'Sales': 'Faturamento'
        },
        color='Sales',
        color_continuous_scale='Blues'
    )

    fig1.update_traces(
        hovertemplate=(
            "<b>Categoria:</b> %{x}<br>"
            "<b>Faturamento:</b> US$ %{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig1.update_layout(
        xaxis_title=None,
        yaxis_title='Faturamento (US$)',
        coloraxis_showscale=False
    )

    st.plotly_chart(fig1, use_container_width=True)


# Faturamento por filial
with col2:

    vendas_filial = (
        df_filtrado
        .groupby('Branch', as_index=False)['Sales']
        .sum()
    )

    fig2 = px.bar(
        vendas_filial,
        x='Branch',
        y='Sales',
        title='Faturamento por filial',
        labels={
            'Branch': 'Filial',
            'Sales': 'Faturamento'
        },
        color='Branch'
    )

    fig2.update_traces(
        hovertemplate=(
            "<b>Filial:</b> %{x}<br>"
            "<b>Faturamento:</b> US$ %{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig2.update_layout(
        xaxis_title='Filial',
        yaxis_title='Faturamento (US$)'
    )

    st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# GRÁFICOS - COMPORTAMENTO DAS VENDAS
# --------------------------------------------------

st.subheader("Comportamento das vendas")

col1, col2 = st.columns(2)


# Vendas por horário
with col1:

    vendas_horario = (
        df_filtrado
        .groupby('Hour')
        .size()
        .reset_index(name='Transações')
    )

    fig3 = px.bar(
        vendas_horario,
        x='Hour',
        y='Transações',
        title='Quantidade de vendas por horário',
        labels={
            'Hour': 'Horário',
            'Transações': 'Transações'
        }
    )

    fig3.update_traces(
        hovertemplate=(
            "<b>Horário:</b> %{x}h<br>"
            "<b>Transações:</b> %{y:,.0f}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig3, use_container_width=True)


# Formas de pagamento
with col2:

    vendas_pagamento = (
        df_filtrado['Payment']
        .value_counts()
        .rename_axis('Payment')
        .reset_index(name='Transações')
    )

    fig4 = px.pie(
        vendas_pagamento,
        names='Payment',
        values='Transações',
        title='Formas de pagamento',
        hole=0.4
    )

    fig4.update_traces(
        hovertemplate=(
            "<b>Pagamento:</b> %{label}<br>"
            "<b>Transações:</b> %{value:,.0f}<br>"
            "<b>Participação:</b> %{percent:.1%}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig4, use_container_width=True)


# --------------------------------------------------
# AVALIAÇÃO DOS CLIENTES
# --------------------------------------------------

st.subheader("Avaliação dos produtos")

avaliacoes = (
    df_filtrado
    .groupby('Product line', as_index=False)['Rating']
    .mean()
    .sort_values('Rating', ascending=False)
)

fig5 = px.bar(
    avaliacoes,
    x='Product line',
    y='Rating',
    title='Avaliação média por categoria',
    labels={
        'Product line': 'Categoria',
        'Rating': 'Avaliação média'
    },
    color='Rating',
    color_continuous_scale='Blues'
)

fig5.update_traces(
    hovertemplate=(
        "<b>Categoria:</b> %{x}<br>"
        "<b>Avaliação média:</b> %{y:.2f}"
        "<extra></extra>"
    )
)

fig5.update_layout(
    coloraxis_showscale=False
)

st.plotly_chart(fig5, use_container_width=True)


# --------------------------------------------------
# APRENDIZADO DE MÁQUINA - K-MEANS
# --------------------------------------------------

st.divider()

st.subheader("Agrupamento de transações - K-Means")

st.write(
    """
    O algoritmo K-Means foi utilizado para agrupar as transações
    considerando a quantidade de produtos e o valor das vendas.
    O objetivo é identificar grupos com características semelhantes.
    """
)

df_clusters = df_filtrado.copy()


fig6 = px.scatter(
    df_clusters,
    x='Quantity',
    y='Sales',
    color='Cluster',
    title='Agrupamento das transações',
    labels={
        'Quantity': 'Quantidade de produtos',
        'Sales': 'Valor da venda (US$)',
        'Cluster': 'Grupo'
    },
    hover_data=['Branch', 'Product line']
)

fig6.update_traces(
    hovertemplate=(
        "<b>Cluster:</b> %{fullData.name}<br>"
        "<b>Quantidade:</b> %{x:.0f} produtos<br>"
        "<b>Valor da compra:</b> US$ %{y:,.2f}<br>"
        "<b>Filial:</b> %{customdata[0]}<br>"
        "<b>Categoria:</b> %{customdata[1]}"
        "<extra></extra>"
    )
)

st.plotly_chart(fig6, use_container_width=True)

st.caption(
    "Os grupos representam perfis de transações, "
    "não perfis individuais de clientes."
)



# --------------------------------------------------
# RODAPÉ
# --------------------------------------------------

st.divider()

st.caption(
    "Projeto Integrador - Análise de Dados de Supermercado"
)

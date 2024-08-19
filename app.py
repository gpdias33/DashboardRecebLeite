import streamlit as st
import pandas as pd
import plotly.express as px


# Definindo os dados.
df = pd.read_csv("RecebimentoLeite-2007-Formatado.csv", sep=";", decimal='.')
df["data"] = pd.to_datetime(df["data"])
df=df.sort_values("data")

df["Month"] = df["data"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Definindo a página
st.set_page_config(layout="wide", )

# Side Bar. Aplicando filtros
st.sidebar.title('Opções de Filtro')
st.title('Análise do Recebimento de Leite ')
month = st.sidebar.selectbox("Mês", df["Month"].unique())
fin = st.sidebar.selectbox("Finalidade", df["desc_finalidade"].unique(), index=None, placeholder='Todas')
# assoc = st.sidebar.selectbox("Associação", df["desc_associacao"].unique(), index=None, placeholder='Todas')
#st.sidebar.balloons()

df_filtered = df[(df["Month"] == month)]

if fin != None:
    df_filtered = df[(df["Month"] == month) & (df["desc_finalidade"] == fin)]

# Estruturando o Dashboard.
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="data", y="qtd_total", color="desc_finalidade", title="Recebimento por dia",
                 labels={ 'data': 'Data', 'qtd_total': 'Total', 'desc_finalidade': 'Finalidade'})
col1.plotly_chart(fig_date, use_container_width=True)


fig_prod = px.bar(df_filtered, x="qtd_total", y="desc_finalidade", 
                   color="desc_finalidade", title="Recebimento por Finalidade (L)",
                   orientation="h",
                  labels={ 'qtd_total': 'Quantidade(L)', 'desc_finalidade': 'Finalidade'})
col2.plotly_chart(fig_prod, use_container_width=True)


fin_val_total = df_filtered.groupby("desc_finalidade")[["valor_total"]].sum().reset_index()
fig_val_fin = px.bar(fin_val_total, x="desc_finalidade", y="valor_total",
                    title="Valor pago por Finalidade (R$)",
                    labels={ 'desc_finalidade': 'Finalidade', 'valor_total': 'Total(R$)'})
col3.plotly_chart(fig_val_fin, use_container_width=True)


fig_kind = px.pie(df_filtered, values="valor_total", names="desc_finalidade",
                   title="Recebimento por Finalidade (%)",
                   labels={ 'valor_total': 'Total', 'desc_finalidade': 'Finalidade'})
col4.plotly_chart(fig_kind, use_container_width=True)


assoc_total = df_filtered.groupby("nome_associacao")[["valor_total"]].mean().reset_index()
fig_rating = px.bar(assoc_total, x="valor_total", y="nome_associacao",
                   title="Valor pago por Associação (R$)",
                   orientation="h",
                   labels={ 'nome_associacao': 'Associação', 'valor_total': 'ValorR$(R$)'})
col5.plotly_chart(fig_rating, use_container_width=True)



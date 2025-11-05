import pandas as pd
import streamlit as st
import yfinance as yf

st.write("# Preço das Ações")
st.write("Gráfico abaixo representa o preço de fechamento das ações desde 2010 até 2024.")

@st.cache_data
def obter_dados(empresas):
    dados = yf.download(empresas, start="2010-01-01", end="2024-12-31")["Close"]
    if isinstance(dados.columns, pd.MultiIndex):
        dados.columns = dados.columns.get_level_values(1)
    if isinstance(dados, pd.Series):
        dados = dados.to_frame()

    return dados 

def carregar_dados_csv():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    ticker= list(base_tickers["Código"])
    ticker=[item + ".SA" for item in ticker]

    return ticker

acoes = carregar_dados_csv()
dados = obter_dados(acoes)

st.sidebar.header("Configurações do Gráfico")

lista_acoes = st.multiselect("Selecione as ações para exibir no gráfico:",acoes,default=["ITUB4.SA"])
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo=st.sidebar.slider("Escolha o intervalo de data desejado",min_value=data_inicial,max_value=data_final,value=(data_inicial,data_final))
dados = dados.loc[intervalo[0]:intervalo[1]]
if lista_acoes:
    df_plot = dados[lista_acoes].copy()

    # Caso apenas uma ação seja selecionada
    if len(lista_acoes) == 1:
        nome_acao = lista_acoes[0]
        df_plot = df_plot.reset_index().rename(columns={nome_acao: "Preço de Fechamento"})
        df_plot = df_plot.set_index("Date")
        st.line_chart(df_plot["Preço de Fechamento"])  # passa uma Series limpa
    else:
        st.line_chart(dados[lista_acoes])



st.write("Obrigado por visitar minha página!")

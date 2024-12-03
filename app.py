import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from data import carregar_dados, salvar_dados, registrar_transacao, remover_transacao
from business_rules import validar_gasto
from utils import calcular_total
from dotenv import load_dotenv
from OllamaAPI import chat_ollama_stream

load_dotenv()


st.set_page_config(
    page_title='Gerenciador Financeiro',
    page_icon='💰',
    layout='wide',
    initial_sidebar_state='expanded'
)


transacoes_df = carregar_dados()

categorias_padrao = ['Salário', 'Investimentos', 'Lazer', 'Saúde', 'Educação', 'Transporte', 'Alimentação', 'Outros']
todas_categorias = list(set(categorias_padrao + transacoes_df['Categoria'].dropna().unique().tolist()))


def gerar_contexto_financeiro(transacoes_filtradas):
    """
    Gera um resumo do contexto financeiro com base nas transações filtradas.

    Args:
        transacoes_filtradas (DataFrame): Transações atuais do usuário.

    Returns:
        str: Resumo do contexto financeiro.
    """
    total_ganhos = calcular_total(transacoes_filtradas, 'Ganho')
    total_gastos = calcular_total(transacoes_filtradas, 'Gasto')
    saldo_atual = total_ganhos - total_gastos

    categorias = transacoes_filtradas.groupby('Categoria')['Valor'].sum().reset_index()

    resumo_categorias = "\n".join(
        [f"{row['Categoria']}: R$ {row['Valor']:.2f}" for _, row in categorias.iterrows()]
    )

    contexto = (
        f"Saldo Atual: R$ {saldo_atual:.2f}\n"
        f"Total de Ganhos: R$ {total_ganhos:.2f}\n"
        f"Total de Gastos: R$ {total_gastos:.2f}\n"
        f"Gastos por Categoria:\n{resumo_categorias}"
    )
    return contexto


st.title('💰 Gerenciador Financeiro Pessoal')

with st.sidebar:
    st.header('Registrar Nova Transação')   
    tipo = st.selectbox('Tipo', ['Ganho', 'Gasto'])
    descricao = st.text_input('Descrição')
    valor = st.number_input('Valor', min_value=0.01, format="%.2f")
    data = st.date_input('Data', datetime.now())

    categoria_existente = st.selectbox('Categoria', ['Outros'] + todas_categorias)
    if categoria_existente == 'Outros':
        nova_categoria = st.text_input('Nova Categoria (opcional)')
        categoria = nova_categoria if nova_categoria else 'Outros'
    else:
        categoria = categoria_existente

    if st.button('Adicionar'):
        if descricao and valor and categoria:
            if tipo == 'Gasto' and not validar_gasto(transacoes_df, valor):
                st.error('Saldo insuficiente para registrar este gasto.')
            else:
                transacoes_df = registrar_transacao(transacoes_df, data, tipo, descricao, valor, categoria)
                salvar_dados(transacoes_df)
                st.success(f'{tipo} registrado com sucesso!')
        else:
            st.error('Por favor, preencha todos os campos corretamente.')


with st.sidebar:
    st.header('🤖 Chatbot Financeiro')
    st.write("Pergunte sobre suas finanças pessoais!")

    pergunta = st.text_input('Digite sua pergunta:')

    if st.button('Perguntar'):
        if pergunta:
            contexto_financeiro = gerar_contexto_financeiro(transacoes_df)
            contexto_financeiro += "\nPor favor, responda sempre em português e de forma natural para obter melhores resultados e muito cuidado em ser prolixo e repetir a mesma coisa duas vezes"
            with st.spinner('Pensando...'):
                resposta = chat_ollama_stream(pergunta, contexto_financeiro)
            st.write('**Resposta:**')
            st.text_area("", resposta, height=200)
        else:
            st.error('Por favor, digite uma pergunta.')


with st.sidebar:
    st.header('Remover Transação')
    if not transacoes_df.empty:
        transacoes_df['Resumo'] = transacoes_df.apply(
            lambda row: f"ID: {row['ID']} | {row['Tipo']} - {row['Descrição']} (R$ {row['Valor']:.2f}) em {row['Data'].strftime('%d/%m/%Y')}",
            axis=1
        )
        id_selecionado = st.selectbox(
            'Selecione a Transação para Remover:',
            options=transacoes_df['Resumo']
        )

        id_para_remover = int(id_selecionado.split('|')[0].replace("ID: ", "").strip())

        if st.button('Remover Transação'):
            transacoes_df = remover_transacao(transacoes_df, id_para_remover)
            salvar_dados(transacoes_df)
            st.success('Transação removida com sucesso!')
    else:
        st.write('Não há transações para remover.')

st.header('Filtros')
col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
with col_filtro1:
    tipos_selecionados = st.multiselect('Tipo de Transação', options=['Ganho', 'Gasto'])
with col_filtro2:
    categorias_selecionadas = st.multiselect('Categorias', options=todas_categorias)
with col_filtro3:
    if not transacoes_df.empty and transacoes_df['Data'].notnull().all():
        min_data = transacoes_df['Data'].min()
        max_data = transacoes_df['Data'].max()
    else:
        min_data = datetime.today() - timedelta(days=30)
        max_data = datetime.today()
    data_inicial = st.date_input('Data Inicial', value=min_data.date())
    data_final = st.date_input('Data Final', value=max_data.date())

    data_inicial = pd.Timestamp(data_inicial)
    data_final = pd.Timestamp(data_final)

if not tipos_selecionados:
    tipos_selecionados = transacoes_df['Tipo'].unique().tolist()

if not categorias_selecionadas:
    categorias_selecionadas = transacoes_df['Categoria'].unique().tolist()

transacoes_filtradas = transacoes_df[
    (transacoes_df['Tipo'].isin(tipos_selecionados)) &
    (transacoes_df['Categoria'].isin(categorias_selecionadas)) &
    (transacoes_df['Data'] >= data_inicial) &
    (transacoes_df['Data'] <= data_final)
]

st.markdown('## Resumo Financeiro')
col1, col2, col3 = st.columns(3)
with col1:
    total_ganhos = calcular_total(transacoes_filtradas, 'Ganho')
    st.metric('💵 Total de Ganhos', f'R$ {total_ganhos:.2f}')
with col2:
    total_gastos = calcular_total(transacoes_filtradas, 'Gasto')
    st.metric('💳 Total de Gastos', f'R$ {total_gastos:.2f}')
with col3:
    saldo_atual = total_ganhos - total_gastos
    st.metric('🏦 Saldo Atual', f'R$ {saldo_atual:.2f}')

st.markdown('## Escolha o Tipo de Dashboard')
dashboard_opcao = st.selectbox(
    'Selecione o tipo de Dashboard que deseja visualizar:',
    [
        'Comparação de Ganhos e Gastos por Categoria',
        'Saldo Acumulado ao Longo do Tempo',
        'Distribuição de Gastos por Categoria',
        'Evolução dos Ganhos e Gastos Mensais',
        'Top 10 Despesas e Receitas',
        'Concentração de Despesas/Ganhos por Dia da Semana e Mês'
    ]
)

if dashboard_opcao == 'Comparação de Ganhos e Gastos por Categoria':
    st.markdown('### Comparação de Ganhos e Gastos por Categoria')

    stacked_bar_data = transacoes_filtradas.groupby(['Categoria', 'Tipo'])['Valor'].sum().reset_index()

    fig_stacked_bar = px.bar(
        stacked_bar_data,
        x='Categoria',
        y='Valor',
        color='Tipo',
        barmode='stack',
        title='Ganhos vs Gastos por Categoria',
        labels={'Valor': 'Valor (R$)', 'Categoria': 'Categoria'},
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig_stacked_bar, use_container_width=True)

elif dashboard_opcao == 'Saldo Acumulado ao Longo do Tempo':
    st.markdown('### Evolução do Saldo Acumulado')

    area_data = transacoes_filtradas.copy()
    area_data['Saldo'] = area_data.apply(lambda row: row['Valor'] if row['Tipo'] == 'Ganho' else -row['Valor'], axis=1)
    area_data['Data'] = pd.to_datetime(area_data['Data'])
    area_data = area_data.groupby('Data')['Saldo'].sum().cumsum().reset_index()

    fig_area = px.area(
        area_data,
        x='Data',
        y='Saldo',
        title='Saldo Acumulado ao Longo do Tempo',
        labels={'Saldo': 'Saldo Acumulado (R$)', 'Data': 'Data'},
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig_area, use_container_width=True)

elif dashboard_opcao == 'Distribuição de Gastos por Categoria':
    st.markdown('### Distribuição de Ganhos e Gastos')

    pie_data = transacoes_filtradas.groupby('Tipo')['Valor'].sum().reset_index()

    fig_pie = px.pie(
        pie_data,
        names='Tipo',
        values='Valor',
        title='Distribuição de Ganhos e Gastos',
        template='plotly_white',
        height=500
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig_pie, use_container_width=True)


elif dashboard_opcao == 'Evolução dos Ganhos e Gastos Mensais':
    st.markdown('### Evolução dos Ganhos e Gastos Mensais')

    line_data = transacoes_filtradas.copy()
    line_data['Mês'] = line_data['Data'].dt.to_period('M').astype(str)  # Corrigido para string
    line_data = line_data.groupby(['Mês', 'Tipo'])['Valor'].sum().reset_index()

    fig_line = px.line(
        line_data,
        x='Mês',
        y='Valor',
        color='Tipo',
        title='Evolução dos Ganhos e Gastos ao Longo do Tempo',
        labels={'Valor': 'Valor (R$)', 'Mês': 'Mês/Ano'},
        template='plotly_white',
        markers=True,
        height=500
    )

    st.plotly_chart(fig_line, use_container_width=True)

elif dashboard_opcao == 'Top 10 Despesas e Receitas':
    st.markdown('### Maiores Despesas e Receitas')

    top_transacoes = transacoes_filtradas.groupby(['Descrição', 'Tipo'])['Valor'].sum().reset_index()
    top_transacoes = top_transacoes.nlargest(10, 'Valor')

    fig_bar_horizontal = px.bar(
        top_transacoes,
        x='Valor',
        y='Descrição',
        color='Tipo',
        title='Top 10 Despesas e Receitas',
        orientation='h',
        labels={'Valor': 'Valor (R$)', 'Descrição': 'Descrição'},
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig_bar_horizontal, use_container_width=True)

elif dashboard_opcao == 'Concentração de Despesas/Ganhos por Dia da Semana e Mês':
    st.markdown('### Concentração de Despesas/Ganhos por Dia da Semana e Mês')

    heatmap_data = transacoes_filtradas.copy()
    heatmap_data['Dia da Semana'] = heatmap_data['Data'].dt.day_name()
    heatmap_data['Mês'] = heatmap_data['Data'].dt.month_name()
    heatmap_data = heatmap_data.groupby(['Dia da Semana', 'Mês'])['Valor'].sum().reset_index()

    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x='Mês',
        y='Dia da Semana',
        z='Valor',
        title='Concentração de Despesas e Ganhos por Dia da Semana e Mês',
        labels={'Valor': 'Total (R$)'},
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)


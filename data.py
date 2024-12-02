import pandas as pd

def carregar_dados():
    """
    Carrega os dados de transações financeiras de um arquivo CSV.
    Se o arquivo não existir, cria um arquivo vazio com as colunas necessárias.
    """
    try:
        transacoes_df = pd.read_csv('transacoes.csv', dtype={'Valor': float}, parse_dates=['Data'])
    except FileNotFoundError:
        transacoes_df = pd.DataFrame(columns=['ID', 'Data', 'Tipo', 'Descrição', 'Valor', 'Categoria'])
        transacoes_df.to_csv('transacoes.csv', index=False)
    else:
        # Garantir que as colunas necessárias existam
        required_columns = ['ID', 'Data', 'Tipo', 'Descrição', 'Valor', 'Categoria']
        for col in required_columns:
            if col not in transacoes_df.columns:
                transacoes_df[col] = None
        # Preencher valores ausentes na categoria com 'Outros'
        transacoes_df['Categoria'] = transacoes_df['Categoria'].fillna('Outros')
        # Garantir que a coluna 'Data' seja do tipo Timestamp
        transacoes_df['Data'] = pd.to_datetime(transacoes_df['Data'], errors='coerce')
    return transacoes_df

def salvar_dados(transacoes_df):
    """
    Salva os dados de transações em um arquivo CSV.
    """
    transacoes_df.to_csv('transacoes.csv', index=False)

def registrar_transacao(transacoes_df, data, tipo, descricao, valor, categoria):
    """
    Registra uma nova transação no DataFrame e retorna o DataFrame atualizado.
    """
    from utils import gerar_id
    novo_id = gerar_id(transacoes_df)
    data = pd.Timestamp(data)  # Converter data para Timestamp
    nova_transacao = pd.DataFrame({
        'ID': [novo_id],
        'Data': [data],
        'Tipo': [tipo],
        'Descrição': [descricao],
        'Valor': [valor],
        'Categoria': [categoria]
    })
    transacoes_df = pd.concat([transacoes_df, nova_transacao], ignore_index=True)
    return transacoes_df

def remover_transacao(transacoes_df, transacao_id):
    """
    Remove uma transação do DataFrame com base no ID da transação.
    """
    transacoes_df = transacoes_df[transacoes_df['ID'] != transacao_id]
    return transacoes_df

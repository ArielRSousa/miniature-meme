def gerar_id(df):
    """
    Gera um novo ID para uma transação. Se o DataFrame estiver vazio, retorna 1.
    Caso contrário, retorna o maior ID existente + 1.
    """
    if df.empty:
        return 1
    else:
        return int(df['ID'].max()) + 1

def calcular_total(df, tipo_transacao=None):
    """
    Calcula o total de valores no DataFrame, opcionalmente filtrando por tipo de transação.
    """
    if tipo_transacao:
        df = df[df['Tipo'] == tipo_transacao]
    return df['Valor'].sum()

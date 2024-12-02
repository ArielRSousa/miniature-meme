from utils import calcular_total

def validar_gasto(transacoes_df, valor_gasto):
    """
    Verifica se o saldo atual é suficiente para registrar um novo gasto.
    
    :param transacoes_df: DataFrame contendo as transações.
    :param valor_gasto: Valor do gasto a ser registrado.
    :return: True se o saldo for suficiente, False caso contrário.
    """
    total_ganhos = calcular_total(transacoes_df, 'Ganho')
    total_gastos = calcular_total(transacoes_df, 'Gasto')
    saldo_atual = total_ganhos - total_gastos
    return saldo_atual >= valor_gasto

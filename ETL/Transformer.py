import pandas as pd

def transform_income_statement(data, empresa):
    if not isinstance(data, list):
        raise ValueError("Esperado uma lista de dicionários como entrada da API.")
    df = pd.DataFrame(data)
    df["empresa"] = empresa

    # Remove coluna se existir
    if 'relatorio' in df.columns:
        df = df.drop(columns=['relatorio'])

    # Preenche valores ausentes com 0 para colunas numéricas
    colunas_numericas = [
        'revenue', 'costOfRevenue', 'grossProfit', 'grossProfitRatio',
        'researchAndDevelopmentExpenses', 'generalAndAdministrativeExpenses',
        'sellingAndMarketingExpenses', 'sellingGeneralAndAdministrativeExpenses',
        'otherExpenses', 'operatingExpenses', 'costAndExpenses', 'interestIncome',
        'interestExpense', 'depreciationAndAmortization', 'ebitda', 'ebitdaratio',
        'operatingIncome', 'operatingIncomeRatio', 'totalOtherIncomeExpensesNet',
        'incomeBeforeTax', 'incomeBeforeTaxRatio', 'incomeTaxExpense', 'netIncome',
        'netIncomeRatio', 'eps', 'epsdiluted', 'weightedAverageShsOut', 'weightedAverageShsOutDil'
    ]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Padroniza strings
    if 'symbol' in df.columns:
        df['symbol'] = df['symbol'].str.upper().str.strip()

    colunas_traduzidas = {
    'date': 'data',
    'symbol': 'símbolo',
    'reportedCurrency': 'moeda_reportada',
    'cik': 'cik',
    'fillingDate': 'data_registro',
    'acceptedDate': 'data_aceite',
    'calendarYear': 'ano_fiscal',
    'period': 'periodo',
    'revenue': 'receita_bruta',
    'costOfRevenue': 'custo_receita',
    'grossProfit': 'lucro_bruto',
    'grossProfitRatio': 'margem_bruta',
    'researchAndDevelopmentExpenses': 'despesas_pesquisa_desenvolvimento',
    'generalAndAdministrativeExpenses': 'despesas_gerais_administrativas',
    'sellingAndMarketingExpenses': 'despesas_vendas_marketing',
    'sellingGeneralAndAdministrativeExpenses': 'despesas_vendas_gerais_administrativas',
    'otherExpenses': 'outras_despesas',
    'operatingExpenses': 'despesas_operacionais',
    'costAndExpenses': 'custos_despesas',
    'interestIncome': 'receita_juros',
    'interestExpense': 'despesa_juros',
    'depreciationAndAmortization': 'depreciacao_amortizacao',
    'ebitda': 'ebitda',
    'ebitdaratio': 'margem_ebitda',
    'operatingIncome': 'lucro_operacional',
    'operatingIncomeRatio': 'margem_operacional',
    'totalOtherIncomeExpensesNet': 'outras_receitas_despesas_liquidas',
    'incomeBeforeTax': 'lucro_antes_impostos',
    'incomeBeforeTaxRatio': 'margem_antes_impostos',
    'incomeTaxExpense': 'despesa_impostos',
    'netIncome': 'lucro_liquido',
    'netIncomeRatio': 'margem_lucro_liquido',
    'eps': 'lucro_por_acao',
    'epsdiluted': 'lucro_por_acao_diluido',
    'weightedAverageShsOut': 'media_ponderada_acoes',
    'weightedAverageShsOutDil': 'media_ponderada_acoes_diluida',
    'link': 'link_relatorio',
    'finalLink': 'link_final',
    'empresa': 'empresa'
}

    df.rename(columns=colunas_traduzidas, inplace= True)
    df = df.drop(columns=["link_relatorio", "link_final"], errors="ignore")
    
    df = df.sort_values(['empresa', 'ano_fiscal', 'data'])

    # Calcula Faturamento LY (Last Year) com base no ano_fiscal anterior
    df['ano_fiscal'] = pd.to_numeric(df['ano_fiscal'], errors='coerce')
    df_ly = df[['empresa', 'ano_fiscal', 'receita_bruta']].copy()
    df_ly['ano_fiscal'] += 1
    df_ly = df_ly.rename(columns={'receita_bruta': 'faturamento_ly'})

    # Faz o merge para trazer o faturamento do ano anterior
    df = pd.merge(df, df_ly, on=['empresa', 'ano_fiscal'], how='left')

    # Calcula Faturamento YoY (%) em percentual
    df['faturamento_yoy'] = ((df['receita_bruta'] - df['faturamento_ly']) / df['faturamento_ly'])

    colunas_kpi = [
        'data', 'empresa', 'ano_fiscal', 'receita_bruta', 'lucro_bruto', 'lucro_operacional',
        'lucro_liquido', 'ebitda', 'margem_bruta', 'margem_operacional', 'margem_ebitda',
        'margem_lucro_liquido', 'faturamento_ly', 'faturamento_yoy','despesas_operacionais'
    ]

    df_kpis = df[colunas_kpi]

    return df_kpis

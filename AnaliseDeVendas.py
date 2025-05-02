import pandas as pd
import glob

arquivos = glob.glob("Base Vendas - 20*.xlsx")

dfs = []

for arquivo in arquivos:
    df = pd.read_excel(arquivo)
    dfs.append(df)
    
vendas_df_completo = pd.concat(dfs, ignore_index=True)
produtos_df = pd.read_excel(r'Cadastro Produtos.xlsx')

vendas_df_completo = vendas_df_completo.merge(produtos_df, on="SKU")

vendas_df_completo['Data da Venda'] = pd.to_datetime(vendas_df_completo['Data da Venda'])
vendas_df_completo['Ano'] = vendas_df_completo['Data da Venda'].dt.year
vendas_df_completo['Mês'] = vendas_df_completo['Data da Venda'].dt.month

vendas_df_completo['Valor Venda'] = vendas_df_completo['Qtd Vendida'] * vendas_df_completo['Preço Unitario']

vendas_ano = vendas_df_completo.groupby('Ano')['Valor Venda'].sum().reset_index()
vendas_mes = vendas_df_completo.groupby(['Ano', 'Mês'])['Valor Venda'].sum().reset_index()

total_vendas = vendas_df_completo['Valor Venda'].sum()

vendas_ano['Crescimento (%)'] = vendas_ano['Valor Venda'].pct_change() * 100

media_crescimento_ano = vendas_ano['Crescimento (%)'].mean()

vendas_mes['Crescimento (%)'] = vendas_mes.groupby('Mês')['Valor Venda'].pct_change() * 100

media_crescimento_mes = vendas_mes['Crescimento (%)'].mean()

vendas_2021 = vendas_ano.loc[vendas_ano['Ano'] == 2021, 'Valor Venda'].values[0]

vendas_2022 = vendas_ano.loc[vendas_ano['Ano'] == 2022, 'Valor Venda'].values[0]

crescimento_2021_2022 = ((vendas_2022 - vendas_2021) / vendas_2021) * 100

valor_vendas_2023_todos_anos = vendas_ano.loc[vendas_ano['Ano'] == 2022, 'Valor Venda'].values[0] * (1 + media_crescimento_ano / 100)

valor_vendas_2023_ultimos_anos = vendas_ano.loc[vendas_ano['Ano'] == 2022, 'Valor Venda'].values[0] * (1 + crescimento_2021_2022 / 100)


print(f'Vendas por ano:\n{vendas_ano}\n')
print(f'Vendas por mes:\n{vendas_mes}\n')
print(f'Total de vendas:\n{total_vendas}\n')
print(f'Media de Crescimento Anual (2020 ~ 2022): {media_crescimento_ano:.2f}%')
print(f'Media de Crescimento Anual (2021 ~ 2022): {crescimento_2021_2022:.2f}%\n')
print(f'Tendencia de Crescimento 2023 (2020 ~ 2022): {valor_vendas_2023_todos_anos:.2f} Valor calculado com base na media de crescimento feita dos anos de 2020 ate atual de 2022, que e o valor de vendas conquistado do ultimo ano de 2022 crescendo em 95,98% com base media dos ultimos anos.\n')
print(f'\nTendencia de Crescimento 2023 (2021 ~ 2022): {valor_vendas_2023_ultimos_anos:.2f} Valor que acredito ser mais realista, pois esse valor e com base no crescimento visto de 2021 para 2022, onde as vendas tiveram uma linha de crescimento mais realista.')

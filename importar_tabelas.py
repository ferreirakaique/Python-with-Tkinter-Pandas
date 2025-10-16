import pandas as pd

tabela = pd.read_csv('nota_alunos.csv',sep=';',encoding='UTF-8')
tabela.index = range(1, len(tabela) + 1)


notas_maior_7 = tabela[tabela['Nota final']>=7]
print(notas_maior_7)
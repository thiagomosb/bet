import pandas as pd

df = pd.read_excel("PROVA - ANÁLISE DE DADOS.xlsx", sheet_name="Planilha1")
df.to_csv("planilha_cassino.csv", index=False, encoding="utf-8")

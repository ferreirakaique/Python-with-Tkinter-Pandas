import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.title("Tabela com Treeview")
janela.geometry("400x200")

# Criar tabela
tabela = ttk.Treeview(janela)
tabela["columns"] = ("Nome", "Idade", "Cidade")

# Cabeçalhos
for col in tabela["columns"]:
    tabela.heading(col, text=col)
    tabela.column(col, width=100)

# Inserir dados
dados = [
    ("Alice", 25, "São Paulo"),
    ("Bob", 30, "Rio de Janeiro"),
    ("Carol", 22, "Belo Horizonte")
]

for linha in dados:
    tabela.insert("", "end", values=linha)

tabela.pack(expand=True, fill="both")

janela.mainloop()

# Kaique Bernardes Ferreira

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os

class SistemaAlunos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro e Relatórios de Alunos")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f2f5")

        # === Estilo visual ===
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#fdfdfd", foreground="black", rowheight=25, fieldbackground="#fdfdfd")
        estilo.map("Treeview", background=[("selected", "#0078D7")])
        estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
        estilo.configure("TLabel", font=("Segoe UI", 10))
        estilo.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

        # === DataFrame inicial vazio e contador de IDs ===
        self.id_counter = 1
        self.df = pd.DataFrame(columns=["ID", "Aluno", "Idade", "Curso", "Nota Final"])

        # === Frame de Cadastro ===
        frame_cadastro = ttk.LabelFrame(root, text="Cadastrar Novo Aluno")
        frame_cadastro.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = ttk.Entry(frame_cadastro, width=25)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_cadastro, text="Idade:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_idade = ttk.Entry(frame_cadastro, width=10)
        self.entry_idade.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_cadastro, text="Curso:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_curso = ttk.Entry(frame_cadastro, width=25)
        self.entry_curso.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_cadastro, text="Nota Final:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_nota = ttk.Entry(frame_cadastro, width=10)
        self.entry_nota.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar_aluno).grid(row=2, column=0, columnspan=4, pady=10)

        # === Frame da Tabela ===
        frame_tabela = ttk.LabelFrame(root, text="Tabela de Alunos")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ["ID", "Aluno", "Idade", "Curso", "Nota Final"]
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=150, anchor="center")
        self.tabela.pack(fill="both", expand=True)

        # === Frame de Botões ===
        frame_botoes = ttk.LabelFrame(root, text="Relatórios e Arquivos")
        frame_botoes.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_botoes, text="Filtrar notas acima de:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_media = ttk.Entry(frame_botoes, width=10)
        self.entry_media.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_botoes, text="Filtrar", command=self.filtrar_notas).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes, text="Exportar CSV (Filtrados)", command=self.exportar_csv).grid(row=0, column=3, padx=5)
        ttk.Button(frame_botoes, text="Salvar CSV", command=self.salvar_csv).grid(row=0, column=4, padx=5)
        ttk.Button(frame_botoes, text="Carregar CSV", command=self.carregar_csv).grid(row=0, column=5, padx=5)
        ttk.Button(frame_botoes, text="Mostrar Todos", command=self.mostrar_todos).grid(row=0, column=6, padx=5)
        ttk.Button(frame_botoes, text="Limpar Tabela", command=self.limpar_tabela).grid(row=0, column=7, padx=5)

    # === Funções ===
    def cadastrar_aluno(self):
        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()
        curso = self.entry_curso.get().strip()
        nota = self.entry_nota.get().strip()

        if not nome or not idade or not curso or not nota:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            idade = int(idade)
            nota = float(nota)
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser número inteiro e nota deve ser número!")
            return

        # Adiciona novo aluno
        novo = pd.DataFrame([[self.id_counter, nome, idade, curso, nota]], columns=self.df.columns)
        self.df = pd.concat([self.df, novo], ignore_index=True)
        self.id_counter += 1
        self.atualizar_tabela()
        self.limpar_campos()

    def atualizar_tabela(self, dados=None):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        dados = dados if dados is not None else self.df
        for _, row in dados.iterrows():
            self.tabela.insert("", "end", values=list(row))

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.entry_curso.delete(0, tk.END)
        self.entry_nota.delete(0, tk.END)

    def filtrar_notas(self):
        media = self.entry_media.get().strip()
        if not media:
            messagebox.showwarning("Aviso", "Informe uma média para filtrar!")
            return
        try:
            media = float(media)
        except ValueError:
            messagebox.showerror("Erro", "Informe um número válido!")
            return

        filtrados = self.df[self.df["Nota Final"] > media]
        if filtrados.empty:
            messagebox.showinfo("Resultado", "Nenhum aluno com nota acima dessa média.")
        self.atualizar_tabela(filtrados)
        self.df_filtrado = filtrados

    def mostrar_todos(self):
        self.atualizar_tabela()

    def salvar_csv(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            self.df.to_csv(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Dados salvos em:\n{caminho}")

    def carregar_csv(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
        if caminho and os.path.exists(caminho):
            self.df = pd.read_csv(caminho)
            self.atualizar_tabela()
            self.id_counter = self.df["ID"].max() + 1 if not self.df.empty else 1
            messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")

    def exportar_csv(self):
        if not hasattr(self, "df_filtrado") or self.df_filtrado.empty:
            messagebox.showwarning("Aviso", "Nenhum dado filtrado para exportar!")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            self.df_filtrado.to_csv(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{caminho}")

    def limpar_tabela(self):
        self.df = pd.DataFrame(columns=["ID", "Aluno", "Idade", "Curso", "Nota Final"])
        self.atualizar_tabela()
        self.id_counter = 1
        messagebox.showinfo("Sucesso", "Tabela limpa com sucesso!")


# === EXECUÇÃO ===
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAlunos(root)
    root.mainloop()
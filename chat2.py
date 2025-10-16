import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os

# --- Configurações iniciais ---
COLUNAS = ["Nome", "Idade", "Curso", "Nota Final"]
CSV_DEFAULT = "alunos.csv"

class AlunosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro e Relatórios de Alunos")
        self.root.geometry("1024x768")
        self.root.resizable(False, False)

        # DataFrame que armazena os dados
        self.df = pd.DataFrame(columns=COLUNAS)

        # Variáveis dos inputs
        self.var_nome = tk.StringVar()
        self.var_idade = tk.StringVar()
        self.var_curso = tk.StringVar()
        self.var_nota = tk.StringVar()
        self.var_media_filtro = tk.StringVar()

        self._criar_interface()
        self._refresh_table()

    def _criar_interface(self):
        # Frame de cadastro
        frame_cadastro = tk.LabelFrame(self.root, text="Cadastrar Aluno", padx=10, pady=10)
        frame_cadastro.place(x=10, y=10, width=380, height=200)

        tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_cadastro, textvariable=self.var_nome, width=30).grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_cadastro, text="Idade:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_cadastro, textvariable=self.var_idade, width=10).grid(row=1, column=1, sticky="w", pady=5, padx=5)

        tk.Label(frame_cadastro, text="Curso:").grid(row=2, column=0, sticky="w")
        tk.Entry(frame_cadastro, textvariable=self.var_curso, width=30).grid(row=2, column=1, pady=5, padx=5)

        tk.Label(frame_cadastro, text="Nota Final:").grid(row=3, column=0, sticky="w")
        tk.Entry(frame_cadastro, textvariable=self.var_nota, width=10).grid(row=3, column=1, sticky="w", pady=5, padx=5)

        btn_add = tk.Button(frame_cadastro, text="Cadastrar", command=self.add_aluno, width=12)
        btn_add.grid(row=4, column=0, pady=10)

        btn_limpar = tk.Button(frame_cadastro, text="Limpar campos", command=self.limpar_campos, width=12)
        btn_limpar.grid(row=4, column=1, sticky="w", pady=10)

        # Frame de ações (salvar/carregar/exportar/filtro)
        frame_acoes = tk.LabelFrame(self.root, text="Ações / Relatórios", padx=10, pady=10)
        frame_acoes.place(x=10, y=220, width=380, height=200)

        # Filtro por média
        tk.Label(frame_acoes, text="Filtrar notas acima de:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_acoes, textvariable=self.var_media_filtro, width=10).grid(row=0, column=1, sticky="w", padx=5)

        btn_filtrar = tk.Button(frame_acoes, text="Aplicar filtro", command=self.aplicar_filtro, width=12)
        btn_filtrar.grid(row=1, column=0, pady=8)

        btn_limpar_filtro = tk.Button(frame_acoes, text="Remover filtro", command=self.remover_filtro, width=12)
        btn_limpar_filtro.grid(row=1, column=1, pady=8, sticky="w")

        # Botões de salvar / carregar / exportar
        btn_save = tk.Button(frame_acoes, text="Salvar CSV (Salvar)", command=self.salvar_csv, width=12)
        btn_save.grid(row=2, column=0, pady=8)

        btn_load = tk.Button(frame_acoes, text="Carregar CSV (Abrir)", command=self.carregar_csv, width=12)
        btn_load.grid(row=2, column=1, pady=8, sticky="w")

        btn_export = tk.Button(frame_acoes, text="Exportar filtrados", command=self.exportar_filtrado, width=26)
        btn_export.grid(row=3, column=0, columnspan=2, pady=8)

        # Frame da tabela
        frame_tabela = tk.LabelFrame(self.root, text="Tabela de Alunos", padx=5, pady=5)
        frame_tabela.place(x=400, y=10, width=380, height=510)

        # Treeview (tabela)
        columns = COLUNAS
        self.tree = ttk.Treeview(frame_tabela, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            # largura razoável por coluna
            if col == "Nome":
                self.tree.column(col, width=150, anchor="w")
            elif col == "Curso":
                self.tree.column(col, width=100, anchor="w")
            else:
                self.tree.column(col, width=60, anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.place(x=5, y=5, width=350, height=450)
        vsb.place(x=355, y=5, height=450)
        hsb.place(x=5, y=460, width=350)

        # Botões para manipular seleção (opcional)
        btn_excluir = tk.Button(self.root, text="Excluir selecionado", command=self.excluir_selecionado, width=18)
        btn_excluir.place(x=10, y=430)

        btn_editar = tk.Button(self.root, text="Editar selecionado", command=self.editar_selecionado, width=18)
        btn_editar.place(x=200, y=430)

        # Label status
        self.label_status = tk.Label(self.root, text="Pronto", anchor="w")
        self.label_status.place(x=10, y=500, width=770, height=25)

    # ------------- Funções de ação -------------
    def add_aluno(self):
        nome = self.var_nome.get().strip()
        idade = self.var_idade.get().strip()
        curso = self.var_curso.get().strip()
        nota = self.var_nota.get().strip()

        # Validações básicas
        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório.")
            return

        try:
            idade_int = int(idade)
            if idade_int < 0:
                raise ValueError
        except Exception:
            messagebox.showwarning("Atenção", "Idade inválida. Use um número inteiro.")
            return

        try:
            nota_float = float(nota)
            if nota_float < 0 or nota_float > 10:
                messagebox.showwarning("Atenção", "Nota deve estar entre 0 e 10.")
                return
        except Exception:
            messagebox.showwarning("Atenção", "Nota inválida. Use um número (ex: 7.5).")
            return

        # Adiciona ao DataFrame
        nova_linha = {"Nome": nome, "Idade": idade_int, "Curso": curso, "Nota Final": nota_float}
        self.df = pd.concat([self.df, pd.DataFrame([nova_linha])], ignore_index=True)

        self._refresh_table()
        self.limpar_campos()
        self.label_status.config(text=f"Aluno '{nome}' cadastrado.")

    def limpar_campos(self):
        self.var_nome.set("")
        self.var_idade.set("")
        self.var_curso.set("")
        self.var_nota.set("")

    def _refresh_table(self, df_para_mostrar=None):
        """Atualiza os itens do treeview com os dados do DataFrame (ou df_para_mostrar)."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if df_para_mostrar is None:
            df_para_mostrar = self.df

        # Exibir com formatação de nota (1 casa decimal)
        for idx, row in df_para_mostrar.reset_index().iterrows():
            vals = (row["Nome"], int(row["Idade"]), row["Curso"], float(row["Nota Final"]))
            self.tree.insert("", "end", iid=str(idx), values=vals)

    def aplicar_filtro(self):
        media_text = self.var_media_filtro.get().strip()
        if not media_text:
            messagebox.showinfo("Filtro", "Digite a média para filtrar.")
            return
        try:
            media = float(media_text)
        except Exception:
            messagebox.showwarning("Atenção", "Média inválida. Use um número.")
            return

        df_filtrado = self.df[self.df["Nota Final"] > media].reset_index(drop=True)
        self._refresh_table(df_filtrado)
        self.label_status.config(text=f"Filtro aplicado: notas > {media}. {len(df_filtrado)} registro(s).")

    def remover_filtro(self):
        self.var_media_filtro.set("")
        self._refresh_table()
        self.label_status.config(text="Filtro removido.")

    def salvar_csv(self):
        # Pergunta onde salvar (nome do arquivo)
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")],
                                            initialfile=CSV_DEFAULT,
                                            title="Salvar CSV")
        if not path:
            return
        try:
            # Salva o DataFrame atual
            self.df.to_csv(path, index=False, encoding="utf-8")
            self.label_status.config(text=f"Dados salvos em '{os.path.basename(path)}'.")
            messagebox.showinfo("Salvar CSV", f"Arquivo salvo em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar CSV:\n{e}")

    def carregar_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Abrir CSV")
        if not path:
            return
        try:
            df = pd.read_csv(path)
            # Verifica colunas essenciais
            if not set(COLUNAS).issubset(df.columns):
                messagebox.showerror("Erro", f"O CSV precisa conter as colunas: {COLUNAS}")
                return
            # Força tipos
            df = df[COLUNAS].copy()
            df["Idade"] = df["Idade"].astype(int)
            df["Nota Final"] = df["Nota Final"].astype(float)
            self.df = df.reset_index(drop=True)
            self._refresh_table()
            self.label_status.config(text=f"Dados carregados de '{os.path.basename(path)}'. {len(self.df)} registro(s).")
            messagebox.showinfo("Carregar CSV", f"Arquivo carregado:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar CSV:\n{e}")

    def exportar_filtrado(self):
        media_text = self.var_media_filtro.get().strip()
        if not media_text:
            messagebox.showinfo("Exportar", "Defina um filtro de média antes de exportar (campo 'Filtrar notas acima de').")
            return
        try:
            media = float(media_text)
        except Exception:
            messagebox.showwarning("Atenção", "Média inválida. Use um número.")
            return

        df_filtrado = self.df[self.df["Nota Final"] > media].reset_index(drop=True)
        if df_filtrado.empty:
            messagebox.showinfo("Exportar", "Nenhum registro corresponde ao filtro.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")],
                                            initialfile=f"relatorio_notas_maiores_que_{media}.csv",
                                            title="Exportar relatório filtrado")
        if not path:
            return

        try:
            df_filtrado.to_csv(path, index=False, encoding="utf-8")
            messagebox.showinfo("Exportar", f"Relatório exportado para:\n{path}")
            self.label_status.config(text=f"Relatório exportado ({len(df_filtrado)} registros) para '{os.path.basename(path)}'.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar relatório:\n{e}")

    def excluir_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Excluir", "Nenhum item selecionado.")
            return
        idx = int(sel[0])
        # Tentativa de mapear índice para DataFrame: a tabela mostra df.reset_index() no refresh,
        # então usamos o índice da exibição. Aqui assumimos que a visualização atual está sincronizada.
        try:
            nome = self.df.iloc[idx]["Nome"]
            confirm = messagebox.askyesno("Confirmar exclusão", f"Excluir '{nome}'?")
            if not confirm:
                return
            self.df = self.df.drop(self.df.index[idx]).reset_index(drop=True)
            self._refresh_table()
            self.label_status.config(text=f"Aluno '{nome}' excluído.")
        except Exception:
            messagebox.showerror("Erro", "Não foi possível excluir o item selecionado.")

    def editar_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Editar", "Nenhum item selecionado.")
            return
        idx = int(sel[0])
        try:
            linha = self.df.iloc[idx]
        except Exception:
            messagebox.showerror("Erro", "Índice inválido.")
            return

        # Abre uma janela modal simples para edição
        ed = tk.Toplevel(self.root)
        ed.title("Editar Aluno")
        ed.geometry("320x200")
        ed.transient(self.root)
        ed.grab_set()

        v_nome = tk.StringVar(value=linha["Nome"])
        v_idade = tk.StringVar(value=str(linha["Idade"]))
        v_curso = tk.StringVar(value=linha["Curso"])
        v_nota = tk.StringVar(value=str(linha["Nota Final"]))

        tk.Label(ed, text="Nome:").pack(anchor="w", padx=10, pady=2)
        tk.Entry(ed, textvariable=v_nome, width=35).pack(padx=10)

        tk.Label(ed, text="Idade:").pack(anchor="w", padx=10, pady=2)
        tk.Entry(ed, textvariable=v_idade, width=10).pack(padx=10)

        tk.Label(ed, text="Curso:").pack(anchor="w", padx=10, pady=2)
        tk.Entry(ed, textvariable=v_curso, width=35).pack(padx=10)

        tk.Label(ed, text="Nota Final:").pack(anchor="w", padx=10, pady=2)
        tk.Entry(ed, textvariable=v_nota, width=10).pack(padx=10)

        def salvar_edicao():
            nome_n = v_nome.get().strip()
            idade_n = v_idade.get().strip()
            curso_n = v_curso.get().strip()
            nota_n = v_nota.get().strip()

            if not nome_n:
                messagebox.showwarning("Atenção", "Nome é obrigatório.")
                return
            try:
                idade_int = int(idade_n)
            except Exception:
                messagebox.showwarning("Atenção", "Idade inválida.")
                return
            try:
                nota_f = float(nota_n)
            except Exception:
                messagebox.showwarning("Atenção", "Nota inválida.")
                return

            # Atualiza o DataFrame
            self.df.at[idx, "Nome"] = nome_n
            self.df.at[idx, "Idade"] = idade_int
            self.df.at[idx, "Curso"] = curso_n
            self.df.at[idx, "Nota Final"] = nota_f

            self._refresh_table()
            self.label_status.config(text=f"Aluno '{nome_n}' atualizado.")
            ed.destroy()

        tk.Button(ed, text="Salvar", command=salvar_edicao, width=12).pack(pady=10)

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = AlunosApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro fatal", f"Ocorreu um erro:\n{e}")
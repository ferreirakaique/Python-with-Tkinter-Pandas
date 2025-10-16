from tkinter import ttk, filedialog
import tkinter as tk
import pandas as pd


import pandas as pd

def importar_tabela():
    
    caminho_arquivo = filedialog.askopenfilename(title='Selecione um arquivo',filetypes=[("Arquivos CSV","*.csv")])
    
    if caminho_arquivo:
        rotulo_nova_tabela.pack_forget()
        rotulo_criar_tabela.pack_forget()
        botao_criar_tabela.pack_forget()
        
        ler_tabela = pd.read_csv(caminho_arquivo,sep=';',encoding='UTF-8')
        ler_tabela = ler_tabela.loc[:,~ler_tabela.columns.str.contains('^Unnamed')]
        
        colunas = list(ler_tabela.columns)
        
        tabela = ttk.Treeview(janela,columns=colunas,show='headings')
        tabela.pack(fill='both',expand=True,pady=10)
        
        for coluna in colunas:
            tabela.heading(coluna,text=coluna)
            tabela.column(coluna,width=60,anchor='center')
            
        for _, linha in ler_tabela.iterrows():
            tabela.insert('','end',values=list(linha))
            
        filtrar_notas = ttk.Button(janela, text="Filtrar notas")
        filtrar_notas.pack(side='top', padx=10, pady=10)

        def voltar_menu():
            tabela.pack_forget()
            rotulo_nova_tabela.pack()
            rotulo_criar_tabela.pack()
            botao_criar_tabela.pack(pady=10)
            filtrar_notas.pack_forget()
            voltar.pack_forget()
            
        voltar = ttk.Button(janela, text="Voltar",command=voltar_menu)
        voltar.pack(side='top', padx=10, pady=10)

def filtrar_notas():
    return

def exportar_tabela():
    return

def criar_tabela():
    return



janela = tk.Tk()
janela.geometry('800x600')
janela.title('Atividade Pyhton - Tkinter e Pandas')

ttk.Label(janela,text='Seja bem vindo ao gerenciamento de notas: SENAI Félix Guizard',font=('Arial',15,'bold')).pack(pady=10)
ttk.Label(janela,text='Clique aqui para carregar uma tabela existente').pack()
ttk.Button(janela,text='Carregar tabela', command=importar_tabela).pack(pady=20)


rotulo_nova_tabela = ttk.Label(janela,text='Criar uma nova tabela',font=('Arial',15,'bold'))
rotulo_nova_tabela.pack()
rotulo_criar_tabela = ttk.Label(janela,text='Clique aqui para criar uma tabela')
rotulo_criar_tabela.pack()
botao_criar_tabela = ttk.Button(janela,text='Criar Tabela',command=criar_tabela)
botao_criar_tabela.pack(pady=20)


janela.mainloop()
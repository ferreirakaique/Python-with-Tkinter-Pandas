import tkinter as tk

def clique():
    if rotulo.cget('text') == 'Clique no botão abaixo':
        rotulo.config(text="Você clicou no botão")
        janela.config(background="lightblue")
        botao_mudar_texto.config(text='Voltar')
    else:
        rotulo.config(text="Clique no botão abaixo")
        janela.config(background='white')
        botao_mudar_texto.config(text='Clique aqui')

janela = tk.Tk()
janela.title("Botao de sair da janela e mudar o texto")
janela.geometry("300x200")

rotulo = tk.Label(janela,text="Clique no botão abaixo",font=('Arial',12))
rotulo.pack(pady=30)

botao_mudar_texto = tk.Button(janela,text="Clique aqui",command=clique)
botao_mudar_texto.pack()

botao_sair = tk.Button(janela,text="Sair",width=10,bg='red',fg='white',font=('Arial',8,'bold'),command=janela.destroy)

botao_sair.pack(pady=20)

janela.mainloop()
import tkinter as tk

def enviar():
    nome = nome_digitado.get()
    if nome == "":
        rotulo_resposta.config(text='ATENÇÃO: você não colocou nenhum nome')
    else:
        rotulo_resposta.config(text=f'Seja muito bem vindo: {nome}')

janela = tk.Tk()
janela.title('Coletando dados do usuário')
janela.geometry('300x300')
janela.config(bg='lightblue')

rotulo = tk.Label(janela,text='Digite seu nome',font=('Arial',12,'bold'))
rotulo.pack(pady=20)

nome_digitado = tk.Entry(janela)
nome_digitado.pack(pady=20)

botao_enviar = tk.Button(janela,text='Enviar', command=enviar)
botao_enviar.pack(pady=20)

rotulo_resposta = tk.Label(janela,text="",bg='lightblue')
rotulo_resposta.pack()

janela.mainloop()
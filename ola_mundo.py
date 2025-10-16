import tkinter as tk

#cria uma janela com tkinter
janela = tk.Tk()
janela.title("Meu primeiro app com tkinter")
janela.configure(bg='lightblue')
janela.geometry("100x100")

#adiciona um texto dentro da janela
rotulo = tk.Label(janela, text="Olá! Mundo!", font=("Arial",30))
rotulo.pack(pady=20)

janela.mainloop()
from tkinter import *
from tkinter import ttk

tabuleiro = []
qtd_posicoes = 9
for i in range(qtd_posicoes):
  linha = []
  for j in range(qtd_posicoes):
    peca = '*'
    if i == 0 or i == 8 or j == 0 or j == 8:
      peca = ' '
    elif (i < 3 or i > 5) and (j < 3 or j > 5):
      peca = ' '
    if (i == j == 4):
      peca = 'O'
    linha.append(peca)
  tabuleiro.append(linha)

# def calculate(*args):
#   try:
#     value = float(feet.get())
#     meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
#   except ValueError:
#     pass

def selecionaPeca(x, y, tag):
  canvas.itemconfigure(tag, image=img_vazio)

janela = Tk()
janela.title("Resta um")
janela.geometry("800x800")
# Canvas com o negocio
canvas = Canvas(janela, width=745, height=745)
canvas.place(x=0, y=0)
img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
img_nada = PhotoImage(file="assets/nada.png")
img_peca = PhotoImage(file="assets/peca.png")
img_vazio = PhotoImage(file="assets/vazio.png")

canvas.create_image(5,5, anchor=NW, image=img_tabuleiro)

style = ttk.Style()
style.configure(
  "Peca.TButton",
    padding=0,
    relief="flat",
    bg="#FFF",
    border=0,
  )

tagPecas = []
tags = []
for i in range(1, qtd_posicoes-1):
  linha = []
  for j in range(1, qtd_posicoes-1):
    lin, col = 20 + ((i-1) * 100) + ((i-1) * 5), 20 + ((j-1) * 100) + ((j-1) * 5)
    tagItem = -1
    if tabuleiro[i][j] == '*':
      tagItem = canvas.create_image(col, lin, anchor=NW, image=img_peca)
      tags.append((tagItem, i-1, j-1))
    if tabuleiro[i][j] == 'O':
      tagItem = canvas.create_image(col, lin, anchor=NW, image=img_vazio)
      tags.append((tagItem, i-1, j-1))
    linha.append(tagItem)
  tagPecas.append(linha[:])

# canvas.delete(posicoes[0][2])
cont = 1
for t in tags:
  tag, i, j = t
  canvas.tag_bind(
    tag,
    "<Button-1>",
    lambda e, x=i, y=j, id=tag: selecionaPeca(x+1, y+1, id)
  )
  cont += 1

# posicoes[0][2].configure(image=img_vazio)
# posicoes[0][2].update()
# canvas.delete(posicoes[1][2])

# Cada letra tem 5px de largura (<->)
# Cada linha tem 20px de altura

# feet = StringVar()
# feet_entry = ttk.Entry(janela, width=7, textvariable=feet)
# feet_entry.place(x=20, y=10)

# meters = StringVar()
# ttk.Label(janela, textvariable=meters).place(x=95, y=30)

# ttk.Button(janela, text="Calculate", command=calculate).place(x=30, y=80)

# ttk.Label(janela, text="feet").place(x=60, y=10)
# ttk.Label(janela, text="is equivalent to").place(x=10, y=30)
# ttk.Label(janela, text="meters").place(x=135, y=30)

# for child in container.winfo_children(): 
#   child.place_configure(padx=5, pady=5)

# feet_entry.focus()
# janela.bind("<Return>", calculate)

janela.mainloop()
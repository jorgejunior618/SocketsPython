from tkinter import *
from tkinter import ttk
from models.cli_tabuleiro import CliTabuleiroSocket

class RestaUmInterface:
  jogada = ""
  meuTurno = True
  img_tabuleiro = None
  img_nada = None
  img_peca = None
  img_vazio = None

  @staticmethod
  def selecionaPeca(x: int, y: int, tag: int, ct) -> bool:
    posicaoJogada = ["","a", "b", "c", "d", "e", "f", "g",""]
    pecaSelecionada = f"{posicaoJogada[x]}{y}"
    if len(RestaUmInterface.jogada) == 0:
      RestaUmInterface.jogada = f"{pecaSelecionada}"
      return False

    RestaUmInterface.jogada = f"{RestaUmInterface.jogada} {pecaSelecionada}"
    RestaUmInterface.meuTurno = not ct.enviarLance(RestaUmInterface.jogada)
    RestaUmInterface.jogada = ""
    if RestaUmInterface.meuTurno:
      return False
    return True
    # canvas.itemconfigure(tag, image=img_vazio)

  def fazJogada(self, x: int, y: int, tag: int):
    reposicionar = RestaUmInterface.selecionaPeca(x, y, tag, self.cliTab)
    if reposicionar:
      self.reposicionaPecas()

  def __init__(self, cli_tabuleiro):
    self.cliTab = cli_tabuleiro
    self.cliTab.jogo.reiniciaTabuleiro()
    self.criaJanela()

    RestaUmInterface.img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
    RestaUmInterface.img_nada = PhotoImage(file="assets/nada.png")
    RestaUmInterface.img_peca = PhotoImage(file="assets/peca.png")
    RestaUmInterface.img_vazio = PhotoImage(file="assets/vazio.png")

    self.criaTabuleiro()
    self.configuraEstilos()
    self.criaPecas()
  
  def criaJanela(self):
    self.janela = Tk()
    self.janela.title("Resta um")
    self.janela.geometry("800x800")

  def configuraEstilos(self):
    style = ttk.Style()
    style.configure(
      "Peca.TButton",
        padding=0,
        relief="flat",
        bg="#FFF",
        border=0,
      )

  def criaTabuleiro(self):
    self.canvas = Canvas(self.janela, width=745, height=745)
    self.canvas.place(x=0, y=0)
    self.canvas.create_image(5,5, anchor=NW, image=RestaUmInterface.img_tabuleiro)

  def criaPecas(self):
    self.tagPecas = []
    for i in range(1, 8):
      linha = []
      for j in range(1, 8):
        lin, col = 20 + ((i-1) * 100) + ((i-1) * 5), 20 + ((j-1) * 100) + ((j-1) * 5)
        tagItem = -1
        if self.cliTab.jogo.tabuleiro[i][j] == '*':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=RestaUmInterface.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=RestaUmInterface.img_vazio)
        self.canvas.tag_bind(
          tagItem,
          "<Button-1>",
          lambda e, x=i, y=j, id=tagItem: self.fazJogada(x, y, id)
        )
        linha.append(tagItem)
      self.tagPecas.append(linha[:])
  
  def reposicionaPecas(self):
    for i in range(1, 8):
      for j in range(1, 8):
        if self.cliTab.jogo.tabuleiro[i][j] == '*':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=RestaUmInterface.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=RestaUmInterface.img_vazio)
  
  def iniciaAplicacao(self):
    self.janela.mainloop()

ct = CliTabuleiroSocket(('localhost', 1234), ('localhost', 4321))
meuJogo = RestaUmInterface(ct)
meuJogo.iniciaAplicacao()

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

# janela.mainloop()
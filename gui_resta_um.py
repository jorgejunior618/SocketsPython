from tkinter import *
from tkinter import ttk
import threading
from pygame import mixer

from models.cli_tabuleiro import CliTabuleiroSocket

class GuiRestaUm:
  ''' # RestaUmInterface

  Classe que inicializa uma interface grafica, com `TKinter`, para o jogo Resta Um.

  ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
  jogada = ""
  pecaDestacada = -1
  meuTurno = True
  img_tabuleiro = None
  img_peca = None
  img_vazio = None
  img_peca_high = None
  dictImgs = {
    'peca': '2',
    'vazio': '3',
    'destacada': '4',
  }

  def __init__(self, cli_tabuleiro: CliTabuleiroSocket):
    '''
    Inicializa a interface grafica do jogo

    ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
    self.cliTab: CliTabuleiroSocket = cli_tabuleiro
    self.cliTab.jogo.reiniciaTabuleiro()
    self.criaJanela()

    GuiRestaUm.img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
    GuiRestaUm.img_peca = PhotoImage(file="assets/peca.png")
    GuiRestaUm.img_vazio = PhotoImage(file="assets/vazio.png")
    GuiRestaUm.img_peca_high = PhotoImage(file="assets/peca_highlight.png")

    self.criaTabuleiro()
    self.configuraEstilos()
    self.criaPecas()

  @staticmethod
  def reproduzSom(efeito: str):
    ''' ## reproduzSom(efeito)

    Reproduz um efeito sonoro referente ao movimento/ação do jogo

    ## Parâmetro:
    efeito : str
        A ação realizada, gatilho para o efeito sonoro
    '''
    efeitos = {
      'derrota': 'derrota_1',
      'vitoria': 'vitoria_1',
      'movimento': 'movimento_1',
      'mov_erro': 'mov_erro_2',
    }
    mixer.init()
    mixer.music.load(f"assets/{efeitos[efeito]}.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()

  @staticmethod
  def selecionaPeca(
    x: int,
    y: int,
    tag: int,
    ct: CliTabuleiroSocket
  ) -> tuple[bool, int, bool]:
    posicaoJogada = ["","a", "b", "c", "d", "e", "f", "g",""]
    pecaSelecionada = f"{posicaoJogada[x]}{y}"
    removerDestaque = GuiRestaUm.pecaDestacada

    if (removerDestaque == tag):
      GuiRestaUm.jogada = ""
      GuiRestaUm.pecaDestacada = -1
      return False, tag, False
    GuiRestaUm.pecaDestacada = tag

    if len(GuiRestaUm.jogada) == 0:
      GuiRestaUm.jogada = f"{pecaSelecionada}"
      return False, removerDestaque, False

    GuiRestaUm.jogada = f"{GuiRestaUm.jogada} {pecaSelecionada}"
    meuTurno = not ct.enviarLance(GuiRestaUm.jogada)

    if meuTurno:
      GuiRestaUm.pecaDestacada = tag
      GuiRestaUm.jogada = pecaSelecionada
      return False, removerDestaque, True

    GuiRestaUm.jogada = ""
    GuiRestaUm.pecaDestacada = -1
    return True, removerDestaque, False

  def fazJogada(self, x: int, y: int, tag: int):
    if self.cliTab.jogo.turno == 0:
      pecaID = self.canvas.itemcget(tag, 'image')[-1]
      if pecaID != '3':
        reposicionar, rmDst, movErrado = GuiRestaUm.selecionaPeca(x, y, tag, self.cliTab)
        if GuiRestaUm.pecaDestacada != -1:
          self.canvas.itemconfigure(tag, image=GuiRestaUm.img_peca_high)
        if rmDst != -1:
          self.canvas.itemconfigure(rmDst, image=GuiRestaUm.img_peca)

        if reposicionar:
          self.reposicionaPecas()
          GuiRestaUm.reproduzSom('movimento')
        if movErrado:
          GuiRestaUm.reproduzSom('mov_erro')

  def recebeJogadaAdversario(self):
    while True:
      print("esperando adversario")
      try:
        recebeu = self.cliTab.receberLance()
        if recebeu:
          GuiRestaUm.meuTurno = True
          self.reposicionaPecas()
          GuiRestaUm.reproduzSom('movimento')
      except:
        print("nenhuma resposta obtida")

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
    self.canvas = Canvas(self.janela, width=800, height=800)
    self.canvas.place(x=0, y=0)
    self.canvas.create_image(5,5, anchor=NW, image=GuiRestaUm.img_tabuleiro)

  def criaPecas(self):
    self.tagPecas = []
    for i in range(1, 8):
      linha = []
      for j in range(1, 8):
        lin = 140 + ((i-1) * 64) + ((i-1) * 10)
        col = 60 + ((j-1) * 80) + ((j-1) * 20)
        tagItem = -1
        if self.cliTab.jogo.tabuleiro[i][j] == '*':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=GuiRestaUm.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=GuiRestaUm.img_vazio)
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
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_vazio)
  
  def iniciaAplicacao(self):
    self.janela.mainloop()

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
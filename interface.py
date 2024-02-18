from tkinter import *
from tkinter import ttk
import threading
from pygame import mixer

from models.cli_tabuleiro import CliTabuleiroSocket

class RestaUmInterface:
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

    RestaUmInterface.img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
    RestaUmInterface.img_peca = PhotoImage(file="assets/peca.png")
    RestaUmInterface.img_vazio = PhotoImage(file="assets/vazio.png")
    RestaUmInterface.img_peca_high = PhotoImage(file="assets/peca_highlight.png")

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
    removerDestaque = RestaUmInterface.pecaDestacada

    if (removerDestaque == tag):
      RestaUmInterface.jogada = ""
      RestaUmInterface.pecaDestacada = -1
      return False, tag, False
    RestaUmInterface.pecaDestacada = tag

    if len(RestaUmInterface.jogada) == 0:
      RestaUmInterface.jogada = f"{pecaSelecionada}"
      return False, removerDestaque, False

    RestaUmInterface.jogada = f"{RestaUmInterface.jogada} {pecaSelecionada}"
    meuTurno = not ct.enviarLance(RestaUmInterface.jogada)

    if meuTurno:
      RestaUmInterface.pecaDestacada = tag
      RestaUmInterface.jogada = pecaSelecionada
      return False, removerDestaque, True

    RestaUmInterface.jogada = ""
    RestaUmInterface.pecaDestacada = -1
    return True, removerDestaque, False

  def fazJogada(self, x: int, y: int, tag: int):
    if self.cliTab.jogo.turno == 0:
      pecaID = self.canvas.itemcget(tag, 'image')[-1]
      if pecaID != '3':
        reposicionar, rmDst, movErrado = RestaUmInterface.selecionaPeca(x, y, tag, self.cliTab)
        if RestaUmInterface.pecaDestacada != -1:
          self.canvas.itemconfigure(tag, image=RestaUmInterface.img_peca_high)
        if rmDst != -1:
          self.canvas.itemconfigure(rmDst, image=RestaUmInterface.img_peca)

        if reposicionar:
          self.reposicionaPecas()
          RestaUmInterface.reproduzSom('movimento')
        if movErrado:
          RestaUmInterface.reproduzSom('mov_erro')

  def recebeJogadaAdversario(self):
    while True:
      print("esperando adversario")
      recebeu = self.cliTab.receberLance()
      if recebeu:
        RestaUmInterface.meuTurno = True
        self.reposicionaPecas()
        RestaUmInterface.reproduzSom('movimento')

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

# Inicializando o socket do cliente do jogador
ct = CliTabuleiroSocket(('localhost', 1234), ('localhost', 4321))

# Inicializando o objeto que instanciará o jogo
meuJogo = RestaUmInterface(ct)

# Criando a thread que recebe a jogada do adversário via Socket
thread_jogo = threading.Thread(target=meuJogo.recebeJogadaAdversario)
thread_jogo.daemon = True
thread_jogo.start()

# Inicializando a aplicação grafica do jogo
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
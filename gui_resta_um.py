from tkinter import *
from tkinter import font
from tkinter import ttk
import time
import threading
from pygame import mixer

from models.cli_tabuleiro import CliTabuleiroSocket
from models.cli_chat import CliChatSocket

class GuiRestaUm:
  ''' # RestaUmInterface

  Classe que inicializa uma interface grafica, com `TKinter`, para o jogo Resta Um.

  ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
  jogada = ""
  pecaDestacada = -1
  meuTurno = -1
  prontoPJogar = False
  turnoVar: StringVar = None
  labelInfoTurno: ttk.Label = None
  tagFimJogo = None
  img_tabuleiro = None
  img_peca = None
  img_vazio = None
  img_peca_high = None
  fim_jogo = None
  dictImgs = {}

  def __init__(self, cli_tabuleiro: CliTabuleiroSocket, cli_chat: CliChatSocket):
    '''
    Inicializa a interface grafica do jogo

    ## Parâmetros:
    cli_tabuleiro : CliTabuleiroSocket
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
    self.cliTab: CliTabuleiroSocket = cli_tabuleiro
    self.cliChat: CliChatSocket = cli_chat
    self.cliTab.jogo.reiniciaTabuleiro()
    self.criaComponenteJanela()
    mixer.init()
    GuiRestaUm.turnoVar = StringVar()
    GuiRestaUm.labelInfoTurno = ttk.Label(self.janela, textvariable=GuiRestaUm.turnoVar)
    GuiRestaUm.img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
    GuiRestaUm.img_peca = PhotoImage(file="assets/peca.png")
    GuiRestaUm.img_vazio = PhotoImage(file="assets/vazio.png")
    GuiRestaUm.img_peca_high = PhotoImage(file="assets/peca_highlight.png")
    GuiRestaUm.fim_jogo = PhotoImage(file="assets/fim_jogo.png")

    GuiRestaUm.dictImgs['peca'] = GuiRestaUm.img_peca.name[-1]
    GuiRestaUm.dictImgs['vazio'] = GuiRestaUm.img_vazio.name[-1]
    GuiRestaUm.dictImgs['destacada'] = GuiRestaUm.img_peca_high.name[-1]
    
    self.criaComponenteTabuleiro()
    self.criaComponenteEstilos()
    self.criaComponentePecas()
    self.criaComponenteTurnos()

    self.mensagens = []
    self.minhaMensagem = StringVar()
    self.criaComponenteChat()

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
    arq = f"assets/{efeitos[efeito]}.mp3"
    if mixer.music.get_busy():
      mixer.music.queue(arq)
    else:
      mixer.music.load(arq)

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
    minhaVez = not ct.enviarLance(GuiRestaUm.jogada)

    if minhaVez:
      GuiRestaUm.pecaDestacada = tag
      GuiRestaUm.jogada = pecaSelecionada
      return False, removerDestaque, True

    GuiRestaUm.jogada = ""
    GuiRestaUm.pecaDestacada = -1
    return True, removerDestaque, False

  def criaComponenteJanela(self):
    self.janela = Tk()
    self.janela.title("Resta um")
    self.janela.geometry("1200x800")

  def criaComponenteEstilos(self):
    style = ttk.Style()
    style.configure(
      "Peca.TButton",
        padding=0,
        relief="flat",
        bg="#FFF",
        border=0,
      )

  def criaComponenteTabuleiro(self):
    self.canvas = Canvas(self.janela, width=800, height=800)
    self.canvas.place(x=0, y=0)
    self.canvas.create_image(0,0, anchor=NW, image=GuiRestaUm.img_tabuleiro)

  def criaComponenteTurnos(self, texto: str = "Escolha seu turno"):
    GuiRestaUm.botaoT1 = ttk.Button(self.janela, text="1º", command=lambda t=0: self._setTurno(t))
    GuiRestaUm.botaoT2 = ttk.Button(self.janela, text="2º", command=lambda t=1: self._setTurno(t))
    GuiRestaUm.labelDecTurno = ttk.Label(self.janela, text=texto)
    
    GuiRestaUm.botaoT1.place(x=850, y=45)
    GuiRestaUm.botaoT2.place(x=950, y=45)
    GuiRestaUm.labelDecTurno.place(x=850, y=15)

  def criaComponentePecas(self):
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

  def criaComponenteChat(self):
    GuiRestaUm.inputChat = ttk.Entry(self.janela, textvariable=self.minhaMensagem, width=44)
    GuiRestaUm.inputChat.place(x=820, y=763)
    GuiRestaUm.botaoEnviarChat = ttk.Button(
      self.janela,
      text="Enviar",
      command=self.chatEnviaMensagem,
      padding=5
    )
    GuiRestaUm.botaoEnviarChat.place(x=1105, y=758)

  def desceFimDeJogo(self):
    GuiRestaUm.tagFimJogo = self.canvas.create_image(75,-520, anchor=NW, image=GuiRestaUm.fim_jogo)
    def desce():
      cont = 0
      for i in range(104):
        alturaAtual = i*5 - 520
        balancoAtual = 0
        if GuiRestaUm.meuTurno == -1:
          self.canvas.moveto(GuiRestaUm.tagFimJogo, 75, -520)
          break
        if cont < 20:
          balancoAtual = 0 - cont*2
        elif cont < 56:
          balancoAtual = cont*2 - 78
        elif cont < 82:
          balancoAtual = 144 - cont*2
        elif cont < 98:
          balancoAtual = cont*2 - 180
        else:
          balancoAtual = 210 - cont*2

        self.canvas.moveto(GuiRestaUm.tagFimJogo, 75 + balancoAtual, alturaAtual)
        cont += 1

        time.sleep(0.025)
        # time.sleep(0.025)

    thread_placa = threading.Thread(target=desce, daemon=True)
    thread_placa.start()

  def recebeJogadaAdversario(self):
    while True:
      try:
        recebeu = self.cliTab.receberLance()

        if recebeu:
          GuiRestaUm.reproduzSom('movimento')
          self.reposicionaPecas()
        else: break
      except:
        print("[Movimento]: nenhuma resposta obtida")

  def fazJogada(self, x: int, y: int, tag: int):
    if self.cliTab.jogo.turno == GuiRestaUm.meuTurno and GuiRestaUm.prontoPJogar:
      pecaID = self.canvas.itemcget(tag, 'image')[-1]
      if pecaID != GuiRestaUm.dictImgs['vazio']:
        reposicionar, rmDst, movErrado = GuiRestaUm.selecionaPeca(x, y, tag, self.cliTab)
        if GuiRestaUm.pecaDestacada != -1:
          self.canvas.itemconfigure(tag, image=GuiRestaUm.img_peca_high)
        if rmDst != -1:
          self.canvas.itemconfigure(rmDst, image=GuiRestaUm.img_peca)

        if reposicionar:
          GuiRestaUm.reproduzSom('movimento')
          self.reposicionaPecas()
        if movErrado:
          GuiRestaUm.reproduzSom('mov_erro')

  def setTurnoAdversario(self):
    while True:
      try:
        turnoAdv = self.cliTab.receberTurno()
        print(f"escolha do adv: {turnoAdv}")
        while GuiRestaUm.meuTurno == -1:
          time.sleep(0.5)
        if turnoAdv != GuiRestaUm.meuTurno:
          GuiRestaUm.prontoPJogar = True
          if GuiRestaUm.meuTurno == 0:
            GuiRestaUm.turnoVar.set("Você inicia a partida")
          elif GuiRestaUm.meuTurno == 1:
            GuiRestaUm.turnoVar.set("Seu adversario iniciará a partida")
          thread_jogo = threading.Thread(target=self.recebeJogadaAdversario, daemon=True)
          thread_jogo.start()
          break
        else:
          GuiRestaUm.meuTurno = -1
          self.criaComponenteTurnos(texto="Conflito na resposta, tentem novamente")
      except:
        print("[Turno]: nenhuma resposta obtida")

  def _setTurno(self, t: int):
    GuiRestaUm.meuTurno = t
    self.cliTab.definirTurno(f"{t}")
    GuiRestaUm.botaoT1.destroy()
    GuiRestaUm.botaoT2.destroy()
    GuiRestaUm.labelDecTurno.destroy()

    GuiRestaUm.turnoVar.set("Aguardando resposta do seu adversário")
    GuiRestaUm.labelInfoTurno = ttk.Label(self.janela, textvariable=GuiRestaUm.turnoVar)
    GuiRestaUm.labelInfoTurno.place(x=850, y=15)

  def reposicionaPecas(self):
    for i in range(1, 8):
      for j in range(1, 8):
        if self.cliTab.jogo.tabuleiro[i][j] == '*':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_peca)
        if self.cliTab.jogo.tabuleiro[i][j] == 'O':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_vazio)
    if GuiRestaUm.meuTurno == self.cliTab.jogo.turno:
      GuiRestaUm.turnoVar.set("Sua vez")
    else:
      GuiRestaUm.turnoVar.set("Vez do adversário")

    self.checaFimDeJogo()

  def checaFimDeJogo(self):
    terminou, contPecas = self.cliTab.jogo.estaNoFim()
    if terminou:
      self.desceFimDeJogo()
      GuiRestaUm.prontoPJogar = False
      self.cliTab.enviarLance("fim")

      vencedor = False
      if contPecas > 1:
        vencedor = self.cliTab.jogo.turno == GuiRestaUm.meuTurno
      else:
        vencedor = self.cliTab.jogo.turno != GuiRestaUm.meuTurno
      fonteResultado = font.Font(size=25, weight="bold")

      if vencedor:
        GuiRestaUm.labelInfoResultado = ttk.Label(self.janela,text="  Parabéns!\nVocê venceu",font=fonteResultado)
        GuiRestaUm.labelInfoResultado.place(x=830, y=15)
        self.reproduzSom("vitoria")
      else:
        GuiRestaUm.labelInfoResultado = ttk.Label(self.janela,text="  Você perdeu :(\nTalvez na Proxima",font=fonteResultado)
        GuiRestaUm.labelInfoResultado.place(x=830, y=15)
        self.reproduzSom("derrota")

      GuiRestaUm.botaoResetaJogo = ttk.Button(self.janela, text="Novo Jogo", command=self.resetaJogo)
      GuiRestaUm.botaoResetaJogo.place(x=850, y=115)

  def resetaJogo(self):
    thread_turno = threading.Thread(target=self.setTurnoAdversario, daemon=True)
    thread_turno.start()

    GuiRestaUm.meuTurno = -1

    self.cliTab.jogo.reiniciaTabuleiro()
    self.reposicionaPecas()
    GuiRestaUm.turnoVar.set("")
    GuiRestaUm.labelInfoResultado.destroy()
    GuiRestaUm.botaoResetaJogo.destroy()
    self.canvas.moveto(GuiRestaUm.tagFimJogo, 75, -520)

    self.criaComponenteTurnos()
  
  def chatRecebeMensagem(self):
    msg = self.cliChat.receber_mensagen()
    self.mensagens.append(f"Adversário: {msg}")
  
  def chatEnviaMensagem(self):
    msg = self.minhaMensagem.get()
    self.mensagens.append(f"Você: {msg}")
    self.minhaMensagem.set("")
    self.cliChat.enviar_mensagem(msg)

  def iniciaAplicacao(self):
    # Criando a thread que recebe a escolha do turno do adversário via Socket
    thread_turno = threading.Thread(target=self.setTurnoAdversario, daemon=True)
    thread_turno.start()

    thread_chat = threading.Thread(target=self.chatRecebeMensagem, daemon=True)
    thread_chat.start()

    self.janela.mainloop()
